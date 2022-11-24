#!/usr/bin/env python3

import sys
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    print("This script requires a python version of at least 3.6 Exiting.")
    exit(-1)
if sys.version_info[1] != 8 or sys.version_info[2] != 3:
    print("WARN: This script is only tested with python version 3.8.3")

# Module imports
import datetime
import shlex
import subprocess
import argparse
import smtplib
import getpass
from pathlib import Path
from os import getcwd
from os import getenv
from os import system
from os import listdir
from os import path
from os import sep
from time import time
from time import localtime
from time import sleep
from time import strftime
from socket import gethostname
from email.mime.text import MIMEText
import re
import json
# Importing functions from other local files
from update import source_setup_warning
from update import systest_job_mon
from update import print_systest_mon_status
from update import update_json_with_timeout
from update import read_json
from update import write_json
from validity import is_exist_profile
from validity import is_cmt_profile
from help import get_host_location
from options import pci_cluster_dictionary
from database import myMongoDB
import run_burst
import run_status
 
# Used instead of #defines
ERROR_MSG_ENABLE = 1
LAUNCH_ENABLE = 1
CREATE_CSV = True

# Interval of systest monitoring(sec)
monitor_interval = 3

# Saves the start of job monitoring
monitor_start_time = datetime.datetime.now()
regression_utc_time = datetime.datetime.utcnow()
print(str(monitor_start_time))

# Argument parser
parser = argparse.ArgumentParser(
    description='Run BURST regression',
    epilog='Queries Contact: burst_script_team@xilinx.com')

parser.add_argument('-l', '--list',
                    action='store_true',
                    help='List out the available profiles')

parser.add_argument('profile', nargs='*',
                    help='Accepts profile names to run')

parser.add_argument('-nb', '--no_build',
                    action='store_true',
                    help='BURST Build disable flag')

parser.add_argument('-nu', '--no_update',
                    action='store_true',
                    help='Run burst update disable flag')

parser.add_argument('-nm', '--no_monitor',
                    action='store_true',
                    help='Run burst update disable flag')

parser.add_argument('-te', '--toggle_exclude',
                    action='store_true',
                    help='Flag to toggle using the daily regression '
                         ' board exclude file located at /home/xppc/burst/'
                         'latest_burst/manual_board_exclude.json')

parser.add_argument('-upe', '--update_exclude',
                    action='store_true',
                    help='Flag to update the manual exclude file'
                         'located in $SCRIPTS/run_burst/'
                         'manual_board_exclude.json')

parser.add_argument('-rd', '--read',
                    help='Reads a profile, expects a valid profile name')

parser.add_argument('-frd', '--force_read',
                    help='Reads a profile, creates the log folders'
                         ' and prints run burst commands')

parser.add_argument('-dl', '--dont_launch',
                    action='store_true',
                    help='Dont execute systest commands')

parser.add_argument('--logs_dir', '-lp',
                    help='Specify a log path to save the results')

parser.add_argument('--board_tag', '-bt',
                    default=None,
                    help='Specify the complete board tag to acquire a specific '
                         'setup, will be used for all runs in profile')

parser.add_argument('-to', '--time_out',
                    type=int,
                    help='time out value to kill launched regressions seconds')

parser.add_argument('-ndb', '--no_database',
                    action='store_true',
                    help='Do not store results in database')

parser.add_argument('--run_time', '-rt',
                    help='Run time/run if not in profile, default: 30mts')

parser.add_argument('--burst_path', '-bp',
                    help='Specify location of BURST elf')

parser.add_argument('--cmd_path', '-cp',
                    help='Specify a cmd/dat search base folder path',
                    default=False)

parser.add_argument('--message', '-msg',
                    default=False,
                    help='Systest message')

parser.add_argument('--knobs', '-k',
                    default=False,
                    help='Pass command line knobs Format: knob1,knob2,knob3,')

parser.add_argument('--copy_profile', '-cpp',
                    default=False,
                    help='Profile to copy to $PWD')

parser.add_argument('--email', '-em',
                    nargs='?',
                    const=str(getpass.getuser()),
                    default=None,
                    help='This flag will email <input>@xilinx.com when '
                         'the regression finishes. Default: <your username>'
                         '@xilinx.com')

parser.add_argument('--carbon_copy', '-cc',
                    nargs='?',
                    const=str(getpass.getuser()),
                    default=None,
                    help='Pass a comma delimited list of usernames and the '
                         'script will email <username>@xilinx.com when the '
                         'regression finishes.')

parser.add_argument('--summary', '-s',
                    choices=['pretty', 'normal'],
                    default=None,
                    help='Enable regression job summary : formats'
                         '(pretty/normal)')

parser.add_argument('-rf', '--retrig_fail',
                    action='store_true',
                    help='Rerun failed jobs on a different setup')

parser.add_argument('--subset', '-ss',
                    nargs='?',
                    default=None,
                    help='Pass a comma delimited list of run numbers in a profile to run')

parser.add_argument('--python', '-py',
                    action="store_true",
                    help='Pick the bf2.0 python version of the script')

#  Used to disable status prints in regressions, can be used to other special
# cases that need to be taken care while running daily/weekly regression.
parser.add_argument('-ar', '--auto_regres',
                    action='store_true',
                    help='Flag to indicate auto generated regression'
                         '(daily.weekly)')

class Jobs(object):
    """
    Class that conatins a regression job status and results
    """
    def __init__(self, jobid, name):
        self.state = "ISSUED"  # issued, pend, run, complete(now)
        self.jobid = jobid
        self.profile = None
        self.name = name
        self.result = None
        self.req_runtime = 0
        self.run_time = 0
        self.board = None
        self.result_msg = ""
        self.last_test = '-1'
        self.log_base = None
        self.cmd_path = None
        self.knobs = None
        self.binary_path = None
        self.fail_tags = None
        self.failing_setup = None
        self._store2db = True

    def __str__(self):
        string = f"jobid={self.jobid}\n"
        string += f"\tjob_name={self.name}\n"
        string += f"\tprofile={self.profile}\n"
        string += f"\tjob_state={self.state}\n"
        string += f"\tresult={self.result}\n"
        string += f"\trun_time={self.run_time}\n"
        string += f"\treq_runtime={self.req_runtime}\n"
        string += f"\tboard={self.board}\n"
        string += f"\tresult_msg={self.result_msg}\n"
        string += f"\tresult_msg={self.last_test}\n"
        string += f"\tlog_base={self.log_base}\n"
        string += f"\tcmd_path={self.cmd_path}\n"
        string += f"\tknobs={self.knobs}\n"
        string += f"\tbinary_path={self.binary_path}\n"
        string += f"\tfail_tags={self.fail_tags}\n"
        string += f"\tfailing_setup={self.failing_setup}\n"
        return string

    def __repr__(self):
        string = f"jobid={self.jobid},"
        string += f"job_name={self.name},"
        string += f"profile={self.profile},"
        string += f"job_state={self.state},"
        string += f"result={self.result},"
        string += f"run_time={self.run_time},"
        string += f"req_runtime={self.req_runtime},"
        string += f"board={self.board},"
        string += f"result_msg={self.result_msg},"
        string += f"result_msg={self.last_test},"
        string += f"log_base={self.log_base},"
        string += f"cmd_path={self.cmd_path},"
        string += f"knobs={self.knobs},"
        string += f"binary_path={self.binary_path},"
        string += f"fail_tags={self.fail_tags},"
        string += f"failing_setup={self.failing_setup};"    # semicolon
        return string

    def job_dict(self, user, host_machine):
        # Use UTC timestamp to store to database
        self.timestamp = regression_utc_time
        self.author = user
        self.host_machine = host_machine
        if not self._store2db:
            return self.__dict__
        # Remove the private variables
        # Remove extra quotes to avoid JSON format errors in database
        # Replace coma with spaces to avoid regression viewer formatting issues
        jobs = {k:v for (k,v) in self.__dict__.items() if not k.startswith("_")}
        try:
            temp = jobs["result_msg"].replace(",", " ").strip()
            jobs["result_msg"] = temp.replace("\"", "").strip()
        except (KeyError, AttributeError):
            jobs["result_msg"] = "Unable to determine"
        return jobs
 
    def is_log_folder_empty(self):
        folder_items_list = listdir(self.log_base)
        if not len(folder_items_list):
            return True
        elif len(folder_items_list) == 1 and folder_items_list[0] == "recall":
            return True
        else:
            return False


