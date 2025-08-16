import os
import random
import sys
import time

from utils import Log

from lpd import ActsBillsPage

log = Log("scrape")
DEFAULT_MAX_DT = 1_200
MAX_YEAR = 2025
MIN_YEAR = 1800

P_SCRAPE_AGAIN = 0.1


def has_year_been_scraped(year: str) -> bool:
    dir_year = os.path.join("data", "acts", str(year))
    return os.path.exists(dir_year) and os.path.isdir(dir_year)


def scrape_year(year):
    if has_year_been_scraped(year):
        log.info(f"{year=} already scraped.")
        if random.random() < P_SCRAPE_AGAIN:
            log.info(f"Re-scraping {year=}.")
        else:
            log.info(f"Skipping {year=}.")
            return

    page = ActsBillsPage("acts", str(year))
    page.scrape()


def scrape(max_dt):
    year = MAX_YEAR
    t_start = time.time()
    while True:
        dt = time.time() - t_start
        if dt > max_dt:
            log.info(f"Stopping. 🛑 {dt:.1f}s > {max_dt}s.")
            sys.exit(0)

        log.debug("-" * 32)
        log.info(f"[{dt:.1f}s/{max_dt}s] Running scrape for {year=}")
        scrape_year(year)
        log.debug("-" * 32)

        year -= 1
        if year < MIN_YEAR:
            log.info(f"Stopping. 🛑 {year} < {MIN_YEAR}")
            sys.exit(0)


if __name__ == "__main__":
    scrape(
        max_dt=float(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_MAX_DT,
    )
