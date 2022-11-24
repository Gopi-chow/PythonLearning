#!/usr/bin/env python3

import sys
import os
import argparse
from datetime import timedelta
from datetime import datetime
from collections import defaultdict
from socket import gethostname
from xcom.email import send_email
import getpass
import xlsxwriter
from database import myMongoDB
from update import read_json, write_json
from xcom.helper import get_user_cred, get_cluster_name
from xcom.jira import BoardfarmCR, JiraQuery
import logging
import glob
import re

# Globals
message_txt = ""
user = getpass.getuser()


# Setup logging to print to console
log = logging.getLogger()
logFormatter = logging.Formatter(
    "%(asctime)s:  %(message)s", datefmt="%m:%d:%Y %I:%M %p"
)

parser = argparse.ArgumentParser(
    description="Check BURST regression related setup issues",
    epilog="Queries Contact: burst_script_team@xilinx.com",
)
valid_days = list(range(1, 11))
parser.add_argument(
    "--days",
    "-d",
    nargs=1,
    type=int,
    default=[1],
    choices=valid_days,
    help="Accepts number of days of regression results to parse",
)

parser.add_argument(
    "-to",
    nargs=1,
    type=str,
    help="Accepts user name to send email, no need to specify @xilinx.com",
)

parser.add_argument(
    "-cc",
    nargs=1,
    type=str,
    help="Accepts user name to cc email, no need to specify @xilinx.com; must be used with -to option",
)

parser.add_argument(
    "--strict",
    "-s",
    action="store_true",
    help="Consider maybe setup fails as setup fails when this flag is used",
)

parser.add_argument(
    "--cr_disable",
    "-cd",
    action="store_true",
    help="CR filing feature is disbaled when this flag is passed",
)

parser.add_argument(
    "-user",
    type=str,
    default="burst-test",
    help="Accepts user whose regression results need to be checked can be all OR a specific user name",
)

parser.add_argument(
    "--test_mode",
    action="store_true",
    help="Use JIRA UAT test enviroment instead of production instance",
)


def find_results(filter_user="burst-test", window=1, board=None):
    """Get regression results from past regression

    Args:
        filter_user(str, optional): user name OR all
        window (int, optional): Number of days to check. Defaults to 1.
        board (str, optional): Board-number to filter runs.

    Returns:
        [mongodb cursor]: cursor to read the results from database.
    """
    day_range = datetime.utcnow() - timedelta(days=window)
    proj = {"_id": 0, "board": 1, "log_base": 1, "fail_tags": 1}
    if filter_user == "all":
        filt = {
            "jobid": {"$exists": True},
            "timestamp": {"$gt": day_range},
        }
    else:
        filt = {
            "jobid": {"$exists": True},
            "timestamp": {"$gt": day_range},
            "author": filter_user,
        }
    if board:
        filt["board"] = board
        proj["jobid"] = 1
        proj["cmd_path"] = 1
        proj["binary_path"] = 1
        proj["result_msg"] = 1
        proj["result"] = 1
        proj["knobs"] = 1
    result_list = []
    with myMongoDB() as db:
        if not db.check_collection():
            exit(0)
        results = db.print_filtered_data(filt, proj, False)
        for item in results:
            result_list.append(item)
    return result_list


def alias_file_path(file_path, board="", force_site=False):
    """get the xsj alias path for an xhd file

    Args:
        file_path (str): linux path string
        board (str): board name indicating where the log file is present
        force_site (str, optional): force the file path to a given site (xsj/xhd)

    Returns:
        [str]: returns path accessible from XSJ
    """

    host_location = str(gethostname())[0:3].upper()
    tmp = file_path.split("/")

    board_loc = ""
    if board:
        if "xhd" in board or "bf" in board:
            board_loc = "xhd"
        else:
            board_loc = "xsj"
    # Looking for a XHD path from XSJ
    if host_location == "XSJ":
        if board_loc == "xhd" or force_site == "xsj":
            tmp[2] = f"{tmp[2]}_xhd"
    # Looking for a XSJ path from XHD
    elif host_location == "XHD":
        if board_loc == "xsj" or force_site == "xhd":
            if tmp[2] != "xppc":  # /home/xppc is not mirrored
                tmp[2] = f"{tmp[2]}_xsj"
    return "/".join(tmp)


def print1(value, force=False):
    """print value and append it to global string message_txt

    Args:
        value ([str]): value to print
        force (boolean): Set true to print irrespective of user
    """
    global message_txt
    if user != "burst-test" or force:
        print(value)
    message_txt += f"{value}\n"