class Regression(object):
    """
    Class that has results of the regression.
    """
    def __init__(self):
        self.job_count = 0
        self.pend_count = 0
        self.run_count = 0
        self.done_count = 0
        self.base_log_path = None
        self.job_list = []
        self.complete = None
        self._remove_folder_list = []

    def add_job(self, job_item):
        self.job_list.append(job_item)
        self.job_count += 1
        if self.base_log_path:
            job_item.log_base = path.join(
                "/", self.base_log_path, job_item.profile, job_item.name)
                
    def add_rerun_job(self, job_item, failed_job_name):
        self.job_list.append(job_item)
        self.job_count += 1
        if self.base_log_path:
            job_item.log_base = "{a}/{b}/{c}/{d}".format(a=self.base_log_path, 
                        b=job_item.profile, c=failed_job_name, d=job_item.name)

    def __repr__(self):
        string = f"==summary==\n"
        string += f"job_count={self.job_count},"
        string += f"pend_count={self.pend_count},"
        string += f"run_count={self.run_count},"
        string += f"done_count={self.done_count},"
        string += f"log_base={self.base_log_path},"
        string += f"Done={self.complete};"   # semicolon to separate sections
        for item in self.job_list:
            string += repr(item)
        string += f"\n====end====\n"
        return string

    def __str__(self):
        string = f"==summary==\n"
        string += f"job_count={self.job_count}\n"
        string += f"pend_count={self.pend_count}\n"
        string += f"run_count={self.run_count}\n"
        string += f"done_count={self.done_count}\n"
        string += f"log_base={self.base_log_path}\n"
        string += f"Done={self.complete}\n"
        for item in self.job_list:
            string += str(item)
        string += f"\n====end====\n"
        return string
        
    def return_info_list(self, info_type='id'):
        info_list = []
        for item in self.job_list:
            if info_type == 'id':
                info_list.append(item.jobid)
            elif info_type == 'name':
                info_list.append(item.name)
        return info_list

    def job_dict_list(self, user, machine):
        job_data = []
        for job in self.job_list:
            job_dict = job.job_dict(user, machine)
            if str(job.jobid) not in self._remove_folder_list and job._store2db:
                job_data.append(job_dict)
        return job_data

    # status_list = [run(1)/complete(0),
    #         [total_count, pend_count, run_count, done_count],
    #         [current status of runs] - list of size total_count]
    def update_status(self, status_list):
        # Possible status: ISSUED, PENDING, RUNNING, COMPLETE NOW, COMPLETED
        status_dict = {  0 : "ISSUED",
                            1 : "PENDING",
                            2 : "RUNNING",
                            3 : "COMPLETED NOW",
                            4 : "COMPLETED" }
        # status list should be of length 3, if not ignore
        if len(status_list) == 3:
            self.complete = not(status_list[0])
            self.pend_count = status_list[1][1]
            self.run_count = status_list[1][2]
            self.done_count = status_list[1][3]
            for i, item in enumerate(self.job_list):
                item.state = status_dict[status_list[2][i]]

    def find_runtime(self, jobid1):
        run_time = '0'
        try:
            data = subprocess.check_output(f"/proj/systest/bin/lsf-wrapper "
                                            f"bhist -l {jobid1}".split())
            for line in reversed(data.decode('utf-8').split('\n')):
                if line != '':
                    run_time = re.findall(r"[0-9]+", line)[2]
                    break
        except (IndexError,subprocess.CalledProcessError):
            pass
        return run_time

    def set_complete(self):
        """Run once when the regression is complete to do some housekeeping"""
        # Update completed now to complete, find runtime
        for job in self.job_list:
            if job.state == "COMPLETED NOW":
                job.state = "COMPLETED"
            job.run_time = self.find_runtime(job.jobid)

    def remove_empty_folders_of_untested_runs(self, is_automated_regression):
        state_list = ["COMPLETE (Pending Timeout)", "ISSUED", "PENDING"]
        if is_automated_regression:
            for job in self.job_list:
                if job.state in state_list and job.is_log_folder_empty():
                    print("Job {} did not run. Removing folder {}".format(job.jobid, job.log_base))
                    self._remove_folder_list.append(job.jobid)
                    system("rm -r " + job.log_base)


# Stores the details of the jobs launched by regression.
results = Regression()


# Function definitions
def run_monitor(total_runs, wait_time, hostenv):
    """
    Function that monitors systest queue and gives run summary
    Input:
        wait_time = job monitor sampling interval
    Output:
        status_list = [
        run(1)/complete(0),
        [total_count, pend_count, run_count, done_count],
        [current status of runs] - list of size total_count
        ]
    current status: 0 : ISSUED
                    1 : PENDING
                    2 : RUNNING
                    3 : COMPLETED NOW
                    4 : COMPLETED
    """
    running = 1
    # Initial condition (never valid condition)
    prev_count_status = [0, 10, -1, 0]
    id_list = results.return_info_list('id')
    old_status = [0] * results.job_count
    print_count = 1
    status_list = []
    while running:
        curr_time = localtime(time())
        time_delta = datetime.datetime.now() - monitor_start_time
        time_diff = time_delta.days * 86400 + time_delta.seconds
        status_list = systest_job_mon(total_runs,
                                      id_list,
                                      old_status,
                                      hostenv)
        results.update_status(status_list)
        if hostenv.time_out:
            status_list = check_timeout_kill(hostenv, status_list, time_diff)
        if status_list == -1:
            sleep(120)  # Wait for two minutes if there is LSF connection error
            continue
        running = status_list[0]
        count_status = status_list[1]
        # Adding prints every two hours to find out script hangs/ failures
        if time_diff / 7200 == print_count:
            print_count = print_count + 1
            print_systest_mon_status(count_status, curr_time)
        # There is some status change, do status prints if required
        if (count_status != prev_count_status) or (running == 0):
            if (not hostenv.monitor_flag) or running == 0:
                print_systest_mon_status(count_status, curr_time)
                print_run_result(status_list[2], hostenv, running)
            old_status = status_list[2]
            prev_count_status = count_status
        sleep(wait_time)


