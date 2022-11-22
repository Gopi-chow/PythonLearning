import re
import os,fnmatch
import datetime
from prettytable import PrettyTable
import argparse

parser = argparse.ArgumentParser(
    description="Check BURST regression related setup issues",
    epilog="Queries Contact: burst_script_team@xilinx.com",
)

parser.add_argument(
    "-lp",
    "--logs_path",
    type=str,
    help="Accepts logs root path from user to analyze RTC",
    required=True,
)


def find_serial(pattern, path):
        result = []
        for root, dirs, files in os.walk(path):
            for name in files:
                if fnmatch.fnmatch(name, pattern):
                    result.append(os.path.join(root, name))
        return result


def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        if dirs:
            dir=dirs[0]
            if re.match(pattern,dir):
                result.append(os.path.join(root,dir))
    return result


def find_serial_time_stamp(file_name_ip):
    f=open(file_name_ip,"r")
    for line in f.readlines():
        if line.strip().startswith("The time is"):
            dt_from_log=line.rsplit("=")[1]
            dt_from_log=int(dt_from_log,16)
            serial_date_time = datetime.datetime.fromtimestamp(dt_from_log)
            return serial_date_time


def find_folder_time_stamp(folder_time_stamp):
    date=folder_time_stamp.split("_")[0]
    time=folder_time_stamp.split("_")[1]
    my_year=date[0:4]
    my_month=date[4:6]
    my_date=date[6:8]
    my_hour=time[0:2]
    my_min=time[2:4]
    folder_date_time = datetime.datetime(int(my_year), int(my_month), int(my_date), int(my_hour),int(my_min))
    return folder_date_time


def print_table(table_list):
    myTable = PrettyTable(table_list[0])
    myTable.field_names = table_list[0]
    myTable.align = "l"
    i = 0
    j = len(table_list)
    while (i < j):
        if (i != 0):
            myTable.add_row(table_list[i])
        i += 1
    print(str(myTable))
    print("\n")


args = parser.parse_args()
logs_root=os.path.abspath(args.logs_path)
print(logs_root)
mytable=[]
result_dict={}
result_dict["SERIAL_LOG"]="TIME DIFFERENCE IN SECONDS"
result_dict[""]=""
folders_data=find("\d\d\d\d\d\d\d\d_\d\d\d\d",logs_root)

for data in folders_data:
   serial = find_serial("*serial*.log", data)
   if not serial:
       continue
   serial_time_stamp = find_serial_time_stamp(serial[0])
   if not serial_time_stamp:
       continue
   name=data.rsplit("/",1)[1]
   folder_time_stamp=find_folder_time_stamp(name)
   diff=serial_time_stamp-folder_time_stamp
   diff=diff.total_seconds()
   result_dict[serial[0]]=diff

for key in result_dict:
    mytable.append((key+"*"+str(result_dict[key])).split("*"))

print_table(mytable)
