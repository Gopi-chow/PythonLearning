from pathlib import Path
from os import system
from help import get_host_location
from subprocess import check_output
from subprocess import CalledProcessError
from subprocess import Popen
from subprocess import PIPE
from shlex import split
from sys import exit
from sys import argv
from os import getenv
from os import sep
import json
from monitor import Monitor
from monitor import systest_q_json
from random import randint
from help import ColourTextFormatter


def cluster_ping(script_dir, user_id, time_string):
    """ Function that does cluster ping and caches the results"""
    print("Updating setup files..")
    rand_str = str(randint(1, 10000))
    pfile_path = Path(script_dir + "/cping_" + time_string + rand_str + ".txt")
    bfile_path = Path(script_dir + "/boards.txt")
    sfile_path = Path(script_dir + "/valid_config.txt")
    version_file = Path(script_dir + '/cping_version_local.txt')
    vfile = open(str(version_file), 'w')
    vfile.seek(0)
    vfile.write(str(time_string)+'\n')
    vfile.close()
    print('Doing a cluster ping, ' + str(user_id) +
          ' please wait for  25 sec ..')
    if not (pfile_path.is_file()):
        cmd_string = '/proj/systest/bin/cluster-ping > ' + str(pfile_path)
        system(cmd_string)
    print('Processing the results')
    # Processing the cluster ping result to isolate list
    # of unique boards and board tags
    cping_host_offset = 0  # first few lines are different in XSJ
    if get_host_location() == 'XSJ':
        cping_host_offset = 3
    elif get_host_location() == 'XHD':
        cping_host_offset = 10
    bfile = open(str(bfile_path), 'w')
    sfile = open(str(sfile_path), 'w')
    line_count = 0
    with open(str(pfile_path), 'r') as pfile:
        for line in pfile:
            if (line != '\n') and (line != '-' * 83 + '\n') and (line != ''):
                temp = line.split(' ')
                temp2 = ''
                for j in temp:
                    if str(j) != '':
                        temp2 = temp2 + '#' + str(j)
                temp2 = temp2.rstrip('\n')
                temp3 = temp2.split('#')
                line_tag = line_has_tag(temp3)
                board_name = str(temp3[1])
                if str(temp3[1]) == 'Images':
                    break
                if line_count > cping_host_offset:
                    if str(temp3[4]) != 'Image':
                        if line_tag != '':
                            sfile.write(board_name + ' ' + line_tag + '\n')
                        else:
                            sfile.write(board_name + '\n')
                    else:
                        bfile.write(str(temp3[1]) + '\n')
            line_count += 1
    sfile.close()
    bfile.close()
    if pfile_path.is_file():
        cmd_string = 'rm ' + str(pfile_path)
        system(cmd_string)
    print("Update complete !\n")


def busg_generation(busg_path):
    """Function that generates all the alto busg cmd scripts"""
    busg_main_file = str(busg_path) + '/script_gen.py'
    busg_out = "BUSG cmd file generation: "
    if Path(busg_main_file).is_file():
        busg_cmd_string = busg_main_file + ' -db all'
        busg_cmd = split(busg_cmd_string)
        out_proc = Popen(busg_cmd, stdout=PIPE, stderr=PIPE)
        (out, err) = out_proc.communicate()
        busg_out = busg_out + out.decode('utf-8')
        if out_proc.returncode:
            print(busg_out + "\nFAILED!")
            exit(-1)
        else:
            print(busg_out)
    else:
        print('BUSG files missing: script_gen.py')
        exit(-1)
    return 0


def source_setup_warning():
    """ Function that gives warning to source setup scripts"""
    _shell = str(getenv('SHELL').split(sep)[2])
    if _shell == 'bash':
        _shell = 'sh'
    _script_path_full = (Path(argv[0])).resolve().absolute()
    _setup_path = str(_script_path_full).split('burst-scripts')[0]
    print("$XSLV is not set ! Please source the setup scripts")
    print('source '+_setup_path+'burst-scripts/setup.'+_shell)
    print('source '+_setup_path+'burst-scripts/toolchains.'+_shell)
    _busg_path = str(_setup_path.split('burst-scripts')[0])
    return _busg_path


def line_has_tag(tag_list):
    """ Function that returns board tag from a line list of 
    cluster ping result"""
    # Location of tag in cluster ping line ( starts counting from 0 )
    tag_location = 3
    tag = ''
    start = 0
    end = 0
    line_list = []
    for i, tag_item in enumerate(tag_list):
        if tag_item != '':
            line_list.append(tag_item)
    for i, line_item in enumerate(line_list):
            if str(line_item) == '[':
                start = i
            if str(line_item) == ']':
                end = i
                break
    if start != 0 and end != 0:
        for i in range(start, end+1):
            tag = tag + ' ' + line_list[i]
        # Avoiding run time tags
        if start == tag_location:
            return tag
        else:
            return ''
    else:
        return ''