def check_timeout_kill(hostenv, status_list, time_diff):
    """
    Function that checks the jobs and kills them after timeout
    """
    job_status = status_list[2]
    id_list = results.return_info_list('id')
    count_status = status_list[1]
    run_list = []
    pend_list = []
    running = 1
    # Add 4 mins (240 sec)to give time for run regression to launch runs
    if time_diff > hostenv.time_out + 240:
        print("WARN: Regression timed out terminating jobs !!")
        for i, job in enumerate(results.job_list):
            log_base = job.profile
            job_id = job.jobid
            run_name = job.name
            if job_status[i] == 1: # "PENDING"
                print('Terminate pending job: ' + log_base + '/' + run_name)
                subprocess.call(['/proj/systest/bin/systest', '-k',
                                 str(job_id)])
                pend_list.append(job_id)
                job_status[i] = 3
                results.job_list[i].state = "COMPLETE (Pending Timeout)"
                count_status[1] = count_status[1] - 1
                count_status[3] = count_status[3] + 1
            elif job_status[i] == 2: # "RUNNING":
                if hostenv.user != 'burst-test':
                    print('Terminate running job: ' + log_base + '/' + run_name)
                    subprocess.call(['/proj/systest/bin/systest', '-k',
                                     str(job_id)])
                    run_list.append(job_id)
                    job_status[i] = 3
                    results.job_list[i].state = "COMPLETE (Run Timeout)"
                    count_status[2] = count_status[2] - 1
                    count_status[3] = count_status[3] + 1
        # Allow time for systest to kill jobs
        print("Waiting for systest to kill all jobs . .")
        run_flag = 1
        while run_flag:
            line = subprocess.check_output(['/proj/systest/bin/systest', '-q'])
            read_job_ids = re.findall('(([\d]{7,}) )', str(line))
            if len(read_job_ids) == 0:
                run_flag = 0
            else:
                current_job_ids = [x[1] for x in read_job_ids]
                regression_job_ids = list(filter(lambda x: x in id_list,
                                                 current_job_ids))
                if len(regression_job_ids) == 0:
                    run_flag = 0
                sleep(60)
        update_json_with_timeout(hostenv.base_log_dir, results,
                                run_list, pend_list)
        running = 0
    return [running, count_status, job_status]


def print_run_result(status, hostenv, running):
    """
    Function that prints the results of the last completed test
    """
    if not running:
        print("\nParsing the results of Regression . . . \n")
    for i, status_val in enumerate(status):
        result_data = []
        # Job completed just now or entire regression set completed
        if status_val == 3 or (not running):
            log_dir = results.job_list[i].log_base
            parser_cmd = log_dir + ' -ns -nc'
            parser_cmd_list = parser_cmd.split()
            args_in = run_status.parser.parse_args(parser_cmd_list)
            fail_count, result_data = run_status.main(args_in, True)
            try:
                if len(result_data) == 1 and len(result_data[0]) == 1:
                    # P/F , board, last_test(hex), profile , status
                    result_list = result_data[0][0]
                    results.job_list[i].result = result_list[0]
                    results.job_list[i].board = result_list[1]
                    results.job_list[i].last_test = result_list[2]
                    results.job_list[i].result_msg = result_list[4].rstrip("\n")
                    if len(result_data[0][0]) == 6:
                        results.job_list[i].fail_tags = result_list[5].rstrip(".")
                    else:
                        results.job_list[i].fail_tags = ".."
                else:
                    print(f"""WARN: run_status.py {parser_cmd}\n
                           Unexpected result : {result_data}""")
                    # Disable storing unexpected results in database
                    results.job_list[i]._store2db = False
            except (TypeError, IndexError):
                print(f"""WARN: run_status.py {parser_cmd}\n
                            No data found in parser results.""")
                results.job_list[i]._store2db = False


def launch_sanity_check(run_count, hostenv):
    """
    Function that checks if at least few jobs are running
    If the number of launched jobs equals the  number of completed
    tests just after the launch, it implies that the jobs were not
    launched properly
    """
    global monitor_start_time
    id_list = results.return_info_list('id')
    old_status = [0] * results.job_count
    status_list = systest_job_mon(run_count, id_list,
                                  old_status, hostenv, False)
    results.update_status(status_list)
    if status_list == -1:
        if ERROR_MSG_ENABLE:
            print("ERROR: Systest not responding!")
        sys.exit(-1)
    if status_list[1][0] == status_list[1][3]:
        if ERROR_MSG_ENABLE:
            print("WARN:No systest jobs running")
        sys.exit(-1)
    monitor_start_time = datetime.datetime.now()
    print('Monitor start: '+str(monitor_start_time))
    curr_time = localtime(time())
    print_systest_mon_status(status_list[1], curr_time)


def post_launch_analysis(hostenv, run_count):
    """
    Function that does job monitoring and parses the regression results
    """
    global monitor_interval
    global CREATE_CSV
    fail_count = 0
    print('\nStarting Job Monitor . . .')
    sleep(5)
    # Making sure that jobs were properly launched.
    launch_sanity_check(run_count, hostenv)
    # Run the job monitor
    sleep(125)  # To account for 2 minute delay in updating bjobs_all.json file
    monitor_interval = 120
    run_monitor(run_count, monitor_interval, hostenv)
    results.set_complete()
    # Creating summary files
    CREATE_CSV ^= hostenv.rerun_failed
    for profile in hostenv.profile_list:
        out_file = profile.split('/')[-1] + '_' + hostenv.time_string + '.csv'
        log_dir = str(hostenv.base_log_dir) + '/' + out_file.rstrip('.csv')
        
        if CREATE_CSV:
            parser_cmd = "{a} -o {a}/{b} -nd".format(a=log_dir, b=out_file)
        else:
            parser_cmd = log_dir + " -nc"
        parser_cmd_list = parser_cmd.split()
        args_in = run_status.parser.parse_args(parser_cmd_list)
        fail_count = fail_count + run_status.main(args_in, True)[0]
    return fail_count


def list_profile(host_env):
    """
    Function that lists valid regression profile in /profile folder
    """
    profile_list = []
    pwd_list = []
    for filename in listdir(str(host_env.profile_dir)):
        if filename.endswith(".profile") and str(filename)[0] != '#':
            profile_list.append(str(filename).split('.')[0])

    for filename in listdir(str(getcwd())):
        if filename.endswith(".profile") and str(filename)[0] != '#':
            pwd_list.append(str(filename).split('.')[0])

    profile_list = sorted(profile_list)
    if len(profile_list) % 2 == 1:
        profile_list.append('')
    print("\nList of valid profiles in /profile dir:")
    for i in range(0, len(profile_list), 2):
        print('{:40} {:40}'.format(profile_list[i], profile_list[i+1]))
    if len(pwd_list) > 0:
        pwd_list = sorted(pwd_list)
        if(len(pwd_list) % 2) == 1:
            pwd_list.append('')
        print("\nList of valid profiles in /$PWD dir:")
        for i in range(0, len(pwd_list), 2):
            print('{:40} {:40}'.format(pwd_list[i], pwd_list[i+1]))
    print("\nNote: /profile dir has higher priority than /$PWD so if \n"
          "profiles with same name exits in both dir, profile in /profile will"
          " be used")


