from prometheus_client.core import REGISTRY, Metric
from prometheus_client import start_http_server
from logconf import get_logger
from get_all_tenants_alarms import collect_all_tenant_enm_management_alarms

import time
import urllib3

# Suppress InsecureWarning while contacting endpoints
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Initiating STDOUT log handler

logger = get_logger()


class AlarmCollector(object):

    def __init__(self):
        #  self._metrics_dict = metrics_dict
        pass

    def collect(self):
        logger.info('Collecting ENM Management Alarm Metrics')
        tenant_alarm_list = collect_all_tenant_enm_management_alarms()

        metric = Metric('enm_management_alarms', "Metrics taken in every N sec", 'summary')
        for tenant_alarm_dict in tenant_alarm_list:
            tenant_name = next(iter(tenant_alarm_dict.keys()))
            alarm_list = next(iter(tenant_alarm_dict.values()))
            # alarm list extracted above is a list of dict of alarms object per tenant
            for alarm in alarm_list:
                if alarm['Alarm_count']:
                    is_repeated_alarm = 1
                else:
                    is_repeated_alarm = 0
                metric.add_sample('enm_management_alarms', value=is_repeated_alarm,
                                  labels={'severity': alarm['Severity'],
                                          'object_of_reference': alarm['object_of_reference'],
                                          'probable_cause': alarm['Probable_cause'],
                                          'event_time': alarm['Event_time'],
                                          'specific_problem': alarm['Specific_Problem'],
                                          'tenant_name': tenant_name})
        yield metric


if __name__ == '__main__':
    logger.info('Initializing Alarm Exporter')
    start_http_server(8082)
    logger.info('Alarm Exporter listening on 8082')
    REGISTRY.register(AlarmCollector())

    while True:
        time.sleep(10)
