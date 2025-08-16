from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils import Log

from utils_future import WebPage

log = Log("ActsBillsPage")


class ActsBillsPage(WebPage):

    def __init__(self, year, doc_type_name):
        super().__init__("https://www.parliament.lk/en/acts-bills")
        assert len(year) == 4
        assert doc_type_name in ["acts", "bills"]
        self.year = year
        self.doc_type_name = doc_type_name

    def __parse_div_acts_box__(self, div_acts_box):
        h4 = div_acts_box.find("h4")
        heading_text = h4.text.strip()
        doc_num, description = heading_text.split(" : ")
        assert "/" in doc_num, f'"{doc_num}"'
        doc_id = doc_num.replace("/", "-")

        div_body = div_acts_box.find("div", class_="nTabber_content")
        div_con_box_list = div_body.find_all("div", class_="con_box")
        endorsed_date = (
            div_con_box_list[1].text.replace("Endorsed Date: ", "").strip()
        )
        assert len(endorsed_date) == 10, f'"{endorsed_date}"'

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

        return dict(
            doc_type_name=self.doc_type_name,
            date=endorsed_date,
            description=description,
            endorsed_date=endorsed_date,
            lang_to_source_url=dict(
                en=url_en,
                si=url_si,
                ta=url_ta,
            ),
            doc_num=doc_num,
            doc_id=doc_id,
        )

    def get_doc_list(self):
        driver = self.open()

        if self.doc_type_name == "bills":
            a_bills = driver.find_element(By.XPATH, "//a[@id='hbills']")
            a_bills.click()

        div_dropdown = driver.find_element(
            By.XPATH, "//div[@id='legis_chzn']"
        )
        div_dropdown.click()

        li_legis = driver.find_element(
            By.XPATH, "//li[@id='legis_chzn_o_21']"
        )
        li_legis.click()

        input_year = driver.find_element(By.XPATH, "//input[@id='year']")
        input_year.send_keys(self.year + Keys.RETURN)

        self.sleep(3)
        driver.save_screenshot("acts_bills_page-1.png")

        source = self.driver.page_source
        soup = BeautifulSoup(source, "html.parser")

        doc_list = []
        for div_acts_box in soup.find_all("div", class_="acts_box"):
            doc = self.__parse_div_acts_box__(div_acts_box)
            doc_list.append(doc)

        self.quit()
        log.debug(f"Found {len(doc_list)} docs for {self}")
        return doc_list
