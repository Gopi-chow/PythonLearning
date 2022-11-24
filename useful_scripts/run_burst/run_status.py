#!/usr/bin/env python3

from json.decoder import JSONDecodeError
import sys

if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    print("This script requires a python version of at least 3.6 Exiting.")
    exit(-1)
if sys.version_info[1] != 8 or sys.version_info[2] != 3:
    print("WARN: This script is only tested with python version 3.8.3")

import os.path
import re
import fnmatch
from datetime import datetime
import csv
import json
import argparse
from time import perf_counter
from collections import defaultdict

"""
This script is used to determine the status of a BURST regression runs.

Pass in the folder of the regression you want to look at. This
script looks for debug files and the associated com/serial logs to get the
info it needs.

The output of the script is a csv table of the current results of the runs.
The csv file is dir_name.csv and will be in the folder you launch the script
from. An abbreviated table is also printed to the console output for quick
viewing.

Exit code is the number of failed tests + tests that were never launched.
If no valid logs exist in folder, exit code is -1. Return 0 if all tests pass.

Flags:
-h      Show help
-nc (--no_csv)      Prevents saving output .csv file
-ns (--no_summary)  Removes summary from console output
-nd (--no_details)  Removes details of individual runs from console output
-o                  Save csv output to file after -o argument
-lk                 Search for given keyword in .log file name.
-s  (--strict)      When enabled a test groups fails if a single run in a test 
                    group fails

Example usage:
run_status.py burst/logs                    Saves output to burst/logs.csv
run_status.py burst/logs -nc                No saved .csv file
run_status.py burst/logs -o log_trace.csv   Saves to log_trace.csv

NOTE:
If the file structure or file name structure of regression
is changed, then it is likely this script will be broken. Please update this
script with any updates to the file structure/naming in BUSG scripts.

-1 run_time means that the log time format is not standard and the time could
not be determined from the debug log.
"""
parser = argparse.ArgumentParser(
    description="View status of BURST regression using command line flags",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    epilog="Queries Contact: burst_script_team@xilinx.com",
)
parser.add_argument(
    "search_path",
    action="store",
    help="Target directory to look for burst logs created with run_regression.py",
)
parser.add_argument(
    "-o",
    action="store",
    help="Name of output csv file. This option will not"
    " add .csv extension automatically",
)
parser.add_argument(
    "-ns",
    "--no_summary",
    action="store_true",
    help="Removes summary from console output",
)
parser.add_argument(
    "-nd",
    "--no_details",
    action="store_true",
    help="Removes details of individual runs from console output",
)
parser.add_argument(
    "-nc", "--no_csv", action="store_true", help="Prevents saving output .csv file"
)
parser.add_argument(
    "-lk",
    action="store",
    help="Specify keyword in a .log filename."
)
parser.add_argument(
    "-s",
    "--strict",
    action="store_true",
    help="strict checking for test groups, when enabled a test \
                    groups fails if a single run in a test group fails",
)
parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    help="print more results indicating any issues while\
                    results are parsed",
)
run_status_verbose = False


def check_log_form(path):
    if re.search(r"(burst_debug_.*\.log)$", path):
        return True
    else:
        return False


def line_filter(key_phrase, regex, line, val=""):
    if not val:
        if re.search(key_phrase, line):
            try:
                val = re.findall(regex, line)[0]
            except IndexError:
                val = key_phrase + " Err"
    return val


def pcie_dna_filter(val1, val2, switch, key_phrase, regex, line):
    if switch and not val2:
        val2 = line_filter(key_phrase, regex, line)
    elif not switch and not val1:
        val1 = line_filter(key_phrase, regex, line)
    return val1, val2


