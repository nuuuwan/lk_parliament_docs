import sys
import time

from utils import Log

from lk_acts import Act, ActExt
from workflows.metadata_scraper import DEFAULT_MAX_DT, get_options

log = Log("scrape")


def text_extractor_for_act(act):
    act.extract_txt()

    try:
        ActExt.from_pdf(act.pdf_path).build(act.act_id)
    except Exception as e:
        log.error(f"Error processing {act.act_id}: {e}")


def text_extractor(max_dt, decade):
    log.debug(f"{max_dt=}")
    log.debug(f"{decade=}")
    act_list = Act.list_from_decade(decade)

    t_start = time.time()
    for act in act_list:
        dt = time.time() - t_start
        if dt > max_dt:
            log.info(f"Stopping. 🛑 {dt:.0f}s > {max_dt}s.")
            sys.exit(0)

        text_extractor_for_act(act)

    log.info("Stopping. 🛑 ALL acts complete.")


if __name__ == "__main__":
    options = get_options()
    text_extractor(
        max_dt=options.max_dt or DEFAULT_MAX_DT,
        decade=options.decade,
    )
