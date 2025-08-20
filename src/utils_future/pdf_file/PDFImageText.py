import time
from functools import cache
from multiprocessing import Pool, cpu_count
from tempfile import NamedTemporaryFile

import pytesseract
from pdf2image import convert_from_path
from utils import Log

from utils_future.pdf_file.PDFCompress import PDFCompress

TESSERACT_FAST_CONFIG = r"""
--oem 1
--psm 6
"""

log = Log("PDFImageText")


class PDFImageText:

    @staticmethod
    def __get_image_text_from_im__(i_page, im):
        temp_img_path = NamedTemporaryFile(suffix=".png", delete=False).name
        im.save(temp_img_path, format="PNG")
        t_start = time.time()
        try:
            image_text = pytesseract.image_to_string(
                temp_img_path, lang="eng", config=TESSERACT_FAST_CONFIG
            )
            dt_ms = 1_000 * (time.time() - t_start)
            log.debug(
                f"[Page {i_page}] Extracted {
                    len(image_text):,} B in {
                    dt_ms:,.0f} ms"
            )

            return image_text
        except Exception as e:
            log.error(f"[Page {i_page}] Error extracting text from page: {e}")
            return None

    def __worker__(self, x):
        return self.__get_image_text_from_im__(x[0], x[1])

    @cache
    def get_image_text(self):
        im_list = convert_from_path(self.path, dpi=PDFCompress.DPI_TARGET)
        n_pages = len(im_list)
        log.debug(f"{n_pages=}")
        n_cpus = cpu_count()
        log.debug(f"{n_cpus=}")

        page_text_list = Pool(processes=n_cpus).map(
            self.__worker__,
            enumerate(im_list, start=1),
        )

        page_text_list = [
            page_text for page_text in page_text_list if page_text is not None
        ]

        text = "\n\n".join(page_text_list)
        return self.__log_text_info_and_return__(text, "Image text")
