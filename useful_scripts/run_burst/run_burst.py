#!/usr/bin/env python3

import sys
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    print("This script requires a python version of at least 3.6 Exiting.")
    exit(-1)
if sys.version_info[1] != 8 or sys.version_info[2] != 3:
    print("WARN: This script is only tested with python version 3.8.3")

# Importing modules
from shlex import split
from subprocess import Popen
from subprocess import check_output
from subprocess import CalledProcessError
import argparse
import json
import re
import getpass
import os
from os import getcwd
from os import getenv
from os import system
from os import sep
from pathlib import Path
from time import time
from time import localtime
from time import strftime
from socket import gethostname
from help import print_boards
from misc import create_run_name
from help import print_example
from help import list_board_setups
from help import get_host_location
from help import get_git_revision_hash
from help import recall_list
from help import create_systest_message
from update import busg_generation
from update import cluster_ping
from update import source_setup_warning
from update import create_exclude_file
from misc import save_config
from misc import systest_cmd_create
from misc import pick_cmd_file
from validity import is_board_valid
from validity import is_elf_present
from validity import check_cping_version
from run_status import return_to_run_regression
from options import options

# Used instead of #define
PRINT_RUN_CONDITION = True
LAUNCH_ENABLE = True
# TRUE: Issue jobs to systest;
# FALSE: Do not issue jobs to systest;

# Adding new arguments
# Note: Use long (--argument) and short (-arg) form for an argument
# when adding a new argument. The short form should be max 3 character
# long and the long forms should minimum 4 character long and the corresponding
# class object should be named same as the long/short form name of the argument.
# 2. if the arguments have fixed list of choices, it muust be added to options
# dictionary and used by parser instead of directly adding to the parser choices


# Parse General Arguments
parser = argparse.ArgumentParser(
    description='Run BURST using command line flags',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    epilog='Queries Contact: burst_script_team@xilinx.com')

group = parser.add_mutually_exclusive_group()

group.add_argument('--list_setups', '-ls',
                    help='(STANDALONE) Print out boards, expects a board name')
group.add_argument('--list_boards', '-lb',
                    action='store_true',
                    help='(STANDALONE) Print out boards')
group.add_argument('--example', '-ex',
                    action="store_true",
                    help='(STANDALONE) Prints example usage commands')
group.add_argument('--update', '-u',
                    choices=['all', 'busg', 'boards', 'exclude'],
                    help='(STANDALONE) Update dependencies <all/busg/boards>')
group.add_argument('--recall', '-r',
                    help='(STANDALONE) Expects a recall JSON file')
group.add_argument('--recall_last', '-rl',
                    action='store_true',
                    help='(STANDALONE) Reruns the previous BURST run')
parser.add_argument('--run_number', '-rn',
                    help='Run number to distinguish'
                    'between two identical runs/ regression profile'
                    'line number')

# Parse Platform Arguments
parser.add_argument('--board', '-b',
                    help='(REQUIRED) Specify the board type/board_number to '
                         'run test')
parser.add_argument('--board_tag', '-bt',
                    help='Specify the complete board tag to acquire a specific '
                         'setup, user need to specify other flags like '
                         '-si/-dc/-br to pick cmd file')
parser.add_argument('--daughter_card', '-dc',
                    choices=options["daughter_card"],
                    help='(REQUIRED for zc1751 board) Specify daughter card or '
                         'board revision')
parser.add_argument('--silicon_revision', '-si',
                    choices=options["silicon_revision"],
                    help='(REQUIRED) Specify silicon version/ emulation '
                         'platform')
parser.add_argument('--board_revision', '-br',
                    choices=options["board_revision"],
                    help='(REQUIRED for zcu102 board) Specify board revision')
parser.add_argument('--root_complex', '-rc',
                    choices=options["root_complex"],
                    help='Specify board pcie root complex')
parser.add_argument('--end_point', '-ep',
                    choices=options["end_point"],
                    help='Specify the pcie end point')
parser.add_argument('--lane_count', '-lc',
                    choices=options["lane_count"],
                    help='Specify the pcie lane count')
parser.add_argument('--pcie_gen', '-pg',
                    choices=options["pcie_gen"],
                    help='Specify the pcie gen')
