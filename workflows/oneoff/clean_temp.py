import os

from utils import JSONFile, Log

from lk_acts.core.act import Act

log = Log("clean_temp")


def delete_files_if_exists(act, file_path_list):
    for delete_path in file_path_list:
        if os.path.exists(delete_path):
            os.remove(delete_path)
            log.debug(f"[{act}] ❌ Deleted {delete_path}")


def clean_temp_for_act(act):
    delete_files_if_exists(
        act,
        [
            act.blocks_path,
            act.blocks_fail_path,
            act.text_path,
            act.text_fail_path,
            act.ocr_blocks_path,
            act.ocr_blocks_fail_path,
            act.ocr_text_path,
            act.ocr_text_fail_path,
        ],
    )


def clean_temp():
    act_list = Act.list_all()
    for act in act_list:
        clean_temp_for_act(act)
    log.info("clean_temp Complete.")


if __name__ == "__main__":
    clean_temp()