def faulty_setup2exclude(
    exclude_file, exclude_data, exclude_boards, site, strict, email_en
):
    """Add faulty setup to exclude list

    Args:
        exclude_file (str): JSON file path to exclude JSON file
        exclude_data (dict): data from the exclude JSON file
        exclude_boards(list): List of faulty boards in site
        site (str): XSJ/ XHD
        strict (boolean): Indicate is fault cheching is strict (1 failure => faulty setup)
        email_en (boolean): email enable

    """
    if user == "burst-test" and (not strict) and host_location == site:
        for board in sorted(exclude_boards):
            cluster = get_cluster_name(board)
            try:
                excluded_boards = exclude_data[cluster]
                excluded_boards.append(board)
                exclude_data[cluster] = sorted(set(excluded_boards))
            except KeyError:
                print1(f"WARN: Unable to map {board} to a cluster in {exclude_file}")
        write_json(exclude_file, exclude_data)
        print1(f"Added {exclude_boards} to {exclude_file}")
        exclude_boards = None
        email_en = 1
    if exclude_boards:
        print1(f"{exclude_boards} is missing from {site} exclude file, Please add it")
    return email_en, exclude_boards


def create_result_summary(faulty_setup_list, window, timestamp, user):
    faulty_fails = defaultdict(lambda: [])
    for board_name in faulty_setup_list:
        results = find_results(filter_user=user, window=window, board=board_name)
        for run in results:
            if run["board"] is None:
                continue
            else:
                board = run["board"].strip()
                faulty_fails[board].append(run)
        file_name = f"{board_name}_{timestamp}.xlsx"
        workbook = xlsxwriter.Workbook(file_name)
        worksheet = workbook.add_worksheet()
        for row, entry in enumerate(faulty_fails[board_name]):
            col = 0
            for value in entry.values():
                worksheet.write(row + 1, col, value)
                col += 1
        col = 0
        for key in faulty_fails[board_name][0].keys():
            worksheet.write(0, col, key)
            col += 1
        workbook.close()
    return faulty_fails


def create_cr_dict(run_dict, cr_settings_dict, timestamp, fail_count, run_count):
    setup = run_dict["board"]
    attachment = f"{setup}_{timestamp}.xlsx"
    summary = f""
    if run_dict["result_msg"]:  # Avoid None, NA, Nil etc..
        if len(run_dict["result_msg"]) > 5:
            summary += f"{run_dict['result_msg']} "
        else:
            summary += "fails to run BURST "
    else:
        summary += "fails to run BURST "
    if fail_count and run_count:
        summary += f"{fail_count}/{run_count} times "
        description = f"BURST fails with setup like failures {fail_count}/{run_count} times in regression runs.\n"
    else:
        description = f"BURST fails with setup like failures in regression runs.\n"
    summary += f"({timestamp})"
    description += (
        f" All regression results from {setup} in attached file {attachment}\n\n"
    )
    description += f"Sample run details\n"
    description += f" log : {run_dict['log_base']}\n"
    description += f" binary: {run_dict['binary_path']}\n"
    description += f" cmd_path: {run_dict['cmd_path']}\n"
    description += f" knobs: {run_dict['knobs']}\n"
    steps2reproduce = f"Run burst with provided sample details on {setup}\n"
    knobs = run_dict["knobs"].replace(",", ";")
    cmd_path = run_dict["cmd_path"].replace("_preempt.cmd", ".cmd")
    steps2reproduce += f"/proj/systest/bin/systest -b {board} {cmd_path} n {run_dict['binary_path']} 1800 {knobs} CR-testing"
    cluster = get_cluster_name(board)
    try:
        cluster_details = cr_settings_dict[cluster]
    except KeyError:
        cluster_details = {
            "device_family": "NA",
            "verifier": "burst-test",
            "epic": "EB-423",
        }

    issue_dict = {
        "board": board,
        "project": "CR",
        "device_family": cluster_details["device_family"],
        "epic_link": cluster_details["epic"],
        "attachment": attachment,
        "summary": summary,
        "description": description,
        "steps2reproduce": steps2reproduce,
        "verifier": cluster_details["verifier"],
        "assignee": cluster_details["verifier"],
        "labels": ["burst_found_setup", "burst-bot-created"],
    }
    return issue_dict


