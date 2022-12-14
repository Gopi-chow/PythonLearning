                                   README
################################################################################
            This script is used to generate all BURST cmd scripts
################################################################################
USER INSTRUCTIONS - Generating scripts using script_gen

Generate all cmd scripts supported by script_gen
./script_gen.py -db all

List all available databases (scripts are generated by iterating through the databases)
./script_gen.py -ld

Generate scripts from a specific database
./script_gen.py -db <database_name>

NOTE: The base folder for the generated cmd scripts is $BURST_SCRIPTS/cmd_scripts
or $PWD/cmd_scripts (if setup and toolchain script is not sourced)
-------------------------------------------------------------------------------------
CMD file naming and folder structure
-------------------------------------------------------------------------------------
The file name for the script should follow a standard convention so that cmd from
different users does not get get named the same and it to keep it consistent with BUSG naming.

The file name is created by joining together different parts that provide detail about
the test that is done by the CMD file. Each part is separated by an underscore ( _ ) and
a part is present in the name only if the part is relevant or present in the test done 
by the cmd file.

File Name
Syntax

 Non-pcie setups

        <board name as in board-farm>_<board_revison or daughter_card>_<BURST host processor>
		    _<big_endian>_<ecc>_<display_port>_<clock_profile>_<bup>_<pre_emptable>

         Eg: zc1751_dc1_a53_be_dp_sivdef_preempt, zc1751_dc1_a53_dp_sivdef,
		     zcu102_rev1.0_a53_be_ecc_av_preempt

PCIe-setups

       GENERAL: <root_complex>_rc_<bridge_rc>_<config_rc>_<end_point>_ep_<bridge_ep>_<cpm_mode>
			 _<ddr_mode>_<ospi>_<big_endian>_x<lane_count>_<processor>_<pre-emptable>

       PCIE LEGACY: <root_complex>_rc_<bridge_rc>_<end_point>_ep_<bridge_ep>_x<lane_count>
			  _<processor>_<pre-emptable>

       Eg: alto_rc_axipcie_k7_ep_axipxie_x4_a53_preempt, alto_rc_axipcie_k7_ep_axipxie_x1_r5

       Everest SPP and Silicon: <root_complex>_rc_<end_point>_ep_<cpm_mode>_x<lane_count>
				   _<processor>_<pre-emptable>

       Eg: hoodipp_rc_cpm_ep_sgdmaCSW_x4_a72, cpm_rc_cpm_ep_A0_be_x4_a72_preempt

       Note: root_complex, endpoint, lane_count, processor are mandatory

Folder Structure

The cmd files are organized in BUSG in a three level folder structure

    <project>/<silicon_version or emulation platform version>/ <board_name or pcie>
			_<board_revison or daughter_card>

        Eg: /alto/da7_prod/afx_b1156,  /alto/remus/ep108, /alto/da7_es2/zcu102_rev1.0,
	/alto/da7_prod/pcie, /everest/es1_cpm/pcie
______________________________________________________________________________

DEVELOPER INSTRUCTIONS - Adding, Removing setups (cmd scripts) to script_gen

-------------------------------------------------------------------------------

I. Main file components of the script

--------------------------------------------------------------------------------
1. template files = blueprints for creating the cmd scripts
2. database files = contain setup specific information of each cmd script
3. infile = File that specifies the type of script
4. outfile = script generated form, that user should add cmd specific details.
5. subtemplate files = contain workarounds/sequence of steps that differ from
			one setup/ cmd script to other.

1. template files
--------------------------------------------------------------------------------
template files are .txt located in /templates folder. User need to edit/add
these files only when an entire new type of script needs to be generated. It
contains a parametrized form of a cmd script, ie, blueprint. Although any part
of the template can be parametrized, it should be limited to the parts of the
cmd script that differ from one test cmd setup to the other.  (Eg. elf name,
processor) 
Note: A template file should contain at least one parameter.

2. database files
--------------------------------------------------------------------------------
database files are .json files in /database folder. User need not directly edit
these files but it needs to be edited using a sequence of commands and other
file edits for adding a new cmd file as part of the script_gen framework.
These are explained in section II of this README file.

database files store the specific values of each parameter that a template needs
to be meaningful cmd scripts. The cmd scripts are generated by adding the
parameter values from database to templates.
 
3. infile 
--------------------------------------------------------------------------------
infile is a .json file in the script base folder. User needs to edit this file
before adding a new cmd script to any database. It contains the information that
is used to generate the folder location and file name of the 'to be
generated/added to database' cmd file.

4. outfile
--------------------------------------------------------------------------------
outfile is a .json file in the script base folder. User needs to edit this file
before adding a new cmd script to any database file. Outfile is an intermediate
staging area for creating a entry to a database.

  4.1 Printing a template json entry to console
       ./script_gen.py --print_form/-pf <required template list separated by coma>
         Eg. ./script_gen.py -pf pele OR ./script_gen.py -pf pele,everest_protium
	
	The inputs that need to be edited by user will be specified as "INPUT" in
	the printed form. If the form is as expected it can be saved in outfile
	using create_form argument ( as in 4.2 ) and then transferred to any
	existing  database file.
	
  4.2 Creating a outfile/database entry.
       ./script_gen.py --create_form/-cf <required template list separated by coma>
         Eg. ./script_gen.py -cf pele OR ./script_gen.py -cf pele,everest

