
# This is to parse a log file

import argparse
import os 
import sys
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument("-p","--path", help = "file path to write file")
parser.add_argument("-o", "--outputfile", help = "filename to get decoded data")
parser.add_argument("-i", "--inputfile", help = "filename to decode the data")
args = parser.parse_args()
burst_type={'0': ':Fixed','1':':INCR','2':':WRAP','3':':Reserved'}
burst_size={'0':':1B  ','1': ':2B  ','2':':4B  ','3':':8B  ','4':':16B ','5':':32B ','6':':64B ','7':':128B'}
prot={'0':':UpSDa','1': ':PSDa ','2':':UpNsDa','3':':UpNsIa','4':':UpSIa','5':':PSIa ','6':':UpSDa','7':':PNsIa '}
cache={'0':':NbNcNrNw','1': ':BNcNrNw ','2':':NbCNrNw ','3':':BCNrNw  ','4':':NbNcRNw ','5':':BNcRNw  ',
       '6':':NbCRNw  ','7':':BCRNw   ','8':':NbNcNrW ','9':':BNcNrW  ','a':':NbCNrW  ','b':':BCNrW   ','c':':NbNcRW  ','d':':BNcRW   ','e':':NbCRW   ','f':':BCRW    '}
offset_1 = defaultdict(lambda: 0)
offset_2 = defaultdict(lambda: 0)
offset_3 = defaultdict(lambda: 0)

def convert_hex_binary(value):
    hexadecimal = value
    end_length = len(hexadecimal) * 4
    hex_as_int = int(hexadecimal, 16)
    hex_as_binary = bin(hex_as_int)
    #padded_binary = hex_as_binary[2:].zfill(end_length)
    padded_binary = bin(int(value, 16))[2:].zfill(len(value)*4)
    return padded_binary

def calculate_offset(offset):

    print("Word Offset : +00")
    print("\n")
    offset0_val=get_value_offset_00(convert_hex_binary(offset[0]))
    print(offset0_val)
    print("\n")

    print("Word Offset : +01")
    print("\n")
    offset1_val=get_value_offset_01(convert_hex_binary(offset[1]))
    print(offset1_val)
    print("\n")

    print("Word Offset : +02")
    print("\n")
    offset2_val=get_value_offset_02(convert_hex_binary(offset[2]))
    print(offset2_val)
    print("\n")

    print("Word Offset : +03")
    print("\n")
    offset3_val=get_value_offset_03(convert_hex_binary(offset[3]))
    print(offset3_val)
    print("\n")



