from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils import Log

from lpd.core import Doc
from utils_future import WebPage

log = Log("ActsBillsPage")


class ActsBillsPage(WebPage):

    def __init__(self, doc_type_name, year):
        super().__init__("https://www.parliament.lk/en/acts-bills")
        assert doc_type_name in ["acts"]
        assert len(year) == 4

        self.doc_type_name = doc_type_name
        self.year = year

    def __str__(self) -> str:
        return f"ActsBillsPage({self.doc_type_name}, {self.year})"

    def __parse_div_acts_box__(self, div_acts_box):
        h4 = div_acts_box.find("h4")
        heading_text = h4.text.strip()
        if " : " in heading_text:
            doc_num, description = heading_text.split(" : ")
        else:
            heading_text = heading_text.replace(": ", "").strip()
            doc_num = heading_text.lower().replace(" ", "-")

        div_body = div_acts_box.find("div", class_="nTabber_content")
        div_con_box_list = div_body.find_all("div", class_="con_box")
        endorsed_date = (
            div_con_box_list[1].text.replace("Endorsed Date: ", "").strip()
        )
        if len(endorsed_date) != 10:
            log.warning(f"Unexpected date format: {endorsed_date}")
            return None

        a = div_con_box_list[2].find("a")
        url_en = a.get("href") if a else None
        url_si = None
        url_ta = None
        if url_en:
            assert url_en.startswith(
                "https://www.parliament.lk/uploads"
            ), f'"{url_en}"'
            assert "/english/" in url_en, f'"{url_en}"'
            url_si = url_en.replace("/english/", "/sinhala/")
            url_ta = url_en.replace("/english/", "/tamil/")

        d = dict(
            doc_num=doc_num,
            date=endorsed_date,
            description=description,
            lang_to_source_url=dict(
                en=url_en,
                si=url_si,
                ta=url_ta,
            ),
        )
        return Doc.from_dict(d)

    def __get_doc_list_for_page__(self, driver):
        source = driver.page_source
        soup = BeautifulSoup(source, "html.parser")
        doc_list = []
        for div_acts_box in soup.find_all("div", class_="acts_box"):
            doc = self.__parse_div_acts_box__(div_acts_box)
            if doc:
                doc_list.append(doc)

        log.debug(f"Found {len(doc_list)} docs.")
        return doc_list

    def __get_doc_list__(self):
        driver = self.open()

        log.debug('Select "Please select a Legislature"...')
        driver.find_element(By.XPATH, "//div[@id='legis_chzn']").click()
        driver.find_element(By.XPATH, "//li[@id='legis_chzn_o_21']").click()

        log.debug(f"Select {self.year=}...")
        driver.find_element(By.XPATH, "//input[@id='year']").send_keys(
            self.year + Keys.RETURN
        )
        self.sleep(3)

        doc_list = []
        i = 0
        while True:
            i += 1
            doc_list_for_page = self.__get_doc_list_for_page__(driver)
            doc_list.extend(doc_list_for_page)

            a_next = None
            try:
                a_next = driver.find_element(By.XPATH, "//a[text()='Next']")
            except NoSuchElementException:
                log.debug('No "Next" button.')
                break

            if a_next.get_attribute("style") != "cursor: pointer;":
                log.debug("No more pages to scrape.")
                break

            log.debug(f"Clicking Next {i}...")
            a_next.click()
            self.sleep(3)

        self.quit()
        log.debug(f"Found {len(doc_list)} docs for {self}")
        return doc_list

    def scrape(self):
        doc_list = self.__get_doc_list__()
        for doc in doc_list:
            doc.write()
        return doc_list