def build_burst(profile_list):
    """
    Function that Builds BURST
    """
    build_cmd = 'build-all'
    if 'pre-checkin' in profile_list:
        build_cmd = 'build-all all'
    build_status = system(build_cmd)
    print('BUILD_STATUS: ' + str(build_status))
    if build_status != 0:
        print('BURST build failed !')
        sys.exit(-1)
    return 0


def run_burst_update(hostenv):
    """
    Function that update all setup files required
    by run_burst.py
    """
    exec_cmd = hostenv.executable + ' -u all'
    if LAUNCH_ENABLE:
        try:
            subprocess.check_call(exec_cmd, shell=True)
        except subprocess.CalledProcessError:
            exit(-1)
    return 0


def check_user_input(hostenv):
    """
    Function that checks if the user input valid profile(s)
    """
    profile_count = len(hostenv.profile_list)
    invalid_list = []
    profile_path_list = []
    for profile in hostenv.profile_list:
        profile_path = is_exist_profile(hostenv, profile)
        if not profile_path:
            invalid_list.append(profile)
        elif is_cmt_profile(hostenv, profile_path):
            invalid_list.append(profile)
        else:
            profile_path_list.append(profile_path)
    if profile_count == len(invalid_list):
            print("ERROR: No valid profile input !")
            list_profile(hostenv)
            sys.exit(-1)
    elif len(invalid_list):
        for profile in invalid_list:
            print("WARN: Invalid profile: " + str(profile + '.profile'))
    # List of valid profiles abs path without .profile extension
    hostenv.profile_list = [x[:-8] for x in profile_path_list]
    # Make sure that same profile is not repeated more than once.
    hostenv.profile_list = list(set(hostenv.profile_list))
    return 0


def manual_exclude_list(hostenv, cmd_line):
    """ Function that returns the manual maintained list of boards to exclude
    for automated daily regression or normal regression"""
    _exclude_file = str(hostenv.script_dir) + '/manual_board_exclude.json'
    settings_file = Path(str(hostenv.script_dir) + '/settings.json')
    if hostenv.use_exclude or (not Path(_exclude_file).is_file()):
        hostenv.update_manual_excludes()
    exclude_string = ''
    _board_key = ''
    if ('-b ' in cmd_line) or ('--board ' in cmd_line):
        try:
            # Find the board name from the profile line
            _board_key = str(re.search('((-b|--board) *([a-zA-Z0-9-_]*))',
                                       cmd_line).group(3))
        except AttributeError:
            return exclude_string
        if len(_board_key.split('-')) > 1 and \
                str(_board_key.split('-')[-1]).isnumeric():
            # Boards requested by board number: No manual exclusion required
            return exclude_string
    elif ('-rc' in cmd_line) or ('--root_complex' in cmd_line):
        try:
            # Find the rc,ep name from the profile line
            _rc = str(re.search('((-rc|--root_complex) *([a-zA-Z0-9-]*))',
                                cmd_line).group(3))
            _ep = str(re.search('((-ep|--end_point) *([a-zA-Z0-9-]*))',
                                cmd_line).group(3))
            _set_key = "{}_rc_{}_ep".format(_rc, _ep)
        except AttributeError:
            return exclude_string
        try:
            _board_key = pci_cluster_dictionary[_set_key]
        except (ValueError, KeyError):
            print(f"key=pci_cluster_dictionary[{_set_key}] is invalid")
            return exclude_string

    try:
        with open(str(_exclude_file)) as data_file:
            try:
                ex_boards = json.load(data_file)[_board_key]
            except (ValueError, KeyError):
                print(
                    f"ERROR: {_exclude_file}, board={_board_key} is invalid"
                    )
                return exclude_string
    except IOError:
        print('IOError: manual_exclude_list')
        return exclude_string
    exclude_string = ','.join(ex_boards)
    return exclude_string


def parse_run_line(hostenv, cmd_line, line_num):
    """Function that adds extra parameters for a regression run line"""
    if hostenv.burst_path:
        burst_path = hostenv.burst_path
    else:
        burst_path = str(hostenv.precheck_dir)
    exec_cmd = ' --logs_dir ' + \
        str(hostenv.precheck_dir) + \
        ' -m regres --no_build --run_number ' + str(line_num)
    if ('-bp ' not in cmd_line) and ('--build_path ' not in cmd_line):
        exec_cmd = exec_cmd + ' -bp ' + burst_path
    if ('-cp ' not in cmd_line) and ('--cmd_path ' not in cmd_line) \
                            and (hostenv.cmd_path):
        exec_cmd = exec_cmd + ' -cp ' + hostenv.cmd_path
    # min runtime in palladium = 3hrs to get any useful information
    run_time = hostenv.run_time
    if 'palladium' in cmd_line:
        run_time = max(10800, int(hostenv.run_time))
    if ('haps' in cmd_line) and ('-rt' not in cmd_line) and ('--run_time' not in cmd_line):
        exec_cmd = exec_cmd + ' -rt 10800'
    if 'Fail_after_test' not in cmd_line:
        if hostenv.run_time_override:
            exec_cmd = exec_cmd + ' -rt ' + str(run_time)
    if ('-msg ' not in cmd_line) and ('--message ' not in cmd_line) and \
            hostenv.message:
        exec_cmd = exec_cmd + ' -msg "' + str(hostenv.message) + '"'
    elif hostenv.message:
        temp = shlex.split(cmd_line)
        try:
            msg_index = temp.index('-msg') + 1
        except ValueError:
            msg_index = temp.index('--message') + 1
        temp[msg_index] = "\"{} {}\"".format(hostenv.message, temp[msg_index])
        cmd_line = " ".join(temp)
    if ('-k ' not in cmd_line) and ('--knobs ' not in cmd_line) and \
            hostenv.knobs:
        exec_cmd = exec_cmd + ' -k ' + str(hostenv.knobs)
    elif hostenv.knobs:
        try:
            cmd_line = cmd_line.replace(' -k ', ' --knobs ')
            knob = re.search(r"--knobs ([\"'a-zA-Z0-9_=,]+)", cmd_line).group(1)
            knob = knob.strip("\"',")
            knob = knob + ',' + hostenv.knobs.strip("\"',")
            exec_cmd = exec_cmd + ' -k ' + str(knob)
            cmd_line = re.sub(r"--knobs ([\"'a-zA-Z0-9_=,]+)", "", cmd_line)
        except (IndexError, TypeError):
            print('WARN: Unable to add command line knobs! L: ' + str(line_num))
    # Exclude boards from local or global exclude(default) file
    exclude_boards = manual_exclude_list(hostenv, cmd_line)
    if ('-e ' not in cmd_line) and ('--exclude ' not in cmd_line):
        if exclude_boards != '':
            exec_cmd = exec_cmd + ' -e ' + exclude_boards
    elif exclude_boards != '':
        try:
            cmd_line = cmd_line.replace(' -e ', ' --exclude ')
            exclude = re.search(r"--exclude ([\"'a-zA-Z0-9_,-]+)", cmd_line).group(1)
            exclude = exclude.strip("\"',")
            exclude_boards = exclude + ',' + exclude_boards
            exec_cmd = exec_cmd + ' -e ' + str(exclude_boards)
            cmd_line = re.sub(r"--exclude ([\"'a-zA-Z0-9_,-]+)", "", cmd_line)
        except (IndexError, TypeError):
            print('WARN: Unable to add excluded boards! L: ' + str(line_num))
    if LAUNCH_ENABLE:
        print('Manually Excluded : ' + exclude_boards)
    if hostenv.board_tag:
        exec_cmd = exec_cmd + ' -bt ' + str(hostenv.board_tag)
    if ('-py' not in cmd_line) and ('--python' not in cmd_line) \
                            and (hostenv.python):
        exec_cmd = exec_cmd + ' -py '
    return cmd_line + exec_cmd