def get_log_info(log_base):
    log_data = f""
    if not os.path.isdir(log_base):
        return log_data
    serial_log = glob.glob(log_base + "/**/*burst_serial*.log", recursive=True)
    debug_log = glob.glob(log_base + "/**/*burst_debug*.log", recursive=True)
    if len(debug_log) != 1:
        return log_data
    debug_log_file = debug_log[0]
    log_data += f"\n{'='*20}\ndebug_log: {debug_log_file}\n{'='*20}\n"
    # Get last 5 lines of debug log
    with open(debug_log_file, "r") as dbg_file:
        lines = dbg_file.readlines()
        lines = [x for x in lines if x != "\n"]
        if len(lines) >= 10:
            for line in lines[-10:]:
                if line.strip():
                    log_data += line
        else:
            for line in lines:
                if line.strip():
                    log_data += line
    if len(serial_log) != 1:
        return log_data
    serial_log_file = serial_log[0]
    log_data += f"{'='*20}\nserial_log: {serial_log_file}\n{'='*20}\n"
    start, req_start, end, req_end, line_num = [0, 0, 0, 0, 0]
    burst_status = ""
    with open(serial_log_file, "r") as srl_file:
        lines = srl_file.readlines()
        for line_num, line in enumerate(lines):
            if line.startswith("BURST is starting:"):
                log_data += line
            if line.startswith("WARN"):
                start = line_num - 2
            if line.startswith("Failing at test:"):
                end = line_num + 2
        # get lines from warn to fail for a log with WARN
        if start and end and (end > start):
            req_start = start
            req_end = end
        # get 25 lines before fail for a log without WARN
        elif end > 25:
            req_start = end - 25
            req_end = end
        for line in lines[req_start:req_end]:
            if line.strip():
                log_data += line
        if not line_num:
            log_data += "Serial log is empty!\n"
        if not burst_status:
            log_data += "BURST code execution did not start!\n"
    log_data += f"{'='*20}\n"
    return log_data


