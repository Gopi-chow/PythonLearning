import sys
from math import ceil
from subprocess import check_output
from subprocess import CalledProcessError
from subprocess import DEVNULL
from socket import gethostname
from os import sep
from pathlib import Path
from operator import itemgetter
import json
from options import pre_silicon_boards

class ColourTextFormatter:
    """
    Contains numerous escape sequences apply colour to text
    """
    # For error messages
    RED_COL = '\033[91m'
    # To reset back to original
    RESET = '\033[0m'
    # For warning messages
    YELLOW_COL = '\033[93m'
    # For info messages
    GREEN_COL = '\033[92m'

def print_boards(bfile_path):
    """Function that lists the available boards in board farm"""
    if bfile_path.is_file():
        with open(bfile_path, 'r') as board_file:
            bfile_line_count = len(board_file.readlines())
            board_file.seek(0)
            print('\n')
            for bfile_lc in range(ceil(bfile_line_count/4)):
                print('{:15} {:15} {:15} {:15}'.
                    format(board_file.readline().rstrip('\n'),
                            board_file.readline().rstrip('\n'),
                            board_file.readline().rstrip('\n'),
                            board_file.readline().rstrip('\n')))
    else:
        print('Missing setup file: ' + str(bfile_path))
        print('\nRun ' + sys.argv[0] + ' -u board' +
              ' to update setup files, then run ' + sys.argv[
            0] + ' -lb again to list the boards\n')
    print('\n')
    exit(0)


def recall_list(recall_path, parser, user_exclude):
    """ Function tht creates the arguments to pass to argpass on recall run"""
    # Creating the list of valid arguments accepted by parser
    valid_args = []
    for item in parser.__dict__['_actions']:
        valid_args = valid_args + item.option_strings
    _valid_args_list = [(x.lstrip('-')).lstrip('-') for x in valid_args]
    # Filtering the data from the recall json to recreate the args typed
    # by the user at initial run
    _rfile_path = Path(recall_path)
    _rfile_path = _rfile_path.resolve()
    _excludes = ['False', '', 'None']
    small_key_max = 3
    if _rfile_path.is_file():
        try:
            with open(str(_rfile_path), 'r') as rfile:
                _data = json.load(rfile)
                _args_list = recall_list_add_item(_data["BurstConfig"],
                                                  _excludes,
                                                  small_key_max,
                                                  _valid_args_list,
                                                  user_exclude)
                _args_list = _args_list + recall_list_add_item(
                                            _data["Platform"],
                                            _excludes,
                                            small_key_max,
                                            _valid_args_list, user_exclude)
                _args_list = _args_list + recall_list_add_item(_data["TestEnv"],
                                                               _excludes,
                                                               small_key_max,
                                                               _valid_args_list,
                                                               user_exclude)
                return _args_list

        except IOError:
            print("WARN: Error opening " + str(_rfile_path))
            sys.exit(-1)
    else:
        print("WARN: Recall file missing !")
        sys.exit(-1)


def recall_list_add_item(input_dict, excludes, small_key_max,
                         valid_args, user_exclude):
    """ Function that creates a list of valid arguments from
    a dictionary created from class object saved in recall json"""
    _args_line = []
    _sorted_x = sorted(input_dict.items(), key=itemgetter(0))
    for (key, value) in _sorted_x:
        if str(key) == 'exclude' and user_exclude:
            _args_line.append('--exclude')
            if value != "None":     # Remove [ ] brackets
                _args_line.append(str(value[1:-1]).rstrip(',') + ','
                                  + user_exclude)
            else:
                _args_line.append(user_exclude)
        elif str(value) not in excludes and str(key) in valid_args:
            if len(key) > small_key_max:
                _args_line.append('--' + str(key))
            else:
                _args_line.append('-' + str(key))
            if str(value) != 'True':
                if str(key) == 'exclude':
                    _args_line.append(str(value[1:-1]))
                else:
                    _args_line.append(str(value))
    return _args_line


def list_board_setups(board_name, sfile_path):
    """ Function that prints the available setups in board farm for
    a given board name"""
    if sfile_path.is_file():
        with open(str(sfile_path), 'r') as sfile:
            for line in sfile:
                if board_name in line:
                    print(line.strip())
    else:
        print('Missing setup file: boards.txt')
        print('\nRun ' + sys.argv[0] + ' -u boards' +
              ' to update setup files, then run ' +
              sys.argv[0] +
              ' -ls <board_name> again to list the boards\n')
    exit(0)


