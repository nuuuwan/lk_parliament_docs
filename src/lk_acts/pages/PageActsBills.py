from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils import Log

from lk_acts.core import Act
from utils_future import WebPage

log = Log("PageActsBills")


class PageActsBills(WebPage):
    URL = "https://www.parliament.lk/en/acts-bills"

    def __init__(self, doc_type_name, year):
        super().__init__(self.URL)
        assert doc_type_name in ["acts"]
        assert len(year) == 4

        self.doc_type_name = doc_type_name
        self.year = year

    def __str__(self) -> str:
        return f"PageActsBills({self.doc_type_name}, {self.year})"

    def __parse_div_acts_box__(self, div_acts_box):  # noqa: CFQ004 !HACK
        h4 = div_acts_box.find("h4")
        if not h4:
            log.error("No heading found.")
            return None
        heading_text = h4.text.strip()
        if " : " in heading_text:
            num, description = heading_text.split(" : ")
        else:
            heading_text = heading_text.replace(": ", "").strip()
            num = heading_text.lower().replace(" ", "-")
            description = heading_text
        div_body = div_acts_box.find("div", class_="nTabber_content")
        div_con_box_list = div_body.find_all("div", class_="con_box")
        endorsed_date = (
            div_con_box_list[1].text.replace("Endorsed Date: ", "").strip()
        )
        if len(endorsed_date) != 10:
            log.error(f"Unexpected date format: {endorsed_date}")
            return None
        a = div_con_box_list[2].find("a")
        url_pdf_en = a.get("href") if a else None
        if not url_pdf_en:
            log.warning(f"[{num}] No PDF URL found.")

        return Act.from_dict(
            dict(
                num=num,
                date=endorsed_date,
                description=description,
                url_pdf_en=url_pdf_en,
            )
        )

    def __get_act_list_for_page__(self, driver):
        source = driver.page_source
        soup = BeautifulSoup(source, "html.parser")
        act_list = []
        for div_acts_box in soup.find_all("div", class_="acts_box"):
            doc = self.__parse_div_acts_box__(div_acts_box)
            if doc and doc.is_within_valid_time_range():
                act_list.append(doc)

        log.debug(f"Found {len(act_list)} docs.")
        return act_list

    def __get_act_list__(self):
        driver = self.open()

        log.debug('Select "Please select a Legislature"...')
        driver.find_element(By.XPATH, "//div[@id='legis_chzn']").click()
        driver.find_element(By.XPATH, "//li[@id='legis_chzn_o_21']").click()

        log.debug(f"Select {self.year=}...")
        driver.find_element(By.XPATH, "//input[@id='year']").send_keys(
            self.year + Keys.RETURN
        )
        self.sleep(3)

        act_list = []
        i = 0
        while True:
            i += 1
            act_list_for_page = self.__get_act_list_for_page__(driver)
            act_list.extend(act_list_for_page)

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
        log.debug(f"Found {len(act_list)} docs for {self}")
        return act_list

    def scrape(self):
        act_list = self.__get_act_list__()
        for doc in act_list:
            doc.write()
        return act_list