5. subtemplate files
 -------------------------------------------------------------------------------
subtemplate files are .txt files located in /templates/subtemplate folder.  
subtemplates contains chucks of instructions like some workarounds or calucations
that can be optionally inserted in the script. sub-templates cannot be parameterized.
They can be added as paramaterer to a templates using special syntax (below) and
can be specified wether to add it or not to be included in a script.

  5.1 Creating  a new subtemplate
	Create a .txt file with the steps/instructions/workarounds (as is)
	inside the /templates/subtemplate folder. Make sure to have the filename
	that make sense like a DT number for workaound or something that is
	indicative of what the instrutions in the subtemplate achieve.

  5.2 Including an existing subtemplate in template.
        Subtemplates can be added inside  a template with a special syntax. 
        Special syntax: <::__SUB_TEMPLATE__<subtemplate_name>__:=:<default_value>::>
        The <subtemplate_name> can be replaced by the subtamplate file name and
        the <default_value> can be either an yes or a no.
Note: The major difference between a paramater and a subtemplate is that
      parameters can have  single line values (not limited)
      and subtemplates are multi-line paraematers that can be set to 'yes'
      or a 'no' incicatiting weather to use it or not in a script.

--------------------------------------------------------------------------------

II. Adding a new cmd script to be generated using the script_gen script.

--------------------------------------------------------------------------------

 1 Adding a template (may not be necessary)
     Copy the existing script (if it cannot be generated using existing
     templates) to  /templates folder and save it as .txt file.
     Say the filename is "template1.txt"
 
 2 Adding parameters to a script (required only if step 1 is done)
     Any part of the script can be made a parameter by enclosing it inside the
     special syntax "<::parameter_name:=:default_value::>" or <::paramter_name::>
 
          Eg: Say the cmd script (template1.txt) contains the following
 
              if run "[ \"$2\" == \"n\" ]" then
			$BURST_ELF = "$PWD/burstarm64.elf"
		else
			$BURST_ELF = "$2/burstarm64.elf"
		endif
         And we need the burst elf (burstarm64.elf) to be a parameter.
         We can achieve this by replacing the above part of the script as follows.
 
		if run "[ \"$2\" == \"n\" ]" then
			$BURST_ELF = "$PWD/<::burst_elf::>"
		else
			$BURST_ELF = "$2/<::burst_elf::>"
		endif
	Now "burst_elf" becomes a parameter that can be specified to be
        different between the cmd files that is generated using this template.

        If a default value is required for a parameter, instead use
                if run "[ \"$2\" == \"n\" ]" then
			$BURST_ELF = "$PWD/<::burst_elf:=:burstarm64.elf>"
		else
			$BURST_ELF = "$2/<::burst_elf::>"
		endif
        The default value need to be only specified once in the template.

3 Adding workaronds/sequence of commands in the script.
      Adding workarounds can be done using sub-template files and can be 
      added in like a parameter.
      see the instructions above in subtemplate section step 5.2.
     Note: The major difference between a paramater and a subtemplate is that
     parameters can have  single line values (not limited)
     and subtemaplates are multi-line paraematers that can be set to yes or a no

 4 Edit the infile.json to indicate the type of script. 
      The setup can be pcie_setup/normal_setup. The infile contain fields that
      need to be edited to match the type of the script to be added to the
      database file. This information is used to generate the script name and the
      folder location for placing the script.
  
 5 Create the outfile ( as in 4.2 above )
      Here, ./script_gen.py -cf template1
  
          Note: A cmd script can be generated using multiple templates.
          Eg: ./script_gen.py -cf template1,template2
          The available templates can be listed as: ./script_gen.py -lt

 6 Edit the outfile to replace all "INPUT" in the file with meaningful values
      The parameters in the templates (here template1) will be added to the
      outfile.
          Here, the outfile will contain the following in it 
           "burst_elf" : "INPUT"
          It should be replaced as 
           burst_elf" : "burstarm64.elf"
		
	Note: script_location, script number and the name of the entry need 
	not be edited as it is handled by script_gen. If you feel the script
	name and location is wrong you will have do restart from step 4.
		
 7 Add the outfile content to the required database
      ./script_gen.py -db <database_name> -as/--add_setup
  
          Here, ./script_gen.py -db test -as
  
 8 List the existing setup names and setup numbers in a database to make sure
   new setup is added.
      ./script_gen.py -db <database_name> -ls/--list_setup
  
 9 Generate the script and test it
     ./script_gen.py -db <database_name>
 
 -------------------------------------------------------------------------------

 III. Removing an existing cmd script form database
 
 ------------------------------------------------------------------------------
   1. List the setups in the required database (same as II. 7 above) and note 
      the setup number that needs to be removed
         Here,
         ./script_gen.py -db test -ls
 
   2. Remove the setup
      ./script_gen.py -db <database_name> -rs/ --remove_setup

      Here,
      ./script_gen.py -db test -rs 1

Note: The setups will be renumbered alphabetically after a setup is added or 
removed.

--------------------------------------------------------------------------------

IV. Adding a new database

--------------------------------------------------------------------------------
  1. Create a empty json file inside the script_gen/databases folder.
	The file name of the .json file will be the new database name.
	File content : {}

  2. Check the database is recognized by listing all databases
         ./script_gen.py -ld

  3. New setups can be added to this as specified in step II.
--------------------------------------------------------------------------------


