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


def download_pdfs(max_dt):
    act_list = Act.list_all()
    t_start = time.time()
    for act in act_list:
        dt = time.time() - t_start
        if dt > max_dt:
            log.info(f"Stopping. 🛑 {dt:.1f}s > {max_dt}s.")
            sys.exit(0)

        download_pdf_for_act(act)

    log.info("Stopping. 🛑 ALL acts complete.")


if __name__ == "__main__":
    download_pdfs(
        max_dt=float(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_MAX_DT,
    )
