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
    if os.path.exists(act.blocks_path):
        blocks = JSONFile(act.blocks_path).read()
        block_text = "\n\n".join([block["text"] for block in blocks])
        if len(block_text) < Act.MIN_BLOCK_TEXT_CHARS:
            delete_files_if_exists(act, [act.blocks_path, act.text_path])
        else:
            delete_files_if_exists(
                act,
                [
                    act.ocr_blocks_path,
                    act.ocr_blocks_fail_path,
                    act.ocr_text_path,
                    act.ocr_text_fail_path,
                ],
            )
    else:
        delete_files_if_exists(act, [act.text_path])


def clean_temp():
    act_list = Act.list_all()
    for act in act_list:
        clean_temp_for_act(act)
    log.info(f"clean_temp Complete.")


if __name__ == "__main__":
    clean_temp()