parser.add_argument('--bridge_rc', '-brc',
                    choices=options["bridge_rc"],
                    default=None,
                    help='Specify the rc side bridge')
parser.add_argument('--bridge_ep', '-bep',
                    choices=options["bridge_ep"],
                    default=None,
                    help='Specify the ep side bridge')
parser.add_argument('--cpm_mode', '-cm',
                    choices=options["cpm_mode"],
                    default=None,
                    help='Specify the mode in which CPM is running')
parser.add_argument('--ddr_mode', '-dm',
                    choices=options["ddr_mode"],
                    default=None,
                    help='Specify the DDR mode in which CPM is running')
parser.add_argument('--config_rc', '-cr',
                    choices=options["config_rc"],
                    default=None,
                    help='Specify the configuration type in which CPM RC is running')

# Parse BURST config Arguments
parser.add_argument('--project', '-pj',
                    choices=options["project"],
                    help="Project name")
parser.add_argument('--processor', '-p',
                    choices=options["processor"],
                    help='Specify a53/r5/mb/x86 default: chosen based on board')
parser.add_argument('--burst_path', '-bp',
                    help='Specify location of BURST elf')
parser.add_argument('--clock', '-clk',
                    choices=options["clock"],
                    help='Specify clock profile for da7_prod'
                         ' sivdef/av default: av')
parser.add_argument('-dp',
                    action="store_true",
                    help='Pass flag to run with display port')
parser.add_argument('-be',
                    action="store_true",
                    help='Pass flag to make run big endian')
parser.add_argument('--ospi_enable', '-ospi',
                    action="store_true",
                    help='Pass flag to use ospi enabled runs (everest only)')
parser.add_argument('-ecc',
                    action="store_true",
                    help='Pass flag to run with DDR ECC ON')
parser.add_argument('--bup_enable', '-bup',
                    action="store_true",
                    help='Pass flag to use bup enabled runs (everest only)')
parser.add_argument('--bupcoh_enable', '-bupcoh',
                    action="store_true",
                    help='Pass flag to use coherent bup enabled runs (everest only)')
parser.add_argument('--tile', '-tl',
                    choices=options["tile"],
                    help='Pass flag to use specify ME tile (everest only)')
parser.add_argument('--knobs', '-k',
                    default='n',
                    help='Pass command line knobs Format: knob1,knob2,knob3,')
parser.add_argument('--run_time', '-rt',
                    default='1800',
                    help='Run time limit for the run, default: 30mts')
parser.add_argument('--session', '-s',
                    default='0',
                    choices=['0', '1', '2'],
                    help='Palladium session number 0 or 1')
parser.add_argument('--tool_version', '-tv',
                    default=False,
                    help='Specify the XSDB tool version to use.')

# Parse Environment Arguments
parser.add_argument('--mode', '-m',
                    default='batch', choices=['interact', 'batch', 'regres'],
                    help='Select which mode to run, default: batch')
parser.add_argument('--dont_save', '-ds',
                    action="store_true",
                    help='Pass flag to not save recall file')
parser.add_argument('--preempt', '-pm',
                    choices=['1', '2', '3', '4', '5', '6'],
                    help='Pass number of pre-emptable jobs to launch')
parser.add_argument('--cmd_path', '-cp',
                    help='Specify a cmd/dat file to run the test')
parser.add_argument('--logs_dir', '-lp',
                    help='Specify a log path to save the results')
parser.add_argument('--no_build', '-nb',
                    action="store_true",
                    help='Disable BURST build')
parser.add_argument('--exclude', '-e',
                    help='Boards that needs to be excluded,coma separated')
parser.add_argument('--message', '-msg',
                    help='Systest message')
parser.add_argument('--dont_launch', '-dl',
                    action="store_true",
                    help='Dont execute systest commands')
parser.add_argument('--python', '-py',
                    action="store_true",
                    help='Pick the bf2.0 python version of the script')

