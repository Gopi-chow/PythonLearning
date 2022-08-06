from operator import itemgetter
import json,os

# PACKAGE_PARENT = "../run_burst"
# script_dir = os.path.dirname(
#     os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
# )
#
# print(os.getcwd())
# print(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
# print(script_dir)
# print(os.path.expanduser(__file__))

# with open("ex.json") as db_file_handle:
#     data = json.load(db_file_handle)
    # out_dict = {}
    # for in_dict in data:
    #     print(in_dict)
        # _sorted_items = sorted(in_dict.items(), key=itemgetter(0))
        # for key, value in _sorted_items:
        #     out_dict[str(key)] = str(value)

# print(data)
# print(data["burst"])

form = [
    {
        "keys": {
            "burst_elf": "burstarm64.elf",
            "burst_hw": "tenzing_es2_ps",
            "knobs": "",
            "preempt": "NO",
            "script_name": "tenzing_se1_a72_3ddr_bup"
        },
        "template_file": "parameters.txt"
    },
    {
        "keys": {
            "__SUB_TEMPLATE__spp_a72_ta_sel__": "yes",
            "__SUB_TEMPLATE__spp_r5_ta_sel__": "no",
            "__SUB_TEMPLATE__tenzing_pdi_images_dow__": "yes",
            "board_serial_num": "getsn",
            "com": "serial",
            "dwn_burst_wait": "500",
            "image_path": "/everest/set_vnc_bkup/vnc/s80/prod/results/burst/bup/ps/2022.1_int_0112_1/ps4_se1q_1mp_3ddr_Bx_2022_1/hwflow_project_1/project_1.runs/impl_1/project_1_wrapper.pdi",
            "proc": "a72",
            "rst_type": "rst -proc"
        },
        "template_file": "everest_es1.txt"
    },
    {
        "keys": {
            "__SUB_TEMPLATE__exit_protium__": "No",
            "__SUB_TEMPLATE__noc_reg_dump__": "Yes",
            "com": "serial",
            "inactv_t": "300",
            "preemption_off": "",
            "read_power": "readpower"
        },
        "template_file": "run_test.txt"
    }
]

# for i,k in enumerate(form):
#     print(i,k)
# print(enumerate(form))

dict1 ={
    "emp1": {
        "name": "Lisa",
        "designation": "programmer",
        "age": "34",
        "salary": "54000"
    },
    "_emp2": {
        "name": "Elis",
        "designation": "Trainee",
        "age": "24",
        "salary": "40000"
    },
}

dic_ordered = {}
for each_dic in dict1:
    max_key_len = max(map(len, dict1[each_dic]))
    print(max_key_len)
    # format_print = "{0:{max_key_len}}".format(each_dic,max_key_len=max_key_len)
    # print(format_print)
    for each_key in dict1[each_dic]:
        print(each_key)
        each_key_ = each_key
        space = " " * (max_key_len-len(each_key))
        each_key_ += space
        dic_ordered[each_key_] = dict1[each_dic][each_key]
print(dic_ordered)
out_file = open("myfile_write.json", "w")
json.dump(dic_ordered, out_file,indent=2,separators=(',', ': '),sort_keys=True)
out_file.close()