def print_example(script_name):
    """ Function that prints example usage commands"""
    script_name = str(script_name.split(sep)[-1])
    print('-' * 145)
    print('{:40}{}'.format('', 'Sample Command Syntax and Results'))
    print('-' * 145)
    print('Note: Order of inputs does not matter but'
          ' should contain all necessary '
          'inputs for a logical BURST run/Systest Launch')
    print('-' * 145)
    print('{:53}{}'.format('', 'Non PCIe'))
    print('-' * 145)
    print('Note: board, silicon_version/platform version(or board number)'
          ' are mandatory inputs')
    print('')
    print('Syntax : {} {} {} {}'
          .format(str(script_name),
                  '--board/-b', '--silicon_version/-si', '--mode/-m'))
    print('Example: {} {} {} {}'
          .format(str(script_name), '-b zc1751', '-si da7_prod', '-m interact'))
    print('Result : {} '
          .format('Builds BURST, Starts a systest'
                  ' interactive session in one of the '
                  'zc1751 da7_prod boards'))
    print('')
    print('Syntax : {} {} {}'
          .format(str(script_name), '--board/-b', '--mode/-m'))
    print('Example: {} {} {}'
          .format(str(script_name), '-b zc1751-22', '-m interact'))
    print('Result : {} '
          .format('Builds BURST, Starts a systest '
                  'interactive session on zc1751-22 board'))
    print('')
    print('Syntax : {} {} {}'
          .format(str(script_name),
                  '--board/-b', '--silicon_version/-si', '--data_card/-dc'))
    print('Example: {} {} {}'
          .format(str(script_name), '-b zc1751', '-si da7_es2', '-dc dc2'))
    print('Result : {} '
          .format('Builds BURST, Starts a systest on '
                  'in one of the zc1751-da7_es2-dc2 boards'))
    print('')
    print('Syntax : {} {} {} {}'
          .format(str(script_name),
                  '--board/-b', '--silicon_version/-si',
                  '--data_card/-dc'))
    print('Example: {} {} {} {}'
          .format(str(script_name),
                  '-b zc1751', '-si da7_prod', '-dc dc1'))
    print('Result : {} '
          .format('Builds and Runs BURST on one of the '
                  'zc1751-da7-prod-dc1 boards in a53 '
                  'processor in batch mode, '
                  'logs and recall file in /logs folder'))
    print('')
    print('Syntax : {} {} {} {} {} {} {}'
          .format(str(script_name),
                  '--board/-b', '--silicon_version/-si',
                  '--data_card/-dc', '--mode/-m', '--build/-bd',
                  '--processor/-p'))
    print('Example: {} {} {} {} {} {} {}'
          .format(str(script_name),
                  '-b zc1751', '-si da7_prod', '-dc dc1',
                  '-m batch', '--no_build', '-p r5'))
    print('Result : {} '
          .format('Runs previous built BURST on one of '
                  'the zc1751-da7-prod-dc1 boards in'
                  ' r5 processor in batch mode'))
    print('')
    print('Syntax : {} {} {} {} {} {} {} {}'
          .format(str(script_name),
                  '--board/-b', '--silicon_version/-si',
                  '--data_card/-dc', '--mode/-m', '--build/-bd',
                  '--processor/-p', '--exclude/-e'))
    print('Example: {} {} {} {} {} {} {} {}'
          .format(str(script_name),
                  '-b zc1751', '-si da7_prod', '-dc dc1',
                  '-m batch', '--no_build', '-p r5', '-e zc1751-12'))
    print('Result : {} '
          .format('Runs previous built BURST on one of '
                  'the zc1751-da7-prod-dc1 boards (excluding zc1751-12) in'
                  ' r5 processor in batch mode'))
    print('')
    print('-' * 145)
    print('{:55}{}'
          .format('', 'PCIe'))
    print('-' * 145)
    print('Note: root_complex,'
          ' end_point, platform_version/silicon_version(remus/da7_prod)'
          ' lane_count, processor are mandatory')
    print('')
    print('Syntax : {} {} {} {} {} {} {} '
          .format(str(script_name),
                  '--root_complex/-rc',
                  '--endpoint/-ep', '--lane_count/-lc',
                  '--mode/-m', '--silicon_version/-si', '--processor/-p'))
    print('Example: {} {} {} {} {} {} {} '
          .format(str(script_name),
                  '-rc k7', '-ep alto', '-lc x4',
                  '--mode batch', '-si da7_prod', '-p mb'))
    print('Result : {} '
          .format('Build burst, runs BURST on the k7_rc_alto_ep boards'
                  ' in microblaze processor in batch mode'))
    print('')
    print('-' * 145)
    print('{:55}{}'
          .format('', 'Generic'))
    print('-' * 145)
    print('Syntax : {} {} '
          .format(str(script_name), '--list_setups/-ls <board_name>'))
    print('Example: {} {} '
          .format(str(script_name), '-ls zcu102'))
    print('Result : {} '
          .format('Lists all zcu102 setups in board farm'))
    print('')
    print('Syntax : {} {} '
          .format(str(script_name), '--recall_last/-rl'))
    print('Example: {} {} '
          .format(str(script_name), '-rl'))
    print('Result : {} '
          .format('Build BURST, reruns your previous BURST run'))
    print('')
    print('Syntax : {} {} '
          .format(str(script_name), '--recall/-r <recall_file_name>'))
    print('Example: {} {} '
          .format(str(script_name), '-r logs/recall_da7_prod_201747_1830.json'))
    print('Result : {} '
          .format('Builds, BURST, reruns burst run that '
                  'you did on a da7_prod part on 6:30PM on 7th April 2017'))
    print('')
    print('-' * 145)
    return 0


