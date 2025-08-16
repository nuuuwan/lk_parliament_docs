import os
from functools import cached_property

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator
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
        items = sorted(
            ((int(y), v) for y, v in self.year_to_num_docs.items()),
            key=lambda t: t[0],
        )
        years = np.array([y for y, _ in items], dtype=int)
        num_docs = np.array([v for _, v in items])

        plt.bar(years, num_docs)
        plt.xlabel("Year")
        plt.ylabel("Number of Documents")
        plt.title("Number of Documents per Year")

        desired = 7
        num_ticks = min(desired, len(years))
        idx = np.linspace(0, len(years) - 1, num_ticks).round().astype(int)
        tick_positions = years[idx]
        plt.xticks(tick_positions, rotation=0)

        os.makedirs(self.DIR_IMAGES, exist_ok=True)
        plt.savefig(self.DIR_IMAGE_PATH, bbox_inches="tight")
        plt.close()
        log.debug(f"Wrote {self.DIR_IMAGE_PATH}")

        return self.DIR_IMAGE_PATH