def scan_debug(log):
    """Read through Debug then the serial log to determine status and Pass/Fail.
    Returns a list of the relevant info"""
    log = re.sub("\n", "", log)
    status = "Loading files to board"
    status_override = ""
    pass_fail = "FAIL"
    board_num = ""
    run_time_req = ""
    last_test_override = ""
    run_time_override = ""
    ep_rc = 0  # 0 for end point or default, 1 for root complex
    dna1 = ""
    dna2 = ""
    wafer1 = ""
    wafer2 = ""
    wafer_x1 = ""
    wafer_x2 = ""
    wafer_y1 = ""
    wafer_y2 = ""
    lot1 = ""
    lot2 = ""
    vnc_time = ""
    profile = ""
    seed = ""
    start_time_systest = ""
    run_time = ""
    last_test = ""
    dec_last_test = ""
    warn_tag = ""  # WarnFail, NoWarnFail
    fail_point_tag = ""  # PreInitFail, InitFail, TestFail
    fail_type_tag = ""  # SetupFail, NonSetupFail, LikelySetupFail

    if not os.path.isfile(log):
        status = "Still in queue"
        row = ["", board_num, "", "", "", "", "", run_time_req, status, log]
        return row

    log_f = open(log, "r", encoding="ascii", errors="surrogateescape")
    # check to see if it started
    for line in log_f:
        if "EP DNA" in line:
            ep_rc = 0
        if "RC DNA" in line:
            ep_rc = 1
        # These filters look for keywords and values in the debug logs
        # lookahead regex (?<=:) requires fixed width between parenthesis
        # (?<=:\s+) is not allowed
        board_num = line_filter(
            r"(BOARD|Board)\s+", r"(?<=:)[\w_\-]+", line, val=board_num
        )
        dna1, dna2 = pcie_dna_filter(
            dna1, dna2, ep_rc, r"dna:", r"(?<=:\s)[\da-f]+", line
        )
        wafer1, wafer2 = pcie_dna_filter(
            wafer1, wafer2, ep_rc, r"Wafer:", r"(?<=:\s)\d+", line
        )
        wafer_x1, wafer_x2 = pcie_dna_filter(
            wafer_x1, wafer_x2, ep_rc, r"Wafer_X:", r"(?<=:\s)\d+", line
        )
        wafer_y1, wafer_y2 = pcie_dna_filter(
            wafer_y1, wafer_y2, ep_rc, r"Wafer_Y:", r"(?<=:\s)\d+", line
        )
        lot1, lot2 = pcie_dna_filter(
            lot1, lot2, ep_rc, r"Lot:", r"(?<=:\s)[\dA-Z]+", line
        )
        run_time_req = line_filter(r"BURST runtime", r"(?<=:)\d+", line, val=run_time_req)
        run_time_override = line_filter(
            r"run time is", r"(?<=time is )\d+", line, val=run_time_override
        )
        if run_time_override and (pass_fail == "PASS"):
            break

        if "BURST started." in line:
            status = "Running if not complete, FAIL if job is done. Check logs"

        # check if test passed
        elif ("BURST run of" in line) and ("complete!" in line):
            status_override = re.sub("\n", "", line)
            run_time_override = re.findall(r"\d+", line)[0]
            pass_fail = "PASS"
            break

        elif line.startswith("BURST run is preempted"):
            status_override = re.sub("\n", "", line)
            run_time_override = re.findall(r"\d+", line)[0]
            pass_fail = "PASS"
            break

        elif "JOB PREEMPTED" in line:
            status_override = "BURST run is preempted before starting"
            pass_fail = "PASS"
            break

        # check if test failed
        if "FAILURE:" in line:
            status = re.sub("FAILURE:|\n", "", line)
            check_over = re.findall(r"[\da-f]{8}", status)
            if check_over:
                last_test_override = check_over[0]

            # handle failure during burst init
            if "test: ffffffff" in status or (
                "test: 00000000" in status and "Run: -1" in status
            ):
                fail_point_tag = "InitFail"
                last_test_override = check_over[0]
                run_time_override = 0
                status = re.sub("BURST failed", "Fail during init", status)
            pass_fail = "FAIL"
            break

    log_f.close()
    com_log = find_com_log(log)
    if com_log:
        serial_result = parse_serial_log(com_log, pass_fail, warn_tag, fail_point_tag)
        if serial_result[0] != "Unknown":
            pass_fail = serial_result[0]
            status = serial_result[1]
        (
            _,
            _,
            warn_tag,
            start_time_systest,
            seed,
            run_time,
            last_test,
            fail_point_tag,
        ) = serial_result
        if last_test_override:
            last_test = make_hex(last_test_override)
        if run_time_override:
            run_time = run_time_override
        if status_override:
            status = status_override
        try:
            dec_last_test = str(int(last_test, 16))
        except ValueError:
            if run_status_verbose:
                print("Invalid Last test, see {}".format(com_log.name))
            dec_last_test = ""
        split_path = log.split(os.sep)
        vnc_time = convert_time(split_path[-2])
        profile = split_path[-4]

    timeout = check_for_timeout(log)
    if timeout == "run-timeout":
        pass_fail = "PASS"
        status = "regression run-timeout"
    elif timeout == "pend-timeout":
        pass_fail = "TERMINATED"
        status = "regression pend-timeout"

    if pass_fail == "FAIL":
        if not warn_tag:
            warn_tag = "NoWarnFail"
        if not fail_point_tag:
            fail_point_tag = "PreInitFail"
            fail_type_tag = "LikelySetupFail"
        if not fail_type_tag and fail_point_tag == "TestFail":
            fail_type_tag = "NonSetupFail"
    dna1 = make_hex(dna1)
    dna2 = make_hex(dna2)
    row = [
        vnc_time,
        profile,
        pass_fail,
        status,
        board_num,
        run_time,
        run_time_req,
        dec_last_test,
        last_test,
        seed,
        log,
        start_time_systest,
        warn_tag,
        fail_point_tag,
        fail_type_tag,
        dna1,
        wafer1,
        wafer_x1,
        wafer_y1,
        lot1,
        dna2,
        wafer2,
        wafer_x2,
        wafer_y2,
        lot2,
    ]
    return row


