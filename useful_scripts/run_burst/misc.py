from operator import itemgetter
from pathlib import Path
from os import sep
from os import system
from sys import exit
import json
import re
from options import systest_map
from options import pre_silicon_boards
from options import empty_si_board_list
from options import pci_cluster_dictionary, pci_ep_map, pci_rc_map


def save_config(cfile_path, platform, burstconfig, hostenv, systest_cmd):
    """Function that saves the settings in flags to run_config file"""
    json_dict = {}
    with open(str(cfile_path), 'w') as cfile:
        json_dict[str(type(platform).__name__)] = str_dict(platform.__dict__)
        json_dict[str(type(burstconfig).__name__)] = \
            str_dict(burstconfig.__dict__)
        json_dict[str(type(hostenv).__name__)] = str_dict(hostenv.__dict__)
        json_dict['systest'] = systest_cmd
        json.dump(json_dict, cfile,
                  sort_keys=True, separators=(',', ': '),
                  indent=4)
        cfile.write('\n')
    cfile.close()
    _cp_cmd = 'cp -f '+str(cfile_path) + ' ' + \
              str(hostenv.current_dir) + '/recall.json'
    system(_cp_cmd)
    return 0


def str_dict(in_dict):
    """ Function that converts a dictionary to string based dictionary"""
    out_dict = {}
    _board_name = None
    _sorted_items = sorted(in_dict.items(), key=itemgetter(0))
    for key, value in _sorted_items:
        if key == 'board_num' and value:
            _board_name = value
    for key, value in _sorted_items:
        if key == 'board' and _board_name:
            value = _board_name
        elif key == 'board_num':
            continue
        out_dict[str(key)] = str(value)
    return out_dict


def pick_cmd_file(platform, burstconfig, hostenv):
    """Function that picks the cmd file based on flags, tries to generate
     it with BUSG if it doesnt exist and returns the path to the cmd file. """
    if (not platform.root_complex) and (platform.board or platform.board_num):  # Non PCIe
            # this block only works for boards with standard systest name
            # convention <boardname>-<number> ex.zc1751-15
            # if board name and number specified, number takes precedence
        if platform.board_num:
            _board = re.sub(r"-\d+", "", platform.board_num)  # removes -##
            if _board.startswith("sl-tenzing"):
                _board = 'tenzing'
        else:
            _board = platform.board
        if _board.startswith('xhd-'):
            _board = _board[4:]
        if _board.startswith('bf-'):
            _board = _board[3:]
        if platform.dc:
            _board = _board + "_" + platform.dc
        elif platform.board_revision:
            _board = _board + "_" + platform.board_revision.lower()
        _cmd_path = [burstconfig.gen, platform.si, _board]

        # This must be done in a certain order to get the correct file name
        if _board == 'ep108':
            _board = 'remus'
        _cmd_file = [_board, burstconfig.proc]
        if burstconfig.be:
            _cmd_file.append('be')
        if burstconfig.ospi_enable:
            _cmd_file.append('ospi')
        if burstconfig.ecc:
            _cmd_file.append('ecc')
        if burstconfig.dp:
            _cmd_file.append('dp')
        if burstconfig.clk:
            _cmd_file.append(burstconfig.clk)
        if platform.ddr_mode:
            _cmd_file.append(platform.ddr_mode)
        if burstconfig.bup_enable:
            _cmd_file.append('bup')
        if burstconfig.bupcoh_enable:
            _cmd_file.append('bupcoh')
        if burstconfig.tile:
            _cmd_file.append(burstconfig.tile)
    else:       # PCIe script
        _cmd_path = [burstconfig.gen, platform.si, 'pcie']
        _cmd_file = [platform.root_complex, 'rc']
        if platform.bridge_rc:
            _cmd_file.append(platform.bridge_rc)
        if platform.config_rc:
            _cmd_file.append(platform.config_rc)            
        _cmd_file.append(platform.end_point)
        _cmd_file.append('ep')
        if platform.bridge_ep:
            _cmd_file.append(platform.bridge_ep)
        if platform.cpm_mode:
            _cmd_file.append(platform.cpm_mode)
        if platform.ddr_mode:
            _cmd_file.append(platform.ddr_mode)
        if burstconfig.ospi_enable:
            _cmd_file.append('ospi')
        if burstconfig.be:
            _cmd_file.append('be')
        _cmd_file.append(platform.lane_count)
        if platform.pcie_gen:
            _cmd_file.append(platform.pcie_gen)
        _cmd_file.append(burstconfig.proc)
    if hostenv.preempt:
        _cmd_file.append('preempt')

    _cmd_path = "/" + "/".join(map(str, _cmd_path)) + "/"
    ext = ".py" if hostenv.is_python else ".cmd"
    _cmd_file = "_".join(map(str, _cmd_file)) + ext
    try:
        # Doubt - are we using bf2 folder for python
        if Path(hostenv.cmd_path).is_dir():
            if not ext == ".py":
              busg_cmdfile_path = hostenv.cmd_path + '/cmd_scripts' + _cmd_path \
                + _cmd_file
            else:
              busg_cmdfile_path = hostenv.cmd_path + '/cmd_scripts/bf2' + _cmd_path \
                + _cmd_file

    except TypeError:
        if not ext == ".py":
          busg_cmdfile_path = hostenv.burst_folder + \
            '/burst-scripts/cmd_scripts/' + _cmd_path + _cmd_file
        else:
          busg_cmdfile_path = hostenv.burst_folder + \
            '/burst-scripts/cmd_scripts/bf2' + _cmd_path + _cmd_file
    if not Path(busg_cmdfile_path).is_file():
        print('cmd path = ' + str(busg_cmdfile_path))
        print("The cmd file for the requested setup doesn't exist..")
        print("Try running run_burst.py --update busg")
        exit(-1)
    return busg_cmdfile_path


