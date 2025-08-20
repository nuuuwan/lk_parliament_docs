import time

from utils import Log

log = Log("TimedPipeline")


class TimedPipeline:
    def __init__(self, max_dt, func_process, data_list):
        self.max_dt = max_dt
        self.func_process = func_process
        self.data_list = data_list

    def run(self):
        log.debug(f"max_dt={self.max_dt}s")

        t_start = time.time()
        n_data = len(self.data_list)
        for i_data, data in enumerate(self.data_list, start=1):
            dt = time.time() - t_start
            if dt > self.max_dt:
                log.info(f"🛑 Stopping. ⏰ {dt:.0f}s > {self.max_dt}s.")
                return

            log.debug("-" * 64)
            log.info(
                f"[{i_data}/{n_data}]"
                + f" Processing {data}"
                + f" [{dt:.0f}s/{self.max_dt}s] "
            )
            self.func_process(data)

        log.info("🛑 Stopping. ALL data complete.")