def systest_job_mon(total_count, job_id, old_status, hostenv, method=True):
    """ Function that monitors systest queue of user
    Method = True => JSON file based monitoring
           = False => systest -q based monitoring
    """

    try:
        if method:
            monitor = Monitor()
            line = systest_q_json(monitor)
        else:
            line = check_output(['/proj/systest/bin/systest', '-q'])
    except CalledProcessError:
        # Maximum number of systest -q errors tolerate = 5
        if hostenv.error_count == 5:
            print("ERROR: Systest not responding! "
                  ": " + str(hostenv.error_count))
            exit(-1)
        else:
            hostenv.error_count = hostenv.error_count + 1
            print("Systest not responding : " + str(hostenv.error_count))
            return -1
    status = sysmon_parse(str(line), total_count, job_id,
                          old_status)
    hostenv.error_count = 0
    if status[0][3] == total_count:
        return [0, status[0], status[1]]
    else:
        return [1, status[0], status[1]]


def sysmon_parse(line, total_count, job_id_list, old_status):
    """ Function that parses the results of systest -q"""
    current_run_count = 0
    current_pend_count = 0
    # Initializing the status list to 0(ISSUED) and DONE(4)
    new_status = [0] * len(job_id_list)
    """
    REQUESTED, PENDING, RUNNING, COMPLETE NOW, COMPLETED BEFORE
    Status: 0 : ISSUED
            1 : PENDING
            2 : RUNNING
            3 : COMPLETED NOW
            4 : COMPLETED BEFORE
    """
    if 'No unfinished job found in queue <hwboard>' in line:
        test_status = [total_count, 0, 0, total_count]
        for item, _ in enumerate(new_status):
            if (old_status[item] == 3) or (old_status[item] == 4):
                new_status[item] = 4
            else:
                new_status[item] = 3
    else:
        line_list = line.split('\\n')
        for i in range(1, len(line_list)-1):
            sys_job_id = str(line_list[i]).split(' ')[0]
            if sys_job_id in job_id_list:
                if 'RUN' in str(line_list[i]):
                    current_run_count = current_run_count + 1
                    new_status[job_id_list.index(sys_job_id)] = 2
                elif 'PEND' in str(line_list[i]):
                    current_pend_count = current_pend_count + 1
                    new_status[job_id_list.index(sys_job_id)] = 1
        for item, _ in enumerate(job_id_list):
            if (old_status[item] == 3) or (old_status[item] == 4):
                new_status[item] = 4
            # Checking if the job is complete
            elif new_status[item] < old_status[item]:
                new_status[item] = 3
        total_done_count = new_status.count(4) + new_status.count(3)
        test_status = [total_count, current_pend_count,
                       current_run_count, total_done_count]
    return [test_status, new_status]


def print_systest_mon_status(test_status, curr_time):
    """ Function that prints systest monitor status"""
    time_now = str(curr_time.tm_hour) + ':' + str(curr_time.tm_min) + \
               ':' + str(curr_time.tm_sec)
    date_now = str(curr_time.tm_mon) \
        + '/' + str(curr_time.tm_mday)\
        + '/' + str(curr_time.tm_year)
    print('')
    print('DATE: ' + date_now + ' TIME: ' + time_now)
    print('-' * 45)
    print('| {:8} | {:8} | {:8} | {:8} |'
          .format('ISSUED', 'PENDING', 'RUNNING', 'COMPLETE'))
    print('-' * 45)
    print('| {:^8}   {:^8}   {:^8}   {:^8} |'.
          format(str(test_status[0]),
                 str(test_status[1]),
                 str(test_status[2]),
                 str(test_status[3])))
    print('-'*45)


def update_excludes_list(hostenv, ex_out_file, exclude_key):
    """ Function that updates the bad board file excludes.json"""
    settings_file = Path(str(hostenv.script_dir) + '/settings.json')
    if settings_file.is_file():
        try:
            with open(str(settings_file)) as data_file:
                _bad_names = json.load(data_file)[exclude_key]
        except IOError:
            print("WARN: Error opening " + str(settings_file))
            exit(-1)
    else:
        print("ERROR: settings.json file missing !")
        exit(-1)
    _bad_board_list = []
    _exclude_file = ex_out_file
    _setup_file = Path(hostenv.script_dir + "/valid_config.txt")
    if _exclude_file.is_file() and _setup_file.is_file():
        # Reading the setups to list all bad setups
        try:
            with open(str(_setup_file)) as in_file:
                for line in in_file:
                    # print(line.rsplit('\n'))
                    _line = line.rstrip('\n').split('  ')
                    _board_setup = _line[0]
                    if len(_line) == 2:
                        _board_tag = _line[1]
                        for bads in _bad_names:
                            if bads in _board_tag.lower():
                                _bad_board_list.append(str(_board_setup))
                                break
                in_file.close()
        except IOError:
            print("WARN: Error opening " + str(_setup_file))
            exit(-1)
        # Clearing the existing excludes file
        try:
            with open(str(_exclude_file)) as out_file:
                _exclude_data = json.load(out_file)
                for key in _exclude_data:
                    _exclude_data[key] = []
                out_file.close()
        except IOError:
            print("WARN: Error opening " + str(_exclude_file))
            exit(-1)
        # Creating the new bad boards list
        board_name_offset  = 0
        if len(_bad_board_list):
            for item in _bad_board_list:
                # Check if it exist in JSON keys
                if hostenv.host_location == 'XSJ':
                    board_name_offset = 0
                elif hostenv.host_location == 'XHD':
                    board_name_offset = 1
                else:
                    print('Only XSJ and XHD are supported!')
                    exit(-1)
                if "sl-" in item:
                    board_name_offset += 1
                _board = str(item).split('-')[board_name_offset]
                try:
                    _exclude_data[_board].append(str(item))
                # Boards that do not follow board-num/ xhd-board-num/
                # sl-board-num/ xhd-sl-board-num will not be auto-excluded
                except KeyError:
                    continue
        # Saving the new excludes list
        try:
            with open(str(_exclude_file), 'w') as out_file:
                json.dump(_exclude_data, out_file,
                          sort_keys=True, separators=(',', ': '),
                          indent=4)
                out_file.close()
        except IOError:
            print("WARN: Error opening " + str(_exclude_file))
            exit(-1)
    elif not _exclude_file.is_file():
        print("ERROR: File missing: {}!".format(str(_exclude_file)))
        exit(-1)
    else:
        print("ERROR: File missing: valid_config.txt")
        exit(-1)
    return 0