class Platform(object):
    def __init__(self, args, hostenv):
        self.board = args.board
        self.board_tag = args.board_tag
        self.board_num = None
        if args.board:
            if len(args.board.split('-')) > 1 and \
                    str(args.board.split('-')[-1]).isnumeric():
                self.board = None
                self.board_num = args.board
            else:
                self.board_num = None
                self.board = args.board
        if hostenv.host_location == 'XHD':
            if self.board_num:
                if self.board_num.split('-')[0] != 'xhd' and self.board_num.split('-')[0] != 'bf':
                    self.board_num = 'xhd-' + self.board_num
        self.dc = args.daughter_card
        self.si = args.silicon_revision
        self.board_revision = args.board_revision
        # Pick dc1 if the user asks for a zc1751 board and no daughter cards
        if not self.dc:
            if self.board == "zc1751":
                self.dc = "dc1"
        # Pick rev 1.0  if the user asks for a zcu102 board and no revision
        if not self.board_revision:
            if self.board == 'zcu102':
                self.board_revision = 'rev1.0'
        else:
            self.board_revision = args.board_revision
        self.root_complex = args.root_complex
        self.end_point = args.end_point
        self.lane_count = args.lane_count
        self.pcie_gen = args.pcie_gen
        self.bridge_rc = args.bridge_rc
        self.bridge_ep = args.bridge_ep
        self.cpm_mode = args.cpm_mode
        self.ddr_mode = args.ddr_mode
        self.config_rc = args.config_rc
        if args.exclude:
            self.exclude = [x.strip('"\'') for x in args.exclude.split(',')]
        else:
            self.exclude = False
        self.session = args.session


class BurstConfig(object):
    def __init__(self, args, platform, hostenv):
        self.proc = args.processor
        self.gen = args.project
        if (not self.gen) and platform.board:
            self.find_default_genproc(hostenv, platform.board)
        elif(not self.gen) and platform.board_num:
            _board = re.sub("-\d+", "", platform.board_num)
            self.find_default_genproc(hostenv, _board)
        if (not self.gen) and (not platform.board) and (not platform.board_num):  # pcie
            self.find_default_genproc(hostenv, 'pcie')
        if args.burst_path != 'None' and args.burst_path is not None:
            self.burst_path = args.burst_path
        else:
            self.burst_path = hostenv.current_dir
        self.clk = args.clock
        self.dp = args.dp
        self.be = args.be
        self.ecc = args.ecc
        if args.knobs != 'n':
            if args.knobs[-1] != ',':
                args.knobs += ','
            self.knobs = args.knobs
        else:
            self.knobs = 'n'
        self.run_time = args.run_time
        self.busg_path = hostenv.burst_folder + "/burst-scripts/script_gen"
        self.logs_dir = None
        if args.logs_dir != 'None' and args.logs_dir is not None:
            self.logs_base_dir = Path(args.logs_dir)
        else:
            self.logs_base_dir = Path(hostenv.current_dir + "/logs/")
        self.recall_file = Path(hostenv.current_dir + "/logs/recall/")  # temp
        if platform.si == "da7_prod" and not self.clk:
            self.clk = "av"
        self.ospi_enable = args.ospi_enable
        self.bup_enable = args.bup_enable
        self.bupcoh_enable = args.bupcoh_enable
        self.tile = args.tile
        self.tool_version = args.tool_version
    
    def __str__(self):
        string = f"processor={self.proc}\n"
        string += f"\tgen={self.gen}\n"
        string += f"\tburst_path={self.burst_path}\n"
        string += f"\tclock={self.clk}\n"
        string += f"\tdp={self.dp}\n"
        string += f"\tbe={self.be}\n"
        string += f"\tecc={self.ecc}\n"
        string += f"\tknobs={self.knobs}\n"
        string += f"\trun_time={self.run_time}\n"
        string += f"\tbusg_path={self.busg_path}\n"
        string += f"\tlogs_dir={self.logs_dir}\n"
        string += f"\tlogs_base_dir={self.logs_base_dir}\n"
        string += f"\trecall_file={self.recall_file}\n"
        string += f"\tospi_enable={self.ospi_enable}\n"
        string += f"\tbup_enable={self.bup_enable}\n"
        string += f"\ttile={self.tile}\n"
        return string

    def find_default_genproc(self, hostenv, key_word):
        _settings_file = Path(str(hostenv.script_dir) + '/settings.json')
        if key_word.startswith("sl-tenzing"):
            key_word = 'tenzing'
        try:
            with open(str(_settings_file)) as data_file:
                _json_data = json.load(data_file)
                try:
                    self.gen = _json_data['default_project'][key_word]
                except KeyError:
                    print("WARN: Not a run_burst supported board!")
                if (not self.proc) and self.gen:
                    try:
                        self.proc = _json_data['default_'
                                               'processor'][str(self.gen)]
                    except KeyError:
                        print("ERROR: Unsupported project generation")
                        return_to_run_regression(hostenv.mode)
                elif not self.gen:
                    print("ERROR: --project missing")
                    return_to_run_regression(hostenv.mode)
        except IOError:
            print("ERROR: Unable to open " + str(_settings_file))
            return_to_run_regression(hostenv.mode)


