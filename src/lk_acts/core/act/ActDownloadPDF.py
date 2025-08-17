import os
import ssl
from functools import cached_property

import requests
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
from utils import Log

from lk_acts.core.act.ActWrite import ActWrite

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

    @cached_property
    def pdf_path(self):
        return os.path.join(self.dir_act_data, "en.pdf")

    @cached_property
    def _session_parliament(self):
        s = requests.Session()
        s.mount("https://www.parliament.lk", _ParliamentInsecureAdapter())
        return s

    def __download_pdf_hot__(self):
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

        if r.status_code == 200:
            with open(self.pdf_path, "wb") as f:
                f.write(r.content)
            log.info(f"✅ Downloaded PDF from {url} to {self.pdf_path}")
            return self.pdf_path

        log.error(f"Failed to download PDF from {url}: HTTP {r.status_code}")
        return None

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
