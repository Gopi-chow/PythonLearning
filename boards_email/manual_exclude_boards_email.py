""" Manual exclude file has list of excluded setups.
This script sends an email  with list of setups added to it"""

from email.mime.text import MIMEText
import json
import smtplib
from socket import gethostname
import email
import argparse
from email.mime.multipart import MIMEMultipart
from collections import OrderedDict

empty_spaces = " "
XSJ_PATH = "/home/xppc/burst/latest_burst/manual_exclude.json"
XHD_PATH = "/group/siv_burst/proj/latest_burst/manual_xhd_board_exclude.json"
host_location = str(gethostname())[0:3].upper()

parser = argparse.ArgumentParser(description="send excluded boards in a mail")
parser.add_argument("-to", help="Accepts user email ID",required=True)
parser.add_argument("-cc", help="Accepts user email's ID to mention in cc",required=False)

def send_email(location, exclude_json_path):
    """ To send mail
    Args:
        location(string): XHD or XSJ
        exclude_json_path(string): Path of manual exclude json file
    returns:
        None
    """
    html_font_style = 'style="font-size: 13px; font-family: calibri"'
    global msg_text
    global empty_spaces
    with open(exclude_json_path) as exclude_file:
        data = json.load(exclude_file,object_pairs_hook=OrderedDict)
        st = "project"
        text = "Hello BURST users, \n"
        text += "\nDetails of excluded boards: \n"
        message = '<!DOCTYPE html>\n'
        message += '<html>\n'
        message += '<style>\n'
        message += 'table, th, td { \n'
        message += 'border:1px solid black;\n'
        message += '}\n'
        message += '</style>\n'
        message += '<body>\n'
        text_html = "<p {}> {} </p>\n".format(html_font_style,
                                              text.replace('\n', '\n<br /> '))

        table_html = '<table style="width:100%">\n'
        table_html += '<tr><th>Project</th><th>Exclude boards</th></tr> '
        for each_board in data:
            boards = []
            if len(data[each_board]):
                boards.append(each_board)
                boards.append(str(data[each_board]))
                table_html += '<tr>'
                table_html += '  <td> {} <br /> </td>'.format(each_board)
                table_html += '  <td> {} </td>'.format(data[each_board])
                table_html += '  </tr>\n'
        table_html += '</table>\n'
    msage = "\r\nCheers,"
    msage += "\r\nThe BURST Team\r\n"
    msage_html = "<p {}> {} </p>\n".format(html_font_style,
                                           msage.replace('\n', '\n<br /> '))
    message = message + text_html + table_html + msage_html
    msg = MIMEText(message, 'html')
    msg["Subject"] = "Setups added to {}'s exclude list".format(location)
    msg["From"] = "burst-test@xilinx.com"
    msg["To"] = args.to
    msg["CC"] = args.cc
    try:
        with smtplib.SMTP("localhost") as s:
            try:
                s.send_message(msg)
            except smtplib.SMTPRecipientsRefused:
                print("WARN: Could not send email. Recipients refused.")
            except smtplib.SMTPHeloError:
                print("WARN: Could not send email. Server did not respond.")
            except smtplib.SMTPSenderRefused:
                print(("WARN: Could not send email. Server did not accept "
                       + "{} as a sender.").format(msg["From"]))
            except smtplib.SMTPDataError:
                print("WARN: Could not send email. "
                      + "Server responded with unexpected error.")
            except smtplib.SMTPNotSupportedError:
                print("WARN: Could not send email. "
                      + "SMTPUTF8 was given mail_options that are not supported.")
    except smtplib.SMTPConnectError:
        print("WARN: Could not conect to email server. No emails sent.")

args = parser.parse_args()
if host_location == "XSJ":
   send_email("xsj", XSJ_PATH)
elif host_location == "XHD":
   send_email("xhd", XHD_PATH)