def make_hex(num_str):
    """Add 0x so that excel doesn't autoformat and truncate numbers"""
    return f"0x{num_str}" if num_str and isinstance(num_str, str) else num_str


def convert_time(time_str):
    """Converts VNC server time from path to systest time format in log"""
    try:
        dt = datetime.strptime(time_str, "%Y%m%d_%H%M")
        time_str = dt.strftime("%b %d, %Y %H:%M:00")
    except ValueError:
        time_str = ""
    return time_str


def find_com_log(debug_path):
    """returns com log associated with debug log"""
    key = "burst_debug_"  # form is .../burst_debug_protium-44-0.log
    subs = ["burst_serial_", "burst_com0", "burst_log_"]
    last_position = debug_path.rfind(key)
    found = False
    log_f = None

    for sub in subs:
        try:
            com_log = (
                debug_path[:last_position]
                + sub
                + debug_path[(last_position + len(key)) :]
            )
            log_f = open(com_log, "r", encoding="ascii", errors="surrogateescape")
            found = True
            break
        except FileNotFoundError:
            log_f = None

    if not found:
        if run_status_verbose:
            print("Cant find com/serial log associated with {}".format(debug_path))
        log_f = None

    return log_f


def parse_serial_log(com_log, pass_fail, warn_tag, fail_point_tag):
    """Get parse the serial log to get test information"""
    first_test, last_test, failure_line, fat_num = [""] * 4
    start_time, first_seed, run_time, last_test_num = [""] * 4
    pass_fail_serial, status = ["Unknown", "status"]
    for line in com_log:
        if re.match("Test [0-9a-f]{8} seed [0-9a-f]{8}", line):
            if not first_test:
                first_test = line
            last_test = line
        if pass_fail_serial != "FAIL":
            if "WARN at" in line:
                pass_fail_serial = "FAIL"
                warn_tag = "WarnFail"
                fail_point_tag = "InitFail"
            else:  # Saves the line before a WARN line
                status = line.replace("\n", "")
        if line.startswith("Set Fail_after_test ="):
            fat_num = make_hex(line[-9:-1])
        # Gopi - Doubt
        elif line.startswith("Failing after test:"):
            last_test_num = make_hex(line[-9:-1])
            pass_fail_serial = "PASS"
        elif line.startswith("Ctrl-c pressed"):
            pass_fail_serial = "PASS"
        elif "Failing at test: " in line:
            failure_line = line
            break
    com_log.seek(0)

    # Get the last test number from failing line or the last test print line
    if failure_line:
        last_test_num = make_hex(
            re.findall("Failing at test: [0-9a-f]+", failure_line)[0][-8:]
        )
        # last_seed = make_hex(re.findall("seed [0-9a-f]{8}", failure_line)[0][-8:])
    elif last_test and (not last_test_num):
        last_test_num = make_hex(re.findall("Test [0-9a-f]+", last_test)[0][-8:])
        # last_seed = make_hex(re.findall("seed [0-9a-f]{8}", last_test)[0][-8:])
    if first_test and last_test:
        first_test_num = make_hex(re.findall("Test [0-9a-f]+", first_test)[0][-8:])
        first_seed = make_hex(re.findall("seed [0-9a-f]{8}", first_test)[0][-8:])
        try:
            start_time = first_test[-22:].strip("\n")
            dt_first = datetime.strptime(first_test[-22:], "%b %d, %Y %H:%M:%S\n")
            dt_last = datetime.strptime(last_test[-22:], "%b %d, %Y %H:%M:%S\n")
            seconds = (dt_last - dt_first).seconds
            days = (dt_last - dt_first).days * 86400
            run_time = days + seconds
        except ValueError:
            # Non-standard burst time formatting used
            start_time = "Unknown"
            run_time = -1
        if int(last_test_num, 16) > int(first_test_num, 16) and (
            pass_fail_serial == "FAIL" or pass_fail == "FAIL"
        ):
            fail_point_tag = "TestFail"
    # No first and last test line then failure is init failure
    elif pass_fail_serial == "FAIL":
        fail_point_tag = "InitFail"
    # Check if run passed because it hit the Fail_after_test
    if fat_num and (fat_num == last_test_num):
        pass_fail_serial = "PASS"
        status = f"Fail_after_test={last_test_num} hit!"
    return [
        pass_fail_serial,
        status,
        warn_tag,
        start_time,
        first_seed,
        run_time,
        last_test_num,
        fail_point_tag,
    ]