def create_run_name(hostenv, platform, pre_check_index=None):
    """ Function that creates a unique run name for a
    cmd based run"""
    _run_name = str(str(hostenv.cmd_path).split(sep)[-1])\
        .rstrip('.cmd').rstrip('.dat').rstrip('.py') + '_' + hostenv.local_time_std
    if platform.si:
        _run_name = str(platform.si)+'_'+_run_name
    if pre_check_index and hostenv.run_number != '':
        _run_name = '{:03d}_{}_{}'.format(hostenv.run_number,
                                          str(pre_check_index), _run_name)
    elif hostenv.run_number != '':
        _run_name = '{:03d}_{}'.format(hostenv.run_number, _run_name)
    elif pre_check_index:
        _run_name = '{}_{}'.format(_run_name, str(pre_check_index))
    return _run_name

def parse_knobs(knobs):
    """
    The purpose of this function is to split a knob string and return
    only the knob names.
    """
    knobs = knobs.replace("\n", "")
    knobs = knobs.replace(" ",  "")
    knobs_split = []
    if ";" in knobs:
        knobs = knobs.replace(",", ";")
        knobs_split = knobs.split(";")[:-1]
    elif "," in knobs:
        knobs = knobs.replace(";", ",")
        knobs_split = knobs.split(",")[:-1]
    output_knobs = {}
    for knob in knobs_split:
        knob_split = knob.split("=")
        output_knobs[knob_split[0]] = knob_split[1]
    return output_knobs

def check_default_knobs(roast_knobs_string, cmd_file):
    """
    The purpose of this function is to parse the cmd file for default knobs
    and see if any default knobs were passed in by the user. If they were,
    we drop the user passed knob to clean up the knobs being passed, as we
    shouldn't be passing double knobs, even if the default knob comes after
    user entered knobs. The function returns the cleaned knob string to be
    ran in systest command.
    """
    knobs_match = r'if run "[ \"$4\" == \"n\" ]" then'
    f = open(cmd_file, "r")
    knob_line = ""
    count = 0
    for line in f:
        if count == 1:
            result = re.search(r'\"(.*)\"', line)
            knob_line = result.group(1)
            break
        if knobs_match in line:
            count = 1
    if knob_line != "" and roast_knobs_string != "n":
        default_knobs = parse_knobs(knob_line)
        roast_knobs = parse_knobs(roast_knobs_string)
        for knob in default_knobs:
            if knob in roast_knobs.keys():
                print("WARN!! Removing %s due to conflict with default knob value in CMD script" % knob)
                roast_knobs.pop(knob, None)
        roast_knobs_output = ""
        if len(roast_knobs.keys()) == 0:
            return "n"
        for knob in roast_knobs.keys():
            roast_knobs_output += knob + "=" + roast_knobs[knob] + ","
        return roast_knobs_output
    elif knob_line == "" and roast_knobs_string != "n":
        return roast_knobs_string
    else:
        return "n"
