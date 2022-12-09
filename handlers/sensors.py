import datetime
import json
import re
from subprocess import check_output

from .handlers import Handler


class SensorsHandler(Handler):
    """
    Collects information based on lm_sensor

    :param Handler: _description_
    :type Handler: _type_
    """    
    database_name = "sensors"

    def collect(self):
        raw = json.loads(check_output(['sensors','-j']).decode())
        for k,vals in raw.items():
            if "coretemp" in k :

                for coreidstr, fields in vals.items():
                    if isinstance(fields,dict):
                        isa_num=(re.findall('\d+', k) or [''])[0]
                        core_num=(re.findall('\d+', coreidstr) or [''])[0]
                        identifier =f"{isa_num}-{core_num}"
                        clean_fields = {re.sub('\d*','',y):t for y,t in fields.items()}
                        r= {
                                "measurement": "cpu_temp",
                                "tags":{
                                    'identifier': identifier,
                                },
                                "fields":clean_fields,
                                "time":datetime.datetime.now().isoformat()

                            }
                        self.data_buffer.append(r)
            elif "power" in k:
                for pduidstr, fields in vals.items():
                    if isinstance(fields,dict):
                        sens_num=(re.findall('\d+', k) or [''])[0]
                        pdu_num=(re.findall('\d+', pduidstr) or [''])[0]
                        identifier =f"{pdu_num}-{core_num}"
                        clean_fields = {re.sub('\d*','',y):t for y,t in fields.items()}
                        r= {
                                "measurement": "pow_meter",
                                "tags":{
                                    'identifier': identifier,
                                },
                                "fields":clean_fields,
                                "time":datetime.datetime.now().isoformat()

                            }
                        self.data_buffer.append(r)
 