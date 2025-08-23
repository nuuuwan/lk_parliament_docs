import re

from utils_future.Parse import Parse


class ActTextParserMixin:
    MAX_LINES_TO_PARSE = 20

    @staticmethod
    def __parse_generic__(text, regexp, key_list, func_postprocess_list):
        pattern = re.compile(regexp, re.IGNORECASE)
        match = pattern.search(text)

        if not match:
            return None
        d = {}
        for k, func_postprocess in zip(key_list, func_postprocess_list):
            d[k] = func_postprocess(match.group(k))
        return d

    @staticmethod
    def __parse_act_title__(text):
        return ActTextParserMixin.__parse_generic__(
            text,
            r"(?P<name>.+?),\s*No\.\s*(?P<number>\d+)\s*OF\s*(?P<year>\d{4})",
            ["name", "number", "year"],
            [lambda x: x.strip().title(), lambda x: int(x), lambda x: int(x)],
        )

    @staticmethod
    def __parse_certified_date__(text):
        return ActTextParserMixin.__parse_generic__(
            text,
            r"\[Certified on\s+(?P<date>.*)\]",
            ["date"],
            [lambda x: Parse.date(x)],
        )

    @staticmethod
    def __parse_published_as__(text):
        return ActTextParserMixin.__parse_generic__(
            text,
            r"Published as\s+(?P<published_as>.*)",
            ["published_as"],
            [lambda x: x.strip().title()],
        )

    @staticmethod
    def __parse_price__(text):
        return ActTextParserMixin.__parse_generic__(
            text,
            r"Price\s*:\s*Rs\.\s*(?P<price>\d+\.\d+)\s*Postage\s*:\s*Rs\.\s*(?P<price_postage>\d+\.\d+)",  # noqa: E501
            ["price", "price_postage"],
            [Parse.float, Parse.float],
        )

    def parse_text(self):

        text = self.get_text(min_mean_p_confidence=0.5)
        if not text:
            return {}
        lines = text.splitlines()
        for i_line, line in enumerate(
            lines[: self.MAX_LINES_TO_PARSE], start=1
        ):
            print(i_line, line)

        d = {}
        for line in lines[: self.MAX_LINES_TO_PARSE]:
            for func in [
                self.__parse_act_title__,
                self.__parse_certified_date__,
                self.__parse_published_as__,
                self.__parse_price__,
            ]:
                result = func(line)
                if result:
                    d.update(result)
        print(d)
        return d