class TestEnv(object):
    def __init__(self, args):
        self.current_dir = getcwd()
        self.shell = str(getenv('SHELL').split(sep)[2])
        self.user = getpass.getuser()
        self.burst_folder = getenv('XSLV')
        if not self.burst_folder:
            self.burst_folder = Path(source_setup_warning())
        else:
            self.burst_folder = Path(self.burst_folder)
        self.burst_folder = str(self.burst_folder.resolve())
        self.mode = args.mode
        self.dont_save = args.dont_save
        self.no_build = args.no_build
        self.preempt = args.preempt
        self.local_time_std = str(strftime("%Y%m%d_%H%M", localtime(time())))
        self.host_location = get_host_location()
        self.host_machine = str(gethostname())
        self.script_dir = self.burst_folder + "/burst-scripts/run_burst"
        self.version_file = Path(self.script_dir + '/cping_version_local.txt')
        self.xsj_cron_dir = "/home/xppc/burst/cping_cron/"
        self.xhd_cron_dir = "/home/xppc/burst/crons/cping_xhd/"
        self.cmd_path = args.cmd_path
        self.commit_script = get_git_revision_hash(self.script_dir)
        self.commit_code = get_git_revision_hash(self.burst_folder)
        if args.run_number:
            try:
                self.run_number = int(args.run_number)
            except ValueError:
                print("Error: run_number is an invalid value.")
                return_to_run_regression(args.mode)
        else:
            self.run_number = ''
        self.timeout = "No"
        self.is_python = args.python
    
    def __str__(self):
        string = f"current_dir={self.current_dir}\n"
        string += f"\tshell={self.shell}\n"
        string += f"\tuser={self.user}\n"
        string += f"\tburst_folder={self.burst_folder}\n"
        string += f"\tmode={self.mode}\n"
        string += f"\tdont_save={self.dont_save}\n"
        string += f"\tno_build={self.no_build}\n"
        string += f"\tpreempt={self.preempt}\n"
        string += f"\tlocal_time_std={self.local_time_std}\n"
        string += f"\thost_location={self.host_location}\n"
        string += f"\tscript_dir={self.script_dir}\n"
        string += f"\tversion_file={self.version_file}\n"
        string += f"\txsj_cron_dir={self.xsj_cron_dir}\n"
        string += f"\txhd_cron_dir={self.xhd_cron_dir}\n"
        string += f"\tcmd_path={self.cmd_path}\n"
        string += f"\tcommit_script={self.commit_script}\n"
        string += f"\tcommit_code={self.commit_code}\n"
        string += f"\trun_number={self.run_number}\n"
        string += f"\tmessage={self.message}\n"
        string += f"\ttimeout={self.timeout}\n"
        return string


def prepare_test(platform, burstconfig, hostenv):
    """ Function that prepares for a BURST run - Build, cmd generation"""
    global LAUNCH_ENABLE
    if not hostenv.no_build:
        # print('Building BURST')
        # Doubt - what is this build-all command - Used to create elf from the latest C driver files.
        build_status = system('build-all')
        if build_status != 0:
            print('BURST build failed !')
            return_to_run_regression(hostenv.mode)
    elif not burstconfig.burst_path:
        burstconfig.burst_path = hostenv.current_dir
    LAUNCH_ENABLE &= is_elf_present(hostenv, burstconfig)

    # Generate BUSG scripts if the BUSG cmd folder is missing
    if not Path(hostenv.burst_folder + '/burst-scripts/cmd_scripts').is_dir():
        busg_generation(burstconfig.busg_path)

    # Set the cmd_script path to be used.
    try:
        if not Path(hostenv.cmd_path).is_file():
            # Doubt - It is taking only one cmd file itseems?
            hostenv.cmd_path = pick_cmd_file(platform, burstconfig, hostenv)
        else:
            print("Non BUSG cmd: " + str(Path(hostenv.cmd_path).resolve()))
    except TypeError:
        hostenv.cmd_path = pick_cmd_file(platform, burstconfig, hostenv)



