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

P_SHUFFLE = 0.1


def scrape_year(year):
    page = ActsBillsPage("acts", str(year))
    page.scrape()


def get_scrape_years():
    years = [year for year in range(MIN_YEAR, MAX_YEAR + 1)]
    years.sort(reverse=True)
    if random.random() < P_SHUFFLE:
        log.debug("🎲 Shuffling years")
        random.shuffle(years)
    return years


def scrape(max_dt):
    years = get_scrape_years()

    t_start = time.time()
    for year in years:
        dt = time.time() - t_start
        if dt > max_dt:
            log.info(f"Stopping. 🛑 {dt:.1f}s > {max_dt}s.")
            sys.exit(0)

        log.debug("-" * 64)
        log.info(f"[{dt:.1f}s/{max_dt}s] Running scrape for {year=}")
        scrape_year(year)

    log.info("Stopping. 🛑 ALL years complete.")


if __name__ == "__main__":
    scrape(
        max_dt=float(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_MAX_DT,
    )
