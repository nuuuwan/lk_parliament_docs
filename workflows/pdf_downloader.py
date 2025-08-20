import sys
import time

from utils import Log

from lk_acts import Act
from workflows.metadata_scraper import DEFAULT_MAX_DT, get_options

log = Log("scrape")


def pdf_downloader(max_dt, decade):
    log.debug(f"{max_dt=}")
    log.debug(f"{decade=}")
    act_list = Act.list_from_decade(decade)

    t_start = time.time()
    for act in act_list:
        dt = time.time() - t_start
        if dt > max_dt:
            log.info(f"Stopping. 🛑 {dt:.0f}s > {max_dt}s.")
            sys.exit(0)

        act.download_pdf()

    log.info("Stopping. 🛑 ALL acts complete.")


if __name__ == "__main__":
    options = get_options()
    pdf_downloader(
        max_dt=options.max_dt or DEFAULT_MAX_DT,
        decade=options.decade,
    )