def run_profile_jobs(hostenv, profile):
    """
    Function that launches the jobs described in different profiles
    """
    # Error flag to try to recover from first error
    run_count = 0
    fail_count = 0
    launch_count = 0
    line = 0
    file_path = str(profile) + '.profile'
    print("PROFILE: " + str(file_path))
    with open(str(file_path), 'r') as profile_file:
        profile_file.seek(0)
        for cmd_line in profile_file:
            line += 1
            if hostenv.subset:
                if line not in hostenv.subset:
                    continue
            if cmd_line.strip() != '':
                if cmd_line.lstrip(' ')[0][0] != '#':
                    exec_cmd = parse_run_line(hostenv, cmd_line, line)
                    if not LAUNCH_ENABLE:
                        exec_cmd += " -dl"
                    args = shlex.split(exec_cmd)
                    if LAUNCH_ENABLE:
                        print("{:12} : {}".format("Run number", line))
                    try:
                        args_in = run_burst.parser.parse_args(args)
                        out_list = run_burst.main(args_in)
                        if out_list:
                            launch_count = len(out_list)
                            for item in out_list:
                                job_id = item[0]
                                run_name = item[1]
                                j1 = Jobs(job_id, run_name)
                                j1.profile = hostenv.profile_log_name
                                j1.cmd_path = item[2]
                                j1.req_runtime = item[3]
                                j1.knobs = item[4]
                                j1.binary_path = item[5]
                                results.add_job(j1)
                        else:
                            if LAUNCH_ENABLE:
                                print(f"SystestError in line {line} : {cmd_line}")
                            fail_count += 1
                            launch_count -= 1
                        run_count += launch_count
                    except subprocess.CalledProcessError:
                        print(f"CalledProcessError in line {line} : {cmd_line}")
                        fail_count += 1
                else:
                    print(f"Commented Run in line {line} : {cmd_line}")
    return run_count, fail_count


def read_profile(profile_name, hostenv):
    """
    Function that reads a profile and prints it
    """
    if not(is_exist_profile(hostenv, str(profile_name))):
        print("ERROR: Invalid profile, try --list option")
        sys.exit(-1)
    else:
        _file_path = str(hostenv.profile_dir) + '/' + \
            str(profile_name) + '.profile'
        if not Path(_file_path).is_file():
            _file_path = str(getcwd()) + '/' + \
                         str(profile_name) + '.profile'
        pfile_lines = 0
        print("Profile: " + str(profile_name))
        try:
            with open(str(_file_path), 'r') as pfile:
                for line in pfile:
                    pfile_lines += 1
                    if line == '\n':
                        continue
                    elif line[0][0] == '#':
                        print(str(line).rstrip('\n'))
                    else:  # valid run that will get executed
                        print('{}] {} {} -nb'.format(str(pfile_lines),
                                                     hostenv.executable,
                                                     str(line).rstrip('\n')))

        except IOError:
            print("WARN: Error opening " + _file_path)
            sys.exit(-1)


def force_read_profile(profile_name, hostenv):
    """
    Function that reads a profile and prints the run burst command and creates
    the log base folder, copies the elfs to it. Useful for launching selects
    runs in a profile.
    """
    if not(is_exist_profile(hostenv, profile_name)):
        print("ERROR: Invalid profile, try --list option")
        sys.exit(-1)
    else:
        _file_path = str(hostenv.profile_dir) + '/' + \
            str(profile_name) + '.profile'
        if not Path(_file_path).is_file():
            _file_path = str(getcwd()) + '/' + \
                         str(profile_name) + '.profile'
        pfile_lines = 0
        print("Profile: " + str(profile_name))
        try:
            with open(str(_file_path), 'r') as pfile:
                for line in pfile:
                    if line != '\n' and line[0][0] != '#':
                        cmd = parse_run_line(hostenv, line.rstrip('\n'),
                                             pfile_lines)
                        print('{}] {}'.format(str(pfile_lines + 1), str(cmd)))
                        pfile_lines += 1
        except IOError:
            print("WARN: Error opening " + _file_path)
            sys.exit(-1)
        # Creating the regression log dir and copying elfs to it.
        _cmd = ('mkdir  --parents ' + str(hostenv.precheck_dir)).split()
        try:
            subprocess.check_output(_cmd)
        except subprocess.CalledProcessError:
            print('WARN: Unable to make log dir/ copy elfs')
            return
        _cmd = ('cp ' + str(hostenv.current_dir) + '/burst86 ' +
                str(hostenv.precheck_dir)).split()
        try:
            subprocess.check_output(_cmd)
        except subprocess.CalledProcessError:
            print('WARN: Unable to copy burst86 elf, '
                  'to regression folder')
            return
        _cmd = 'find . -maxdepth 1 -name burst*.elf'.split()
        try:
            _elfs = str(subprocess.check_output(
                _cmd, cwd=str(hostenv.current_dir)))
        except subprocess.CalledProcessError:
            print('WARN: Unable to find burst*.elf in $PWD')
            return
        elf_list = re.findall('[a-z,0-9]+.elf', _elfs)
        for item in elf_list:
            _cmd = ('cp ' + str(hostenv.current_dir) +
                    '/' + str(item) + ' ' +
                    str(hostenv.precheck_dir)).split()
            try:
                subprocess.check_output(_cmd)
            except subprocess.CalledProcessError:
                print('WARN: Unable to copy burst*.elf elfs '
                      'to regression folder')
                return
        print('\n' + '-' * 120)
        print("Log dir: " + str(hostenv.precheck_dir))
        print('-' * 120 + '\n')