def systest_cmd_create(platform, burstconfig, hostenv, cmd_file, exclude_bd):
    """ Function that created systest command for non pcie runs"""
    if hostenv.mode == 'interact':
        systest_cmd = '/proj/systest/bin/systest '
    elif hostenv.preempt:
        systest_cmd = '/proj/systest/bin/systest-submit-preemptable '
    else:
        systest_cmd = '/proj/systest/bin/systest -b '

    if platform.board_num:
        if 'palladium' in platform.board_num or 'haps' in platform.board_num:
            systest_cmd = systest_cmd + platform.board_num + \
                          ' -s ' + platform.session
        else:
            systest_cmd = systest_cmd + platform.board_num
        if exclude_bd != '':
            if platform.board_num in exclude_bd:
                print("WARN: Requested an excluded board")
        if hostenv.preempt:
            systest_cmd = systest_cmd + ' 1'
    else:
        tags_list = []
        if platform.board_tag:
            tags_list.append(platform.board_tag)
        elif platform.board:
            # Issue - two -b will be repeated if mode is not specified
            # Reproduce this
            run_line = f"-b {platform.board} -si {platform.si}"
            if platform.board_revision:
                run_line += f" --board_revision {platform.board_revision}"
            if platform.dc:
                run_line += f" --daughter_card {platform.dc}"
            if burstconfig.ospi_enable:
                run_line += " -ospi"
            tags_list = create_board_tag(run_line)
        else:      # pcie
            run_line = f"-rc {platform.root_complex.lower()} -ep {platform.end_point.lower()}"
            if platform.cpm_mode:
                run_line += f" --cpm_mode {platform.cpm_mode}"
            if platform.si:
                run_line += f" -si {platform.si}"
            tags_list = create_board_tag(run_line)

        if tags_list and platform.board:
            tag_string = ",".join(map(str, tags_list))
            systest_cmd = systest_cmd + f"'{platform.board}[{tag_string}]'"
            if 'palladium' in platform.board or 'haps' in platform.board:
                systest_cmd = systest_cmd + ' -s ' + platform.session
        elif platform.board:
            systest_cmd = systest_cmd + f"'{platform.board}'"
            if 'palladium' in platform.board or 'haps' in platform.board:
                systest_cmd = systest_cmd + ' -s ' + platform.session
        elif tags_list:  # pcie
            rc_key = platform.root_complex.lower() + "_rc"
            ep_key = platform.end_point.lower() + "_ep"
            pci_setup_key = f"{rc_key}_{ep_key}"
            cluster = pci_cluster_dictionary[pci_setup_key]
            tag_string = ",".join(map(str, tags_list))
            systest_cmd = systest_cmd + f"'{cluster}[{tag_string}]'"

        if hostenv.preempt:
            systest_cmd = systest_cmd + ' 1'

        if exclude_bd:
            exclude_bd = [x.strip('"\' ') for x in exclude_bd]
            exclude_bd = sorted(set(exclude_bd))
            systest_cmd = systest_cmd + ' -e \'' + \
                ','.join(map(str, exclude_bd)) + '\' '
    message = f"'{hostenv.message}'" if hostenv.message else ""
    tool_version = f"'{burstconfig.tool_version}'" if burstconfig.tool_version else ""
    toggle_reset = "n" if platform.board and 'haps' in platform.board else ""
    exec_command = f"{systest_cmd} '{cmd_file}' '{burstconfig.logs_dir}' '{burstconfig.burst_path}' "
    burstconfig.knobs = check_default_knobs(burstconfig.knobs, cmd_file)
    exec_command += f"'{burstconfig.run_time}' '{burstconfig.knobs}' {message} {tool_version} {toggle_reset}"
    if hostenv.is_python: # boarfarm 2.0 script
        exec_command = f"{systest_cmd} '{cmd_file}' \" "
        exec_command += f"-lp '{burstconfig.logs_dir}' "
        exec_command += f"-bp '{burstconfig.burst_path}' "
        exec_command += f"-rt '{burstconfig.run_time}' "
        if not hostenv.preempt:
            exec_command += f"-k '{burstconfig.knobs}' " if  burstconfig.knobs != "n" else ""
            exec_command += f"-msg {message} " if message else ""
            exec_command += f"-xsdb {tool_version} " if tool_version else ""
        else:
            if (burstconfig.knobs != "n") and message and tool_version:
               print(f"ERROR: Systest supports only for 9 arguments due to BF2-123, try removing -msg or -tv or -k arguments..")
               return
            elif (burstconfig.knobs != "n") and tool_version:
               print("ERROR: Systest supports only for 9 arguments due to BF2-123, try removing -tv or -k arguments..")
               return
            else:
                if tool_version:
                    exec_command += f"-xsdb {tool_version} "
                    print("WARN: message is dropped due to BF2-123")
                elif (burstconfig.knobs != "n"):
                    exec_command += f"-k '{burstconfig.knobs}' "
                    print("WARN: message is dropped due to BF2-123")
                else:
                    exec_command += f"-msg {message} " if message else ""
        exec_command += f"\""
    return exec_command