def check_for_timeout(log_path, abs=False):
    # abs=True bypasses run_regression structure
    if abs:
        rcl_path = log_path
    else:
        # recall file is 3 levels back from debug log then down one level
        rcl_path, _ = os.path.split(log_path)
        rcl_path = rcl_path.split(os.sep)[:-2]
        tail = ["recall", rcl_path[-1] + ".json"]
        rcl_path = os.sep.join(rcl_path)
        tail = os.sep.join(tail)
        rcl_path = os.path.join(rcl_path, tail)
    timeout = ""
    try:
        with open(rcl_path, "r") as data_file:
            try:
                json_dict = json.load(data_file)
            except JSONDecodeError:
                print(f"JSONDecodeError in {rcl_path}")
                return timeout
            try:  # added to deal with old recall files
                timeout = json_dict["TestEnv"]["timeout"]
            except KeyError:
                return timeout
    except IOError:
        if run_status_verbose:
            print(f"WARN: Error opening {rcl_path}")
    return timeout


def check_test_group(test_group, data, PF_str):
    """Checks P/F status of a test group and each test run in the group"""
    pf_inst = 0
    t_inst = 0
    group_PF = 0

    for test in data[test_group]:
        if PF_str in test[0]:
            pf_inst += 1
        elif "TERMINATED" in test[0]:
            t_inst += 1
    run_PF = pf_inst

    if PF_str == "PASS" and pf_inst == 0 and t_inst == 0:
        group_PF = 1
    elif PF_str == "FAIL" and (pf_inst != 0 or t_inst != 0):
        group_PF = 1

    return group_PF, run_PF


def check_test_runs(total_runs, PF_str, data):
    """Check test groups P/F and termination status"""
    run_PF = 0
    group_PF = 0

    for grp in data:
        temp1, temp2 = check_test_group(grp, data, PF_str)
        group_PF += temp1
        run_PF += temp2

    if PF_str == "PASS":
        run_PF = total_runs - run_PF

    return group_PF, run_PF


