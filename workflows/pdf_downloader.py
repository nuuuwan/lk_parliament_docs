from utils import Log

from lk_acts import Act
from utils_future import TimedPipeline
from workflows.metadata_scraper import DEFAULT_MAX_DT, get_options

log = Log("pdf_downloader")


def pdf_downloader(max_dt, decade):
    log.debug(f"{max_dt=}")
    log.debug(f"{decade=}")
    act_list = Act.list_from_decade(decade)

    TimedPipeline(max_dt, lambda act: act.download_pdf, act_list).run()


if __name__ == "__main__":
    options = get_options()
    pdf_downloader(
        max_dt=options.max_dt or DEFAULT_MAX_DT,
        decade=options.decade,
    )