# Copy a profile to $PWD with _pwd profile extension
def copy_profile2pwd(hostenv):
    for item in hostenv.profile_list:
        cmd = 'cp ' + item + '.profile ' +\
              str(getcwd()) + '/' + item.split('/')[-1] + '_pwd.profile'
        system(cmd)
        print("copied: {}_pwd.profile to $PWD".format(item))
    return 0


class EnvironmentSetup(object):
    """
    Class the defines the environment setup conditions
    required to launch regression.
    """
    def __init__(self, args):
        self.current_dir = getcwd()
        self.shell = str(getenv('SHELL').split(sep)[2])
        self.user = getpass.getuser()
        self.host_location = get_host_location()
        self.host_machine = str(gethostname())
        # Do not modify the value of time string after this assignment.
        self.time_string = str(strftime("%Y%m%d_%H%M%S", localtime(time())))
        self.burst_folder = getenv('XSLV')
        if not self.burst_folder:
            self.burst_folder = Path(source_setup_warning())
            sys.exit(-1)
        else:
            self.burst_folder = Path(self.burst_folder)
        self.burst_folder = str(self.burst_folder.resolve())
        self.profile_list = self.strip_profile_name(args.profile)
        self.executable = 'run_burst.py'
        self.parser_name = 'run_status.py'
        self.busg_path = Path(self.burst_folder + "/burst-scripts/script_gen")
        self.precheck_dir = None
        self.base_log_dir = None
        self.profile_log_name = 'regression'
        if args.read:
            self.profile_log_name = args.read + '_' + str(self.time_string)
        if args.force_read:
            self.profile_log_name = args.force_read+'_m_'+str(self.time_string)
        if args.logs_dir:
            self.base_log_dir = Path(args.logs_dir)
            if not self.base_log_dir.is_dir():
                print("ERROR: Log path directory does not exist!\n")
                print("Log path: " + str(args.logs_dir))
                sys.exit(-1)
        else:
            self.base_log_dir = Path(str(self.current_dir) + '/logs/')
        results.base_log_path = str(self.base_log_dir)
        self.profile_dir = Path(self.burst_folder +
                                "/burst-scripts/run_burst/profile")
        self.parser_file = Path(self.burst_folder +
                                "/burst-scripts/run_burst/" + self.parser_name)
        self.script_dir = Path(self.burst_folder +
                               "/burst-scripts/run_burst")
        self.version_file = Path(str(self.script_dir) +
                                 '/cping_version_local.txt')
        self.xsj_cron_dir = Path("/home/xppc/burst/cping_cron/")
        self.xhd_cron_dir = Path("/home/xppc/burst/crons/cping_xhd/")
        if get_host_location() == 'XSJ':
            self.exclude_auto = '/home/xppc/burst/latest_burst/manual_exclude.json'
        elif get_host_location() == 'XHD':
            self.exclude_auto = '/group/siv_burst/proj/latest_burst/manual_xhd_board_exclude.json'
        self.time_out = args.time_out
        self.no_database = args.no_database
        self.error_count = 0
        self.monitor_flag = args.auto_regres
        self.run_time = '1800'
        self.run_time_override = False
        if args.run_time:
            self.run_time = args.run_time
            self.run_time_override = True
        self.burst_path = None
        if args.burst_path:
            if Path(args.burst_path).is_dir():
                self.burst_path = str(Path(args.burst_path).resolve())
            else:
                print("ERROR: Invalid burst elf folder")
                sys.exit(-1)
        self.cmd_path = None
        if args.cmd_path:
            if Path(args.cmd_path).is_dir():
                self.cmd_path = str(Path(args.cmd_path).resolve())
            else:
                print("ERROR: Invalid cmd/dat serach base folder")
                sys.exit(-1)
        self.use_exclude = self.toggle_exculde_setting(args.toggle_exclude)
        self.message = args.message
        self.knobs = args.knobs
        self.board_tag = args.board_tag
        self.python= args.python
        if args.auto_regres:
            self.rerun_failed = 0
        else:
            self.rerun_failed = args.retrig_fail
        self.subset = None
        if args.subset:
            _subset = args.subset.strip(',').split(',')
            try:
                self.subset = list(map(int, _subset))
            except:
                print(f"WARN: Invalid --subset/-ss option {args.subset}, should be integers")

    def create_log_dir(self):
        """
        Function that creates the log directory to save logs and recall files
        """
        if not self.profile_dir.is_dir():
            system('mkdir ' + str(self.profile_dir))
        log_dir = Path(str(self.precheck_dir))
        if not (log_dir.is_dir()):
            system('mkdir --parents ' + str(log_dir))
        if not self.burst_path:
            cp_cmd = 'cp ' + self.current_dir + '/' + '*.elf ' + str(
                self.precheck_dir)
            system(cp_cmd)
            cp_cmd = 'cp -rf ' + self.current_dir + '/obj ' + str(
                self.precheck_dir)
            system(cp_cmd)
            cp_cmd = 'cp ' + self.current_dir + '/' + 'burst86 ' + str(
                self.precheck_dir)
            system(cp_cmd)

    def set_preckin_dir(self, profile_index=0):
        """
        Function that sets the base log folder of a profile in a
         single/multi-profile run
        """
        if self.profile_list and (len(self.profile_list) > profile_index):
            self.profile_log_name = \
                    self.profile_list[profile_index].split('/')[-1] + '_' + \
                                                        str(self.time_string)
        if self.base_log_dir:
            self.precheck_dir = Path(str(self.base_log_dir) + '/' +
                                     self.profile_log_name)
        else:
            print("ERROR: Log path directory does not exist!\n")
            print("Log path: " + str(self.base_log_dir))
            sys.exit(-1)

    def strip_profile_name(self, profile_list):
        profile_list_strip = []
        for item in profile_list:
            if str(item).endswith('.profile'):
                profile_list_strip.append(item[:-8])
            else:
                profile_list_strip.append(item)
        return profile_list_strip

    def update_manual_excludes(self):
        """
        Function that updates the manual board exclude file located in /run_bust
        folder with automated regression exclude file
        :return:
        """
        _exclude_file_local = str(self.script_dir) + \
            '/manual_board_exclude.json'
        if Path(self.exclude_auto).is_file():
            cp_cmd = 'cp -f ' + str(self.exclude_auto) + ' ' + \
                     str(_exclude_file_local)
            system(cp_cmd)
        else:
            print("WARN: Missing" + str(self.exclude_auto))

    def toggle_exculde_setting(self, toggle_exclude):
        settings_file = str(self.script_dir) + '/settings.json'
        settings_data = read_json(settings_file)
        if settings_data:
            try:
                use_exlcude = settings_data['auto_board_exculde']
                if toggle_exclude:
                    settings_data['auto_board_exculde'] = not use_exlcude
                    write_json(settings_file, settings_data, True)
                    use_exlcude = not use_exlcude
            except (ValueError, KeyError):
                use_exlcude = True
                print(
                    "WARN: Check settings.json for auto_board_exculde setting!")
        else:
            use_exlcude = None
        return use_exlcude