def create_exclude_file(hostenv, time_string=None):
    """
    Function that creates an empty excludes list file: excludes.json
    """
    _exclude_file1 = Path(hostenv.script_dir + "/exclude.json")
    _exclude_file2 = Path(hostenv.script_dir + "/exclude_preempt.json")
    _board_file = Path(hostenv.script_dir + "/boards.txt")
    _exclude_dict = {}
    if not _board_file.is_file():
        print(f"{ColourTextFormatter.YELLOW_COL} Missing boards.txt file so generating it {ColourTextFormatter.RESET}")
        cluster_ping(hostenv.script_dir, hostenv.user, time_string)
    try:
        with open(str(_board_file), 'r') as in_file:
            for line in in_file:
                _line = line.rstrip('\n')
                if not line.isspace():
                    _exclude_dict[str(_line)] = []
            in_file.close()
    except IOError:
        print("ERROR: Unable to open " + str(_board_file))
        exit(-1)
    # Saving the empty excludes list
    create_empty_exclude_file(_exclude_file1, _exclude_dict)
    create_empty_exclude_file(_exclude_file2, _exclude_dict)
    update_excludes_list(hostenv, _exclude_file1, 'exclude_tags')
    update_excludes_list(hostenv, _exclude_file2, 'exclude_tags_preempt')


def create_empty_exclude_file(_exclude_file, _exclude_dict):
    try:
        with open(str(_exclude_file), 'w') as out_file:
            json.dump(_exclude_dict, out_file,
                      sort_keys=True, separators=(',', ': '),
                      indent=4)
            out_file.close()
    except IOError:
        print("ERROR: Unable to open " + str(_exclude_file))
        exit(-1)


def update_json_with_timeout(base_dir, results, run_list, pend_list):
    """
    Function that updates the json to indicate that jobs were killed due to
    timeout in all profiles run in the regression
    """
    for job in results.job_list:
        log_base = job.profile
        job_id = job.jobid
        run_name = job.name
        if job_id in run_list:
            value = 'run-timeout'
        elif job_id in pend_list:
            value = 'pend-timeout'
        else:
            value = ''
        if value != '':
            recall_file = Path(str(base_dir) + '/' + log_base + '/' + run_name
                               + '/recall/' + run_name+'.json')
            if recall_file.is_file():
                try:
                    with open(str(recall_file), 'r+') as data_file:
                        json_dict = json.load(data_file)
                        json_dict['TestEnv']['timeout'] = value
                        data_file.seek(0)
                        json.dump(json_dict, data_file, sort_keys=True,
                                  separators=(',', ': '), indent=4)
                except IOError:
                    print("WARN: Error opening/writing to " + str(recall_file))
            else:
                print("WARN: " + run_name + ".json file missing !")
    return


def read_json(file_path):
    """
    Reads json file and returns the dictionary that it returns
    :param file_path: path of json file to be read
    :return: json dictionary
    """
    try:
        with open(file_path) as db_file_handle:
            try:
                data = json.load(db_file_handle)
                return data
            except ValueError:
                print("ERROR: Invalid JSON file: " + str(file_path))
                exit(-1)
            except TypeError:       # NoneType
                print("WARN: Reading " + str(file_path) + " returned TypeErr")
                return None
    except IOError:
        print("Unable to open : " + str(file_path))
        return None
    return None


def write_json(file_path, data, sort=True):
    """
    Writes the json data to the specified file
    :param file_path: file path to write to
    :param data: json dictionary data input
    :param sort: Decides wether or not to sort the dictionary before writing
    :return:
    """
    try:
        with open(file_path, 'w') as db_file_handle:
            json.dump(data, db_file_handle,
                      sort_keys=sort, separators=(',', ': '),
                      indent=4)
    except IOError:
        print("Unable to open : " + str(file_path))
    return None
