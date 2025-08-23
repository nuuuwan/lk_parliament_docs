import argparse

from utils import Log

from lk_acts import Act, PageActsBills
from utils_future import TimedPipeline

log = Log("scrape")
DEFAULT_MAX_DT = 1_200


def get_scrape_years(decade):
    if decade:
        min_year = int(decade[:4])
        max_year = min_year + 9
    else:
        min_year = Act.MIN_YEAR
        max_year = Act.MAX_YEAR

    years = [year for year in range(min_year, max_year + 1)]
    years.reverse()
    return years


def scrape_year(year):
    try:
        page = PageActsBills("acts", str(year))
        page.scrape()
    except Exception as e:
        log.error(f"Error scraping {year=}: {e}")


def metadata_scraper(max_dt, decade):
    log.debug(f"{decade=}")
    years = get_scrape_years(decade)
    log.debug(f"len(years)={len(years):,}, {years=}")

    TimedPipeline(max_dt, scrape_year, years).run()


def float_or_none(v):
    if v == "" or v is None:
        return None
    try:
        return float(v)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{v} is not a valid float")


def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--max_dt", type=float_or_none, default=DEFAULT_MAX_DT
    )
    parser.add_argument("--decade", type=str, default="2020s")
    return parser.parse_args()


if __name__ == "__main__":
    options = get_options()
    metadata_scraper(
        max_dt=options.max_dt or DEFAULT_MAX_DT,
        decade=options.decade,
    )
