import re
from dataclasses import dataclass


@dataclass
class PDFBlock:
    bbox: tuple[float, float, float, float]
    text: str
    font_family: str
    font_size: float

    @staticmethod
    def extract(re_expr, block_list: list["PDFBlock"]) -> float:
        for block in block_list:
            print(block.text)
            match = re.search(re_expr, block.text)
            if match:
                return match.group(1)
        return None
