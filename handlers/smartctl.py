import datetime
import json
import re
import subprocess

from log import log

from .handlers import Handler


class SMARTHandler(Handler):
    """
    Collects information based on smartctl

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

                raw_info = json.loads(cmd.stdout)
        # for k, vals in raw.items():
        #     if "coretemp" in k:

        #         for coreidstr, fields in vals.items():
        #             if isinstance(fields, dict):
        #                 isa_num = (re.findall("\d+", k) or [""])[0]
        #                 core_num = (re.findall("\d+", coreidstr) or [""])[0]
        #                 identifier = f"{isa_num}-{core_num}"
        #                 clean_fields = {
        #                     re.sub("\d*", "", y): t for y, t in fields.items()
        #                 }
        #                 r = {
        #                     "measurement": "cpu_temp",
        #                     "tags": {
        #                         "identifier": identifier,
        #                     },
        #                     "fields": clean_fields,
        #                     "time": datetime.datetime.now().isoformat(),
        #                 }
        #                 self.data_buffer.append(r)
        #     elif "power" in k:
        #         for pduidstr, fields in vals.items():
        #             if isinstance(fields, dict):
        #                 sens_num = (re.findall("\d+", k) or [""])[0]
        #                 pdu_num = (re.findall("\d+", pduidstr) or [""])[0]
        #                 identifier = f"{pdu_num}-{core_num}"
        #                 clean_fields = {
        #                     re.sub("\d*", "", y): t for y, t in fields.items()
        #                 }
        #                 r = {
        #                     "measurement": "pow_meter",
        #                     "tags": {
        #                         "identifier": identifier,
        #                     },
        #                     "fields": clean_fields,
        #                     "time": datetime.datetime.now().isoformat(),
        #                 }
        #                 self.data_buffer.append(r)