def kill_on_usr_interrupt():
    """
        Function that kills all the runs launched by the regression when Ctrl+C
    """
    if results.job_count:
        id_list = results.return_info_list('id')
        for item in id_list:
            print("Killing Job: " + str(item))
            system('/proj/systest/bin/systest -k ' + str(item))


def email_results(total_run_count, fail_count, to_emails, cc_emails, hostenv):
    """
        Function that emails the results to all specified recipients
    """
    if to_emails is None:
        to_emails = cc_emails
        cc_emails = []
    if cc_emails is None:
        cc_emails = []
    if to_emails is None:
        print("WARN: Email_results was called with no recipients.")
        return

    subject = "Regression{} Complete: {}_{}".format(
                "" if len(hostenv.profile_list) == 1 else "s",
                hostenv.profile_list[0] if len(hostenv.profile_list) == 1 else \
                "multi-profile", str(hostenv.time_string + '.profile'))

    curr_hour = int(strftime("%H", localtime(time())))
    msg_text = "Good "
    msg_text += ("Morning,\r\n\r\n" if curr_hour < 12 else
                 ("Afternoon,\r\n\r\n" if curr_hour < 18 else
                 ("Evening,\r\n\r\n")))

    msg_text += "I'd like to inform you that {}'s {}.\r\n".format(
                    str(getpass.getuser()), 
                    "regression has completed" if len(hostenv.profile_list) == 1\
                    else "regressions have completed")
    msg_text += ("You have {} run{} that completed "
                 "with {} failure{}.\r\n").format(
                    total_run_count, "" if total_run_count == 1 else "s", 
                    fail_count, "" if fail_count == 1 else "s")
    msg_text += ("I have listed the status of each profile, BURST elf used and "
                 "the respective log{} for you below:\r\n").format(
                    "" if total_run_count == 1 else "s")

    if (('-bp' in sys.argv) or ('--burst_path' in sys.argv)):
        msg_text += ("BURST_elf_path: {} \r\n").format(hostenv.burst_path)
    else:
        msg_text += ("BURST_elf_path: {} \r\n").format(hostenv.current_dir)

    # Check for the failing jobs in each profile and add their paths
    for profile in hostenv.profile_list:
        msg_text += "\r\n"
        log_dir = "{}/{}_{}".format(str(hostenv.base_log_dir),
                                    str(profile.split('/')[-1]),
                                    str(hostenv.time_string))

        parser_cmd = "{} {} -nc -nd".format(hostenv.parser_file, log_dir)
        p = subprocess.Popen([str(parser_cmd)], 
                             shell=True, 
                             stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE)
        prof_stat_data, prof_stat_err = p.communicate()

        parser_cmd = "{} {} -nc -ns".format(hostenv.parser_file, log_dir)
        p = subprocess.Popen([str(parser_cmd)], 
                             shell=True, 
                             stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE)
        prof_meta_data, prof_meta_err = p.communicate()
        prof_title = "{}_{}".format(profile.split('/')[-1], hostenv.time_string)
        # Retrieve only number of failures [2], passes [3], terminated [4], 
        #   total run [5], total launched [6], and not sure [7]
        prof_stat = str(prof_stat_data.decode("utf-8")).split("\n")
        if len(prof_stat) >= 8:
            prof_stat = prof_stat[1:8]
        # Remove trailing newline for meta data
        prof_meta =  str(prof_meta_data.decode("utf-8")).split("\n")
        if len(prof_meta_data):
            prof_meta = prof_meta[:-1]

        msg_text += "Status for {}:".format(prof_title)
        msg_text += "\r\n\t{}\r\n".format("\r\n\t".join(prof_stat))
        msg_text += "Corresponding log{} for {}:\r\n".format(
                     "" if len(prof_meta) == 1 else "s", prof_title)
        if not len(prof_meta) and len(prof_meta_err.decode("utf-8")):
            msg_text += "\tError: {}".format(prof_meta_err.decode("utf-8"))
        for subjob in prof_meta:
            sj_info = subjob.split(", ") # PASS/FAIL, board, log dir, message
            if 'only tested with python' in subjob:
                continue
            if len(sj_info) < 3:
                msg_text += "\r\n- - - - - STATUS ERROR - - - - -\r\n"
                msg_text += "There was an issue formatting the output of "
                msg_text += "run_status.py\r\n\r\n"
                msg_text += "Command:\r\n{}\r\n\r\n".format(parser_cmd)
                msg_text += "Output:\r\n{}\r\n\r\n".format(subjob)
                msg_text += "continuing to the next job in this profile...\r\n"
                msg_text += "- - - - - - - - - - - - - - - - - - -\r\n\r\n"
                continue
            sj_log_dir = "{}/{}/{}".format(hostenv.base_log_dir, prof_title, 
                                           sj_info[2])
            parser_cmd = "{} {} -nc -nd".format(hostenv.parser_file, sj_log_dir)
            msg_text += "\t({} on {}) {}\r\n".format(sj_info[0], 
                                                     sj_info[1], 
                                                     sj_log_dir)
    msg_text += "\r\nCheers,\r\nThe BURST Team\r\n"

    print("Sending email To: "
          + ", ".join(["{}@xilinx.com".format(x) for x in to_emails])
          + " CC: " + ", ".join(["{}@xilinx.com".format(x) for x in cc_emails]))

    # Create a text/plain message
    msg = MIMEText(msg_text)
    msg["Subject"] = subject
    msg["From"] = "burst-test@xilinx.com"
    msg["CC"] = ", ".join(["{}@xilinx.com".format(x) for x in cc_emails])
    msg["To"] = ", ".join(["{}@xilinx.com".format(x) for x in to_emails])

    # Send the message via SMTP server.
    try:
        with smtplib.SMTP("localhost") as s:
            try:
                s.send_message(msg)
            except smtplib.SMTPRecipientsRefused:
                print("WARN: Could not send email. Recipients refused.")
            except smtplib.SMTPHeloError:
                print("WARN: Could not send email. Server did not respond.")
            except smtplib.SMTPSenderRefused:
                print(("WARN: Could not send email. Server did not accept "
                      + "{} as a sender.").format(msg["From"]))
            except smtplib.SMTPDataError:
                print("WARN: Could not send email. " 
                    + "Server responded with unexpected error.")
            except smtplib.SMTPNotSupportedError:
                print("WARN: Could not send email. " 
                    + "SMTPUTF8 was given mail_options that are not supported.")
    except smtplib.SMTPConnectError:
        print("WARN: Could not conect to email server. No emails sent.")


def find_failing_runs_in_profile(hostenv, profile):
    """Find failing jobs for rerunning"""
    failing_list = []
    for job in results.job_list:
        if job.result == 'FAIL' and profile in job.profile:
            job.failing_setup = job.board
            failing_list.append(job)
    return failing_list


