import os
import shutil
import ssl
import tempfile
from functools import cached_property

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
        temp_pdf_path = PDFFile(temp_pdf_path).compress().path

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
            f"✅ Downloaded PDF from {url}" + f" to {PDFFile(self.pdf_path)}"
        )
        return self.pdf_path

    def __download_pdf_cold_or_hot__(self):
        if os.path.exists(self.pdf_path):
            return self.pdf_path
        return self.__download_pdf_hot__()

    def download_pdf(self):
        url = self.url_pdf_en
        if not url or url == "null":
            log.error(f'No url_pdf_en found for "{self.act_id}"')
            return None
        return self.__download_pdf_cold_or_hot__()

    @cached_property
    def txt_path(self):
        return os.path.join(self.dir_act_data, "en.txt")

    def extract_text(self):
        if os.path.exists(self.txt_path):
            return self.txt_path
        if not os.path.exists(self.pdf_path):
            return None
        try:
            text = PDFFile(self.pdf_path).get_text()
            File(self.txt_path).write(text)
            log.info(f"Wrote {self.txt_path} ({len(text):,} chars)")
        except Exception as e:
            log.error(f"[{self.num}] {e}")
            return None