def create_directories(burstconfig, run_name):
    """ Set BURST folder names and if LAUNCH is enabled create the folder
    structure if it doesnt exist"""
    if not burstconfig.logs_dir:
        burstconfig.logs_dir = Path(burstconfig.logs_base_dir)
    else:
        burstconfig.logs_dir = Path(str(burstconfig.logs_base_dir)+'/'+run_name)
    if not burstconfig.logs_dir.is_dir() and LAUNCH_ENABLE:
        system('mkdir --parents '+str(burstconfig.logs_dir))

    # Creating recall file name
    recall_dir = Path(str(burstconfig.logs_dir) + "/recall/")
    if not recall_dir.is_dir() and LAUNCH_ENABLE:
        system('mkdir --parents '+str(recall_dir))
    burstconfig.recall_file = Path(str(recall_dir) + '/' +
                                   run_name + '.json')


def run_systest(platform, burstconfig, hostenv):
    """ Function that launches the systest job for a BURST run"""
    # First generate a list of boards to avoid if not pcie setup
    ex_boards = []
    _board_exclude = Path(hostenv.script_dir + "/exclude.json")
    if hostenv.preempt:
        _board_exclude = Path(hostenv.script_dir + "/exclude_preempt.json")
    if not(platform.root_complex or platform.lane_count or platform.end_point):
        if _board_exclude.is_file():
            if platform.board_num:
                _board_name = re.sub("-\d+", "", platform.board_num)
                if _board_name.startswith("sl-tenzing"):
                    _board_name = 'tenzing'
            else:
                _board_name = platform.board
            if _board_name.startswith('xhd-'):
                _board_name = _board_name[4:]
            if _board_name.startswith('bf-'):
                _board_name = _board_name[3:]
            try:
                with open(str(_board_exclude)) as data_file:
                    ex_boards = json.load(data_file)[_board_name]
            except IOError:
                print("ERROR: Unable to open " + str(_board_exclude))
                return_to_run_regression(hostenv.mode)
        else:
            print("WARN: Excludes file missing !")
    # Adding the user requested excluded boards to the auto detected
    # excluded boards
    if platform.exclude:
        ex_boards = ex_boards + platform.exclude

    # creating systest command (csh systest syntax command works
    # for bash and csh but not vice-versa)
    run_name = create_run_name(hostenv, platform)
    burstconfig.logs_dir = Path(str(burstconfig.logs_base_dir) + '/' + run_name)
    if not LAUNCH_ENABLE:
        create_directories(burstconfig, run_name)
    systest_cmd = systest_cmd_create(platform, burstconfig,
                                     hostenv, hostenv.cmd_path, ex_boards)
    if not systest_cmd:
         return
    # Run systest
    if LAUNCH_ENABLE:
        if hostenv.mode != 'regres':
            cmd_list = []
            if hostenv.preempt:
                for pre_count in range(1, int(hostenv.preempt) + 1):
                    cmd_list.append(create_premept_runs(hostenv, platform,
                                                         burstconfig, pre_count,
                                                         ex_boards))
                user_signature = input('Do you agree to launch BURST ? '
                                       'yes(y)/no(n):')
                if user_signature.lower() == 'yes' or \
                        user_signature.lower() == 'y':
                    for preempt_run in cmd_list:
                        create_directories(burstconfig, preempt_run[0])
                        if not hostenv.dont_save:
                            save_config(burstconfig.recall_file,
                                        platform,
                                        burstconfig,
                                        hostenv,
                                        systest_cmd)
                        print(burstconfig.logs_dir)
                        Popen(preempt_run[1])
                else:
                    print("User declined the run")
                    exit(0)
            else:
                print('{:12} : {}'.format('run_name', str(run_name)))
                print('{:12} : {}'.format('systest_cmd', systest_cmd))
                user_signature = input('Do you agree to launch BURST ? '
                                       'yes(y)/no(n):')
                if user_signature.lower() == 'yes' or \
                        user_signature.lower() == 'y':
                    create_directories(burstconfig, run_name)
                    args = split(systest_cmd)
                    Popen(args)
                else:
                    print("User declined the run")
                    exit(0)
            if not hostenv.dont_save:
                save_config(burstconfig.recall_file,
                            platform,
                            burstconfig,
                            hostenv,
                            systest_cmd)
            if PRINT_RUN_CONDITION:
                print("Systest process created\n")
        else:  # Regression
            outlist = []
            if hostenv.preempt:
                for pre_count in range(1, int(hostenv.preempt)+1):
                    args = create_premept_runs(hostenv, platform,
                                               burstconfig, pre_count,
                                               ex_boards)
                    try:
                        line = check_output(args[1])
                        # Search for the first 7 digit number in the line
                        id_match = re.findall('Job <(\d+)>', str(line))
                        # Do not remove this for loop print (used by run regression)
                        for job_id in id_match:
                            print('Job ID:' + str(job_id))
                        if not hostenv.dont_save:
                            save_config(burstconfig.recall_file,
                                        platform,
                                        burstconfig,
                                        hostenv,
                                        systest_cmd)
                        outlist.append([job_id, args[0], hostenv.cmd_path,
                                        burstconfig.run_time, burstconfig.knobs,
                                        burstconfig.burst_path])
                    except (UnboundLocalError, CalledProcessError):
                        print("No other board setup available for retesting.")
            else:
                args = split(systest_cmd)
                create_directories(burstconfig, run_name)
                # Do not remove this print ( used by run regression )
                print('{:12} : {}'.format('run_name', str(run_name)))
                print('{:12} : {}'.format('systest_cmd', systest_cmd))
                try:
                    line = check_output(args)
                    # Search for the first 7 digit number in the line
                    id_match = re.findall('Job <(\d+)>', str(line))
                    # Do not remove this for loop print (used by run regression)
                    for job_id in id_match:
                        print(f"Job ID: {job_id}\n")
                    if not hostenv.dont_save:
                        save_config(burstconfig.recall_file,
                                    platform,
                                    burstconfig,
                                    hostenv,
                                    systest_cmd)
                    outlist.append([job_id, run_name, hostenv.cmd_path,
                                        burstconfig.run_time, burstconfig.knobs,
                                        burstconfig.burst_path])
                except (UnboundLocalError, CalledProcessError):
                    print("No other board setup available for retesting.")
            return outlist
    else:       # LAUNCH_ENABLE = 0;
        if hostenv.run_number:
            print(f"{hostenv.run_number} : {systest_cmd}")
        else:
            print(f"{systest_cmd}")
    return 0


