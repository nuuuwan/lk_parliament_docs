import os
from functools import cached_property
from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np
from utils import Log

from lk_acts.core import ActType

log = Log("ChartYear")


class ChartYear:
    DIR_IMAGES = "images"
    DIR_IMAGE_PATH = os.path.join("images", "chart_year.png")

    def __init__(self, year_to_type_to_list: Dict[str, Dict[str, List]]):
        self.year_to_type_to_list = year_to_type_to_list

    @cached_property
    def years_sorted(self) -> List[int]:
        return sorted(int(y) for y in self.year_to_type_to_list.keys())

    @cached_property
    def year_type_counts(self) -> Dict[int, Dict[str, int]]:
        idx = {}
        for y in self.years_sorted:
            y_str = str(y)
            idx[y] = {
                t.name: len(self.year_to_type_to_list[y_str].get(t.name, []))
                for t in ActType.list_all()
            }
        return idx

    @cached_property
    def year_to_num_docs(self) -> Dict[int, int]:
        return {
            y: sum(self.year_type_counts[y].values())
            for y in self.years_sorted
        }

    def draw(self):
        years = np.array(self.years_sorted, dtype=int)
        types = np.array(
            [doc_act_type.name for doc_act_type in ActType.list_all()]
        )

        counts = np.array(
            [
                [self.year_type_counts.get(y, {}).get(t, 0) for y in years]
                for t in types
            ],
            dtype=int,
        )

        plt.figure(figsize=(16, 9))
        bottom = np.zeros(len(years), dtype=int)

        for i, t_key in enumerate(types):
            doc_act_type = ActType.from_name(t_key)
            plt.bar(
                years,
                counts[i],
                bottom=bottom,
                label=f"{doc_act_type.name}",
                color=doc_act_type.color,
                edgecolor="white",
                linewidth=0.25,
            )
            bottom += counts[i]

        plt.xlabel("Year")
        plt.ylabel("Number of Acts")
        plt.title("Number of Acts per Year, by Type")
        plt.xticks(self._tick_positions(years))
        plt.legend()

        os.makedirs(self.DIR_IMAGES, exist_ok=True)
        plt.savefig(self.DIR_IMAGE_PATH, bbox_inches="tight")
        plt.close()
        log.debug(f"Wrote {self.DIR_IMAGE_PATH}")
        return self.DIR_IMAGE_PATH

    @staticmethod
    def _tick_positions(years: np.ndarray, desired: int = 7) -> List[int]:
        if len(years) <= desired:
            return list(years)
        idx = np.linspace(0, len(years) - 1, desired).round().astype(int)
        return list(years[idx])
