import sys
from help import print_boards
from os import listdir
from os import system
from os import getcwd
from pathlib import Path
from run_status import return_to_run_regression
from update import cluster_ping
import datetime
import re
import json


def is_board_valid(platform, bfile_path):
    """Function that checks if the board exits in board farm based
    on cached boards list"""
    # Check if it is a PCIe run (board name = None)
    if platform.root_complex or platform.end_point or platform.lane_count:
        if not (platform.root_complex and platform.end_point
                and platform.lane_count and platform.si):
            print("ERROR: Must specify \n"
                  "1) board, silicon_version OR\n"
                  "2) root complex, end point, lane count, silicon version OR\n"
                  "3) board_number, silicon version, "
                  "board_rev/daughter_card(if it exists) OR\n"
                  "4) board, silicon_version, tile (ipp_me)\n")
            sys.exit(-1)
        else:
            return 1
    if platform.board_num:
        _board_name = re.sub("-\d+", "", platform.board_num)
        if _board_name.startswith("sl-tenzing"):
            _board_name = 'tenzing'
    else:
        _board_name = platform.board
    if not (platform.board and platform.si) and \
            not (platform.board_num and platform.si):
        print("ERROR: Must specify \n"
              "1) board, silicon_version OR\n"
              "2) root complex, end point, lane count, silicon version OR\n"
              "3) board_number, silicon version, "
              "board_rev/daughter_card(if it exists) OR\n"
              "4) board, silicon_version, tile (ipp_me)\n")
        sys.exit(-1)
    if bfile_path.is_file():
        with open(str(bfile_path), 'r') as bfile:
            for line in bfile:
                board_name_in_file = line.strip()
                if 'xhd-' + board_name_in_file == _board_name or \
                        'bf-' + board_name_in_file == _board_name or \
                        board_name_in_file == _board_name:
                    return 1
            print("Invalid board name: " + str(_board_name))
            print("The available boards in board farm: ")
            print_boards(bfile_path)
    else:
        print('Missing setup file: boards.txt')
        print('Run ' + sys.argv[0] + ' -u boards' +
              ' to update setup files and try again\n')


def is_elf_present(hostenv, burstconfig):
    """Function that checks if the elf for the requested processor-endianess
     exist"""
    if not burstconfig.proc or not burstconfig.burst_path:
        return False
    key = burstconfig.proc
    if burstconfig.be:
        key = key + '-be'
    _settings_file = Path(str(hostenv.script_dir) + '/settings.json')
    try:
        with open(str(_settings_file)) as data_file:
            _json_data = json.load(data_file)
            try:
                elf_name = _json_data['elf_dict'][key]
            except KeyError:
                print("ERROR: Not a run_burst supported elf: "+str(key))
                return return_to_run_regression(hostenv.mode)
    except IOError:
        print("WARN: Unable to open " + str(_settings_file))
        return
    elf_file = Path(str(burstconfig.burst_path)+'/'+elf_name)
    if not elf_file.is_file():
        print('ERROR: elf file missing: '+str(elf_file))
        return return_to_run_regression(hostenv.mode)
    return True


def is_exist_profile(hostenv, file_name):
    """Function that checks if the given file exist in the  profile dir/ pwd
     or user provide a profile file path that exist and returns
     and absolute path to the profile"""
    if Path(file_name + '.profile').is_file():
        return str(Path(file_name + '.profile').resolve())
    for filename in listdir(str(hostenv.profile_dir)):
        if filename.endswith(".profile") and str(filename)[0] != '#':
            if filename == (file_name + ".profile"):
                return str(Path(str(hostenv.profile_dir) + '/'
                                                    + filename).resolve())
    for filename in listdir(str(getcwd())):
        if filename.endswith(".profile") and str(filename)[0] != '#':
            if filename == (file_name + ".profile"):
                return str(Path(getcwd() + '/' + filename).resolve())
    return 0

def is_cmt_profile(hostenv, file_path):
    """Function that checks whether all the profile lines 
     in the profile are commented to avoid creating log 
    directories """
    pfile_lines = 0
    try:
        with  open(str(file_path), 'r') as profile_file:
            lines_count = len(profile_file.readlines())
            profile_file.seek(0)
            # Checking if all lines in profile are commented out
            for line in profile_file:
                cmd_line = line.rstrip('\n')
                if cmd_line.strip() != '':
                    if cmd_line.lstrip(' ')[0][0] == '#':
                        pfile_lines += 1
                elif cmd_line.strip() == '':
                    pfile_lines += 1
                if lines_count == pfile_lines:
                    return 1
    except IOError:
        print("ERROR: Unable to open {}".format(file_path))
    return 0

def check_cping_version(update_cron, script_dir, time_string, user):
    """Function that checks if the setup files are outdated and copies
     updated results from cron job results"""
    version_file = Path(script_dir + '/cping_version_local.txt')
    cron_file = Path(update_cron + '/cping_version.txt')
    if version_file.is_file() and cron_file.is_file():
        vfile_local = open(str(version_file), 'r')
        vfile_local.seek(0)
        local_line = vfile_local.readline()
        local_version_list = local_line.rstrip('\n').split('_')
        local_date = datetime.datetime(int(local_version_list[0]),
                                       int(local_version_list[1]),
                                       int(local_version_list[2]),
                                       int(local_version_list[3]),
                                       int(local_version_list[4]))
        vfile_local.close()
        vfile = open(str(cron_file), 'r')
        vfile.seek(0)
        cron_line = vfile.readline()
        cron_version_list = cron_line.rstrip('\n').split('_')
        cron_date = datetime.datetime(int(cron_version_list[0]),
                                      int(cron_version_list[1]),
                                      int(cron_version_list[2]),
                                      int(cron_version_list[3]),
                                      int(cron_version_list[4]))
        vfile.close()
        if cron_date <= local_date:
            return 0
        else:
            print("Outdated cluster ping results found !")
            print("Updating results from CRON Job")
            cp_cmd = 'cp -rf '+str(update_cron)+'cping_result/* ' + \
                     str(script_dir)+'/'
            system(cp_cmd)
            vfile_local = open(str(version_file), 'w')
            vfile_local.seek(0)
            vfile_local.write(cron_line)
            vfile_local.close()
    elif (not version_file.is_file()) and cron_file.is_file():
        print("Updating results from CRON Job")
        cp_cmd = 'cp -rf ' + str(update_cron) + 'cping_result/* ' + \
                 str(script_dir) + '/'
        system(cp_cmd)
        cp_cmd = 'cp -rf ' + str(update_cron) + 'cping_version.txt ' + \
                 str(script_dir) + '/'
        system(cp_cmd)
        cp_cmd = 'mv -f ' + str(script_dir) + '/cping_version.txt ' + \
                 str(script_dir) + '/cping_version_local.txt'
        system(cp_cmd)
    else:
        cluster_ping(script_dir, user, time_string)
    return 1
