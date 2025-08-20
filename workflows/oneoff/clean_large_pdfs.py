import os

from utils import Log

from lk_acts.core.act import Act

log = Log("clean_large_pdfs")
LARGE_PDF_SIZE_LIMIT_K = 100


def __clean_hot__(act):
    pdf_path = act.pdf_path
    pdf_size_k = os.path.getsize(pdf_path) / 1_000.0

    log.warning(f"❌ Deleting {pdf_path} ({pdf_size_k:,.0f} KB)")
    os.remove(pdf_path)

    for other_path in [
        act.txt_path,
        os.path.join(act.dir_act_data, "README.md"),
        os.path.join(act.dir_act_data, "act.json"),
    ]:
        if os.path.exists(other_path):
            log.warning(f"\t❌ Deleting {other_path}")
            os.remove(other_path)

    print("-" * 32)


def clean_large_pdfs_for_act(act):
    pdf_path = act.pdf_path
    if not os.path.exists(pdf_path):
        return

    pdf_size_k = os.path.getsize(pdf_path) / 1_000.0
    if pdf_size_k < LARGE_PDF_SIZE_LIMIT_K:
        return

    __clean_hot__(act)


def clean_large_pdfs():
    act_list = Act.list_all()
    for act in act_list:
        clean_large_pdfs_for_act(act)


if __name__ == "__main__":
    clean_large_pdfs()