def create_premept_runs(hostenv, platform, burstconfig, pre_count, ex_boards):
    """
    Function that create the folders and command for a pre-emptable run
    """
    run_name = create_run_name(hostenv, platform, pre_count)
    burstconfig.logs_dir = Path(
        str(burstconfig.logs_base_dir) + '/' + run_name)
    systest_cmd = systest_cmd_create(platform, burstconfig,
                                     hostenv,
                                     hostenv.cmd_path,
                                     ex_boards)
    if hostenv.mode == 'regres':
        create_directories(burstconfig, run_name)
    args = split(systest_cmd)
    # Do not remove this print ( used by run regression )
    print('{:12} : {}'.format('run_name', str(run_name)))
    print('{:12} : {}\n'.format('systest_cmd', systest_cmd))
    return [run_name, args]


def verify_arguments(args, hostenv, burstconfig, platform):
    """ Function that takes care of help, maintenance arguments"""
    local_time = localtime(time())
    hour = local_time.tm_hour
    minute = local_time.tm_min
    # Creating setup files if it doesn't exist.
    time_string = str(local_time.tm_year) + '_' + \
        str(local_time.tm_mon) + '_' + \
        str(local_time.tm_mday) + '_' + \
        str(hour) + '_' + \
        str(minute)

    # Take care of all single requests
    if args.update == 'all':
        busg_generation(burstconfig.busg_path)
        cluster_ping(hostenv.script_dir, hostenv.user, time_string)
        create_exclude_file(hostenv)
        sys.exit(0)
    # Gopi - busg will generate cmd scripts
    # Gopi - boards will generate list of boards and their line tags into boards.txt
    # Gopi - exclude, I didnt understand
    if args.update == 'busg':
        busg_generation(burstconfig.busg_path)
        sys.exit(0)
    if args.update == 'boards':
        cluster_ping(hostenv.script_dir, hostenv.user, time_string)
        sys.exit(0)
    if args.update == 'exclude':
        # Doubt - what is exclude file creation - simply creating empty dictionaries?
        create_exclude_file(hostenv, time_string)
        sys.exit(0)
    if args.list_setups:
        list_board_setups(args.list_setups,
                          Path(hostenv.script_dir + '/valid_config.txt'))
        sys.exit(0)
    if args.list_boards:
        print_boards(Path(hostenv.script_dir + '/boards.txt'))
        sys.exit(0)
    if args.example:
        print_example(str(sys.argv[0]))
        sys.exit(0)

    # Making sure that the setup files exist and are up to date
    if get_host_location() == 'XSJ':
        files_updated = check_cping_version(hostenv.xsj_cron_dir,
                                            hostenv.script_dir,
                                            time_string,
                                            hostenv.user)
        if files_updated:
            create_exclude_file(hostenv, time_string)
    elif get_host_location() == 'XHD':
        files_updated = check_cping_version(hostenv.xhd_cron_dir,
                                            hostenv.script_dir,
                                            time_string,
                                            hostenv.user)
        if files_updated:
            create_exclude_file(hostenv, time_string)

    _bfile = Path(hostenv.script_dir + "/boards.txt")
    _sfile = Path(hostenv.script_dir + "/valid_config.txt")
    _exfile1 = Path(hostenv.script_dir + "/exclude.json")
    _exfile2 = Path(hostenv.script_dir + "/exclude_preempt.json")
    if (not _bfile.is_file()) or (not _sfile.is_file()):
        cluster_ping(hostenv.script_dir, hostenv.user, time_string)
        create_exclude_file(hostenv, time_string)
    elif (not _exfile1.is_file()) or (not _exfile2.is_file()):
        create_exclude_file(hostenv, time_string)
    # Check to make sure if there is at-least one input and
    # board (pci_root complex and pcie end point) is valid
    if len(sys.argv) > 1:
        is_board_valid(platform, _bfile)
    else:
        print("ERROR: No arguments")
        return_to_run_regression(hostenv.mode)


