import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from validity import is_cmt_profile
from validity import is_exist_profile
from run_regression import EnvironmentSetup
from run_regression import parser
from pathlib import Path
import pytest


################################################################################
# Add required test fixures here


@pytest.fixture
def script_loc(request):
    """Return the directory of the currently running test script"""
    # uses .join instead of .dirname so we get a LocalPath object instead of
    # a string. LocalPath.join calls normpath for us when joining the path
    return request.fspath.join("..")


@pytest.fixture
def hostenv1(script_loc):
    """Return a sample hostenv object used in run_regression/run_burst"""
    parser.auto_regres=False
    parser.board_tag=None
    parser.burst_path=None
    parser.cmd_path=None
    parser.carbon_copy=None
    parser.copy_profile=False
    parser.no_database=False
    parser.dont_launch=False
    parser.email=None
    parser.force_read=None
    parser.knobs=False
    parser.list=False
    parser.logs_dir=None
    parser.message=False
    parser.no_build=True
    parser.no_monitor=False
    parser.no_update=True
    parser.profile=['release', 'release.profile']
    parser.read=None
    parser.run_time='1800'
    parser.time_out=None
    parser.toggle_exclude=False
    parser.update_exclude=False
    parser.retrig_fail=True
    parser.subset=False
    parser.python=False
    inst = EnvironmentSetup(parser)
    inst.burst_folder = str(script_loc.join('../../..'))
    inst.busg_path = Path(str(script_loc.join('../..')) + "/script_gen")
    inst.profile_dir = Path(str(script_loc.join('../..')) + "/run_burst/profile")
    inst.parser_file = Path(str(script_loc.join('../..')) + "/scripts/" + \
                                inst.parser_name)
    inst.script_dir = Path(str(script_loc.join('../..')) + "/run_burst")
    inst.version_file = Path(str(inst.script_dir) + '/cping_version_local.txt')
    return inst


################################################################################
# Add test for each functions and function exceptions here

def test_is_cmt_profile(hostenv1, script_loc):
    # Test for function returning one for all commented profile
    profile_path = script_loc.join("/test_data/all_cmt.profile")
    assert is_cmt_profile(hostenv1, profile_path) ==  1
    # Test for function returning zero for non all commented profile
    profile_path = script_loc.join("/test_data/mixed.profile")
    assert is_cmt_profile(hostenv1, profile_path) ==  0

def test_is_exist_profile(hostenv1, script_loc):
    # Tests to make sure the function checks profile in run_burst/profile
    profile = hostenv1.profile_list[0]
    expected_profile_path = script_loc.join("../profile/release.profile")
    assert is_exist_profile(hostenv1, profile) == expected_profile_path
    profile = hostenv1.profile_list[1]
    assert is_exist_profile(hostenv1, profile) == expected_profile_path
    # Test to make sure that  functions accepts full file path minus .profile
    profile = script_loc.join("/test_data/mixed")
    expected_profile_path = script_loc.join("/test_data/mixed.profile")
    assert is_exist_profile(hostenv1, profile) == expected_profile_path
    #  Test to make sure that a non existant file returns false
    profile = 'non_exitance'
    assert is_exist_profile(hostenv1, profile) == 0


################################################################################