def return_to_run_regression(mode):
    """Handles method of return/exit depending how run_status.py is called"""
    if not (mode == "regres" or mode == True):
        exit(-1)
    else:
        return False


def test_folder_index_finder(file_list, direction):
    """Finds index of test# folder (e.g. 003_) when the file path is listed.
    Helps give proper log folder path to read from when searching keywords.
    Function helps prevent redundancies from occuring when tests were rerun and
    results are nested in the original run's folder.
    Direction:
    0 - Look for first instance of a test # folder from left to right.
    1 - Look for first instance of a test # folder from right to left.

    Example:
    Path: logs/ps2dev/041_..._20190830_1535/041_..._20190903_1101/protium...
    Direction = 0, returns 2
    Direction = 1, returns -1"""
    if direction == 0:
        file_list = file_list[0].split(os.sep)

    folder_index = 0
    i = direction
    while folder_index == 0 and i < len(file_list):
        if direction == 0:
            if bool(re.match("[0-9]{3}[_]+", file_list[i])):
                folder_index = i
        else:
            if bool(re.match("[0-9]{3}[_]+", file_list[-i])):
                folder_index = -i + 1
        i += 1
    return folder_index


def write_csv(match_dict, csv_list, status_list, argvs):
    """save the results summary to csv file

    Args:
        match_dict (dict): match dictionary
        csv_list ([type]): rows of results
        status_list ([type]): list of result counts
    """
    if argvs.o:
        record = open(argvs.o, "w", encoding="ascii")
    elif argvs.search_path[-1] == "/":
        record = open(argvs.search_path[:-1] + ".csv", "w", encoding="ascii")
    else:
        record = open(argvs.search_path + ".csv", "w", encoding="ascii")
    print("status record at : {}".format(record.name))
    csvwriter = csv.writer(record, lineterminator="\n")
    first_line = ["Base dir:", os.path.abspath(argvs.search_path)]
    header = [
        "Start Time",
        "Profile",
        "Pass/Fail",
        "Status",
        "Board Number",
        "Run Time",
        "Run Time Requested",
        "Last Test(dec)",
        "Last Test(hex)",
        "Starting Seed",
        "Log Path",
        "Systest Time",
        "Warn tag",
        "Fail point tag",
        "Fail type",
        "dna1(default/ep)",
        "Wafer1",
        "Wafer_x1",
        "Wafer_y1",
        "Lot1",
        "dna2(rc)",
        "Wafer2",
        "Wafer_x2",
        "Wafer_y2",
        "Lot2",
    ]

    csvwriter.writerow(first_line)
    csvwriter.writerow(header)
    for data in csv_list:
        csvwriter.writerow(data)

    for test_group in match_dict:
        for test in match_dict[test_group]:
            if test[0] == "TERMINATED":
                try:
                    csvwriter.writerow(
                        [convert_time(test[3][-13:]), test[3], test[0], test[4]]
                    )
                except IndexError:
                    csvwriter.writerow(
                        [
                            "",
                            test,
                            "?",
                            "Doesnt follow " "BURST regression naming format",
                        ]
                    )

    csvwriter.writerow("")
    csvwriter.writerow(["Group Failures:", status_list[0]])
    csvwriter.writerow(["Group Passes:", status_list[1]])
    csvwriter.writerow(["Total Test Groups:", status_list[2]])
    csvwriter.writerow(["Total Failures:", status_list[3]])
    csvwriter.writerow(["Total Passes:", status_list[4]])
    csvwriter.writerow(["Total Terminated:", status_list[5]])
    csvwriter.writerow(["Total Tests Run:", status_list[6]])
    csvwriter.writerow(["Total Tests Launched:", status_list[7]])

    # overall pass fail is decided by group fail count
    if status_list[0]:
        csvwriter.writerow(["FAIL"])
    else:
        csvwriter.writerow(["PASS"])
    csvwriter.writerow(["--strict:", argvs.strict])


