import sys
import time

from utils import Log

from lpd import ActsBillsPage

log = Log("scrape")
DEFAULT_MAX_DT = 1_200
MAX_YEAR = 2025
MIN_YEAR = 1800


def scrape_year(year):
    log.debug("-" * 32)
    log.info(f"Running scrape for {year=}")
    page = ActsBillsPage("acts", str(year))
    page.scrape()
    log.debug("-" * 32)


def scrape(max_dt):
    year = MAX_YEAR
    t_start = time.time()
    while True:
        dt = time.time() - t_start
        if dt > max_dt:
            log.info(f"Stopping. 🛑 {dt:.1f}s > {max_dt}s.")
            sys.exit(0)

        scrape_year(year)

        year -= 1
        if year < MIN_YEAR:
            log.info(f"Stopping. 🛑 {year} < {MIN_YEAR}")
            sys.exit(0)


if __name__ == "__main__":
    scrape(max_dt=sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MAX_DT)