def get_host_location():
    """ Function that determines the location of the host to decide
    which board farm to use"""
    host_name = str(gethostname())
    first_three = host_name[0:3]
    return str(first_three.upper())


def get_git_revision_hash(path):
    """ Function that reads the current git revision number
    used to prevent recalling runs with different BURST source code"""
    try:
        version_tag = check_output(['git', 'rev-parse', 'HEAD'], cwd=str(path),
                                   stderr=DEVNULL)
    except CalledProcessError:
        return 'unknown'
    revision_hash = str((str(version_tag).lstrip("b'")).split('\\')[0])
    branch_name = check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                               cwd=str(path))
    branch_name = str((str(branch_name).lstrip("b'")).split('\\')[0])
    git_status = str(check_output(['git', 'status', '-s'], cwd=str(path)))
    if (' M ' in git_status) or (' M' in git_status):
        revision_hash = revision_hash + ',dirty'
    else:
        revision_hash = revision_hash + ',clean'
    return branch_name + ',' + revision_hash


def get_git_revision_short_hash():
    """ Function that reads the current git revision number
        used to prevent recalling runs with different BURST source code"""
    version_tag = check_output(
        ['/home/xbrbbot/ssw_tools/RHEL59/x86_64/bin/git',
            'rev-parse', '--short', 'HEAD'])
    revision_hash = str((str(version_tag).lstrip("b'")).split('\\')[0])
    return revision_hash


def create_systest_message(args, cmd_name):
    """
    Function that creates the systest message
    """
    rt_int = int(args.run_time)
    rt_days = str(rt_int // 86400)
    rt_hours = str((rt_int % 86400) // 3600)
    rt_mts = str((rt_int % 3600) // 60)
    if args.message:
        msg = str(args.message)
    else:
        if  args.board and args.board in cmd_name:
            if args.board in pre_silicon_boards and args.project:
                cmd_msg=cmd_name.replace(args.board, args.project) 
            else:
                cmd_msg=cmd_name.replace(args.board+'_','')  
        else:
            cmd_msg=cmd_name
        msg=cmd_msg
        rt_days = f"{rt_days}d" if rt_days != "0" else ""
        rt_hours = f"{rt_hours}h" if rt_hours != "0" else ""
        rt_mts = f"{rt_mts}m" if rt_mts != "0" else ""
        time_list = filter(bool, [rt_days, rt_hours, rt_mts])
        msg = msg + f" {':'.join(time_list)}"
    msg=msg.replace("_"," ")
    msg_split_list = str(msg).split(' ')
    msg_list = []
    for item in msg_split_list:
        if item != '':
            msg_list.append(item)
    return '-'.join(map(str, msg_list))