def relaunch_failing_runs(hostenv, failing_list):
    """Reluanches failed runs on another board"""
    relaunch_job_count = 0
    fail_count = 0
    print("\nGoing to re-launch {} failing runs on different setups".format(len(failing_list)))
    for job in failing_list:
        rcl_path = '{a}/{b}/{c}/recall/{c}.json'.format(a=hostenv.base_log_dir,
                                                        b=job.profile, # Profile
                                                        c=job.name) # Name
        rcl_cmd = "-r {} -e {}".format(rcl_path, job.failing_setup)
        if LAUNCH_ENABLE:
            try:
                rcl_cmd_list = rcl_cmd.split()
                rcl_args = run_burst.parser.parse_args(rcl_cmd_list)
                args_in = run_burst.check_recall(rcl_args)
                out_list = run_burst.main(run_burst.parser.parse_args(args_in))
                if out_list:
                    launch_count = len(out_list)
                    for item in out_list:
                        job_id = item[0]
                        run_name = item[1]
                        j1 = Jobs(job_id, run_name)
                        j1.profile = hostenv.profile_log_name
                        j1.cmd_path = item[2]
                        j1.req_runtime = item[3]
                        j1.knobs = item[4]
                        j1.binary_path = item[5]
                        results.add_rerun_job(j1, job.name)
                else:
                    if LAUNCH_ENABLE:
                        print("Error launching: " + str(rcl_cmd))
                        fail_count += 1
                relaunch_job_count += launch_count
            except subprocess.CalledProcessError:
                print("CalledProcessError: " + str(rcl_cmd))
                fail_count += 1
            except UnboundLocalError:
                print("Rerun of job {} cancelled!".format(str(job.jobid)))
    print("Relaunched {} failing runs on different "
            "setups".format(str(relaunch_job_count)))
    return relaunch_job_count, fail_count


def main(args):
    global LAUNCH_ENABLE
    hostenv = EnvironmentSetup(args)
    total_run_count = 0
    fail_count = 0
    if args.list:
        list_profile(hostenv)
        exit(0)
    if args.read:
        hostenv.set_preckin_dir(0)
        read_profile(args.read, hostenv)
        exit(0)
    if args.force_read:
        hostenv.set_preckin_dir(0)
        force_read_profile(args.force_read, hostenv)
        exit(0)
    if args.copy_profile:
        hostenv.profile_list = args.copy_profile.strip().split(',')
        check_user_input(hostenv)
        copy_profile2pwd(hostenv)
        exit(0)
    if args.update_exclude:
        print("Update $XSLV/burst-scripts/run_burst/manual_board_exclude.json")
        hostenv.update_manual_excludes()
        exit(0)
    if args.dont_launch:
        print("Regression will not launch any jobs")
        LAUNCH_ENABLE = 0
        args.no_monitor = True
    if len(hostenv.profile_list) == 0:
        print("ERROR: No profile selected.")
        list_profile(hostenv)
        exit(-1)
    # Checking if the user input profile is valid.
    check_user_input(hostenv)
    # Building BURST
    if not args.no_build and not hostenv.burst_path:
        build_burst(hostenv.profile_list)
    # Updating setup files
    if not args.no_update:
        run_burst_update(hostenv)
    # Issuing jobs in all the user requested profiles
    profile_count = 0
    for profile in hostenv.profile_list:
        # Creating log folders
        if not args.dont_launch:
            hostenv.set_preckin_dir(profile_count)
            hostenv.create_log_dir()
        run_count, f = run_profile_jobs(hostenv, profile)
        print("Launched {} job(s) in profile {}".format(str(run_count),
                                                        str(profile)))
        fail_count = fail_count + f
        total_run_count = total_run_count + run_count
        profile_count = profile_count + 1

    print("End of Launching jobs {} job(s)".format(str(total_run_count)))
    # Launching the job monitoring
    if (not args.no_monitor) and (total_run_count != 0):
        # Printing the launched Job names and Job IDs
        print('\n{:10} : {:40} : {} '.format('JOB ID', 'BASE DIR', 'JOB NAME'))
        for job in results.job_list:
            print('{:10} : {:40} : {}'.format(job.jobid , job.profile,
                                                job.name))
        # Monitor the status of jobs running on boardfarm
        # Doubt - Go through this post_launch analysis
        fail_count = fail_count + post_launch_analysis(hostenv, total_run_count)

        # Retrigger failed runs if required.
        if hostenv.rerun_failed:
            failing_job_list = []
            for profile in hostenv.profile_list:
                profile_name = profile.split('/')[-1]
                temp_list = find_failing_runs_in_profile(hostenv, profile_name)
                if temp_list:
                    failing_job_list += temp_list
                else:
                    print("Regression retrigger cancelled for profile: {} \nNo runs failed.".format(profile))
            if len(failing_job_list):
                run_count_st2, fail_count = relaunch_failing_runs(hostenv, failing_job_list)
                if run_count_st2:
                    total_run_count += run_count_st2
                    fail_count = fail_count + post_launch_analysis(hostenv, run_count_st2)
                else:
                    for profile in hostenv.profile_list:
                        out_file = profile.split('/')[-1] + '_' + hostenv.time_string + '.csv'
                        log_dir = str(hostenv.base_log_dir) + '/' + out_file.rstrip('.csv')
                        parser_cmd = "{a} -o {a}/{b} -nd".format(a=log_dir, b=out_file)
                        parser_cmd_list = parser_cmd.split()
                        args_in = run_status.parser.parse_args(parser_cmd_list)
                        fail_count = fail_count + run_status.main(args_in, True)[0]
            else:
                for profile in hostenv.profile_list:
                    out_file = profile.split('/')[-1] + '_' + hostenv.time_string + '.csv'
                    log_dir = str(hostenv.base_log_dir) + '/' + out_file.rstrip('.csv')
                    parser_cmd = "{a} -o {a}/{b} -nd -ns".format(a=log_dir, b=out_file)
                    parser_cmd_list = parser_cmd.split()
                    args_in = run_status.parser.parse_args(parser_cmd_list)
                    fail_count = fail_count + run_status.main(args_in, True)[0]

        # Removes empty folders from untested runs for automated daily regressions
        results.remove_empty_folders_of_untested_runs(hostenv.monitor_flag)

        # Create a list of email IDs and sent email notification.
        cc_emails = args.carbon_copy.split(',') if args.carbon_copy else []
        to_emails = [args.email] if args.email else []
        if to_emails or cc_emails:
            email_results(total_run_count, fail_count, to_emails, 
                            cc_emails, hostenv)

        # Upload regresssion job results to database
        job_data = results.job_dict_list(hostenv.user, hostenv.host_machine)
        if not hostenv.no_database:
            with myMongoDB() as database:
                database.upload_data(job_data)
        else:
            print("Not uploading results to database")

        # Print the regression summary status
        if args.summary:
            if args.summary == 'pretty':
                print(str(results))
            elif args.summary == 'normal':
                print(repr(results))
        if fail_count:
            print("Regression status: FAIL")
        else:
            print("Regression status: PASS")
    return fail_count, results


if __name__ == "__main__":
    try:
        status, result = main(parser.parse_args())
        if status:
            exit(-1)
    except KeyboardInterrupt:
        print("Keyboard Interrupt detected: Terminating regression!")
        kill_on_usr_interrupt()
        exit(0)
