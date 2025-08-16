import os
from functools import cached_property

import matplotlib.pyplot as plt
from utils import Log

log = Log("ChartYear")


class ChartYear:
    DIR_IMAGES = "images"
    DIR_IMAGE_PATH = os.path.join("images", "chart_year.png")

    def __init__(self, year_to_list: dict[str, list]):
        self.year_to_list = year_to_list

    @cached_property
    def year_to_num_docs(self):
        return {
            year: len(docs)
            for year, docs in sorted(
                self.year_to_list.items(), key=lambda x: x[0]
            )
        }

    def draw(self):
        years = list(self.year_to_num_docs.keys())
        num_docs = list(self.year_to_num_docs.values())

        plt.bar(years, num_docs)
        plt.xlabel("Year")
        plt.ylabel("Number of Documents")
        plt.title("Number of Documents per Year")
        os.makedirs(self.DIR_IMAGES, exist_ok=True)
        plt.savefig(self.DIR_IMAGE_PATH)
        plt.close()
        log.debug(f"Wrote {self.DIR_IMAGE_PATH}")

        return self.DIR_IMAGE_PATH
