import argparse
import os
import random
import sys
import time

from utils import Log

from lk_acts import Act, ActsBillsPage

log = Log("scrape")
DEFAULT_MAX_DT = 1_200
MAX_YEAR = 2025
MIN_YEAR = 1945

P_RETRY = 0.1


def get_scrape_years(decade):
    if decade:
        min_year = int(decade[:4])
        max_year = min_year + 9
    else:
        min_year = MIN_YEAR
        max_year = MAX_YEAR

    years = [year for year in range(min_year, max_year + 1)]
    years.reverse()
    years_for_scraping = []
    for year in years:
        dir_year = Act.get_dir_year(year)
        if not os.path.exists(dir_year) or random.random() < P_RETRY:
            years_for_scraping.append(year)
    return years_for_scraping


def scrape_year(year):
    try:
        page = ActsBillsPage("acts", str(year))
        page.scrape()
    except Exception as e:
        log.error(f"Error scraping {year=}: {e}")


def scrape(max_dt, decade):
    log.debug(f"{max_dt=}")
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
    parser.add_argument("--max_dt", type=float, default=DEFAULT_MAX_DT)
    parser.add_argument("--decade", type=str, default=None)
    return parser.parse_args()


if __name__ == "__main__":
    options = get_options()
    scrape(
        max_dt=options.max_dt,
        decade=options.decade,
    )
