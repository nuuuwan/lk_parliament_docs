from dateutil import parser


class Parse:
    DATE_FORMAT = "%Y-%m-%d"

    @staticmethod
    def float(value) -> float:
        try:
            return float(value)
        except ValueError:
            return None

    @staticmethod
    def date(value) -> str:
        try:
            parsed = parser.parse(value)
            formatted = parsed.strftime(Parse.DATE_FORMAT)
            return formatted
        except (ValueError, TypeError):
            return None