def main(argvs, regression_flag):
    """The main function that collects the results of the regression"""
    global run_status_verbose
    run_status_verbose = argvs.verbose
    # check user inputs
    start = perf_counter()
    search_path = ""
    try:
        search_path = argvs.search_path
        directories = [search_path]
    except IndexError:
        print("Error: Needs a target directory")
        return_to_run_regression(regression_flag)
    if argvs.o and argvs.no_csv:
        print("Error: Cannot use both -o and -nc(--no_csv) flags")
        return_to_run_regression(regression_flag)

    # Initialize variables
    matches = []
    rcl_list = []
    run_list = []
    json_dict = {}
    csv_list = []
    fail_count = 0
    tested_count = 0
    total_count = 0

    # check if a search_path is a debug log
    if os.path.isfile(search_path) or check_log_form(search_path):
        matches = [search_path]
    elif not os.path.isdir(search_path):
        print("{} isn't a directory or valid debug log".format(search_path))
        print("{} isn't a directory or valid debug log".format(search_path))
        return_to_run_regression(regression_flag)
    # recursively find all debug log files in search_path
    else:
        if argvs.lk:
            directories.pop()
            for root, _, filenames in os.walk(search_path):
                for filename in fnmatch.filter(filenames, "*.log"):
                    if argvs.lk in filename:
                        temp_list = root.split(os.sep)
                        test_index = test_folder_index_finder(temp_list, 1)
                        directory = os.sep.join(temp_list[:test_index])
                        if not directory in directories:
                            directories.append(directory)
            if run_status_verbose:
                print(
                    "Number of paths containing .log files w/keyword "
                    "[{}]: {}".format(argvs.lk, len(directories))
                )
            try:
                test_index = test_folder_index_finder(directories, 0)
            except IndexError:
                print("No .log files w/ keyword: " + argvs.lk)
        i = 0
        while i < len(directories):
            for root, _, filenames in os.walk(directories[i]):
                for json_f in fnmatch.filter(filenames, "*.json"):
                    if json_f != "recall.json":
                        total_count += 1
                        recall_name = root.split(os.sep)[-2]
                        rcl_list.append(recall_name)
                        json_dict[recall_name] = os.path.join(root, json_f)

                for filename in fnmatch.filter(filenames, "burst*.log"):
                    matches.append(os.path.join(root, filename))
                    run_list.append(root.split(os.sep)[-3])
            i += 1
            if argvs.lk and i < len(directories):
                while (
                    directories[i].split(os.sep)[test_index]
                    == directories[i - 1].split(os.sep)[test_index]
                ):
                    i += 1
                    if i == len(directories):
                        break

    # scan the debug and serial (if available) logs to find the test results
    match_dict = {}
    setup_dict = defaultdict(lambda: {"total": 0, "setup_issue": 0, "faulty": False})
    for match in matches:
        if check_log_form(match):  # get debug log files
            tested_count += 1
            csv_row = scan_debug(match)
            csv_list.append(csv_row)
            board = csv_row[4].strip()
            fail_type_tag = csv_row[14]
            setup_dict[board]["total"] += 1
            if fail_type_tag == "LikelySetupFail":
                setup_dict[board]["setup_issue"] += 1

    # If majority of runs in a setup failed the mark the setup as faulty
    for setup in setup_dict.keys():
        if setup_dict[setup]["total"] > 1:
            setup_issue_count = setup_dict[setup]["setup_issue"]
            setup_run_total_count = setup_dict[setup]["total"]
            if setup_issue_count > setup_run_total_count / 2:
                setup_dict[setup]["faulty"] = True

    for index, csv_row in enumerate(csv_list):
        board = csv_row[4].strip()
        warn_tag = csv_row[12]
        fail_point_tag = csv_row[13]
        fail_type_tag = csv_row[14]
        if setup_dict[board]["faulty"] and fail_type_tag == "LikelySetupFail":
            csv_list[index][14] = "SetupFail"
            fail_type_tag = "SetupFail"
        tag = f"{warn_tag}.{fail_point_tag}.{fail_type_tag}"
        # P/F , board, last_test(hex), profile , status, tag
        match_list = [csv_row[2], board, csv_row[8], csv_row[1], csv_row[3], tag]
        if csv_row[1][:3] in match_dict:
            match_dict[csv_row[1][:3]].append(match_list)
        else:
            match_dict[csv_row[1][:3]] = [match_list]

    # Find tests that were not launched in boardfarm, ie not tested runs
    # No debug/serial log with a recall log present indicates a test not launched
    not_tested_count = 0
    for item in sorted(set(rcl_list) - set(run_list)):
        not_tested_count += 1
        if item[:3] in match_dict:
            match_dict[item[:3]].append(item)
        else:
            match_dict[item[:3]] = [item]

    if not_tested_count:
        # Check if the runs were killed after timeout period or before
        for key in match_dict:
            for rcl in match_dict[key]:
                if isinstance(rcl, str):
                    timeout = check_for_timeout(json_dict[rcl], abs=True)
                    ind = match_dict[key].index(rcl)
                    if timeout == "pend-timeout":
                        terminate_reason = "regression pend-timeout"
                    else:
                        terminate_reason = "manually killed or bad run"
                    match_dict[key][ind] = [
                        "TERMINATED",
                        "None",
                        "None",
                        rcl,
                        terminate_reason,
                        "..",
                    ]

    # prints the individual run results
    if not argvs.no_details:
        for grp in match_dict:
            for run in range(len(match_dict[grp])):
                status_line = "{}, {}, {}, {}".format(
                    match_dict[grp][run][0],
                    match_dict[grp][run][1],
                    match_dict[grp][run][3],
                    match_dict[grp][run][4],
                )
                if match_dict[grp][run][0] == "FAIL":
                    status_line += f" ({match_dict[grp][run][5]})"
                if run > 0:
                    status_line = "    {}".format(status_line)
                print(status_line)

    # calculate the summary of test counts
    pass_fail = "FAIL" if argvs.strict else "PASS"
    group_fail, fail_count = check_test_runs(tested_count, pass_fail, match_dict)
    test_groups = len(match_dict)
    group_pass = test_groups - group_fail
    pass_count = max(total_count, tested_count) - not_tested_count - fail_count
    exit_code = group_fail
    status_count_list = [
        group_fail,
        group_pass,
        test_groups,
        fail_count,
        pass_count,
        not_tested_count,
        tested_count,
        total_count,
    ]

    # Print the summary of results
    if not argvs.no_summary:
        print("\nGroup Failures: {}".format(group_fail))
        print("Group Passes: {}".format(group_pass))
        print("Total Test Groups: {}".format(test_groups))
        print("\nTotal Failures: {}".format(fail_count))
        print("Total Passes: {}".format(pass_count))
        print("Total Terminated: {}".format(not_tested_count))
        print("Total Tests Run: {}".format(tested_count))
        print("Total Tests Launched: {}".format(total_count))
        faulty_setups, faulty_setup_detail = [""] * 2
        for item in setup_dict.keys():
            setup_issue_count = setup_dict[item]["setup_issue"]
            setup_run_total_count = setup_dict[item]["total"]
            is_setup_faulty = setup_dict[item]["faulty"]
            if is_setup_faulty:
                faulty_setups += f"{item}, "
                faulty_setup_detail += f"\n{item}: {setup_issue_count}/{setup_run_total_count} runs failed with setup like failures"
        faulty_setups = faulty_setups.rstrip(", ")
        if faulty_setups:
            print(f"\nFaulty setups: {faulty_setups}{faulty_setup_detail}")
        if exit_code:
            print("\nFAIL")
        else:
            print("\nPASS")

    # save csv file to name of dir.csv
    if not argvs.no_csv:
        write_csv(match_dict, csv_list, status_count_list, argvs)

    # Create result object to be returned to run_regression.py
    if argvs.strict:
        match_list = list(match_dict.values())
    else:  # return only the result of the latest run in a test_group
        match_list = list([x[-1]] for x in match_dict.values())
    if run_status_verbose:
        print(f"run_status took {perf_counter()-start} sec")
    return exit_code, match_list


if __name__ == "__main__":
    try:
        argvs = parser.parse_args()
        regression_flag = False
        fail_count, matches = main(argvs, regression_flag)
        exit(fail_count)
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        exit(0)
