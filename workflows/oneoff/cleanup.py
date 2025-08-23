import os

from utils import JSONFile, Log

from lk_acts.core.act import Act

log = Log("clean_temp")


def cleanup_fails_for_act(act):
    act.cleanup_fails()


def cleanup():
    act_list = Act.list_all()
    for act in act_list:
        cleanup_fails_for_act(act)
    log.info("clean_temp Complete.")


if __name__ == "__main__":
    cleanup()
