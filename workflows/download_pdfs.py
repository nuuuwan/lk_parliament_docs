import argparse
import sys
import time

from utils import Log

from lk_acts import Act, ActExt

log = Log("scrape")
DEFAULT_MAX_DT = 1_200


def download_pdf_for_act(act):
    pdf_path = act.download_pdf()
    act.extract_txt()

    try:
        ActExt.from_pdf(pdf_path).build(act.act_id)
    except Exception as e:
        log.error(f"Error processing {act.act_id}: {e}")


def download_pdfs(max_dt, decade):
    log.debug(f"{max_dt=}")
    log.debug(f"{decade=}")
    act_list = Act.list_all()
    if decade:
        act_list = [act for act in act_list if act.decade == decade]

    t_start = time.time()
    for act in act_list:
        dt = time.time() - t_start
        if dt > max_dt:
            log.info(f"Stopping. 🛑 {dt:.0f}s > {max_dt}s.")
            sys.exit(0)

        download_pdf_for_act(act)

    log.info("Stopping. 🛑 ALL acts complete.")


def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max_dt", type=str, default=str(DEFAULT_MAX_DT))
    parser.add_argument("--decade", type=str, default=None)
    return parser.parse_args()


if __name__ == "__main__":
    options = get_options()
    download_pdfs(
        max_dt=float(options.max_dt),
        decade=options.decade,
    )
