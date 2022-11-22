#####################################################################################################################
##                    CRON JOB to email setups added in  manual excluded file                                      ##
#####################################################################################################################
Authors       : Gopi Marvathi
Email         : gopim@xilinx.com
Script name   : manual_exclude_boards_email.py
Frequency     : Everyday
Machine XSJ   : xsjvsivcron
Script Owner  : burst_test
Default Path  : /home/xppc/burst/latest_burst/latest/burst/burst-scripts/cron_scripts/
Purpose       : To send the mail to the persons mentioned in To and CC arguments
                  Args:
                    To: mention mail ID to whom to send
	            CC: to CC people in the mail
Cron line Eg  : 40 14 * * * /home/xppc/burst/latest_burst/latest/burst/burst-scripts/cron_scripts/boards_email/
		manual_exclude_boards_email.py -to "burst_script_team@amd.com"
#####################################################################################################################