if __name__ == "__main__":
    args = parser.parse_args()
    email_en = 0
    print1(f"Checking {args.days[0]} days regression results...")
    results = find_results(args.user, args.days[0])
    total_entries = len(results)
    print1(f"Found {total_entries} runs in database")
    print1("=" * 80)
    if not total_entries:
        sys.exit(0)
    failing_boards = set()
    fail_counts = defaultdict(lambda: 0)
    run_counts = defaultdict(lambda: 0)
    fail_logs = {}
    for run in results:
        board = run["board"].strip()
        if "LikelySetupFail" in run["fail_tags"]:  # setup fail
            failing_boards.add(board)
            fail_counts[board] += 1
            fail_logs[board] = run["log_base"]
        run_counts[board] += 1

    # Print the faulty setups
    faulty_setup_list = []
    for board in sorted(failing_boards):
        fail_board_count = fail_counts[board]
        run_board_count = run_counts[board]
        status = "Faulty setup"
        # More than 90% runs on the board failed and there were at least 4 setup fails
        if fail_board_count >= (run_board_count * 0.9) and run_board_count > 3:
            faulty_setup_list.append(board)
        elif args.strict:
            faulty_setup_list.append(board)
        else:
            log_path = alias_file_path(fail_logs[board], board)
            status = f"Maybe faulty\nsample log: {log_path}"
        print1(
            f"{board:25} : {fail_board_count:3}/{run_board_count:3} setup fails - {status}"
        )
    print1("=" * 80)
    print1(f"\nFaulty setups: {faulty_setup_list}\n")
    print1("=" * 80)
    if not faulty_setup_list:
        sys.exit(0)

    if user == "burst-test" and args.test_mode:
        print1("burst-test user is not allowed to continue in test mode", True)
        sys.exit(0)

    host_location = str(gethostname())[0:3].upper()
    site_log_file = ""
    if host_location == "XSJ":
        site_log_file = "/home/xppc/burst/latest_burst/cr_log.txt"
    elif host_location == "XHD":
        site_log_file = "/group/siv_burst/proj/latest_burst/cr_log.txt"
    if os.path.isfile(site_log_file):
        file_handler = logging.FileHandler(filename=site_log_file)
        file_handler.setFormatter(logFormatter)
        log.addHandler(file_handler)
        log.setLevel(logging.CRITICAL)

    # Check if faulty setups are added to exclude files
    exclude_xsj = "/home/xppc/burst/latest_burst/manual_exclude.json"
    exclude_xsj_mod = (
        exclude_xsj
        if host_location == "XSJ"
        else "/group/siv_burst/proj/common/manual_exclude.json"
    )
    exclude_xhd = "/group/siv_burst/proj/latest_burst/manual_xhd_board_exclude.json"
    exclude_xhd_mod = (
        exclude_xhd
        if host_location == "XHD"
        else "/group/siv_burst_xhd/proj/latest_burst/manual_xhd_board_exclude.json"
    )
    excludes_xsj = read_json(exclude_xsj_mod)
    excludes_xhd = read_json(exclude_xhd_mod)
    not_excluded_xsj = []
    not_excluded_xhd = []
    if excludes_xsj and excludes_xhd and faulty_setup_list:
        for board_name in faulty_setup_list:
            cluster = get_cluster_name(board_name)
            cluster_exclude = []
            board_site = ""
            if cluster:
                try:
                    if "xhd" in board_name or "bf" in board_name:
                        cluster_exclude = excludes_xhd[cluster]
                        board_site = "xhd"
                    else:  # xsj board
                        cluster_exclude = excludes_xsj[cluster]
                        board_site = "xsj"
                except KeyError:  # Unknown cluster names will be ignored
                    print1(f"WARN: Unable to map {board_name} to a cluster")
                    continue
                if board_name not in cluster_exclude:
                    if board_site == "xsj":
                        not_excluded_xsj.append(board_name)
                    elif board_site == "xhd":
                        not_excluded_xhd.append(board_name)

    # If run with burst-test add faulty setups to exclude file if possible
    if not_excluded_xsj:
        email_en, not_excluded_xsj = faulty_setup2exclude(
            exclude_xsj, excludes_xsj, not_excluded_xsj, "XSJ", args.strict, email_en
        )
    if not_excluded_xhd:
        email_en, not_excluded_xhd = faulty_setup2exclude(
            exclude_xhd, excludes_xhd, not_excluded_xhd, "XHD", args.strict, email_en
        )
    if (not_excluded_xsj or not_excluded_xhd) and user != "burst-test":
        print1("Use burst-test role account to add these setups to exclude file")
        print1("\n" + "=" * 80)
        email_en = 1

    # create summary of results for faulty setups in excel files
    xls_timestamp = f"{datetime.now().strftime('%m-%d-%Y')}"
    faulty_setup_runs = create_result_summary(
        faulty_setup_list, args.days[0], xls_timestamp, args.user
    )

    # Get auth details for JIRA and LDAP
    cred_file = os.path.join(os.path.dirname(__file__), "../jira/credentials.json")
    oauth_file = os.path.join(os.path.dirname(__file__), "../jira/key_cert.pem")
    cred_dict = get_user_cred(user, cred_file, oauth_file)
    oauth = cred_dict["oauth_dict"]
    passwd = cred_dict["password"]
    if not passwd and not oauth:
        passwd = getpass.getpass(f"Xilinx LDAP password of {user}:")

    if not oauth and not passwd:
        log.error(f"Invalid credentials")
        sys.exit(0)

    jira_url = "http://jira.xilinx.com/"
    if args.test_mode:
        jira_url = "http://jirauat.xilinx.com:8280/"

    # Get required results
    jq = JiraQuery(user=user, password=passwd, oauth=oauth, jira_url=jira_url)
    if not jq.jira:
        print("Unable to connect to JIRA, check credentials")
        sys.exit(0)

    print1("CR status:")
    jql = "project = 'Change Request' and (Application = 'Board Farm' OR Application = 'XHD Board Farm') AND status != Closed"
    jq.max_result_count = 200
    jq.run_query(query=jql)

    cr_settings_dict = read_json(
        os.path.join(os.path.dirname(__file__), "cr_settings.json")
    )
    exclude_cr_dict_xsj = {}
    exclude_cr_dict_xhd = {}
    new_faulty_setup_runs = {}
    # Check if the faulty board already has an open CR, if summary field of an open
    # boardarm CR has the board name then it is considered as existing issue.
    for board, value in faulty_setup_runs.items():
        cr_exist = 0
        for cr in jq.results.values():
            # Remove charcters that dont match a board name and search for board name match
            summary_str = re.sub(r"[^A-Za-z0-9- _]", "", cr.summary)
            if board in summary_str.split():
                print1(f"{cr.key} is open for {board}, not filing new CR! : {cr.summary}", True)
                cr_exist = 1
                break
        if not cr_exist:
            new_faulty_setup_runs[board] = value
    # File CR for the faulty board which doesnt have already open CRs
    for board, value in new_faulty_setup_runs.items():
        # Find latest failing log from the results
        sorted_jobs = sorted(value, key=lambda x: x["jobid"], reverse=True)
        for fail_index, run_details_dict in enumerate(sorted_jobs):
            if run_details_dict["result"] == "FAIL":
                break
        jobid_warn = ""
        if fail_index > 0:
            latest_job_id = sorted_jobs[0]["jobid"]
            jobid_warn = f"latest jobid {latest_job_id} is a passing run on this board.. check if the issue persists"
        # File a new CR if allowed
        if not args.cr_disable:
            fail_count = fail_counts[board]
            run_count = run_counts[board]
            issue_dict = create_cr_dict(
                sorted_jobs[fail_index],
                cr_settings_dict,
                xls_timestamp,
                fail_count,
                run_count,
            )
            new_cr = BoardfarmCR(issue_dict=issue_dict, jira_connection=jq.jira)
            new_cr.create_issue()
            print1(f"Filed {new_cr.key} for board : {board}", True)
            if os.path.isfile(site_log_file):
                log.critical(f"{board} : {new_cr.key} opened by {user}")
            if "xhd" in board_name or "bf" in board_name:
                exclude_cr_dict_xhd[board] = new_cr.key
            else:
                exclude_cr_dict_xsj[board] = new_cr.key
            new_cr.add_attachment(issue_dict["attachment"])
            new_cr.set_assignee(issue_dict["verifier"])
            new_cr.add_jira_label(issue_dict["labels"])
            watchers = cr_settings_dict["managers"] + cr_settings_dict["regress_team"]
            new_cr.add_watcher(watchers)
            log_data = get_log_info(sorted_jobs[fail_index]["log_base"])
            comment = (
                f"{new_cr.summary}\n{new_cr.description}\n"
                f"\nsteps to reproduce\n{new_cr.steps2reproduce}\nresult logs will be PWD\n"
                f"\n{log_data}\n"
                f"\n[~{issue_dict['verifier']}] please check the issue and then assign to boardfarm team\n"
                f"Also check EPIC link and Device Family fields in this CR\n"
                f"{jobid_warn}"
            )
            new_cr.add_comment(comment)
            email_en = 1
        if not cr_exist and args.cr_disable:
            print1(
                f"CR filing disabled, no CR filed for {board}, please file manually",
                True,
            )
            email_en = 1

    # Add CR details in manual exclude JSON, remove setups for closed CRs
    if host_location == "XHD" and user == "burst-test":
        new_exclude_cr_dict = exclude_cr_dict_xhd
        site_exclude_file = exclude_xhd_mod
    elif host_location == "XSJ" and user == "burst-test":
        new_exclude_cr_dict = exclude_cr_dict_xsj
        site_exclude_file = exclude_xsj_mod
    else:
        new_exclude_cr_dict = ""
        site_exclude_file = ""
    all_cr_list = jq.key_list
    if new_exclude_cr_dict:
        all_cr_list += list(new_exclude_cr_dict.values())
    if site_exclude_file:
        exclude_data = read_json(site_exclude_file)
        cr_info = exclude_data["cr_info"]
        cr_info_existing = {}
        for board, cr_num in cr_info.items():
            if cr_num in all_cr_list:
                cr_info_existing[board] = cr_num
            else:  # Remove closed CRs boards from exclude list
                cluster = get_cluster_name(board)
                exclude_data[cluster].remove(board)
                if os.path.isfile(site_log_file):
                    log.critical(f"{board} : {cr_num} closed")
        # Add newly filed CRs to existing CR data
        if new_exclude_cr_dict:
            cr_info_existing.update(new_exclude_cr_dict)
        exclude_data["cr_info"] = cr_info_existing
        write_json(site_exclude_file, exclude_data)

    # Email results if any action is to be taken by user
    if email_en and args.to:
        subject = f"Faulty boardfarm setups: {datetime.now().strftime('%m/%d/%Y')} from {host_location}"
        message_txt = f"Hi {args.to[0]},\n\n{message_txt}\nKind Regards,\n{user}\n"
        if args.cc:
            send_email(subject, message_txt, args.to[0], cc=args.cc[0])
            print1(f"Email sent to : {args.to[0]}, cc: {args.cc[0]}", True)
        else:
            send_email(subject, message_txt, args.to[0])
            print1(f"Email sent to : {args.to[0]}", True)
    if not email_en and args.to:
        print1(f"Email not sent because no action is required from user", True)
    print1("\n" + "=" * 80 + "\n", True)
