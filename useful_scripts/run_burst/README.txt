################################################################################
#                        README for run_burst.py                               #
################################################################################
Confluence : http://confluence.xilinx.com/display/XPS/Running+BURST+using+scripts
--------------------------------------------------------------------------------
                   Launch BURST on XHD/XSJ Board Farm
--------------------------------------------------------------------------------
INPUT   : Command line flags or settings in [pwd]/recall.json (auto generated)
OUTPUT  : Runs BURST, saves logs and run settings in recall.json
--------------------------------------------------------------------------------
For example usage: run_burst.py -ex
--------------------------------------------------------------------------------
Flag Name                  : Default    : Description
--------------------------------------------------------------------------------
Group Flags (required flags marked with *)
--------------------------------------------------------------------------------
-b*   | --board            :            : Board select flag, expects a board
                                          name from board farm, run_burst will
                                          not infer any info such as -si or -dc
                                          from systest tag if board-number is
                                          entered. Eg: zc1751 or zc1751-22
-bt   | --board_tag        :            : Specify the complete board tag to 
                                          acquire a specific setup, user need
                                          to specify other flags like
                                          -si/-dc/-br to pick cmd file
-si*  | --silicon_version  :            : Silicon version/Emulation platform
                                          version flag, expects a
                                          silicon/emulation platform version
-p    | --processor        : a53        : Processor flag
                                          Options [a53, r5, mb or x86]
-nb   | --no_build         :            : BURST build flag, if present disables
                                          BURST build (default build enabled)
-bp   | --burst_path       : [pwd]      : Expect the path to the folder that
                                          contains the burst executable
-br*  | --board_revision   :            : Board revision flag, expects a
                                          board revision if it exists
                                          (do ls <board_name>) - required for
                                          zcu102 boards
-dc*  | --daughter_card    :            : Daughter card select flag [dc1-9] -
                                          required for zc1751 boards
-cp   | --cmd_path         :            : cmd/dat path flag, specify full
                                          cmd/dat script file path if it is
                                          not supported by BUSG
-clk  |                    : av         : Clock setup flag for da7_prod
                                          [av or sivdef]
-tl   | --tile             :            : ME tile selection [1x1, 3x3]
-cm   | --cpm_mode         :            : CPM Mode flag, expects
                                          [a0cci, a0noc, a1]
-dm   | --ddr_mode         :            : DDR Mode flag, expects
                                          [sddr, dddr, lpddr, sddrd2, 3ddr]
-cr   | --config_rc        :            : CPM RC Configuration flag, expects
                                          [cfg0, cfg4]
-bup  | --bup_enable       :            : Enable BUP [Everest only]
-dc   | --daughter_card    :            : Daughter card select flag [dc1-9]
-dp   |                    : no         : Display port enable flag
-ds   | --dont_save        :            : Disable saving recall file
-dl   | --dont_launch      :            : Flag that can be used to not launch a
                                          job. Useful for debugging run_burst.py
                                          issues.
-ep   | --end_point        :            : PCIe endpoint flag, expects the
                                          PCIe endpoint name
-e    | --exclude          :            : Specific board-numbers to exclude from
                                          a run, separated by coma(,). Boards
                                          with excluded tags will be excluded
                                          automatically. The tags for excluding
                                          can be found in settings.json file.
-ecc  |                    : no         : Error correction enable flag
-be   |                    :            : Enable big endian flag
-lc   | --lane_count       :            : PCIe GT lane count, [x1, x4, x8]
-lp   | --logs_dir         :            : Log Path, expects full folder path to
                                          the location to save the BURST logs
-k    | --knobs            :            : BURST knobs, expect BURST run knobs
                                          separated by coma(,)
                                          without space
-m    | --mode             : batch      : Mode flag, expects
                                          [interact, batch, regres]
-msg  | --message          :            : Message that can be passed to systest
-rc   | --root_complex     :            : PCIe root complex flag, expects the
                                          PCIe root complex name
-brc  | --bridge_rc        :            : Specify the rc side bridge
-bep  | --bridge_ep        :            : Specify the ep side bridge
-cm   | --cpm_mode         :            : Specify the mode in which CPM is running
-rn   | --run_number       :            : Run number associated with a BURST
                                          run, generally used during regression
-dm   | --ddr_mode         :            : Specify the DDR mode
-cr   | --config_rc        :            : Specify the configuration type in
                                          which CPM RC
-rt   | --run_time         : 1800       : Run time flag, run time in seconds
-pm   | --pre_empt         :            : Pre-emptable flag, expects number of
                                          pre-emptable jobs to launch.
                                          Not advisable to launch more than 1.
-pj   | --project          :            : project flag [pele, alto, everest,
                                          pele_manual, everest manual]
                                          default values for each board
                                          can be found in settings.json file.
