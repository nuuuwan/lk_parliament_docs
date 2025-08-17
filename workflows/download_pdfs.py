import sys
import time

from utils import Log

from lk_acts import Act

log = Log("scrape")
DEFAULT_MAX_DT = 1_200


def download_pdfs(max_dt):
    act_list = Act.list_all()
    t_start = time.time()
    for act in act_list:
        dt = time.time() - t_start
        if dt > max_dt:
            log.info(f"Stopping. 🛑 {dt:.1f}s > {max_dt}s.")
            sys.exit(0)

        act.download_pdf()

    log.info("Stopping. 🛑 ALL acts complete.")


if __name__ == "__main__":
    download_pdfs(
        max_dt=float(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_MAX_DT,
    )
