import os
import re
import shutil
import ssl
import tempfile
from functools import cached_property

import pymupdf
import requests
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
from utils import File, Log

from lk_acts.core.act.ActWrite import ActWrite
from utils_future import PDFFile

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
log = Log("ActDownloadPDF")


class _ParliamentInsecureAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context(ciphers="DEFAULT:@SECLEVEL=1")
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        kwargs["ssl_context"] = ctx
        return super().init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        ctx = create_urllib3_context(ciphers="DEFAULT:@SECLEVEL=1")
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        kwargs["ssl_context"] = ctx
        return super().proxy_manager_for(*args, **kwargs)


class ActDownloadPDF(ActWrite):
    T_TIMEOUT_PDF_DOWNLOAD = 120
    MIN_FILE_SIZE_M = 0.001
    MAX_FILE_SIZE_M = 40
    MIN_TXT_FILE_SIZE_K = 1

    @cached_property
    def pdf_path(self):
        return os.path.join(self.dir_act_data, "en.pdf")

    @cached_property
    def _session_parliament(self):
        s = requests.Session()
        s.mount("https://www.parliament.lk", _ParliamentInsecureAdapter())
        return s

    def __download_to_temp__(self):
        url = self.url_pdf_en
        try:
            if url.startswith("https://www.parliament.lk"):
                r = self._session_parliament.get(
                    url,
                    timeout=self.T_TIMEOUT_PDF_DOWNLOAD,
                    verify=False,
                )
            else:
                r = requests.get(url, timeout=self.T_TIMEOUT_PDF_DOWNLOAD)
        except requests.RequestException as e:
            log.error(f"Failed to download PDF from {url}: {e}")
            return None

        temp_pdf_path = tempfile.NamedTemporaryFile(suffix=".pdf").name
        if r.status_code != 200:
            log.error(
                f"Failed to download PDF from {url}: HTTP {r.status_code}"
            )
            return None
        with open(temp_pdf_path, "wb") as f:
            f.write(r.content)

        return temp_pdf_path

    def __download_pdf_hot__(self):
        url = self.url_pdf_en
        temp_pdf_path = self.__download_to_temp__()
        if not temp_pdf_path:
            return None
        file_size_m = os.path.getsize(temp_pdf_path) / 1_000_000.0
        if (
            file_size_m < ActDownloadPDF.MIN_FILE_SIZE_M
            or file_size_m > ActDownloadPDF.MAX_FILE_SIZE_M
        ):
            log.error(
                f"Downloaded PDF from {url} is invalid:"
                + f" {file_size_m:.1f} MB"
            )
            return None

        shutil.move(temp_pdf_path, self.pdf_path)
        log.info(
            f"✅ Downloaded PDF from {url}"
            + f" to {self.pdf_path} ({file_size_m:.1f} MB)"
        )
        return self.pdf_path

    def __download_pdf_cold_or_hot__(self):
        if os.path.exists(self.pdf_path):
            return self.pdf_path
        return self.__download_pdf_hot__()

    def download_pdf(self):
        url = self.url_pdf_en
        if not url or url == "null":
            log.warning(f'No url_pdf_en found for "{self.act_id}"')
            return None
        return self.__download_pdf_cold_or_hot__()

    @cached_property
    def txt_path(self):
        return os.path.join(self.dir_act_data, "en.txt")

    def extract_txt(self):
        pdf_path = self.pdf_path
        if not os.path.exists(pdf_path):
            return None

        if os.path.exists(self.txt_path):
            return self.__validate_txt__()

        return self.__extract_text_hot__()

    @staticmethod
    def __clean_block_text__(block_text: str) -> str:
        block_text = block_text or ""
        block_text = block_text.replace("\n", " ")
        block_text = re.sub(r"[^\x00-\x7F]+", "", block_text)
        block_text = re.sub(r"\s+", " ", block_text)
        block_text = block_text.strip()
        return block_text

    def __extract_block_text_list__(self):
        doc = pymupdf.open(self.pdf_path)
        block_text_list = []
        for page in doc:
            blocks = page.get_text("blocks")
            blocks = sorted(blocks, key=lambda b: (b[1], b[0]))
            for block in blocks:
                block_type = block[6] if len(block) > 6 else 0
                if block_type != 0:
                    continue  # skip non-text blocks
                block_text = block[4] if len(block) > 4 else ""
                block_text = self.__clean_block_text__(block_text)
                if block_text:
                    block_text_list.append(block_text)
        return block_text_list

    def __extract_image_text_hot__(self):
        image_text = PDFFile(self.pdf_path).get_image_text()
        file_size_k = len(image_text) / 1_000.0
        if file_size_k < ActDownloadPDF.MIN_TXT_FILE_SIZE_K:
            log.error(f"[{self.num}] Insufficient image text.")
            return None

        File(self.txt_path).write(image_text)
        log.info(f"Wrote [image] {self.txt_path} ({file_size_k:.1f} kB)")
        return self.txt_path

    def __validate_txt__(self):
        if os.path.exists(self.txt_path):
            file_size_k = os.path.getsize(self.txt_path) / 1_000.0
            if file_size_k >= ActDownloadPDF.MIN_TXT_FILE_SIZE_K:
                return self.txt_path
            else:
                log.warning(
                    f"[{self.num}] Text extract too small"
                    + f" ({file_size_k:.1f} kB). ❌ Removing."
                )
                os.remove(self.txt_path)
        return self.__extract_image_text_hot__()

    def __extract_text_hot__(self):
        text = "\n\n".join(self.__extract_block_text_list__())
        file_size_k = len(text) / 1_000.0
        if file_size_k < ActDownloadPDF.MIN_TXT_FILE_SIZE_K:
            log.error(f"[{self.num}] Insufficient text.")
            return self.__validate_txt__()
        File(self.txt_path).write(text)
        log.info(f"Wrote {self.txt_path} ({file_size_k:.1f} kB)")
        return self.txt_path
