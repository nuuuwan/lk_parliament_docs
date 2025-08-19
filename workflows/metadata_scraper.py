import argparse
import sys
import time

from utils import Log

from lk_acts import ActsBillsPage

log = Log("scrape")
DEFAULT_MAX_DT = 1_200
MAX_YEAR = 2025
MIN_YEAR = 1945


def get_scrape_years(decade):
    if decade:
        min_year = int(decade[:4])
        max_year = min_year + 9
    else:
        min_year = MIN_YEAR
        max_year = MAX_YEAR

    years = [year for year in range(min_year, max_year + 1)]
    years.reverse()
    return years


def scrape_year(year):
    try:
        page = ActsBillsPage("acts", str(year))
        page.scrape()
    except Exception as e:
        log.error(f"Error scraping {year=}: {e}")


def metadata_scraper(max_dt, decade):
    log.debug(f"{max_dt=}")
    log.debug(f"{decade=}")
    years = get_scrape_years(decade)
    log.debug(f"len(years)={len(years):,}, {years=}")

    t_start = time.time()
    for year in years:
        dt = time.time() - t_start
        if dt > max_dt:
            log.info(f"Stopping. 🛑 {dt:.0f}s > {max_dt}s.")
            sys.exit(0)

        log.debug("-" * 64)
        log.info(f"[{dt:.0f}s/{max_dt}s] Running scrape for {year=}")
        scrape_year(year)

    log.info("Stopping. 🛑 ALL years complete.")


def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max_dt", type=str, default=str(DEFAULT_MAX_DT))
    parser.add_argument("--decade", type=str, default=None)
    return parser.parse_args()


if __name__ == "__main__":
    options = get_options()
    metadata_scraper(
        max_dt=float(options.max_dt),
        decade=options.decade,
    )
