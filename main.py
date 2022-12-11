import os
import time

import yaml
from apscheduler.schedulers.blocking import BlockingScheduler

import handlers
from log import log

if __name__ == "__main__":
    log.info("Launching")
    log.info("Loading config")
    config = yaml.safe_load(open("config.yaml"))["app"]
    os.environ["TZ"] = "Europe/Paris"  # set new timezone
    time.tzset()
    scheduler = BlockingScheduler(timezone="Europe/Paris")
    for to_load in config["handlers_enabled"]:
        log.info(f"loading {to_load}")
        handler = getattr(handlers, to_load)()
        log.info(f"scheduling {handler} jobs")
        scheduler.add_job(
            handler.run, "interval", seconds=handler.config["cmd_interval_sec"]
        )
        if handler.config["has_maintenance"]:
            log.info(f"{handler} has maintenance jobs. Scheduling them...")
            scheduler.add_job(
                handler.run_maintenance,
                "interval",
                seconds=handler.config["maintenance_interval_sec"],
            )

    log.info(f"jobs added : {scheduler.get_jobs()}")
    scheduler.start()
    log.info("running...")