def check_recall(user_args):
    """
    Function that checks the user arguments to find out if the run
    is a recall BURST run
    """
    if user_args.recall:
        if Path(user_args.recall).is_file():
            args_in = recall_list(user_args.recall, parser, user_args.exclude)
        else:
            print("ERROR: Recall file does not exist !")
            return_to_run_regression(user_args.mode)
    elif user_args.recall_last:
        _recall_file = str(getcwd())+'/recall.json'
        if Path(_recall_file).is_file():
            args_in = recall_list(_recall_file, parser, user_args.exclude)
        else:
            print("ERROR: No previous run Recall File exist!")
            return_to_run_regression(user_args.mode)
    else:
        args_in = sys.argv[1:]
    return args_in


def main(args):
    global LAUNCH_ENABLE
    # Initializing the class objects
    if args.dont_launch:
        if args.mode != 'regres':
            print("No tests will be launched !")
        LAUNCH_ENABLE = 0
    hostenv = TestEnv(args)
    platform = Platform(args, hostenv)
    burstconfig = BurstConfig(args, platform, hostenv)
    # Verifying user inputs
    verify_arguments(args, hostenv, burstconfig, platform)
    # Preparing for a run
    prepare_test(platform, burstconfig, hostenv)
    cmd_name = os.path.splitext(os.path.split(hostenv.cmd_path)[1])[0]
    hostenv.message =  create_systest_message(args, cmd_name)
    # Launching a systest job
    out_list = run_systest(platform, burstconfig, hostenv)
    if out_list:
        return out_list
    else:
        return 0


if __name__ == "__main__":
    try:
        # Parsing the user command line arguments
        usr_args = parser.parse_args()
        # Checking if the run is a recall run
        args_in = check_recall(usr_args)
        # Parsing the user/recall arguments
        main(parser.parse_args(args_in))
    except KeyboardInterrupt:
        print("Keyboard interrupt")
        exit(0)