-ss   | --subset           : None       : Pass a comma delimited list of run
                                          numbers in a profile to run
                                          (without space), this can be used to
                                          run a subset of runs in a profile.
-ospi | --ospi_enable      :            : Pass flag to use ospi enabled runs
                                          (everest only)
-bupcoh| --bupcoh_enable   :            : Pass flag to use coherent bup enabled
                                          runs (everest only)
-s    | --session          :            : Session for palladium runs
--------------------------------------------------------------------------------
Single Flags
--------------------------------------------------------------------------------
-ex   | --example          :            : Prints example commands
-h    | --help             :            : Prints the help for the script
-lb   | --list_boards      :            : List boards in board farm
-ls   | --list_setups      :            : Print board setups in board farm,
                                          expects a board name after the flag
-rl   | --recall_last      :            : Recall and run previous BURST run
-r    | --recall           :            : Recall any BURST run, expects a
                                          recall file as input.
-u    | --update           :            : Update the setup files,
                                          Options: [all, board, busg, exclude]
--------------------------------------------------------------------------------

################################################################################
#                        README for run_regression.py                          #
################################################################################
Confluence : http://confluence.xilinx.com/display/XPS/Running+BURST+using+scripts
--------------------------------------------------------------------------------
NOTE : profile with large number of runs is not recommended due to limited
memory, board-farm and network resources.
--------------------------------------------------------------------------------
                            List profiles
--------------------------------------------------------------------------------

run_regression.py -l or run_regression.py --list

--------------------------------------------------------------------------------
                            Read profiles
--------------------------------------------------------------------------------

run_regression.py -rd <profile_name>
or run_regression.py --read <profile_name>

--------------------------------------------------------------------------------
                            Optional Flags
--------------------------------------------------------------------------------

run_regression.py -nb  or run_regression.py --no_build
Disables BURST build step done before running regression.
If this flag is used all burst elfs have to exist in $PWD

run_regression.py -nu  or run_regression.py --no_update
Disables run_burt.py -update step done before running regression.

run_regression.py -msg "<systest message>"
Adds the message passes to each run in the profile provided there is no existing
message specified in the profile.

run_regression.py -k "<knobs>"
Adds or appends the command line knobs to all runs in a regression profile.
<knobs> format: knob1,knob2,knob3 ( no space and seperated by coma(,) )

run_regression.py -nm  or run_regression.py --no_monitor
Disables launching job monitor after launching the jobs in the regression.

run_regression.py -dl  or run_regression.py --dont_launch
Disables launching of jobs to run_burst, useful for debugging

run_regression.py -to <sec> or run_regression.py --time_out <sec>
Expects the timeout value to run a regression. Once the timeout value is
reached all jobs launched (pending and running) will be terminated.

run_regression.py -ndb or run_regression.py --no_database
When this flag is passed results are not stored in database

run_regression.py -rf or run_regression.py --retrig_fail
When this flag is passed, failed jobs will be rerun on a different setup. 
--------------------------------------------------------------------------------
                            Run Regression
--------------------------------------------------------------------------------

run_regression.py profile1 profile2 profile3 ...
    Eg: run_regression.py zc1751_da7_prod_1hr zc1751_da7_prod_smoke

Note: Even though you can run multiple regression profiles in a single run it
is advisable to run only single profile per run.
--------------------------------------------------------------------------------
                    Add new Regression profile
--------------------------------------------------------------------------------

Create <new_regression_profile_name>.profile file to
<BURST_SCRIPTS_MAIN_DIR>/run_burst/profile

One line in the regression profile corresponds to one BURST run.
A sample line in regression profile:
-b zc1751 -si da7_prod -dc dc1 -p a53 -clk av -rt 3600 -k Fail_after_test=0x100,

    This line corresponds to run BURST on zc1751-da7_prod-dc1 board
    with display port and ecc disabled on a53 using clock profile av for 1 hour
    or till test 0x100 (which ever comes first)

One line can correspond to multiple runs if -pm/ -pre-emptable run flag is set
to more than one. run_burst script launches multiple runs with -pm 1 option to
produce the same effect without causing any issue with logs structure that would
break the run_status. In effect, the -pm <number> will create multiple folders
for a single line in regression profile.

--------------------------------------------------------------------------------
           Remove one or more BURST runs from a regression profile
--------------------------------------------------------------------------------

Edit the corresponding regression profile file to comment out the required
line using a #

--------------------------------------------------------------------------------
                    Remove regression profile from list
--------------------------------------------------------------------------------

Rename the profile name to start with at #
in <BURST_SCRIPTS_MAIN_DIR>/run_burst/profile
    Eg: pcie.profile renamed to #pcie.profile
    will remove the pcie.profile from the list

--------------------------------------------------------------------------------

################################################################################