def create_board_tag(run_line):
    """Creates board tags for non-pcie setups(to be extended for pcie setups as well)

    Args:
        run_line (str): commad line arguments used to pick a tag

    Returns:
        [list]: board tags list
    """
    board = None
    rc_key = None
    silicon = None
    if "-b " in run_line:
        board = re.search(r"-b (\w+)", run_line).group(1)
    if "-si " in run_line:
        silicon = re.search(r"-si (\w+)", run_line).group(1)
    if "-rc " in run_line:
        rc_key = re.search(r"-rc (\w+)", run_line).group(1) + "_rc"
    if "-ep " in run_line:
        ep_key = re.search(r"-ep (\w+)", run_line).group(1) + "_ep"
    if "--board_revision" in run_line:
        board_revision = re.search(r"--board_revision ([a-zA-Z0-9_.]+)", run_line).group(1)
    else:
        board_revision = ""
    if "--daughter_card" in run_line:
        dc = re.search(r"--daughter_card (\w+)", run_line).group(1)
    else:
        dc = ""
    if "--cpm_mode" in run_line:
        cm = re.search(r"--cpm_mode (\w+)", run_line).group(1)
    else:
        cm = ""
    ospi_enable = True if "-ospi" in run_line else False

    # Take care of differences in BUSG/Systest naming
    if board_revision in systest_map:
        board_revision = systest_map[board_revision]

    if silicon in systest_map:
        silicon = systest_map[silicon]

    # Handling corner cases si version in some platforms
    if board == "protium" and "psx" in silicon:
        silicon = 'IPP_PSX'
    elif board == "protium":
        silicon = 'SPP_PS_ME_CPM'
    if board == "tenzing" and "es2" in silicon:
        silicon = "S80-prod"
    elif board == "vck190" and "es2" in silicon:
        silicon = "S80-prod"
    elif board in empty_si_board_list:
        silicon = ''

    flag = []
    if board:
        if board_revision:
            board_revision_list = board_revision.split(',')
            flag = flag + board_revision_list
        if silicon:
            flag.append(silicon)
        if dc:
            if dc != 'se1':
                flag.append(dc)
        if ospi_enable and "tenzing" in board:
            flag.append("ospi,reserved-burst")
        elif ospi_enable and board not in pre_silicon_boards:
            flag.append("ospi")
    elif rc_key: #pcie
        pci_setup_key = f"{rc_key}_{ep_key}"
        cluster = pci_cluster_dictionary[pci_setup_key]
        if cluster == "protium":
            flag.append("SPP_PS_ME_CPM")
        else:
            rc_tag = pci_rc_map[rc_key]
            ep_tag = pci_ep_map[ep_key]
            if ep_tag:
                flag.extend(ep_tag.split(","))
            if rc_tag:
                flag.extend(rc_tag.split(","))
            if cm == "aximmc1":
                flag.extend(["pcie-04"])
            if cluster in ["pcie_xa2785", "pcie_x86"] and \
                "es2" in silicon:
                flag.append("S-prod")
            if cluster in ["pcie_cpm"] and "es2" in silicon:
                flag.append("S80-prod")
        if flag:
            flag = sorted(set(flag))
    return sorted(flag)
