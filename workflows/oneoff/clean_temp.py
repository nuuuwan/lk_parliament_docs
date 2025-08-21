import os

from utils import JSONFile, Log

from lk_acts.core.act import Act

log = Log("clean_temp")


def clean_temp_for_act(act):
    print(f"[{act}] Cleaning legacy files.", end="\r")
    if os.path.exists(act.blocks_path):
        blocks = JSONFile(act.blocks_path).read()
        block_text = "\n\n".join([block["text"] for block in blocks])
        if len(block_text) < Act.MIN_BLOCK_TEXT_CHARS:
            for delete_path in [act.blocks_path, act.text_path]:
                if os.path.exists(delete_path):
                    os.remove(delete_path)
                    log.debug(f"[{act}] ❌ Deleted {delete_path}")


def clean_temp():
    act_list = Act.list_all()
    for act in act_list:
        clean_temp_for_act(act)


if __name__ == "__main__":
    clean_temp()
