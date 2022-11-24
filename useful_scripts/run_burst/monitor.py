#!/usr/bin/env python3

import sys
from socket import gethostname
from os import getenv
import json
from time import sleep
import getpass


class Monitor(object):
    def __init__(self):
        self.loc = str(gethostname()).upper()[0:3]
        if self.loc == 'XSJ':
            self.mon_file = '/group/xsjboardfarm/lsfdata/' \
                            'xsj-boardfarm/bjobs_all.json'
        elif self.loc == 'XHD':
            self.mon_file = '/group/bflsfdata/xhd-boardfarm/bjobs_all.json'
        else:
            print("Unsupported machine! Try with a XSJ or XHD machine")
            sys.exit(-1)
        self.user = getpass.getuser()


def systest_q_json(mon):
    count = 0
    line = 'JOBID   USER    STAT  QUEUE      FROM_HOST   EXEC_HOST   ' \
           'JOB_NAME   SUBMIT_TIME\\n'
    try:
        with open(str(mon.mon_file)) as data_file:
            job_data = json.load(data_file)
            for job in job_data:
                if job['USER'] == mon.user:
                    if job['STAT'] == 'RUN' or job['STAT'] == 'PEND':
                        line = line + '{} {} {} {} {} {} {} {} \\n'.format(
                            job['JOBID'], job['USER'], job['STAT'],
                            job['QUEUE'], job['FROM_HOST'], job['EXEC_HOST'],
                            job['JOB_NAME'], job['SUBMIT_TIME'])
                        count = count + 1
            if count == 0:
                line = 'No unfinished job found in queue <hwboard>'
            return line
    except IOError:
        print("ERROR: Unable to open " + str(mon.mon_file))
        sys.exit(-1)


if __name__ == "__main__":
    if sys.version_info[0] < 3 or sys.version_info[1] < 6:
        print("This script requires a python version of at least 3.6 Exiting.")
        exit(-1)
    if sys.version_info[1] != 8 or sys.version_info[2] != 3:
        print("WARN: This script is only tested with python version 3.8.3")
    monitor = Monitor()
    sys_status = systest_q_json(monitor)
    while 'No unfinished job found in queue <hwboard>' not in sys_status:
        line_list = sys_status.split('\\n')
        for item in line_list:
            print(item)
        sys_status = systest_q_json(monitor)
        sleep(120)
