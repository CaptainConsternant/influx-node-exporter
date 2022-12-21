import datetime
import json
import re
import subprocess

from log import log

from .handlers import Handler


class SMARTHandler(Handler):
    """
    Collects information based on smartctl
    Gets command to run from config.yaml

    :param Handler: _description_
    :type Handler: _type_
    """

    def collect(self):
        for drive in self.config["drive_paths"]:
            for cciss in self.config["cciss_identifiers"]:

                cmd = subprocess.run(
                    (
                        self.config["cmd"]
                        .replace("<DP>", str(drive))
                        .replace("<CI>", str(cciss))
                        .split(" ")
                    ),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )

                js = json.loads(cmd.stdout)
                r = {
                    "measurement": "smart_meter",
                    "tags": {
                        "identifier": js["device"]["info_name"],
                    },
                    "fields": {
                        "vendor": js["vendor"],
                        "capacity_bytes": js["user_capacity"]["bytes"],
                        "rpm": js["rotation_rate"],
                        "temp": js["temperature"]["current"],
                        "power_on_minutes": js["power_on_time"]["hours"] * 60
                        + js["power_on_time"]["minutes"],
                        "smart_passed": js["smart_status"]["passed"],
                        "errors": js["scsi_grown_defect_list"]
                        + js["scsi_error_counter_log"]["read"][
                            "total_uncorrected_errors"
                        ]
                        + js["scsi_error_counter_log"]["write"][
                            "total_uncorrected_errors"
                        ],
                    },
                    "time": datetime.datetime.now().isoformat(),
                }
                self.data_buffer.append(r)

    def run_maintenance(self):
        for cmdstr in self.config["maintenance_cmds"]:
            for drive in self.config["drive_paths"]:
                for cciss in self.config["cciss_identifiers"]:
                    cmd = subprocess.run(
                        (
                            cmdstr.replace("<DP>", str(drive))
                            .replace("<CI>", str(cciss))
                            .split(" ")
                        ),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                    )