def get_value(data):
    return hex(int(data,2))[2:].zfill(len(data)//4)

def get_hex_value(data):
    return hex(int(data,2))[2:]

def get_value_offset_00(byteval):
    value = hex(int(byteval[-32:],2))[2:]
    bit_31_0_value = '{:0>10}'.format(value)
    return bit_31_0_value
    
def get_value_offset_01(byteval):
    bit_7_0_value = get_value(byteval[-8:])
    bit_9_8_value = get_value(byteval[-10:-8])
    bit_11_10_value = get_value(byteval[-12:-10])
    for i in range(4):
      if str(i) in bit_11_10_value:
        bit_11_10_value = bit_11_10_value + burst_type[str(i)]
    bit_value = get_value(byteval[-15:-12])
    for i in range(8):
      if str(i) in bit_value:
        bit_14_12_value = bit_value + burst_size[str(i)]
    bit_20_15_value = '{:0>2}'.format(get_hex_value(byteval[-21:-15]))
    bit_23_21_value = get_value(byteval[-24:-21])
    for i in range(8):
      if str(i) in bit_23_21_value:
         bit_23_21_value = bit_23_21_value + prot[str(i)]
    bit_27_24_value = get_value(byteval[-28:-24])
    bit_30_28_value = get_value(byteval[-31:-28])
    bit_31_value = get_value(byteval[-32])
    offset_1["len_0_7"] = bit_7_0_value
    offset_1["lock_9_8"] = bit_9_8_value
    offset_1["burst_11_10"] = bit_11_10_value
    offset_1["size_14_12"] = bit_14_12_value
    offset_1["id_20_15"] = bit_20_15_value
    offset_1["proc_23_21"] = bit_23_21_value
    offset_1["arb_delay_27_24"] = bit_27_24_value
    offset_1["last_addr_30_28"] = bit_30_28_value
    offset_1["valid_cmd"] = bit_31_value

def get_value_offset_02(byteval):
    bit_12_0_value = '{:0>4}'.format(get_hex_value(byteval[-13:]))
    bit_21_13_value = get_value(byteval[-22:-13])
    bit_30_22_value = get_value(byteval[-31:-22])
    bit_31_value = get_value(byteval[-32])
    offset_2["mstram_12_0"] = bit_12_0_value
    offset_2["other_depend_21_13"] = bit_21_13_value
    offset_2["my_depend_30_22"] = bit_30_22_value

def get_value_offset_03(byteval):
    bit_31_24_value = get_value(byteval[-32:-24])
    bit_23_20_value = get_value(byteval[-24:-20])
    bit_19_16_value = get_value(byteval[-20:-16])
    bit_15_8_value = get_value(byteval[-16:-8])
    value = get_value(byteval[-8:-4])
    for i in range(10):
      if str(i) in value :
         bit_7_4_value = value + cache[str(i)]
         break
    if 'a' in value:
       bit_7_4_value = value + cache['a']
    if 'b' in value:
       bit_7_4_value = value + cache['b']
    if 'c' in value:
       bit_7_4_value = value + cache['c']
    if 'd' in value:
       bit_7_4_value = value + cache['d']
    if 'e' in value:
       bit_7_4_value = value + cache['e']
    if 'f' in value:
       bit_7_4_value = value + cache['f']
         
    bit_3_value = get_value(byteval[-4])
    bit_2_0_value = get_value(byteval[-3:])

    offset_3["expected_resp_2_0"] = bit_2_0_value
    offset_3["cache_7_4"] = bit_7_4_value
    offset_3["user_15_8"] = bit_15_8_value
    offset_3["last_addr_23_20"] = bit_23_20_value
    offset_3["reserved_31_24"] = bit_31_24_value

def print_data(offset_dict):
    """ Returns string data.
    args:
      offset_dict (dict) : dictionary values which needs to written to file
    returns:
      string in expected format
    """

    offset_dict_backup = offset_dict.copy()
    print_str = ""
    # change this string according to requirement
    print_str = print_str + str(offset_dict.pop("id_20_15")) + "   " + str(offset_dict.pop(
        "len_0_7")) + "   " + str(offset_dict.pop("size_14_12")) + " " + str(offset_dict.pop(
        "burst_11_10")) + "  " + str(offset_dict.pop("lock_9_8")) + "     " + str(offset_dict.pop(
        "proc_23_21")) + "   " + str(offset_dict.pop("cache_7_4")) + " "

    print_remaining_part = offset_dict["arb_delay_27_24"] + "       " + offset_dict["last_addr_30_28"] + "        " + \
                           offset_dict["valid_cmd"] + "         " + offset_dict["mstram_12_0"] + "        " + \
                           offset_dict["other_depend_21_13"]  + "         " + offset_dict["my_depend_30_22"] + "      " + offset_dict["last_addr_23_20"] + "         " + offset_dict["user_15_8"] + "   " + offset_dict["expected_resp_2_0"]
    return print_str + print_remaining_part

def main():
    outputfile=args.outputfile if args.outputfile != None else "AXIEX_decoding.txt"
    filepath=args.path if args.path != None else os.getcwd()
    fullname = os.path.join(filepath,outputfile)

    output=open(fullname,'w')

    no_of_txn=0
    device_num=0
    if len(args.inputfile) == 35 and " " in args.inputfile:          
        offset = args.inputfile.split(" ")
        calculate_offset(offset)
        return 0
    # file1 = "" if args.inputfile == None else open(args.inputfile, 'r')
    file1 = open("AXIEX_decoding.txt", 'r')
    def decoding(data_cmd):
       for i in range(len(data_cmd)):
            cmd_value = data_cmd[i].split('[')[1].split(']')[0]
            output.write(cmd_value)
            output.write(" ")
            offset = data_cmd[i].split(',')[0].split('=')[1].split(' ')
            axi_address = get_value_offset_00(convert_hex_binary(offset[0]))
            get_value_offset_01(convert_hex_binary(offset[1]))
            get_value_offset_02(convert_hex_binary(offset[2]))
            get_value_offset_03(convert_hex_binary(offset[3]))
            offset = {**offset_1, **offset_2, **offset_3}
            string_to_write = axi_address + "   " + print_data(offset)
            output.write(string_to_write)
            output.write("\n")

    if file1 == "":
         sys.exit("Please give input file to decode")
    output.write("**************************AXIEX CMD DECODING*******************************\n")
    output.write("#Word Offset 00 AXI_address[31:0]")
    output.write("\n#Word Offset 01 Len[7:0]  Lock[9:8]")
    output.write("  Burst[11:10]")
    output.write("  Size[14:12]")
    output.write("  ID[20:15]")
    output.write("  Prot[23:21]")
    output.write("  Arb_delay[27:24]")
    output.write("  Last_addr[30:28]")
    output.write("  Valid_cmd[31]")
    output.write("\n#Burst - 0 - Fixed     Size - 0 - 1B       Prot - 0 - UpSda (Unprivileged Secure Data access)")
    output.write("\n#        1 - INCR             1 - 2B             1 - PSDa  (Privileged Secure Data access)")
    output.write("\n#        2 - WRAP             2 - 4B             2 - UpNsDa (Unprivileged Non-Secure Data access)")
    output.write("\n#        3 - Reserved         3 - 8B             3 - UpNsIa (Unprivileged Non-Secure Instruction access)")
    output.write("\n#                             4 - 16B            4 - UpSIa (Unprivileged Secure Instruction access)")
    output.write("\n#                             5 - 32B            5 - PSIa  (Privileged Secure Instruction access)")
    output.write("\n#                             6 - 64B            6 - UpSDa (Unprivileged Secure Data access)")
    output.write("\n#                             7 - 128B           7 - PNsI (Privileged Non-Secure Instruction access)")
    output.write("\n#Word Offset 02 Mstram_index[12:0]")
    output.write("  Other_depend[21:13]")
    output.write("  My_depend[30:22]")
    output.write("  Reserved[31]")
    output.write("\n#Word Offset 03 Expected_resp[2:0]")
    output.write("  Reserved[3]")
    output.write("  cache[7:4]")
    output.write("  user[15:8]")
    output.write("  Reserved[19:16]")
    output.write("  Last_addr[23:20]")
    output.write("  AX_address[39:32]")
    output.write("\n#Cache - 0 - NbNcNrNw (Non-bufferable Non-cacheable No-read No-writealloc)")
    output.write("\n#      - 1 - BNcNrNw (Bufferable Non-cacheable No-read No-writealloc)")
    output.write("\n#      - 2 - NbCNrNw (Non-Bufferable cacheable No-read No-writealloc)")
    output.write("\n#      - 3 - BCNrNw (Bufferable cacheable No-read No-writealloc)")
    output.write("\n#      - 4 - NbNcRNw (Non-Bufferable Non-cacheable read No-writealloc)")
    output.write("\n#      - 5 - BNcRNw (Bufferable Non cacheable read No-writealloc)")
    output.write("\n#      - 6 - NbCRNw (Non-Bufferable cacheable read No-writealloc)")
    output.write("\n#      - 7 - BCRNw (Bufferable cacheable read No-writealloc)")
    output.write("\n#      - 8 - NbNcNrW  (Non Bufferable Non cacheable no read writealloc)")
    output.write("\n#      - 9 - BNcNrW (Bufferable Non cacheable No read writealloc)")
    output.write("\n#Last two commands are not decoded\n")
    output.write("***************************************************************************\n")
    Lines = file1.readlines()
    count = 0
    one_dma = 0
    name = ''

    dma_devices = []
    for line in Lines:
        if "DMA Device[" in line:
            dma_devices.append(line.split(',')[0])

    if len(dma_devices) == 0:
        print("No DMA devices observed so No decoding required so exiting!!!")
        sys.exit(0)
    elif len(dma_devices) == 1:
        one_dma = 1
        print("Observed only one DMA device")
    for each_dma_device in dma_devices:
        global list_cmd
        list_cmd = []
        write_cmd = []
        current_dma_hit = 1
        for line in Lines:
            if not one_dma:
                if not count:
                    if dma_devices[1] in line:
                        break
                else:
                    if current_dma_hit and each_dma_device not in line:
                        continue
                    else:
                        current_dma_hit = 0
            if "DMA Device[" in line:
                output.write("\n")
                output.write(line.split(',')[0])
            if "base_addr" in line and "io" in line and " type" in line and "cpu_num" in line and "name:" in line and "subtype:" in line:
                name = (line.split('name:')[1]).split(',')[0]
                output.write(name)
                output.write(" , ")
        current_dma_hit = 1
        if 'AXIEX' in name:
            for line in Lines:
                if not one_dma:
                    if not count:
                        if dma_devices[1] in line:
                            break
                    else:
                        if current_dma_hit and each_dma_device not in line:
                            continue
                        else:
                            current_dma_hit = 0
                if 'Number of Read commands:' in line:
                    output.write("\n")
                    output.write(line)
                    output.write("\n")
                if 'Cmd[' in line and 'r_off:' in line and '00000000 00000000 00000000 00000000 0000' not in line:
                    output.write(line)
                    # global list_cmd
                    list_cmd.append(line)

        output.write(
            "\n*************************************************************************************************\n")
        output.write(
            "                                   Read Decoding                                                 ")
        output.write(
            "\n*************************************************************************************************\n")
        output.write(
            "\nCmd AXI_Addr     ID   Len  Size   Burst   lock  Prot      cache      Arb_dly Lst_addr Valid_cmd Mstam_index Other_dpnd My_dpnd Last_addr User Expected_resp\n")
        decoding(list_cmd)

        current_dma_hit = 1

        if 'AXIEX' in name:
            # for line in Lines:
            for line in Lines:
                if not one_dma:
                    if not count:
                        if dma_devices[1] in line:
                            break
                    else:
                        if current_dma_hit and each_dma_device not in line:
                            continue
                        else:
                            current_dma_hit = 0
                if 'Number of Write commands:' in line:
                    output.write("\n")
                    output.write(line)
                    output.write("\n")
                if 'Cmd[' in line and 'w_off:' in line and '00000000 00000000 00000000 00000000 0000' not in line:
                    output.write(line)
                    write_cmd.append(line)
        output.write(
            "\n*************************************************************************************************\n")
        output.write(
            "                                     Write Decoding                                                 ")
        output.write(
            "\n*************************************************************************************************\n")
        output.write(
            "\nCmd AXI_Addr     ID   Len  Size   Burst   lock  Prot      cache      Arb_dly Lst_addr Valid_cmd Mstam_index Other_dpnd My_dpnd Last_addr User Expected_resp\n")
        decoding(write_cmd)
        count += 1


if __name__ == "__main__":
    main()       
