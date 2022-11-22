#!/tools/batonroot/rodin/engkits/lnx64/python-3.8.3_xslv/bin/python
"""
This module includes CPM5N_CDX_CSI_CFG_CSR register decoding methods, From CDO to Text and Text to CDO
"""
import re

import pandas as pd

from cpm5n_register import CSI_SRC_DST


def pcie_snk_npr_START_ADD_REG0(data):
    if "=" in data:
        pcie_snk_npr_start_add_sink_id = data.split("start_add_sink_id= ")[1].split(
            ","
        )[0]
        pcie_snk_npr_start_add_sink_id = hex_to_bin(pcie_snk_npr_start_add_sink_id)
        pcie_snk_npr_start_add_sink_id = format_data_length(
            pcie_snk_npr_start_add_sink_id, 2
        )
        pcie_snk_npr_start_add = data.split("start_add= ")[1]
        pcie_snk_npr_start_add = hex_to_bin(pcie_snk_npr_start_add)
        pcie_snk_npr_start_add = format_data_length(pcie_snk_npr_start_add, 18)
        data_value = pcie_snk_npr_start_add_sink_id + pcie_snk_npr_start_add
        data_value = format_hex_value(data_value)
        return data_value
    print("debug data is:" + data[-20:-18])
    s = (
            "threshold_mode= "
            + bin_to_hex(data[-23:-20])
            + "start_add_sink_id= "
            + bin_to_hex(data[-20:-18])
            + ", start_add= "
            + bin_to_hex(data[-18:])
    )
    data_values = bin_to_hex(data[-18:]) + "," + bin_to_hex(data[-20:-18]) + "," + bin_to_hex(data[-23:-20])
    return s, data_values


def pcie_snk_npr_END_ADD_REG0(data):
    if "=" in data:
        pcie_snk_npr_wr_add_sink_id = data.split("end_add_sink_id= ")[1].split(",")[0]
        pcie_snk_npr_wr_add_sink_id = hex_to_bin(pcie_snk_npr_wr_add_sink_id)
        pcie_snk_npr_wr_add_sink_id = format_data_length(pcie_snk_npr_wr_add_sink_id, 2)
        pcie_snk_npr_wr_add = data.split("end_add= ")[1]
        pcie_snk_npr_wr_add = hex_to_bin(pcie_snk_npr_wr_add)
        pcie_snk_npr_wr_add = format_data_length(pcie_snk_npr_wr_add, 18)
        data_value = pcie_snk_npr_wr_add_sink_id + pcie_snk_npr_wr_add
        data_value = format_hex_value(data_value)
        return data_value
    s = (
            "end_add_sink_id= "
            + bin_to_hex(data[-20:-18])
            + ", end_add= "
            + bin_to_hex(data[-18:])
    )
    data_val = bin_to_hex(data[-18:]) + "," + bin_to_hex(data[-20:-18])
    return s, data_val


def pcie_snk_npr_WR_PTR_REG0(data):
    if "=" in data:
        pcie_snk_npr_wr_add_sink_id = data.split("wr_add_sink_id= ")[1].split(",")[0]
        pcie_snk_npr_wr_add_sink_id = hex_to_bin(pcie_snk_npr_wr_add_sink_id)
        pcie_snk_npr_wr_add_sink_id = format_data_length(pcie_snk_npr_wr_add_sink_id, 2)
        pcie_snk_npr_wr_add = data.split("wr_add= ")[1]
        pcie_snk_npr_wr_add = hex_to_bin(pcie_snk_npr_wr_add)
        pcie_snk_npr_wr_add = format_data_length(pcie_snk_npr_wr_add, 18)
        data_value = pcie_snk_npr_wr_add_sink_id + pcie_snk_npr_wr_add
        data_value = format_hex_value(data_value)
        return data_value
    s = (
            "wr_add_sink_id= "
            + bin_to_hex(data[-20:-18])
            + ", wr_add= "
            + bin_to_hex(data[-18:])
    )
    data_values = bin_to_hex(data[-18:]) + "," + bin_to_hex(data[-20:-18])
    return s, data_values


def pcie_snk_npr_RD_PTR_REG0(data):
    if "=" in data:
        add_sink_id = data.split("rd_add_sink_id= ")[1].split(",")[0]
        add_sink_id = hex_to_bin(add_sink_id)
        add_sink_id = format_data_length(add_sink_id, 2)
        wr_add = data.split("rd_add= ")[1]
        wr_add = hex_to_bin(wr_add)
        wr_add = format_data_length(wr_add, 18)
        data_value = add_sink_id + wr_add
        data_value = format_hex_value(data_value)
        return data_value
    s = (
            "rd_add_sink_id= "
            + bin_to_hex(data[-20:-18])
            + ", rd_add= "
            + bin_to_hex(data[-18:])
    )
    data_val = bin_to_hex(data[-18:]) + "," + bin_to_hex(data[-20:-18])
    return s, data_val


def pcie_snk_npr_JOB_SIZE_REG0(data):
    if "=" in data:
        JOB_SIZE_REG0 = data.split("curr_jb_seg= ")[1].split(",")[0]
        JOB_SIZE_REG0 = hex_to_bin(JOB_SIZE_REG0)
        JOB_SIZE_REG0 = format_data_length(JOB_SIZE_REG0, 10)
        curr_jb_sz = data.split("curr_jb_sz= ")[1].split(",")[0]
        curr_jb_sz = hex_to_bin(curr_jb_sz)
        curr_jb_sz = format_data_length(curr_jb_sz, 11)
        prog_jb_sz = data.split("prog_jb_sz= ")[1]
        prog_jb_sz = hex_to_bin(prog_jb_sz)
        prog_jb_sz = format_data_length(prog_jb_sz, 11)
        data_value = JOB_SIZE_REG0 + curr_jb_sz + prog_jb_sz
        data_value = format_hex_value(data_value)
        return data_value
    s = (
            "curr_jb_seg= "
            + bin_to_hex(data[-32:-22])
            + ", curr_jb_sz= "
            + bin_to_hex(data[-22:-11])
            + ", prog_jb_sz= "
            + bin_to_hex(data[-11:])
    )
    return s, bin_to_hex(data[-11:]) + "," + bin_to_hex(data[-22:-11]) + "," + bin_to_hex(data[-32:-22])


def pcie_snk_npr_TMR_VAL_REG0(data):
    if "=" in data:
        timer_val = data.split("timer_val= ")[1]
        timer_val = hex_to_bin(timer_val)
        timer_val = format_data_length(timer_val, 11)
        data_value = timer_val
        data_value = format_hex_value(data_value)
        return data_value
    s = "timer_val= " + bin_to_hex(data[-10:])
    return s, bin_to_hex(data[-10:])


def pcie_snk_npr_TMR_SNST_REG0(data):
    if "=" in data:
        tmr_seg = data.split("tmr_seg= ")[1].split(",")[0]
        tmr_seg = hex_to_bin(tmr_seg)
        tmr_seg = format_data_length(tmr_seg, 3)
        tmr_armed = data.split("tmr_armed= ")[1].split(",")[0]
        tmr_armed = hex_to_bin(tmr_armed)
        tmr_snp_val = data.split("tmr_snp_val= ")[1]
        tmr_snp_val = hex_to_bin(tmr_snp_val)
        tmr_snp_val = format_data_length(tmr_snp_val, 20)
        data_value = tmr_seg + tmr_armed + tmr_snp_val
        data_value = format_hex_value(data_value)
        return data_value
    s = (
            "txn_on= "
            + bin_to_hex(data[-26])
            + "tmr_exp= "
            + bin_to_hex(data[-25])
            + "tmr_seg= "
            + bin_to_hex(data[-24:-21])
            + ", tmr_armed= "
            + bin_to_hex(data[-21])
            + ", tmr_snp_val= "
            + bin_to_hex(data[-20:])
    )
    return s, bin_to_hex(data[-24:-21]) + "," + bin_to_hex(data[-21]) + "," + bin_to_hex(data[-20:]) + "," + bin_to_hex(
        data[-26]) + "," + bin_to_hex(data[-25])


def pcie_snk_npr_GBL_BUF_ID0(data):
    if "=" in data:
        pcie_snk_npr_gbuf_sink_id = data.split("gbuf_sink_id= ")[1].split(",")[0]
        pcie_snk_npr_gbuf_sink_id = hex_to_bin(pcie_snk_npr_gbuf_sink_id)
        pcie_snk_npr_gbuf_sink_id = format_data_length(pcie_snk_npr_gbuf_sink_id, 2)
        pcie_snk_npr_gbuf_id = data.split("gbuf_id= ")[1]
        pcie_snk_npr_gbuf_id = hex_to_bin(pcie_snk_npr_gbuf_id)
        pcie_snk_npr_tmr_snp_val = format_data_length(pcie_snk_npr_gbuf_id, 9)
        data_value = pcie_snk_npr_gbuf_sink_id + pcie_snk_npr_tmr_snp_val
        data_value = format_hex_value(data_value)
        return data_value
    s = (
            "gbuf_sink_id= "
            + bin_to_hex(data[-11:-9])
            + ", gbuf_id= "
            + bin_to_hex(data[-9:])
    )
    return s, bin_to_hex(data[-9:]) + "," + bin_to_hex(data[-11:-9])


def pcie_snk_npr_SEQ_CNT_REG0(data):
    if "=" in data:
        src_local_cnt_id = data.split("src_local_cnt_id= ")[1].split(",")[0]
        src_local_cnt_id = hex_to_bin(src_local_cnt_id)
        src_local_cnt_id = format_data_length(src_local_cnt_id, 8)
        cmpl_cnt_id = data.split("npr_cmpl_cnt_id= ")[1].split(",")[0]
        cmpl_cnt_id = hex_to_bin(cmpl_cnt_id)
        cmpl_cnt_id = format_data_length(cmpl_cnt_id, 8)
        pr_cnt_id = data.split("pr_cnt_id= ")[1]
        pr_cnt_id = hex_to_bin(pr_cnt_id)
        pr_cnt_id = format_data_length(pr_cnt_id, 8)
        data_value = src_local_cnt_id + cmpl_cnt_id + pr_cnt_id
        data_value = format_hex_value(data_value)
        return data_value
    s = (
            "src_local_cnt_id= "
            + bin_to_hex(data[-23:-16])
            + ", npr_cmpl_cnt_id= "
            + bin_to_hex(data[-16:-8])
            + ", pr_cnt_id= "
            + bin_to_hex(data[-8:])
    )
    return s, bin_to_hex(data[-8:]) + "," + bin_to_hex(data[-16:-8]) + "," + bin_to_hex(data[-23:-16])


def pcie_snk_npr_CAP_MAP_REG0(data):
    if "=" in data:
        ctxt_prog_done = data.split("ctxt_prog_done= ")[1].split(",")[0]
        ctxt_prog_done = hex_to_bin(ctxt_prog_done)
        is_npr = data.split("is_npr= ")[1].split(",")[0]
        is_npr = hex_to_bin(is_npr)
        is_managed = data.split("is_managed= ")[1].split(",")[0]
        is_managed = hex_to_bin(is_managed)
        csched_dst_id = data.split("csched_dst_id= ")[1].split(",")[0]
        csched_dst_id = hex_to_bin(csched_dst_id)
        csched_dst_id = format_data_length(csched_dst_id, 8)
        csi_vc_id = data.split("csi_vc_id= ")[1].split(",")[0]
        csi_vc_id = hex_to_bin(csi_vc_id)
        csi_vc_id = format_data_length(csi_vc_id, 8)
        csi_src_id = data.split("csi_src_id= ")[1]
        csi_src_id = hex_to_bin(csi_src_id)
        csi_src_id = format_data_length(csi_src_id, 8)
        data_value = (
                ctxt_prog_done
                + "00000"
                + is_npr
                + is_managed
                + csched_dst_id
                + csi_vc_id
                + csi_src_id
        )
        data_value = format_hex_value(data_value)
        return data_value
    print("data in ctxt prog is:" + data)
    print(data)
    s = (
            "ctxt_prog_done= "
            + bin_to_hex(data[-32])
            + ", is_npr= "
            + bin_to_hex(data[-26])
            + ", is_managed= "
            + bin_to_hex(data[-25])
            + ", csched_dst_id= "
            + bin_to_hex(data[-24:-16])
            + ", csi_vc_id= "
            + bin_to_hex(data[-16:-8])
            + ", csi_src_id= "
            + bin_to_hex(data[-8:])
    )
    return s, bin_to_hex(data[-8:]) + "," + bin_to_hex(data[-16:-8]) + "," + bin_to_hex(
        data[-24:-16]) + "," + bin_to_hex(data[-25]) + "," + bin_to_hex(data[-26]) + "," + bin_to_hex(data[-32])


def pcie_snk_npr_RSLT_NPR_SIZE0(data):
    if "=" in data:
        rslt_cmpl_sz_npr = data.split("rslt_cmpl_sz_npr= ")[1]
        rslt_cmpl_sz_npr = hex_to_bin(rslt_cmpl_sz_npr)
        rslt_cmpl_sz_npr = format_data_length(rslt_cmpl_sz_npr, 17)
        data_value = rslt_cmpl_sz_npr
        data_value = format_hex_value(data_value)
        return data_value
    s = "rslt_cmpl_sz_npr= " + bin_to_hex(data[-17:])
    return s, bin_to_hex(data[-17:])


def pcie_snk_npr_JOB_LEN_AOFF0(data):
    if "=" in data:
        job_buf_end_addr = data.split("job_buf_end_addr= ")[1].split(",")[0]
        job_buf_end_addr = hex_to_bin(job_buf_end_addr)
        job_buf_end_addr = format_data_length(job_buf_end_addr, 8)
        job_buf_start_addr = data.split("job_buf_start_addr= ")[1]
        job_buf_start_addr = hex_to_bin(job_buf_start_addr)
        job_buf_start_addr = format_data_length(job_buf_start_addr, 11)
        data_value = job_buf_end_addr + "00000" + job_buf_start_addr
        data_value = format_hex_value(data_value)
        return data_value
    s = (
            "job_buf_end_addr= "
            + bin_to_hex(data[-24:-16])
            + ", job_buf_start_addr= "
            + bin_to_hex(data[-11:])
    )
    return s, bin_to_hex(data[-11:]) + "," + bin_to_hex(data[-24:-16])


def pcie_snk_npr_JOB_LEN_PTR0(data):
    if "=" in data:
        pcie_snk_npr_job_buf_read_addr = data.split("job_buf_read_addr= ")[1].split(
            ","
        )[0]
        pcie_snk_npr_job_buf_read_addr = hex_to_bin(pcie_snk_npr_job_buf_read_addr)
        pcie_snk_npr_job_buf_read_addr = format_data_length(
            pcie_snk_npr_job_buf_read_addr, 8
        )
        pcie_snk_npr_job_buf_write_addr = data.split("job_buf_write_addr= ")[1]
        pcie_snk_npr_job_buf_write_addr = hex_to_bin(pcie_snk_npr_job_buf_write_addr)
        pcie_snk_npr_job_buf_write_addr = format_data_length(
            pcie_snk_npr_job_buf_write_addr, 11
        )
        data_value = (
                pcie_snk_npr_job_buf_read_addr + "00000" + pcie_snk_npr_job_buf_write_addr
        )
        data_value = format_hex_value(data_value)
        return data_value
    s = (
            "job_buf_read_addr= "
            + bin_to_hex(data[-24:-16])
            + ", job_buf_write_addr= "
            + bin_to_hex(data[-11:])
    )
    return s, bin_to_hex(data[-11:]) + "," + bin_to_hex(data[-24:-16])


def pcie_snk_npr_SINK_BUF_FILL0(data):
    if "=" in data:
        pcie_snk_npr_max_fill_level = data.split("max_fill_level= ")[1].split(",")[0]
        pcie_snk_npr_max_fill_level = hex_to_bin(pcie_snk_npr_max_fill_level)
        pcie_snk_npr_max_fill_level = format_data_length(
            pcie_snk_npr_max_fill_level, 16
        )
        pcie_snk_npr_job_buf_write_addr = data.split("job_buf_write_addr= ")[1]
        pcie_snk_npr_job_buf_write_addr = hex_to_bin(pcie_snk_npr_job_buf_write_addr)
        pcie_snk_npr_job_buf_write_addr = format_data_length(
            pcie_snk_npr_job_buf_write_addr, 16
        )
        data_value = pcie_snk_npr_max_fill_level + pcie_snk_npr_job_buf_write_addr
        data_value = format_hex_value(data_value)
        return data_value
    s = (
            "max_fill_level= "
            + bin_to_hex(data[-32:-16])
            + ", curr_fill_level= "
            + bin_to_hex(data[-16:])
    )
    return s, bin_to_hex(data[-16:]) + "," + bin_to_hex(data[-32:-16])


def pcie_snk_npr_READ_GOVERNER0(data):
    if "=" in data:
        pcie_snk_npr_max_num_out = data.split("max_num_out= ")[1].split(",")[0]
        pcie_snk_npr_max_num_out = hex_to_bin(pcie_snk_npr_max_num_out)
        pcie_snk_npr_max_num_out = format_data_length(pcie_snk_npr_max_num_out, 12)
        pcie_snk_npr_max_cmpl_out = data.split("max_cmpl_out= ")[1]
        pcie_snk_npr_max_cmpl_out = hex_to_bin(pcie_snk_npr_max_cmpl_out)
        pcie_snk_npr_max_cmpl_out = format_data_length(pcie_snk_npr_max_cmpl_out, 17)
        data_value = pcie_snk_npr_max_num_out + pcie_snk_npr_max_cmpl_out
        data_value = format_hex_value(data_value)
        return data_value
    s = (
            "max_num_out= "
            + bin_to_hex(data[-28:-17])
            + ", max_cmpl_out= "
            + bin_to_hex(data[-17:])
    )
    return s


def bin_to_hex(data):
    """Convert binary to hex"""
    if not data:
        return "0x00"
    return hex(int(data, 2))


def hex_to_bin(data):
    """Hexadecimal to binary conversion"""
    return bin(int(data, 16)).replace("0b", "")


def format_data_length(data, data_len):
    """Format binary values in particular length"""
    return data if len(data) == data_len else (data_len - len(data)) * "0" + data


def format_hex_value(data_value):
    """Format passed data value in 0x00000000 format"""
    data_value = hex(int(data_value, 2))
    data_value = (
        data_value
        if len(data_value) == 10
        else "0x" + (10 - len(data_value)) * "0" + data_value.replace("0x", "")
    )
    return data_value


def convert_hex_binary(value):
    """Convert Hex to binary"""
    print("converting from hex to binary")
    print(value)
    print(type(value))
    if value.strip() == "0":
        print("Returning all zeros because data is empty")
        return "00000000000000000000000000000000"
    print("Returning actual value")
    hexadecimal = value
    end_length = len(hexadecimal) * 4
    hex_as_int = int(hexadecimal, 16)
    hex_as_binary = bin(hex_as_int)
    padded_binary = hex_as_binary[2:].zfill(end_length)
    return padded_binary


def get_data(count, Lines, register):
    """
    This method get and decode data for 8 registers of psx/pcie bridge and return values with specific register
    """
    base_add = ''
    reg_add_dict = {'write 0xfc': '0xfc440000',
                    'write_print 0xe4': '0xe4440000',
                    'write 0xb4': '0xb4440000',
                    'write 0xbc': '0xbc440000'}
    value = ""
    Count_0 = count - 1
    data8 = data7 = data6 = data5 = data4 = data3 = data2 = data1 = data0 = ""
    for i in range(7, -1, -1):
        for key in reg_add_dict.keys():
            if key in Lines[Count_0 - 1]:
                base_add = reg_add_dict[key]
        print(f"base address is {base_add}")
        if re.search(r"440840", Lines[Count_0 - 1], re.IGNORECASE):
            add = re.search(r"440840", Lines[Count_0 - 1], re.IGNORECASE).start()
        if "mask_poll" not in Lines[Count_0 - 1] and len(Lines[Count_0 - 1]) != 0 \
                and f"440840 " not in Lines[Count_0 - 1]:
            data = Lines[Count_0 - 1].replace("\n", "").split(" ")
            print(f"data is:{data}")
            # if "0x" not in data[1]:
            #     Count_0 += 1
            data = Lines[Count_0 - 1].replace("\n", "").split(" ")
                # print(f"observed dummy data {data}")
            offset_val = data[1]
            add_val = data[2].replace("0x", "")
            offset = hex(int(offset_val, 16) - int(base_add, 16))
            # else:
            #     offset_val = data[1]
            #     add_val = data[2].replace("0x", "")
            #     offset = hex(int(offset_val, 16) - int(base_add, 16))
            if str(offset) == "0x800" and not data0:
                data0 = add_val
            elif str(offset) == "0x804" and not data1:
                data1 = add_val
            elif str(offset) == "0x808" and not data2:
                data2 = add_val
            elif str(offset) == "0x80c" and not data3:
                data3 = add_val
            elif str(offset) == "0x810" and not data4:
                data4 = add_val
            elif str(offset) == "0x814" and not data5:
                data5 = add_val
            elif str(offset) == "0x818" and not data6:
                data6 = add_val
            elif str(offset) == "0x81c" and not data7:
                data7 = add_val
            line1 = (
                    data8 + data7 + data6 + data5 + data4 + data3 + data2 + data1 + data0
            )
            register = "\n" + str(Count_0) + "-->" + Lines[Count_0 - 1] + register
            value = convert_hex_binary(line1)
            Count_0 = Count_0 - 1
        else:
            break
    return register, value


def remove_space_from_cdo_file(cdo_file):
    cdo_file = open(cdo_file, 'r')
    cdo_write = open('cdo_to_text_input.cdo', 'w')
    for i in cdo_file:
        if i.strip():
            cdo_write.write(i.strip() + '\n')
    cdo_write.close()
    cdo_file.close()


def SCHED_MON_SRC_ID_TBL(data):
    if "=" in data:
        A2_sched_mon_src_id = data.split("A2_sched_mon_src_id=")[1]
        A2_sched_mon_src_id = hex_to_bin(A2_sched_mon_src_id)
        A2_sched_mon_src_id = format_data_length(A2_sched_mon_src_id, 13)
        data_value = A2_sched_mon_src_id
        data_value = format_hex_value(data_value)
        return data_value
    return (
            ":: A2_sched_mon_src_id="
            + data[-14:]
    )


def SCHED_MON_ALIVE_SRC_ID_TBL(data):
    if "=" in data:
        A2_sched_mon_alive_src_id = data.split("A2_sched_mon_alive_src_id=")[1]
        A2_sched_mon_alive_src_id = hex_to_bin(A2_sched_mon_alive_src_id)
        A2_sched_mon_alive_src_id = format_data_length(A2_sched_mon_alive_src_id, 13)
        data_value = A2_sched_mon_alive_src_id
        data_value = format_hex_value(data_value)
        return data_value
    return (
            ":: A2_sched_mon_alive_src_id="
            + data[-14:]
    )


def SCHED_DBG_CTRL_REG(data):
    if "=" in data:
        A2_one_sec_mode = data.split("A2_one_sec_mode=")[1].split(',')[0]
        A2_one_sec_mode = hex_to_bin(A2_one_sec_mode)
        A2_dbg_pipe_cnt_stats = data.split("A2_dbg_pipe_cnt_stats=")[1].split(',')[0]
        A2_dbg_pipe_cnt_stats = hex_to_bin(A2_dbg_pipe_cnt_stats)
        A2_dbg_mtu_sel = data.split("A2_dbg_mtu_sel=")[1].split(',')[0]
        A2_dbg_mtu_sel = hex_to_bin(A2_dbg_mtu_sel)
        A2_dbg_mtu_sel = format_data_length(A2_dbg_mtu_sel, 4)
        A2_src_bw_unit_scred = data.split("A2_src_bw_unit_scred=")[1].split(',')[0]
        A2_src_bw_unit_scred = hex_to_bin(A2_src_bw_unit_scred)
        A2_dest_bw_unit_dcred = data.split("A2_dest_bw_unit_dcred=")[1].split(',')[0]
        A2_dest_bw_unit_dcred = hex_to_bin(A2_dest_bw_unit_dcred)
        A2_mask_drr_covr_sticky = data.split("A2_mask_drr_covr_sticky=")[1].split(',')[0]
        A2_mask_drr_covr_sticky = hex_to_bin(A2_mask_drr_covr_sticky)
        A2_mask_alive_sticky = data.split("A2_mask_alive_sticky=")[1].split(',')[0]
        A2_mask_alive_sticky = hex_to_bin(A2_mask_alive_sticky)
        A2_mask_pipe_err_sticky = data.split("A2_mask_pipe_err_sticky=")[1].split(',')[0]
        A2_mask_pipe_err_sticky = hex_to_bin(A2_mask_pipe_err_sticky)
        A2_mask_imdest_dest_msg_if_err_sticky = data.split("A2_mask_imdest_dest_msg_if_err_sticky=")[1].split(',')[0]
        A2_mask_imdest_dest_msg_if_err_sticky = hex_to_bin(A2_mask_imdest_dest_msg_if_err_sticky)
        A2_mask_pktsrc_jresp_msg_if_err_sticky = data.split("A2_mask_pktsrc_jresp_msg_if_err_sticky=")[1].split(',')[0]
        A2_mask_pktsrc_jresp_msg_if_err_sticky = hex_to_bin(A2_mask_pktsrc_jresp_msg_if_err_sticky)
        A2_mask_bar_msg_fifo_non_empty = data.split("A2_mask_bar_msg_fifo_non_empty=")[1].split(',')[0]
        A2_mask_bar_msg_fifo_non_empty = hex_to_bin(A2_mask_bar_msg_fifo_non_empty)
        A2_mask_cmd_resp_fifo_non_empty = data.split("A2_mask_cmd_resp_fifo_non_empty=")[1].split(',')[0]
        A2_mask_cmd_resp_fifo_non_empty = hex_to_bin(A2_mask_cmd_resp_fifo_non_empty)
        A2_mask_ecc_ucerr_status = data.split("A2_mask_ecc_ucerr_status=")[1].split(',')[0]
        A2_mask_ecc_ucerr_status = hex_to_bin(A2_mask_ecc_ucerr_status)
        A2_mask_ecc_cerr_status = data.split("A2_mask_ecc_cerr_status=")[1]
        A2_mask_ecc_cerr_status = hex_to_bin(A2_mask_ecc_cerr_status)
        data_value = A2_mask_ecc_cerr_status + A2_mask_ecc_ucerr_status + A2_mask_cmd_resp_fifo_non_empty + A2_mask_bar_msg_fifo_non_empty + A2_mask_pktsrc_jresp_msg_if_err_sticky + A2_mask_imdest_dest_msg_if_err_sticky + A2_mask_pipe_err_sticky + A2_mask_alive_sticky + "00000000" + A2_mask_drr_covr_sticky + A2_dest_bw_unit_dcred + A2_src_bw_unit_scred + A2_dbg_mtu_sel + A2_dbg_pipe_cnt_stats + A2_one_sec_mode
        data_value = format_hex_value(data_value)
        return data_value
    return (
            ":: A2_one_sec_mode="
            + data[-1]
            + ", A2_dbg_pipe_cnt_stats="
            + data[-2]
            + ", A2_dbg_mtu_sel="
            + data[-6:-2]
            + ", A2_src_bw_unit_scred="
            + data[-7]
            + ", A2_dest_bw_unit_dcred="
            + data[-8]
            + ", A2_mask_drr_covr_sticky="
            + data[-17]
            + ", A2_mask_alive_sticky="
            + data[-18]
            + ", A2_mask_pipe_err_sticky="
            + data[-19]
            + ", A2_mask_imdest_dest_msg_if_err_sticky="
            + data[-20]
            + ", A2_mask_pktsrc_jresp_msg_if_err_sticky="
            + data[-21]
            + ", A2_mask_bar_msg_fifo_non_empty="
            + data[-22]
            + ", A2_mask_cmd_resp_fifo_non_empty="
            + data[-23]
            + ", A2_mask_ecc_ucerr_status="
            + data[-24]
            + ", A2_mask_ecc_cerr_status="
            + data[-25]
    )


def SCHED_DBG_CNTR_LSW(data):
    if "=" in data:
        A2_sid1_cnt_smsg_bwc_LSB = data.split("A2_sid1_cnt_smsg_bwc_LSB=")[1].split(
            ","
        )[0]
        A2_sid1_cnt_smsg_bwc_LSB = hex_to_bin(A2_sid1_cnt_smsg_bwc_LSB)
        A2_sid1_cnt_smsg_bwc_LSB = format_data_length(A2_sid1_cnt_smsg_bwc_LSB, 4)
        A2_sid1_cnt_jres_bwp_LSB = data.split("A2_sid1_cnt_jres_bwp_LSB=")[1].split(
            ","
        )[0]
        A2_sid1_cnt_jres_bwp_LSB = hex_to_bin(A2_sid1_cnt_jres_bwp_LSB)
        A2_sid1_cnt_jres_bwp_LSB = format_data_length(A2_sid1_cnt_jres_bwp_LSB, 4)
        A2_sid2_cnt_smsg_bwc_LSB = data.split("A2_sid2_cnt_smsg_bwc_LSB=")[1].split(
            ","
        )[0]
        A2_sid2_cnt_smsg_bwc_LSB = hex_to_bin(A2_sid2_cnt_smsg_bwc_LSB)
        A2_sid2_cnt_smsg_bwc_LSB = format_data_length(A2_sid2_cnt_smsg_bwc_LSB, 4)
        A2_sid2_cnt_jres_bwp_LSB = data.split("A2_sid2_cnt_jres_bwp_LSB=")[1].split(
            ","
        )[0]
        A2_sid2_cnt_jres_bwp_LSB = hex_to_bin(A2_sid2_cnt_jres_bwp_LSB)
        A2_sid2_cnt_jres_bwp_LSB = format_data_length(A2_sid2_cnt_jres_bwp_LSB, 4)

        A2_did_cnt_dmsg_bwc_LSB = data.split("A2_did_cnt_dmsg_bwc_LSB=")[1].split(
            ","
        )[0]
        A2_did_cnt_dmsg_bwc_LSB = hex_to_bin(A2_did_cnt_dmsg_bwc_LSB)
        A2_did_cnt_dmsg_bwc_LSB = format_data_length(A2_did_cnt_dmsg_bwc_LSB, 4)
        A2_did_cnt_jres_bwp_LSB = data.split("A2_did_cnt_jres_bwp_LSB=")[1].split(
            ","
        )[0]
        A2_did_cnt_jres_bwp_LSB = hex_to_bin(A2_did_cnt_jres_bwp_LSB)
        A2_did_cnt_jres_bwp_LSB = format_data_length(A2_did_cnt_jres_bwp_LSB, 4)
        data_value = A2_did_cnt_jres_bwp_LSB + A2_did_cnt_dmsg_bwc_LSB + A2_sid2_cnt_jres_bwp_LSB + A2_sid2_cnt_smsg_bwc_LSB + A2_sid1_cnt_jres_bwp_LSB + A2_sid1_cnt_smsg_bwc_LSB
        data_value = format_hex_value(data_value)
        return data_value
    return (
            ":: A2_sid1_cnt_smsg_bwc_LSB="
            + data[-4:]
            + ", A2_sid1_cnt_jres_bwp_LSB="
            + data[-8:-4]
            + ", A2_sid2_cnt_smsg_bwc_LSB="
            + data[-12:-8]
            + ", A2_sid2_cnt_jres_bwp_LSB="
            + data[-16:-12]
            + ", A2_did_cnt_dmsg_bwc_LSB="
            + data[-20:-16]
            + ", A2_did_cnt_jres_bwp_LSB="
            + data[-24:-20]
    )


def SCHED_SID1_CNT_SMSG_BWC(data):
    if "=" in data:
        A2_sid1_cnt_smsg_bwc = data.split("A2_sid1_cnt_smsg_bwc=")[1]
        A2_sid1_cnt_smsg_bwc = hex_to_bin(A2_sid1_cnt_smsg_bwc)
        A2_sid1_cnt_smsg_bwc = format_data_length(A2_sid1_cnt_smsg_bwc, 6)
        data_value = A2_sid1_cnt_smsg_bwc
        data_value = format_hex_value(data_value)
        return data_value
    return (
            ":: A2_sid1_cnt_smsg_bwc="
            + data[-32:]
    )


def SCHED_SID1_CNT_JRES_BWP(data):
    if "=" in data:
        A2_sid1_cnt_jres_bwp = data.split("A2_sid1_cnt_jres_bwp=")[1]
        A2_sid1_cnt_jres_bwp = hex_to_bin(A2_sid1_cnt_jres_bwp)
        A2_sid1_cnt_jres_bwp = format_data_length(A2_sid1_cnt_jres_bwp, 6)
        data_value = A2_sid1_cnt_jres_bwp
        data_value = format_hex_value(data_value)
        return data_value
    return (
            ":: A2_sid1_cnt_jres_bwp="
            + data[-32:]
    )


def SCHED_SID2_CNT_SMSG_BWC(data):
    if "=" in data:
        A2_sid1_cnt_jres_bwp = data.split("A2_sid1_cnt_jres_bwp=")[1]
        A2_sid1_cnt_jres_bwp = hex_to_bin(A2_sid1_cnt_jres_bwp)
        A2_sid1_cnt_jres_bwp = format_data_length(A2_sid1_cnt_jres_bwp, 6)
        data_value = A2_sid1_cnt_jres_bwp
        data_value = format_hex_value(data_value)
        return data_value
    return (
            ":: A2_sid1_cnt_jres_bwp="
            + data[-32:]
    )


def SCHED_SID2_CNT_JRES_BWP(data):
    if "=" in data:
        A2_sid2_cnt_jres_bwp = data.split("A2_sid2_cnt_jres_bwp=")[1]
        A2_sid2_cnt_jres_bwp = hex_to_bin(A2_sid2_cnt_jres_bwp)
        A2_sid2_cnt_jres_bwp = format_data_length(A2_sid2_cnt_jres_bwp, 6)
        data_value = A2_sid2_cnt_jres_bwp
        data_value = format_hex_value(data_value)
        return data_value
    return (
            ":: A2_sid2_cnt_jres_bwp="
            + data[-32:]
    )


def SCHED_DID_CNT_DMSG_BWC(data):
    if "=" in data:
        A2_did_cnt_dmsg_bwc = data.split("A2_did_cnt_dmsg_bwc=")[1]
        A2_did_cnt_dmsg_bwc = hex_to_bin(A2_did_cnt_dmsg_bwc)
        A2_did_cnt_dmsg_bwc = format_data_length(A2_did_cnt_dmsg_bwc, 6)
        data_value = A2_did_cnt_dmsg_bwc
        data_value = format_hex_value(data_value)
        return data_value
    return (
            ":: A2_did_cnt_dmsg_bwc="
            + data[-32:]
    )


def SCHED_DID_CNT_JRES_BWP(data):
    if "=" in data:
        A2_did_cnt_jres_bwp = data.split("A2_did_cnt_jres_bwp=")[1]
        A2_did_cnt_jres_bwp = hex_to_bin(A2_did_cnt_jres_bwp)
        A2_did_cnt_jres_bwp = format_data_length(A2_did_cnt_jres_bwp, 6)
        data_value = A2_did_cnt_jres_bwp
        data_value = format_hex_value(data_value)
        return data_value
    return (
            ":: A2_did_cnt_jres_bwp="
            + data[-32:]
    )


def SCHED_SER_ING_MSG_IF_1_2_3_4_ERR_STICKY_REG(data):
    if "=" in data:
        A2_sing_1_invalid_bar_jerr_msg_sop_eop = data.split("A2_sing_1_invalid_bar_jerr_msg_sop_eop=")[1].split(',')[0]
        A2_sing_1_invalid_bar_jerr_msg_sop_eop = hex_to_bin(A2_sing_1_invalid_bar_jerr_msg_sop_eop)
        A2_sing_1_invalid_msg_type = data.split("A2_sing_1_invalid_msg_type=")[1].split(',')[0]
        A2_sing_1_invalid_msg_type = hex_to_bin(A2_sing_1_invalid_msg_type)
        A2_sing_1_invalid_src_dest_cred_msg_sop_eop = \
            data.split("A2_sing_1_invalid_src_dest_cred_msg_sop_eop=")[1].split(',')[0]
        A2_sing_1_invalid_src_dest_cred_msg_sop_eop = hex_to_bin(A2_sing_1_invalid_src_dest_cred_msg_sop_eop)
        A2_sing_1_invalid_jresp_msg_sop_eop = data.split("A2_sing_1_invalid_jresp_msg_sop_eop=")[1].split(',')[0]
        A2_sing_1_invalid_jresp_msg_sop_eop = hex_to_bin(A2_sing_1_invalid_jresp_msg_sop_eop)
        A2_sing_1_neg_scred_in_src_cred_msg = data.split("A2_sing_1_neg_scred_in_src_cred_msg=")[1].split(',')[0]
        A2_sing_1_neg_scred_in_src_cred_msg = hex_to_bin(A2_sing_1_neg_scred_in_src_cred_msg)
        A2_sing_1_neg_scred_in_jresp_msg = data.split("A2_sing_1_neg_scred_in_jresp_msg=")[1].split(',')[0]
        A2_sing_1_neg_scred_in_jresp_msg = hex_to_bin(A2_sing_1_neg_scred_in_jresp_msg)
        A2_sing_1_neg_dcred_in_jresp_dcred_msg = data.split("A2_sing_1_neg_dcred_in_jresp_dcred_msg=")[1].split(',')[0]
        A2_sing_1_neg_dcred_in_jresp_dcred_msg = hex_to_bin(A2_sing_1_neg_dcred_in_jresp_dcred_msg)
        A2_sing_1_neg_cost_in_jresp_msg = data.split("A2_sing_1_neg_cost_in_jresp_msg=")[1].split(',')[0]
        A2_sing_1_neg_cost_in_jresp_msg = hex_to_bin(A2_sing_1_neg_cost_in_jresp_msg)
        A2_sing_2_invalid_bar_jerr_msg_sop_eop = data.split("A2_sing_2_invalid_bar_jerr_msg_sop_eop=")[1].split(',')[0]
        A2_sing_2_invalid_bar_jerr_msg_sop_eop = hex_to_bin(A2_sing_2_invalid_bar_jerr_msg_sop_eop)
        A2_sing_2_invalid_msg_type = data.split("A2_sing_2_invalid_msg_type=")[1].split(',')[0]
        A2_sing_2_invalid_msg_type = hex_to_bin(A2_sing_2_invalid_msg_type)
        A2_sing_2_invalid_src_dest_cred_msg_sop_eop = \
            data.split("A2_sing_2_invalid_src_dest_cred_msg_sop_eop=")[1].split(',')[0]
        A2_sing_2_invalid_src_dest_cred_msg_sop_eop = hex_to_bin(A2_sing_2_invalid_src_dest_cred_msg_sop_eop)
        A2_sing_2_invalid_jresp_msg_sop_eop = data.split("A2_sing_2_invalid_jresp_msg_sop_eop=")[1].split(',')[0]
        A2_sing_2_invalid_jresp_msg_sop_eop = hex_to_bin(A2_sing_2_invalid_jresp_msg_sop_eop)
        A2_sing_2_neg_scred_in_src_cred_msg = data.split("A2_sing_2_neg_scred_in_src_cred_msg=")[1].split(',')[0]
        A2_sing_2_neg_scred_in_src_cred_msg = hex_to_bin(A2_sing_2_neg_scred_in_src_cred_msg)
        A2_sing_2_neg_scred_in_jresp_msg = data.split("A2_sing_2_neg_scred_in_jresp_msg=")[1].split(',')[0]
        A2_sing_2_neg_scred_in_jresp_msg = hex_to_bin(A2_sing_2_neg_scred_in_jresp_msg)
        A2_sing_2_neg_dcred_in_jresp_dcred_msg = data.split("A2_sing_2_neg_dcred_in_jresp_dcred_msg=")[1].split(',')[0]
        A2_sing_2_neg_dcred_in_jresp_dcred_msg = hex_to_bin(A2_sing_2_neg_dcred_in_jresp_dcred_msg)
        A2_sing_2_neg_cost_in_jresp_msg = data.split("A2_sing_2_neg_cost_in_jresp_msg=")[1].split(',')[0]
        A2_sing_2_neg_cost_in_jresp_msg = hex_to_bin(A2_sing_2_neg_cost_in_jresp_msg)
        A2_sing_3_invalid_bar_jerr_msg_sop_eop = data.split("A2_sing_3_invalid_bar_jerr_msg_sop_eop=")[1].split(',')[0]
        A2_sing_3_invalid_bar_jerr_msg_sop_eop = hex_to_bin(A2_sing_3_invalid_bar_jerr_msg_sop_eop)
        A2_sing_3_invalid_msg_type = data.split("A2_sing_3_invalid_msg_type=")[1].split(',')[0]
        A2_sing_3_invalid_msg_type = hex_to_bin(A2_sing_3_invalid_msg_type)
        A2_sing_3_invalid_src_dest_cred_msg_sop_eop = \
            data.split("A2_sing_3_invalid_src_dest_cred_msg_sop_eop=")[1].split(',')[0]
        A2_sing_3_invalid_src_dest_cred_msg_sop_eop = hex_to_bin(A2_sing_3_invalid_src_dest_cred_msg_sop_eop)
        A2_sing_3_invalid_jresp_msg_sop_eop = data.split("A2_sing_3_invalid_jresp_msg_sop_eop=")[1].split(',')[0]
        A2_sing_3_invalid_jresp_msg_sop_eop = hex_to_bin(A2_sing_3_invalid_jresp_msg_sop_eop)
        A2_sing_3_neg_scred_in_src_cred_msg = data.split("A2_sing_3_neg_scred_in_src_cred_msg=")[1].split(',')[0]
        A2_sing_3_neg_scred_in_src_cred_msg = hex_to_bin(A2_sing_3_neg_scred_in_src_cred_msg)
        A2_sing_3_neg_scred_in_jresp_msg = data.split("A2_sing_3_neg_scred_in_jresp_msg=")[1].split(',')[0]
        A2_sing_3_neg_scred_in_jresp_msg = hex_to_bin(A2_sing_3_neg_scred_in_jresp_msg)
        A2_sing_3_neg_dcred_in_jresp_dcred_msg = data.split("A2_sing_3_neg_dcred_in_jresp_dcred_msg=")[1].split(',')[0]
        A2_sing_3_neg_dcred_in_jresp_dcred_msg = hex_to_bin(A2_sing_3_neg_dcred_in_jresp_dcred_msg)
        A2_sing_3_neg_cost_in_jresp_msg = data.split("A2_sing_3_neg_cost_in_jresp_msg=")[1].split(',')[0]
        A2_sing_3_neg_cost_in_jresp_msg = hex_to_bin(A2_sing_3_neg_cost_in_jresp_msg)
        A2_sing_4_invalid_bar_jerr_msg_sop_eop = data.split("A2_sing_4_invalid_bar_jerr_msg_sop_eop=")[1].split(',')[0]
        A2_sing_4_invalid_bar_jerr_msg_sop_eop = hex_to_bin(A2_sing_4_invalid_bar_jerr_msg_sop_eop)
        A2_sing_4_invalid_msg_type = data.split("A2_sing_4_invalid_msg_type=")[1].split(',')[0]
        A2_sing_4_invalid_msg_type = hex_to_bin(A2_sing_4_invalid_msg_type)
        A2_sing_4_invalid_src_dest_cred_msg_sop_eop = \
            data.split("A2_sing_4_invalid_src_dest_cred_msg_sop_eop=")[1].split(',')[0]
        A2_sing_4_invalid_src_dest_cred_msg_sop_eop = hex_to_bin(A2_sing_4_invalid_src_dest_cred_msg_sop_eop)
        A2_sing_4_invalid_jresp_msg_sop_eop = data.split("A2_sing_4_invalid_jresp_msg_sop_eop=")[1].split(',')[0]
        A2_sing_4_invalid_jresp_msg_sop_eop = hex_to_bin(A2_sing_4_invalid_jresp_msg_sop_eop)
        A2_sing_4_neg_scred_in_src_cred_msg = data.split("A2_sing_4_neg_scred_in_src_cred_msg=")[1].split(',')[0]
        A2_sing_4_neg_scred_in_src_cred_msg = hex_to_bin(A2_sing_4_neg_scred_in_src_cred_msg)
        A2_sing_4_neg_scred_in_jresp_msg = data.split("A2_sing_4_neg_scred_in_jresp_msg=")[1].split(',')[0]
        A2_sing_4_neg_scred_in_jresp_msg = hex_to_bin(A2_sing_4_neg_scred_in_jresp_msg)
        A2_sing_4_neg_dcred_in_jresp_dcred_msg = data.split("A2_sing_4_neg_dcred_in_jresp_dcred_msg=")[1].split(',')[0]
        A2_sing_4_neg_dcred_in_jresp_dcred_msg = hex_to_bin(A2_sing_4_neg_dcred_in_jresp_dcred_msg)
        A2_sing_4_neg_cost_in_jresp_msg = data.split("A2_sing_4_neg_cost_in_jresp_msg=")[1]
        A2_sing_4_neg_cost_in_jresp_msg = hex_to_bin(A2_sing_4_neg_cost_in_jresp_msg)
        data_value = A2_sing_4_neg_cost_in_jresp_msg + A2_sing_4_neg_dcred_in_jresp_dcred_msg + A2_sing_4_neg_scred_in_jresp_msg + A2_sing_4_neg_scred_in_src_cred_msg + A2_sing_4_invalid_jresp_msg_sop_eop + A2_sing_4_invalid_src_dest_cred_msg_sop_eop + A2_sing_4_invalid_msg_type + A2_sing_4_invalid_bar_jerr_msg_sop_eop + A2_sing_3_neg_cost_in_jresp_msg + A2_sing_3_neg_dcred_in_jresp_dcred_msg + A2_sing_3_neg_scred_in_jresp_msg + A2_sing_3_neg_scred_in_src_cred_msg + A2_sing_3_invalid_jresp_msg_sop_eop + A2_sing_3_invalid_src_dest_cred_msg_sop_eop + A2_sing_3_invalid_msg_type + A2_sing_3_invalid_bar_jerr_msg_sop_eop + A2_sing_2_neg_cost_in_jresp_msg + A2_sing_2_neg_dcred_in_jresp_dcred_msg + A2_sing_2_neg_scred_in_jresp_msg + A2_sing_2_neg_scred_in_src_cred_msg + A2_sing_2_invalid_jresp_msg_sop_eop + A2_sing_2_invalid_src_dest_cred_msg_sop_eop + A2_sing_2_invalid_msg_type + A2_sing_2_invalid_bar_jerr_msg_sop_eop + A2_sing_1_neg_cost_in_jresp_msg + A2_sing_1_neg_dcred_in_jresp_dcred_msg + A2_sing_1_neg_scred_in_jresp_msg + A2_sing_1_neg_scred_in_src_cred_msg + A2_sing_1_invalid_jresp_msg_sop_eop + A2_sing_1_invalid_src_dest_cred_msg_sop_eop + A2_sing_1_invalid_msg_type + A2_sing_1_invalid_bar_jerr_msg_sop_eop
        data_value = format_hex_value(data_value)
        return data_value
    return (
            ":: A2_sing_1_invalid_bar_jerr_msg_sop_eop="
            + data[-1]
            + ", A2_sing_1_invalid_msg_type="
            + data[-2]
            + ", A2_sing_1_invalid_src_dest_cred_msg_sop_eop="
            + data[-3]
            + ", A2_sing_1_invalid_jresp_msg_sop_eop="
            + data[-4]
            + ", A2_sing_1_neg_scred_in_src_cred_msg="
            + data[-5]
            + ", A2_sing_1_neg_scred_in_jresp_msg="
            + data[-6]
            + ", A2_sing_1_neg_dcred_in_jresp_dcred_msg="
            + data[-7]
            + ", A2_sing_1_neg_cost_in_jresp_msg="
            + data[-8]
            + ", A2_sing_2_invalid_bar_jerr_msg_sop_eop="
            + data[-9]
            + ", A2_sing_2_invalid_msg_type="
            + data[-10]
            + ", A2_sing_2_invalid_src_dest_cred_msg_sop_eop="
            + data[-11]
            + ", A2_sing_2_invalid_jresp_msg_sop_eop="
            + data[-12]
            + ", A2_sing_2_neg_scred_in_src_cred_msg="
            + data[-13]
            + ", A2_sing_2_neg_scred_in_jresp_msg="
            + data[-14]
            + ", A2_sing_2_neg_dcred_in_jresp_dcred_msg="
            + data[-15]
            + ", A2_sing_2_neg_cost_in_jresp_msg="
            + data[-16]
            + ", A2_sing_3_invalid_bar_jerr_msg_sop_eop="
            + data[-17]
            + ", A2_sing_3_invalid_msg_type="
            + data[-18]
            + ", A2_sing_3_invalid_src_dest_cred_msg_sop_eop="
            + data[-19]
            + ", A2_sing_3_invalid_jresp_msg_sop_eop="
            + data[-20]
            + ", A2_sing_3_neg_scred_in_src_cred_msg="
            + data[-21]
            + ", A2_sing_3_neg_scred_in_jresp_msg="
            + data[-22]
            + ", A2_sing_3_neg_dcred_in_jresp_dcred_msg="
            + data[-23]
            + ", A2_sing_3_neg_cost_in_jresp_msg="
            + data[-24]
            + ", A2_sing_4_invalid_bar_jerr_msg_sop_eop="
            + data[-25]
            + ", A2_sing_4_invalid_msg_type="
            + data[-26]
            + ", A2_sing_4_invalid_src_dest_cred_msg_sop_eop="
            + data[-27]
            + ", A2_sing_4_invalid_jresp_msg_sop_eop="
            + data[-28]
            + ", A2_sing_4_neg_scred_in_src_cred_msg="
            + data[-29]
            + ", A2_sing_4_neg_scred_in_jresp_msg="
            + data[-30]
            + ", A2_sing_4_neg_dcred_in_jresp_dcred_msg="
            + data[-31]
            + ", A2_sing_4_neg_cost_in_jresp_msg="
            + data[-32]
    )


def SCHED_SING_5_6_7_MSG_IF_ERR_STICKY_REG(data):
    if "=" in data:
        A2_sing_5_invalid_bar_jerr_msg_sop_eop = data.split("A2_sing_5_invalid_bar_jerr_msg_sop_eop=")[1].split(',')[0]
        A2_sing_5_invalid_bar_jerr_msg_sop_eop = hex_to_bin(A2_sing_5_invalid_bar_jerr_msg_sop_eop)
        A2_sing_5_invalid_msg_type = data.split("A2_sing_5_invalid_msg_type=")[1].split(',')[0]
        A2_sing_5_invalid_msg_type = hex_to_bin(A2_sing_5_invalid_msg_type)
        A2_sing_5_invalid_src_dest_cred_msg_sop_eop = \
            data.split("A2_sing_5_invalid_src_dest_cred_msg_sop_eop=")[1].split(',')[0]
        A2_sing_5_invalid_src_dest_cred_msg_sop_eop = hex_to_bin(A2_sing_5_invalid_src_dest_cred_msg_sop_eop)
        A2_sing_5_invalid_jresp_msg_sop_eop = data.split("A2_sing_5_invalid_jresp_msg_sop_eop=")[1].split(',')[0]
        A2_sing_5_invalid_jresp_msg_sop_eop = hex_to_bin(A2_sing_5_invalid_jresp_msg_sop_eop)
        A2_sing_5_neg_scred_in_src_cred_msg = data.split("A2_sing_5_neg_scred_in_src_cred_msg=")[1].split(',')[0]
        A2_sing_5_neg_scred_in_src_cred_msg = hex_to_bin(A2_sing_5_neg_scred_in_src_cred_msg)
        A2_sing_5_neg_scred_in_jresp_msg = data.split("A2_sing_5_neg_scred_in_jresp_msg=")[1].split(',')[0]
        A2_sing_5_neg_scred_in_jresp_msg = hex_to_bin(A2_sing_5_neg_scred_in_jresp_msg)
        A2_sing_5_neg_dcred_in_jresp_dcred_msg = data.split("A2_sing_5_neg_dcred_in_jresp_dcred_msg=")[1].split(',')[0]
        A2_sing_5_neg_dcred_in_jresp_dcred_msg = hex_to_bin(A2_sing_5_neg_dcred_in_jresp_dcred_msg)
        A2_sing_5_neg_cost_in_jresp_msg = data.split("A2_sing_5_neg_cost_in_jresp_msg=")[1].split(',')[0]
        A2_sing_5_neg_cost_in_jresp_msg = hex_to_bin(A2_sing_5_neg_cost_in_jresp_msg)
        A2_sing_6_invalid_bar_jerr_msg_sop_eop = data.split("A2_sing_6_invalid_bar_jerr_msg_sop_eop=")[1].split(',')[0]
        A2_sing_6_invalid_bar_jerr_msg_sop_eop = hex_to_bin(A2_sing_6_invalid_bar_jerr_msg_sop_eop)
        A2_sing_6_invalid_msg_type = data.split("A2_sing_6_invalid_msg_type=")[1].split(',')[0]
        A2_sing_6_invalid_msg_type = hex_to_bin(A2_sing_6_invalid_msg_type)
        A2_sing_6_invalid_src_dest_cred_msg_sop_eop = \
            data.split("A2_sing_6_invalid_src_dest_cred_msg_sop_eop=")[1].split(',')[0]
        A2_sing_6_invalid_src_dest_cred_msg_sop_eop = hex_to_bin(A2_sing_6_invalid_src_dest_cred_msg_sop_eop)
        A2_sing_6_invalid_jresp_msg_sop_eop = data.split("A2_sing_6_invalid_jresp_msg_sop_eop=")[1].split(',')[0]
        A2_sing_6_invalid_jresp_msg_sop_eop = hex_to_bin(A2_sing_6_invalid_jresp_msg_sop_eop)
        A2_sing_6_neg_scred_in_src_cred_msg = data.split("A2_sing_6_neg_scred_in_src_cred_msg=")[1].split(',')[0]
        A2_sing_6_neg_scred_in_src_cred_msg = hex_to_bin(A2_sing_6_neg_scred_in_src_cred_msg)
        A2_sing_6_neg_scred_in_jresp_msg = data.split("A2_sing_6_neg_scred_in_jresp_msg=")[1].split(',')[0]
        A2_sing_6_neg_scred_in_jresp_msg = hex_to_bin(A2_sing_6_neg_scred_in_jresp_msg)
        A2_sing_6_neg_dcred_in_jresp_dcred_msg = data.split("A2_sing_6_neg_dcred_in_jresp_dcred_msg=")[1].split(',')[0]
        A2_sing_6_neg_dcred_in_jresp_dcred_msg = hex_to_bin(A2_sing_6_neg_dcred_in_jresp_dcred_msg)
        A2_sing_6_neg_cost_in_jresp_msg = data.split("A2_sing_6_neg_cost_in_jresp_msg=")[1].split(',')[0]
        A2_sing_6_neg_cost_in_jresp_msg = hex_to_bin(A2_sing_6_neg_cost_in_jresp_msg)
        A2_sing_7_invalid_bar_jerr_msg_sop_eop = data.split("A2_sing_7_invalid_bar_jerr_msg_sop_eop=")[1].split(',')[0]
        A2_sing_7_invalid_bar_jerr_msg_sop_eop = hex_to_bin(A2_sing_7_invalid_bar_jerr_msg_sop_eop)
        A2_sing_7_invalid_msg_type = data.split("A2_sing_7_invalid_msg_type=")[1].split(',')[0]
        A2_sing_7_invalid_msg_type = hex_to_bin(A2_sing_7_invalid_msg_type)
        A2_sing_7_invalid_src_dest_cred_msg_sop_eop = \
            data.split("A2_sing_7_invalid_src_dest_cred_msg_sop_eop=")[1].split(',')[0]
        A2_sing_7_invalid_src_dest_cred_msg_sop_eop = hex_to_bin(A2_sing_7_invalid_src_dest_cred_msg_sop_eop)
        A2_sing_7_invalid_jresp_msg_sop_eop = data.split("A2_sing_7_invalid_jresp_msg_sop_eop=")[1].split(',')[0]
        A2_sing_7_invalid_jresp_msg_sop_eop = hex_to_bin(A2_sing_7_invalid_jresp_msg_sop_eop)
        A2_sing_7_neg_scred_in_src_cred_msg = data.split("A2_sing_7_neg_scred_in_src_cred_msg=")[1].split(',')[0]
        A2_sing_7_neg_scred_in_src_cred_msg = hex_to_bin(A2_sing_7_neg_scred_in_src_cred_msg)
        A2_sing_7_neg_scred_in_jresp_msg = data.split("A2_sing_7_neg_scred_in_jresp_msg=")[1].split(',')[0]
        A2_sing_7_neg_scred_in_jresp_msg = hex_to_bin(A2_sing_7_neg_scred_in_jresp_msg)
        A2_sing_7_neg_dcred_in_jresp_dcred_msg = data.split("A2_sing_7_neg_dcred_in_jresp_dcred_msg=")[1].split(',')[0]
        A2_sing_7_neg_dcred_in_jresp_dcred_msg = hex_to_bin(A2_sing_7_neg_dcred_in_jresp_dcred_msg)
        A2_sing_7_neg_cost_in_jresp_msg = data.split("A2_sing_7_neg_cost_in_jresp_msg=")[1]
        A2_sing_7_neg_cost_in_jresp_msg = hex_to_bin(A2_sing_7_neg_cost_in_jresp_msg)
        data_value = A2_sing_7_neg_cost_in_jresp_msg + A2_sing_7_neg_dcred_in_jresp_dcred_msg + A2_sing_7_neg_scred_in_jresp_msg + A2_sing_7_neg_scred_in_src_cred_msg + A2_sing_7_invalid_jresp_msg_sop_eop + A2_sing_7_invalid_src_dest_cred_msg_sop_eop + A2_sing_7_invalid_msg_type + A2_sing_7_invalid_bar_jerr_msg_sop_eop + A2_sing_6_neg_cost_in_jresp_msg + A2_sing_6_neg_dcred_in_jresp_dcred_msg + A2_sing_6_neg_scred_in_jresp_msg + A2_sing_6_neg_scred_in_src_cred_msg + A2_sing_6_invalid_jresp_msg_sop_eop + A2_sing_6_invalid_src_dest_cred_msg_sop_eop + A2_sing_6_invalid_msg_type + A2_sing_6_invalid_bar_jerr_msg_sop_eop + A2_sing_5_neg_cost_in_jresp_msg + A2_sing_5_neg_dcred_in_jresp_dcred_msg + A2_sing_5_neg_scred_in_jresp_msg + A2_sing_5_neg_scred_in_src_cred_msg + A2_sing_5_invalid_jresp_msg_sop_eop + A2_sing_5_invalid_src_dest_cred_msg_sop_eop + A2_sing_5_invalid_msg_type + A2_sing_5_invalid_bar_jerr_msg_sop_eop
        data_value = format_hex_value(data_value)
        return data_value
    return (
            ":: A2_sing_5_invalid_bar_jerr_msg_sop_eop="
            + data[-1]
            + ", A2_sing_5_invalid_msg_type="
            + data[-2]
            + ", A2_sing_5_invalid_src_dest_cred_msg_sop_eop="
            + data[-3]
            + ", A2_sing_5_invalid_jresp_msg_sop_eop="
            + data[-4]
            + ", A2_sing_5_neg_scred_in_src_cred_msg="
            + data[-5]
            + ", A2_sing_5_neg_scred_in_jresp_msg="
            + data[-6]
            + ", A2_sing_5_neg_dcred_in_jresp_dcred_msg="
            + data[-7]
            + ", A2_sing_5_neg_cost_in_jresp_msg="
            + data[-8]
            + ", A2_sing_6_invalid_bar_jerr_msg_sop_eop="
            + data[-9]
            + ", A2_sing_6_invalid_msg_type="
            + data[-10]
            + ", A2_sing_6_invalid_src_dest_cred_msg_sop_eop="
            + data[-11]
            + ", A2_sing_6_invalid_jresp_msg_sop_eop="
            + data[-12]
            + ", A2_sing_6_neg_scred_in_src_cred_msg="
            + data[-13]
            + ", A2_sing_6_neg_scred_in_jresp_msg="
            + data[-14]
            + ", A2_sing_6_neg_dcred_in_jresp_dcred_msg="
            + data[-15]
            + ", A2_sing_6_neg_cost_in_jresp_msg="
            + data[-16]
            + ", A2_sing_7_invalid_bar_jerr_msg_sop_eop="
            + data[-17]
            + ", A2_sing_7_invalid_msg_type="
            + data[-18]
            + ", A2_sing_7_invalid_src_dest_cred_msg_sop_eop="
            + data[-19]
            + ", A2_sing_7_invalid_jresp_msg_sop_eop="
            + data[-20]
            + ", A2_sing_7_neg_scred_in_src_cred_msg="
            + data[-21]
            + ", A2_sing_7_neg_scred_in_jresp_msg="
            + data[-22]
            + ", A2_sing_7_neg_dcred_in_jresp_dcred_msg="
            + data[-23]
            + ", A2_sing_7_neg_cost_in_jresp_msg="
            + data[-24]
    )


def SCHED_PIPE_ERR_STICKY_REG(data):
    if "=" in data:
        A2_pipe_err_fatal_0 = data.split("A2_pipe_err_fatal_0=")[1].split(',')[0]
        A2_pipe_err_fatal_0 = hex_to_bin(A2_pipe_err_fatal_0)
        A2_pipe_err_fatal_1 = data.split("A2_pipe_err_fatal_1=")[1].split(',')[0]
        A2_pipe_err_fatal_1 = hex_to_bin(A2_pipe_err_fatal_1)
        A2_pipe_err_fatal_2 = data.split("A2_pipe_err_fatal_2=")[1].split(',')[0]
        A2_pipe_err_fatal_2 = hex_to_bin(A2_pipe_err_fatal_2)
        A2_pipe_err_fatal_4 = data.split("A2_pipe_err_fatal_4=")[1].split(',')[0]
        A2_pipe_err_fatal_4 = hex_to_bin(A2_pipe_err_fatal_4)
        A2_pipe_err_fatal_5 = data.split("A2_pipe_err_fatal_5=")[1].split(',')[0]
        A2_pipe_err_fatal_5 = hex_to_bin(A2_pipe_err_fatal_5)
        A2_pipe_err_fatal_6 = data.split("A2_pipe_err_fatal_6=")[1].split(',')[0]
        A2_pipe_err_fatal_6 = hex_to_bin(A2_pipe_err_fatal_6)
        A2_pipe_err_fatal_8 = data.split("A2_pipe_err_fatal_8=")[1].split(',')[0]
        A2_pipe_err_fatal_8 = hex_to_bin(A2_pipe_err_fatal_8)
        A2_pipe_err_fatal_9 = data.split("A2_pipe_err_fatal_9=")[1].split(',')[0]
        A2_pipe_err_fatal_9 = hex_to_bin(A2_pipe_err_fatal_9)
        A2_pipe_err_fatal_10 = data.split("A2_pipe_err_fatal_10=")[1].split(',')[0]
        A2_pipe_err_fatal_10 = hex_to_bin(A2_pipe_err_fatal_10)
        A2_pipe_err_fatal_12 = data.split("A2_pipe_err_fatal_12=")[1].split(',')[0]
        A2_pipe_err_fatal_12 = hex_to_bin(A2_pipe_err_fatal_12)
        A2_pipe_err_fatal_13 = data.split("A2_pipe_err_fatal_13=")[1].split(',')[0]
        A2_pipe_err_fatal_13 = hex_to_bin(A2_pipe_err_fatal_13)
        A2_pipe_err_fatal_14 = data.split("A2_pipe_err_fatal_14=")[1].split(',')[0]
        A2_pipe_err_fatal_14 = hex_to_bin(A2_pipe_err_fatal_14)
        A2_pipe_err_fatal_15 = data.split("A2_pipe_err_fatal_15=")[1]
        A2_pipe_err_fatal_15 = hex_to_bin(A2_pipe_err_fatal_15)
        data_value = A2_pipe_err_fatal_15 + A2_pipe_err_fatal_14 + A2_pipe_err_fatal_13 + A2_pipe_err_fatal_12 + '0' \
                     + A2_pipe_err_fatal_10 + A2_pipe_err_fatal_9 + A2_pipe_err_fatal_8 + '0' + A2_pipe_err_fatal_6 \
                     + A2_pipe_err_fatal_5 + A2_pipe_err_fatal_4 + '0' + A2_pipe_err_fatal_2 + A2_pipe_err_fatal_1 \
                     + A2_pipe_err_fatal_0
        data_value = format_hex_value(data_value)
        return data_value
    return (
            ":: A2_pipe_err_fatal_0="
            + data[-1]
            + ", A2_pipe_err_fatal_1="
            + data[-2]
            + ", A2_pipe_err_fatal_2="
            + data[-3]
            + ", A2_pipe_err_fatal_4="
            + data[-5]
            + ", A2_pipe_err_fatal_5="
            + data[-6]
            + ", A2_pipe_err_fatal_6="
            + data[-7]
            + ", A2_pipe_err_fatal_8="
            + data[-9]
            + ", A2_pipe_err_fatal_9="
            + data[-10]
            + ", A2_pipe_err_fatal_10="
            + data[-12]
            + ", A2_pipe_err_fatal_12="
            + data[-13]
            + ", A2_pipe_err_fatal_13="
            + data[-14]
            + ", A2_pipe_err_fatal_14="
            + data[-15]
            + ", A2_pipe_err_fatal_15="
            + data[-16]
    )


def SCHED_ALIVE_STICKY_REG(data):
    if "=" in data:
        A2_alive_ind_0 = data.split("A2_alive_ind_0=")[1].split(',')[0]
        A2_alive_ind_0 = hex_to_bin(A2_alive_ind_0)
        A2_alive_ind_1 = data.split("A2_alive_ind_1=")[1].split(',')[0]
        A2_alive_ind_1 = hex_to_bin(A2_alive_ind_1)
        A2_alive_ind_2 = data.split("A2_alive_ind_2=")[1].split(',')[0]
        A2_alive_ind_2 = hex_to_bin(A2_alive_ind_2)
        A2_alive_ind_3 = data.split("A2_alive_ind_3=")[1].split(',')[0]
        A2_alive_ind_3 = hex_to_bin(A2_alive_ind_3)
        A2_alive_ind_4 = data.split("A2_alive_ind_4=")[1].split(',')[0]
        A2_alive_ind_4 = hex_to_bin(A2_alive_ind_4)
        A2_alive_ind_5 = data.split("A2_alive_ind_5=")[1].split(',')[0]
        A2_alive_ind_5 = hex_to_bin(A2_alive_ind_5)
        A2_alive_ind_6 = data.split("A2_alive_ind_6=")[1].split(',')[0]
        A2_alive_ind_6 = hex_to_bin(A2_alive_ind_6)
        A2_alive_ind_7 = data.split("A2_alive_ind_7=")[1].split(',')[0]
        A2_alive_ind_7 = hex_to_bin(A2_alive_ind_7)
        A2_alive_ind_8 = data.split("A2_alive_ind_8=")[1].split(',')[0]
        A2_alive_ind_8 = hex_to_bin(A2_alive_ind_8)
        A2_alive_ind_9 = data.split("A2_alive_ind_9=")[1].split(',')[0]
        A2_alive_ind_9 = hex_to_bin(A2_alive_ind_9)
        A2_alive_ind_10 = data.split("A2_alive_ind_10=")[1].split(',')[0]
        A2_alive_ind_10 = hex_to_bin(A2_alive_ind_10)
        A2_alive_ind_11 = data.split("A2_alive_ind_11=")[1].split(',')[0]
        A2_alive_ind_11 = hex_to_bin(A2_alive_ind_11)
        A2_alive_ind_12 = data.split("A2_alive_ind_12=")[1].split(',')[0]
        A2_alive_ind_12 = hex_to_bin(A2_alive_ind_12)
        A2_alive_ind_13 = data.split("A2_alive_ind_13=")[1].split(',')[0]
        A2_alive_ind_13 = hex_to_bin(A2_alive_ind_13)
        A2_alive_ind_14 = data.split("A2_alive_ind_14=")[1].split(',')[0]
        A2_alive_ind_14 = hex_to_bin(A2_alive_ind_14)
        A2_alive_ind_15 = data.split("A2_alive_ind_15=")[1].split(',')[0]
        A2_alive_ind_15 = hex_to_bin(A2_alive_ind_15)
        A2_alive_ind_16 = data.split("A2_alive_ind_16=")[1].split(',')[0]
        A2_alive_ind_16 = hex_to_bin(A2_alive_ind_16)
        A2_alive_ind_17 = data.split("A2_alive_ind_17=")[1].split(',')[0]
        A2_alive_ind_17 = hex_to_bin(A2_alive_ind_17)
        A2_alive_ind_18 = data.split("A2_alive_ind_18=")[1].split(',')[0]
        A2_alive_ind_18 = hex_to_bin(A2_alive_ind_18)
        A2_alive_ind_19 = data.split("A2_alive_ind_19=")[1].split(',')[0]
        A2_alive_ind_19 = hex_to_bin(A2_alive_ind_19)
        A2_alive_ind_20 = data.split("A2_alive_ind_20=")[1].split(',')[0]
        A2_alive_ind_20 = hex_to_bin(A2_alive_ind_20)
        A2_alive_ind_21 = data.split("A2_alive_ind_21=")[1].split(',')[0]
        A2_alive_ind_21 = hex_to_bin(A2_alive_ind_21)
        A2_alive_ind_22 = data.split("A2_alive_ind_22=")[1].split(',')[0]
        A2_alive_ind_22 = hex_to_bin(A2_alive_ind_22)
        A2_alive_ind_23 = data.split("A2_alive_ind_23=")[1]
        A2_alive_ind_23 = hex_to_bin(A2_alive_ind_23)
        data_value = A2_alive_ind_23 + A2_alive_ind_22 + A2_alive_ind_21 + A2_alive_ind_20 + A2_alive_ind_19 + A2_alive_ind_18 + A2_alive_ind_17 + A2_alive_ind_16 + A2_alive_ind_15 + A2_alive_ind_14 + A2_alive_ind_13 + A2_alive_ind_12 + A2_alive_ind_11 + A2_alive_ind_10 + A2_alive_ind_9 + A2_alive_ind_8 + A2_alive_ind_7 + A2_alive_ind_6 + A2_alive_ind_5 + A2_alive_ind_4 + A2_alive_ind_3 + A2_alive_ind_2 + A2_alive_ind_1 + A2_alive_ind_0
        data_value = format_hex_value(data_value)
        return data_value
    return (
            ":: A2_alive_ind_0="
            + data[-1]
            + ", A2_alive_ind_1="
            + data[-2]
            + ", A2_alive_ind_2="
            + data[-3]
            + ", A2_alive_ind_3="
            + data[-4]
            + ", A2_alive_ind_4="
            + data[-5]
            + ", A2_alive_ind_5="
            + data[-6]
            + ", A2_alive_ind_6="
            + data[-7]
            + ", A2_alive_ind_7="
            + data[-8]
            + ", A2_alive_ind_8="
            + data[-9]
            + ", A2_alive_ind_9="
            + data[-10]
            + ", A2_alive_ind_10="
            + data[-11]
            + ", A2_alive_ind_11="
            + data[-12]
            + ", A2_alive_ind_12="
            + data[-13]
            + ", A2_alive_ind_13="
            + data[-14]
            + ", A2_alive_ind_14="
            + data[-15]
            + ", A2_alive_ind_15="
            + data[-16]
            + ", A2_alive_ind_16="
            + data[-17]
            + ", A2_alive_ind_17="
            + data[-18]
            + ", A2_alive_ind_18="
            + data[-19]
            + ", A2_alive_ind_19="
            + data[-20]
            + ", A2_alive_ind_20="
            + data[-21]
            + ", A2_alive_ind_21="
            + data[-22]
            + ", A2_alive_ind_22="
            + data[-23]
            + ", A2_alive_ind_23="
            + data[-24]
    )


def SCHED_DRR_COVR_STICKY_REG(data):
    if "=" in data:
        A2_drr_lvl_0_cover_00 = data.split("A2_drr_lvl_0_cover_00=")[1].split(',')[0]
        A2_drr_lvl_0_cover_00 = hex_to_bin(A2_drr_lvl_0_cover_00)
        A2_drr_lvl_0_cover_01 = data.split("A2_drr_lvl_0_cover_01=")[1].split(',')[0]
        A2_drr_lvl_0_cover_01 = hex_to_bin(A2_drr_lvl_0_cover_01)
        A2_drr_lvl_0_cover_02 = data.split("A2_drr_lvl_0_cover_02=")[1].split(',')[0]
        A2_drr_lvl_0_cover_02 = hex_to_bin(A2_drr_lvl_0_cover_02)
        A2_drr_lvl_0_cover_03 = data.split("A2_drr_lvl_0_cover_03=")[1].split(',')[0]
        A2_drr_lvl_0_cover_03 = hex_to_bin(A2_drr_lvl_0_cover_03)
        A2_drr_lvl_0_cover_04 = data.split("A2_drr_lvl_0_cover_04=")[1].split(',')[0]
        A2_drr_lvl_0_cover_04 = hex_to_bin(A2_drr_lvl_0_cover_04)
        A2_drr_lvl_0_cover_05 = data.split("A2_drr_lvl_0_cover_05=")[1].split(',')[0]
        A2_drr_lvl_0_cover_05 = hex_to_bin(A2_drr_lvl_0_cover_05)
        A2_drr_lvl_0_cover_06 = data.split("A2_drr_lvl_0_cover_06=")[1].split(',')[0]
        A2_drr_lvl_0_cover_06 = hex_to_bin(A2_drr_lvl_0_cover_06)
        A2_drr_lvl_0_cover_07 = data.split("A2_drr_lvl_0_cover_07=")[1].split(',')[0]
        A2_drr_lvl_0_cover_07 = hex_to_bin(A2_drr_lvl_0_cover_07)
        A2_drr_lvl_1_cover_08 = data.split("A2_drr_lvl_1_cover_08=")[1].split(',')[0]
        A2_drr_lvl_1_cover_08 = hex_to_bin(A2_drr_lvl_1_cover_08)
        A2_drr_lvl_1_cover_09 = data.split("A2_drr_lvl_1_cover_09=")[1].split(',')[0]
        A2_drr_lvl_1_cover_09 = hex_to_bin(A2_drr_lvl_1_cover_09)
        A2_drr_lvl_1_cover_10 = data.split("A2_drr_lvl_1_cover_10=")[1].split(',')[0]
        A2_drr_lvl_1_cover_10 = hex_to_bin(A2_drr_lvl_1_cover_10)
        A2_drr_lvl_1_cover_11 = data.split("A2_drr_lvl_1_cover_11=")[1].split(',')[0]
        A2_drr_lvl_1_cover_11 = hex_to_bin(A2_drr_lvl_1_cover_11)
        A2_drr_lvl_1_cover_12 = data.split("A2_drr_lvl_1_cover_12=")[1].split(',')[0]
        A2_drr_lvl_1_cover_12 = hex_to_bin(A2_drr_lvl_1_cover_12)
        A2_drr_lvl_1_cover_13 = data.split("A2_drr_lvl_1_cover_13=")[1].split(',')[0]
        A2_drr_lvl_1_cover_13 = hex_to_bin(A2_drr_lvl_1_cover_13)
        A2_drr_lvl_1_cover_14 = data.split("A2_drr_lvl_1_cover_14=")[1].split(',')[0]
        A2_drr_lvl_1_cover_14 = hex_to_bin(A2_drr_lvl_1_cover_14)
        A2_drr_lvl_1_cover_15 = data.split("A2_drr_lvl_1_cover_15=")[1].split(',')[0]
        A2_drr_lvl_1_cover_15 = hex_to_bin(A2_drr_lvl_1_cover_15)
        data_value = A2_drr_lvl_1_cover_15 + A2_drr_lvl_1_cover_14 + A2_drr_lvl_1_cover_13 + A2_drr_lvl_1_cover_12 + A2_drr_lvl_1_cover_11 + A2_drr_lvl_1_cover_10 + A2_drr_lvl_1_cover_09 + A2_drr_lvl_1_cover_08 + A2_drr_lvl_0_cover_07 + A2_drr_lvl_0_cover_06 + A2_drr_lvl_0_cover_05 + A2_drr_lvl_0_cover_04 + A2_drr_lvl_0_cover_03 + A2_drr_lvl_0_cover_02 + A2_drr_lvl_0_cover_01 + A2_drr_lvl_0_cover_00
        data_value = format_hex_value(data_value)
        return data_value
    return (
            ":: A2_drr_lvl_0_cover_00="
            + data[-1]
            + ", A2_drr_lvl_0_cover_01="
            + data[-2]
            + ", A2_drr_lvl_0_cover_02="
            + data[-3]
            + ", A2_drr_lvl_0_cover_03="
            + data[-4]
            + ", A2_drr_lvl_0_cover_04="
            + data[-5]
            + ", A2_drr_lvl_0_cover_05="
            + data[-6]
            + ", A2_drr_lvl_0_cover_06="
            + data[-7]
            + ", A2_drr_lvl_0_cover_07="
            + data[-8]
            + ", A2_drr_lvl_1_cover_08="
            + data[-9]
            + ", A2_drr_lvl_1_cover_09="
            + data[-10]
            + ", A2_drr_lvl_1_cover_10="
            + data[-11]
            + ", A2_drr_lvl_1_cover_11="
            + data[-12]
            + ", A2_drr_lvl_1_cover_12="
            + data[-13]
            + ", A2_drr_lvl_1_cover_13="
            + data[-14]
            + ", A2_drr_lvl_1_cover_14="
            + data[-15]
            + ", A2_drr_lvl_1_cover_15="
            + data[-16]
    )


def SCHED_RATE_MAX_CREDITS(data):
    if "=" in data:
        A2_max_rate_cost_credit_value = data.split("A2_max_rate_cost_credit_value=")[1]
        A2_max_rate_cost_credit_value = hex_to_bin(A2_max_rate_cost_credit_value)
        A2_max_rate_cost_credit_value = format_data_length(A2_max_rate_cost_credit_value, 20)
        data_value = A2_max_rate_cost_credit_value
        data_value = format_hex_value(data_value)
        return data_value
    return (
            ":: A2_max_rate_cost_credit_value="
            + data[-20:]
    )


def SCHED_CONFIG_1(data):
    if "=" in data:
        A2_sched_clr_state_tbls = data.split("A2_sched_clr_state_tbls=")[1].split(',')[0]
        A2_sched_clr_state_tbls = hex_to_bin(A2_sched_clr_state_tbls)
        A2_dis_sched_pipeline = data.split("A2_dis_sched_pipeline=")[1]
        A2_dis_sched_pipeline = hex_to_bin(A2_dis_sched_pipeline)
        data_value = A2_dis_sched_pipeline + A2_sched_clr_state_tbls
        data_value = format_hex_value(data_value)
        return data_value
    return (
            ":: A2_sched_clr_state_tbls="
            + data[-1]
            + ", A2_dis_sched_pipeline="
            + data[-2]
    )


def SCHED_RESET_DONE_STATUS_REG(data):
    if "=" in data:
        A2_src_comp_reset_done = data.split("A2_src_comp_reset_done=")[1].split(',')[0]
        A2_src_comp_reset_done = hex_to_bin(A2_src_comp_reset_done)
        A2_rate_comp_lvl_0_reset_done = data.split("A2_rate_comp_lvl_0_reset_done=")[1].split(',')[0]
        A2_rate_comp_lvl_0_reset_done = hex_to_bin(A2_rate_comp_lvl_0_reset_done)
        A2_drr_comp_lvl_0_reset_done = data.split("A2_drr_comp_lvl_0_reset_done=")[1].split(',')[0]
        A2_drr_comp_lvl_0_reset_done = hex_to_bin(A2_drr_comp_lvl_0_reset_done)
        A2_iclass0_comp_lvl_0_reset_done = data.split("A2_iclass0_comp_lvl_0_reset_done=")[1].split(',')[0]
        A2_iclass0_comp_lvl_0_reset_done = hex_to_bin(A2_iclass0_comp_lvl_0_reset_done)
        A2_iclass1_comp_lvl_0_reset_done = data.split("A2_iclass1_comp_lvl_0_reset_done=")[1].split(',')[0]
        A2_iclass1_comp_lvl_0_reset_done = hex_to_bin(A2_iclass1_comp_lvl_0_reset_done)
        A2_iclass2_comp_lvl_0_reset_done = data.split("A2_iclass2_comp_lvl_0_reset_done=")[1].split(',')[0]
        A2_iclass2_comp_lvl_0_reset_done = hex_to_bin(A2_iclass2_comp_lvl_0_reset_done)
        A2_prio_comp_lvl_0_reset_done = data.split("A2_prio_comp_lvl_0_reset_done=")[1].split(',')[0]
        A2_prio_comp_lvl_0_reset_done = hex_to_bin(A2_prio_comp_lvl_0_reset_done)
        A2_dest_comp_lvl_0_reset_done = data.split("A2_dest_comp_lvl_0_reset_done=")[1].split(',')[0]
        A2_dest_comp_lvl_0_reset_done = hex_to_bin(A2_dest_comp_lvl_0_reset_done)
        A2_rate_comp_lvl_1_reset_done = data.split("A2_rate_comp_lvl_1_reset_done=")[1].split(',')[0]
        A2_rate_comp_lvl_1_reset_done = hex_to_bin(A2_rate_comp_lvl_1_reset_done)
        A2_drr_comp_lvl_1_reset_done = data.split("A2_drr_comp_lvl_1_reset_done=")[1].split(',')[0]
        A2_drr_comp_lvl_1_reset_done = hex_to_bin(A2_drr_comp_lvl_1_reset_done)
        A2_iclass0_comp_lvl_1_reset_done = data.split("A2_iclass0_comp_lvl_1_reset_done=")[1].split(',')[0]
        A2_iclass0_comp_lvl_1_reset_done = hex_to_bin(A2_iclass0_comp_lvl_1_reset_done)
        A2_iclass1_comp_lvl_1_reset_done = data.split("A2_iclass1_comp_lvl_1_reset_done=")[1].split(',')[0]
        A2_iclass1_comp_lvl_1_reset_done = hex_to_bin(A2_iclass1_comp_lvl_1_reset_done)
        A2_iclass2_comp_lvl_1_reset_done = data.split("A2_iclass2_comp_lvl_1_reset_done=")[1].split(',')[0]
        A2_iclass2_comp_lvl_1_reset_done = hex_to_bin(A2_iclass2_comp_lvl_1_reset_done)
        A2_prio_comp_lvl_1_reset_done = data.split("A2_prio_comp_lvl_1_reset_done=")[1].split(',')[0]
        A2_prio_comp_lvl_1_reset_done = hex_to_bin(A2_prio_comp_lvl_1_reset_done)
        A2_dest_comp_lvl_1_reset_done = data.split("A2_dest_comp_lvl_1_reset_done=")[1].split(',')[0]
        A2_dest_comp_lvl_1_reset_done = hex_to_bin(A2_dest_comp_lvl_1_reset_done)
        A2_rate_comp_lvl_2_reset_done = data.split("A2_rate_comp_lvl_2_reset_done=")[1].split(',')[0]
        A2_rate_comp_lvl_2_reset_done = hex_to_bin(A2_rate_comp_lvl_2_reset_done)
        A2_drr_comp_lvl_2_reset_done = data.split("A2_drr_comp_lvl_2_reset_done=")[1].split(',')[0]
        A2_drr_comp_lvl_2_reset_done = hex_to_bin(A2_drr_comp_lvl_2_reset_done)
        A2_iclass0_comp_lvl_2_reset_done = data.split("A2_iclass0_comp_lvl_2_reset_done=")[1].split(',')[0]
        A2_iclass0_comp_lvl_2_reset_done = hex_to_bin(A2_iclass0_comp_lvl_2_reset_done)
        A2_iclass1_comp_lvl_2_reset_done = data.split("A2_iclass1_comp_lvl_2_reset_done=")[1].split(',')[0]
        A2_iclass1_comp_lvl_2_reset_done = hex_to_bin(A2_iclass1_comp_lvl_2_reset_done)
        A2_iclass2_comp_lvl_2_reset_done = data.split("A2_iclass2_comp_lvl_2_reset_done=")[1].split(',')[0]
        A2_iclass2_comp_lvl_2_reset_done = hex_to_bin(A2_iclass2_comp_lvl_2_reset_done)
        A2_prio_comp_lvl_2_reset_done = data.split("A2_prio_comp_lvl_2_reset_done=")[1].split(',')[0]
        A2_prio_comp_lvl_2_reset_done = hex_to_bin(A2_prio_comp_lvl_2_reset_done)
        A2_dest_comp_lvl_2_reset_done = data.split("A2_dest_comp_lvl_2_reset_done=")[1].split(',')[0]
        A2_dest_comp_lvl_2_reset_done = hex_to_bin(A2_dest_comp_lvl_2_reset_done)
        A2_rate_comp_lvl_3_reset_done = data.split("A2_rate_comp_lvl_3_reset_done=")[1].split(',')[0]
        A2_rate_comp_lvl_3_reset_done = hex_to_bin(A2_rate_comp_lvl_3_reset_done)
        A2_drr_comp_lvl_3_reset_done = data.split("A2_drr_comp_lvl_3_reset_done=")[1].split(',')[0]
        A2_drr_comp_lvl_3_reset_done = hex_to_bin(A2_drr_comp_lvl_3_reset_done)
        A2_iclass0_comp_lvl_3_reset_done = data.split("A2_iclass0_comp_lvl_3_reset_done=")[1].split(',')[0]
        A2_iclass0_comp_lvl_3_reset_done = hex_to_bin(A2_iclass0_comp_lvl_3_reset_done)
        A2_iclass1_comp_lvl_3_reset_done = data.split("A2_iclass1_comp_lvl_3_reset_done=")[1].split(',')[0]
        A2_iclass1_comp_lvl_3_reset_done = hex_to_bin(A2_iclass1_comp_lvl_3_reset_done)
        A2_iclass2_comp_lvl_3_reset_done = data.split("A2_iclass2_comp_lvl_3_reset_done=")[1].split(',')[0]
        A2_iclass2_comp_lvl_3_reset_done = hex_to_bin(A2_iclass2_comp_lvl_3_reset_done)
        A2_prio_comp_lvl_3_reset_done = data.split("A2_prio_comp_lvl_3_reset_done=")[1].split(',')[0]
        A2_prio_comp_lvl_3_reset_done = hex_to_bin(A2_prio_comp_lvl_3_reset_done)
        A2_dest_comp_lvl_3_reset_done = data.split("A2_dest_comp_lvl_3_reset_done=")[1].split(',')[0]
        A2_dest_comp_lvl_3_reset_done = hex_to_bin(A2_dest_comp_lvl_3_reset_done)
        A2_default_reset_done = data.split("A2_default_reset_done=")[1].split(',')[0]
        A2_default_reset_done = hex_to_bin(A2_default_reset_done)
        A2_default_reset_done = format_data_length(A2_default_reset_done, 3)
        data_value = A2_default_reset_done + A2_dest_comp_lvl_3_reset_done + A2_prio_comp_lvl_3_reset_done + A2_iclass2_comp_lvl_3_reset_done + A2_iclass1_comp_lvl_3_reset_done + A2_iclass0_comp_lvl_3_reset_done + A2_drr_comp_lvl_3_reset_done + A2_rate_comp_lvl_3_reset_done + A2_dest_comp_lvl_2_reset_done + A2_prio_comp_lvl_2_reset_done + A2_iclass2_comp_lvl_2_reset_done + A2_iclass1_comp_lvl_2_reset_done + A2_iclass0_comp_lvl_2_reset_done + A2_drr_comp_lvl_2_reset_done + A2_rate_comp_lvl_2_reset_done + A2_dest_comp_lvl_1_reset_done + A2_prio_comp_lvl_1_reset_done + A2_iclass2_comp_lvl_1_reset_done + A2_iclass1_comp_lvl_1_reset_done + A2_iclass0_comp_lvl_1_reset_done + A2_drr_comp_lvl_1_reset_done + A2_rate_comp_lvl_1_reset_done + A2_dest_comp_lvl_0_reset_done + A2_prio_comp_lvl_0_reset_done + A2_iclass2_comp_lvl_0_reset_done + A2_iclass1_comp_lvl_0_reset_done + A2_iclass0_comp_lvl_0_reset_done + A2_drr_comp_lvl_0_reset_done + A2_rate_comp_lvl_0_reset_done + A2_src_comp_reset_done
        data_value = format_hex_value(data_value)
        return data_value
    return (
            ":: A2_src_comp_reset_done="
            + data[-1]
            + ", A2_rate_comp_lvl_0_reset_done="
            + data[-2]
            + ", A2_drr_comp_lvl_0_reset_done="
            + data[-3]
            + ", A2_iclass0_comp_lvl_0_reset_done="
            + data[-4]
            + ", A2_iclass1_comp_lvl_0_reset_done="
            + data[-5]
            + ", A2_iclass2_comp_lvl_0_reset_done="
            + data[-6]
            + ", A2_prio_comp_lvl_0_reset_done="
            + data[-7]
            + ", A2_dest_comp_lvl_0_reset_done="
            + data[-8]
            + ", A2_rate_comp_lvl_1_reset_done="
            + data[-9]
            + ", A2_drr_comp_lvl_1_reset_done="
            + data[-10]
            + ", A2_iclass0_comp_lvl_1_reset_done="
            + data[-11]
            + ", A2_iclass1_comp_lvl_1_reset_done="
            + data[-12]
            + ", A2_iclass2_comp_lvl_1_reset_done="
            + data[-13]
            + ", A2_prio_comp_lvl_1_reset_done="
            + data[-14]
            + ", A2_dest_comp_lvl_1_reset_done="
            + data[-15]
            + ", A2_rate_comp_lvl_2_reset_done="
            + data[-16]
            + ", A2_drr_comp_lvl_2_reset_done="
            + data[-17]
            + ", A2_iclass0_comp_lvl_2_reset_done="
            + data[-18]
            + ", A2_iclass1_comp_lvl_2_reset_done="
            + data[-19]
            + ", A2_iclass2_comp_lvl_2_reset_done="
            + data[-20]
            + ", A2_prio_comp_lvl_2_reset_done="
            + data[-21]
            + ", A2_dest_comp_lvl_2_reset_done="
            + data[-22]
            + ", A2_rate_comp_lvl_3_reset_done="
            + data[-23]
            + ", A2_drr_comp_lvl_3_reset_done="
            + data[-24]
            + ", A2_iclass0_comp_lvl_3_reset_done="
            + data[-25]
            + ", A2_iclass1_comp_lvl_3_reset_done="
            + data[-26]
            + ", A2_iclass2_comp_lvl_3_reset_done="
            + data[-27]
            + ", A2_prio_comp_lvl_3_reset_done="
            + data[-28]
            + ", A2_dest_comp_lvl_3_reset_done="
            + data[-29]
            + ", A2_default_reset_done="
            + data[-32:-29]
    )


def SCHED_ECC_CERR_STATUS_REG(data):
    if "=" in data:
        A2_src_comp_ecc_cerr = data.split("A2_src_comp_ecc_cerr=")[1].split(',')[0]
        A2_src_comp_ecc_cerr = hex_to_bin(A2_src_comp_ecc_cerr)
        A2_rate_comp_lvl_0_ecc_cerr = data.split("A2_rate_comp_lvl_0_ecc_cerr=")[1].split(',')[0]
        A2_rate_comp_lvl_0_ecc_cerr = hex_to_bin(A2_rate_comp_lvl_0_ecc_cerr)
        A2_drr_comp_lvl_0_ecc_cerr = data.split("A2_drr_comp_lvl_0_ecc_cerr=")[1].split(',')[0]
        A2_drr_comp_lvl_0_ecc_cerr = hex_to_bin(A2_drr_comp_lvl_0_ecc_cerr)
        A2_iclass0_comp_lvl_0_ecc_cerr = data.split("A2_iclass0_comp_lvl_0_ecc_cerr=")[1].split(',')[0]
        A2_iclass0_comp_lvl_0_ecc_cerr = hex_to_bin(A2_iclass0_comp_lvl_0_ecc_cerr)
        A2_iclass1_comp_lvl_0_ecc_cerr = data.split("A2_iclass1_comp_lvl_0_ecc_cerr=")[1].split(',')[0]
        A2_iclass1_comp_lvl_0_ecc_cerr = hex_to_bin(A2_iclass1_comp_lvl_0_ecc_cerr)
        A2_iclass2_comp_lvl_0_ecc_cerr = data.split("A2_iclass2_comp_lvl_0_ecc_cerr=")[1].split(',')[0]
        A2_iclass2_comp_lvl_0_ecc_cerr = hex_to_bin(A2_iclass2_comp_lvl_0_ecc_cerr)
        A2_prio_comp_lvl_0_ecc_cerr = data.split("A2_prio_comp_lvl_0_ecc_cerr=")[1].split(',')[0]
        A2_prio_comp_lvl_0_ecc_cerr = hex_to_bin(A2_prio_comp_lvl_0_ecc_cerr)
        A2_dest_comp_lvl_0_ecc_cerr = data.split("A2_dest_comp_lvl_0_ecc_cerr=")[1].split(',')[0]
        A2_dest_comp_lvl_0_ecc_cerr = hex_to_bin(A2_dest_comp_lvl_0_ecc_cerr)
        A2_rate_comp_lvl_1_ecc_cerr = data.split("A2_rate_comp_lvl_1_ecc_cerr=")[1].split(',')[0]
        A2_rate_comp_lvl_1_ecc_cerr = hex_to_bin(A2_rate_comp_lvl_1_ecc_cerr)
        A2_drr_comp_lvl_1_ecc_cerr = data.split("A2_drr_comp_lvl_1_ecc_cerr=")[1].split(',')[0]
        A2_drr_comp_lvl_1_ecc_cerr = hex_to_bin(A2_drr_comp_lvl_1_ecc_cerr)
        A2_iclass0_comp_lvl_1_ecc_cerr = data.split("A2_iclass0_comp_lvl_1_ecc_cerr=")[1].split(',')[0]
        A2_iclass0_comp_lvl_1_ecc_cerr = hex_to_bin(A2_iclass0_comp_lvl_1_ecc_cerr)
        A2_iclass1_comp_lvl_1_ecc_cerr = data.split("A2_iclass1_comp_lvl_1_ecc_cerr=")[1].split(',')[0]
        A2_iclass1_comp_lvl_1_ecc_cerr = hex_to_bin(A2_iclass1_comp_lvl_1_ecc_cerr)
        A2_iclass2_comp_lvl_1_ecc_cerr = data.split("A2_iclass2_comp_lvl_1_ecc_cerr=")[1].split(',')[0]
        A2_iclass2_comp_lvl_1_ecc_cerr = hex_to_bin(A2_iclass2_comp_lvl_1_ecc_cerr)
        A2_prio_comp_lvl_1_ecc_cerr = data.split("A2_prio_comp_lvl_1_ecc_cerr=")[1].split(',')[0]
        A2_prio_comp_lvl_1_ecc_cerr = hex_to_bin(A2_prio_comp_lvl_1_ecc_cerr)
        A2_dest_comp_lvl_1_ecc_cerr = data.split("A2_dest_comp_lvl_1_ecc_cerr=")[1].split(',')[0]
        A2_dest_comp_lvl_1_ecc_cerr = hex_to_bin(A2_dest_comp_lvl_1_ecc_cerr)
        A2_rate_comp_lvl_2_ecc_cerr = data.split("A2_rate_comp_lvl_2_ecc_cerr=")[1].split(',')[0]
        A2_rate_comp_lvl_2_ecc_cerr = hex_to_bin(A2_rate_comp_lvl_2_ecc_cerr)
        A2_drr_comp_lvl_2_ecc_cerr = data.split("A2_drr_comp_lvl_2_ecc_cerr=")[1].split(',')[0]
        A2_drr_comp_lvl_2_ecc_cerr = hex_to_bin(A2_drr_comp_lvl_2_ecc_cerr)
        A2_iclass0_comp_lvl_2_ecc_cerr = data.split("A2_iclass0_comp_lvl_2_ecc_cerr=")[1].split(',')[0]
        A2_iclass0_comp_lvl_2_ecc_cerr = hex_to_bin(A2_iclass0_comp_lvl_2_ecc_cerr)
        A2_iclass1_comp_lvl_2_ecc_cerr = data.split("A2_iclass1_comp_lvl_2_ecc_cerr=")[1].split(',')[0]
        A2_iclass1_comp_lvl_2_ecc_cerr = hex_to_bin(A2_iclass1_comp_lvl_2_ecc_cerr)
        A2_iclass2_comp_lvl_2_ecc_cerr = data.split("A2_iclass2_comp_lvl_2_ecc_cerr=")[1].split(',')[0]
        A2_iclass2_comp_lvl_2_ecc_cerr = hex_to_bin(A2_iclass2_comp_lvl_2_ecc_cerr)
        A2_prio_comp_lvl_2_ecc_cerr = data.split("A2_prio_comp_lvl_2_ecc_cerr=")[1].split(',')[0]
        A2_prio_comp_lvl_2_ecc_cerr = hex_to_bin(A2_prio_comp_lvl_2_ecc_cerr)
        A2_dest_comp_lvl_2_ecc_cerr = data.split("A2_dest_comp_lvl_2_ecc_cerr=")[1].split(',')[0]
        A2_dest_comp_lvl_2_ecc_cerr = hex_to_bin(A2_dest_comp_lvl_2_ecc_cerr)
        A2_rate_comp_lvl_3_ecc_cerr = data.split("A2_rate_comp_lvl_3_ecc_cerr=")[1].split(',')[0]
        A2_rate_comp_lvl_3_ecc_cerr = hex_to_bin(A2_rate_comp_lvl_3_ecc_cerr)
        A2_drr_comp_lvl_3_ecc_cerr = data.split("A2_drr_comp_lvl_3_ecc_cerr=")[1].split(',')[0]
        A2_drr_comp_lvl_3_ecc_cerr = hex_to_bin(A2_drr_comp_lvl_3_ecc_cerr)
        A2_iclass0_comp_lvl_3_ecc_cerr = data.split("A2_iclass0_comp_lvl_3_ecc_cerr=")[1].split(',')[0]
        A2_iclass0_comp_lvl_3_ecc_cerr = hex_to_bin(A2_iclass0_comp_lvl_3_ecc_cerr)
        A2_iclass1_comp_lvl_3_ecc_cerr = data.split("A2_iclass1_comp_lvl_3_ecc_cerr=")[1].split(',')[0]
        A2_iclass1_comp_lvl_3_ecc_cerr = hex_to_bin(A2_iclass1_comp_lvl_3_ecc_cerr)
        A2_iclass2_comp_lvl_3_ecc_cerr = data.split("A2_iclass2_comp_lvl_3_ecc_cerr=")[1].split(',')[0]
        A2_iclass2_comp_lvl_3_ecc_cerr = hex_to_bin(A2_iclass2_comp_lvl_3_ecc_cerr)
        A2_prio_comp_lvl_3_ecc_cerr = data.split("A2_prio_comp_lvl_3_ecc_cerr=")[1]
        A2_prio_comp_lvl_3_ecc_cerr = hex_to_bin(A2_prio_comp_lvl_3_ecc_cerr)
        data_value = A2_prio_comp_lvl_3_ecc_cerr + A2_iclass2_comp_lvl_3_ecc_cerr + A2_iclass1_comp_lvl_3_ecc_cerr + A2_iclass0_comp_lvl_3_ecc_cerr + A2_drr_comp_lvl_3_ecc_cerr + A2_rate_comp_lvl_3_ecc_cerr + A2_dest_comp_lvl_2_ecc_cerr + A2_prio_comp_lvl_2_ecc_cerr + A2_iclass2_comp_lvl_2_ecc_cerr + A2_iclass1_comp_lvl_2_ecc_cerr + A2_iclass0_comp_lvl_2_ecc_cerr + A2_drr_comp_lvl_2_ecc_cerr + A2_rate_comp_lvl_2_ecc_cerr + A2_dest_comp_lvl_1_ecc_cerr + A2_prio_comp_lvl_1_ecc_cerr + A2_iclass2_comp_lvl_1_ecc_cerr + A2_iclass1_comp_lvl_1_ecc_cerr + A2_iclass0_comp_lvl_1_ecc_cerr + A2_drr_comp_lvl_1_ecc_cerr + A2_rate_comp_lvl_1_ecc_cerr + A2_dest_comp_lvl_0_ecc_cerr + A2_prio_comp_lvl_0_ecc_cerr + A2_iclass2_comp_lvl_0_ecc_cerr + A2_iclass1_comp_lvl_0_ecc_cerr + A2_iclass0_comp_lvl_0_ecc_cerr + A2_drr_comp_lvl_0_ecc_cerr + A2_rate_comp_lvl_0_ecc_cerr + A2_src_comp_ecc_cerr
        data_value = format_hex_value(data_value)
        return data_value
    return (
            ":: A2_src_comp_ecc_cerr="
            + data[-1]
            + ", A2_rate_comp_lvl_0_ecc_cerr="
            + data[-2]
            + ", A2_drr_comp_lvl_0_ecc_cerr="
            + data[-3]
            + ", A2_iclass0_comp_lvl_0_ecc_cerr="
            + data[-4]
            + ", A2_iclass1_comp_lvl_0_ecc_cerr="
            + data[-5]
            + ", A2_iclass2_comp_lvl_0_ecc_cerr="
            + data[-6]
            + ", A2_prio_comp_lvl_0_ecc_cerr="
            + data[-7]
            + ", A2_dest_comp_lvl_0_ecc_cerr="
            + data[-8]
            + ", A2_rate_comp_lvl_1_ecc_cerr="
            + data[-9]
            + ", A2_drr_comp_lvl_1_ecc_cerr="
            + data[-10]
            + ", A2_iclass0_comp_lvl_1_ecc_cerr="
            + data[-11]
            + ", A2_iclass1_comp_lvl_1_ecc_cerr="
            + data[-12]
            + ", A2_iclass2_comp_lvl_1_ecc_cerr="
            + data[-13]
            + ", A2_prio_comp_lvl_1_ecc_cerr="
            + data[-14]
            + ", A2_dest_comp_lvl_1_ecc_cerr="
            + data[-15]
            + ", A2_rate_comp_lvl_2_ecc_cerr="
            + data[-16]
            + ", A2_drr_comp_lvl_2_ecc_cerr="
            + data[-17]
            + ", A2_iclass0_comp_lvl_2_ecc_cerr="
            + data[-18]
            + ", A2_iclass1_comp_lvl_2_ecc_cerr="
            + data[-19]
            + ", A2_iclass2_comp_lvl_2_ecc_cerr="
            + data[-20]
            + ", A2_prio_comp_lvl_2_ecc_cerr="
            + data[-21]
            + ", A2_dest_comp_lvl_2_ecc_cerr="
            + data[-22]
            + ", A2_rate_comp_lvl_3_ecc_cerr="
            + data[-23]
            + ", A2_drr_comp_lvl_3_ecc_cerr="
            + data[-24]
            + ", A2_iclass0_comp_lvl_3_ecc_cerr="
            + data[-25]
            + ", A2_iclass1_comp_lvl_3_ecc_cerr="
            + data[-26]
            + ", A2_iclass2_comp_lvl_3_ecc_cerr="
            + data[-27]
            + ", A2_prio_comp_lvl_3_ecc_cerr="
            + data[-28]
    )


def SCHED_ECC_UCERR_STATUS_REG(data):
    if "=" in data:
        A2_src_comp_ecc_ucerr = data.split("A2_src_comp_ecc_ucerr=")[1].split(',')[0]
        A2_src_comp_ecc_ucerr = hex_to_bin(A2_src_comp_ecc_ucerr)
        A2_rate_comp_lvl_0_ecc_ucerr = data.split("A2_rate_comp_lvl_0_ecc_ucerr=")[1].split(',')[0]
        A2_rate_comp_lvl_0_ecc_ucerr = hex_to_bin(A2_rate_comp_lvl_0_ecc_ucerr)
        A2_drr_comp_lvl_0_ecc_ucerr = data.split("A2_drr_comp_lvl_0_ecc_ucerr=")[1].split(',')[0]
        A2_drr_comp_lvl_0_ecc_ucerr = hex_to_bin(A2_drr_comp_lvl_0_ecc_ucerr)
        A2_iclass0_comp_lvl_0_ecc_ucerr = data.split("A2_iclass0_comp_lvl_0_ecc_ucerr=")[1].split(',')[0]
        A2_iclass0_comp_lvl_0_ecc_ucerr = hex_to_bin(A2_iclass0_comp_lvl_0_ecc_ucerr)
        A2_iclass1_comp_lvl_0_ecc_ucerr = data.split("A2_iclass1_comp_lvl_0_ecc_ucerr=")[1].split(',')[0]
        A2_iclass1_comp_lvl_0_ecc_ucerr = hex_to_bin(A2_iclass1_comp_lvl_0_ecc_ucerr)
        A2_iclass2_comp_lvl_0_ecc_ucerr = data.split("A2_iclass2_comp_lvl_0_ecc_ucerr=")[1].split(',')[0]
        A2_iclass2_comp_lvl_0_ecc_ucerr = hex_to_bin(A2_iclass2_comp_lvl_0_ecc_ucerr)
        A2_prio_comp_lvl_0_ecc_ucerr = data.split("A2_prio_comp_lvl_0_ecc_ucerr=")[1].split(',')[0]
        A2_prio_comp_lvl_0_ecc_ucerr = hex_to_bin(A2_prio_comp_lvl_0_ecc_ucerr)
        A2_dest_comp_lvl_0_ecc_ucerr = data.split("A2_dest_comp_lvl_0_ecc_ucerr=")[1].split(',')[0]
        A2_dest_comp_lvl_0_ecc_ucerr = hex_to_bin(A2_dest_comp_lvl_0_ecc_ucerr)
        A2_rate_comp_lvl_1_ecc_ucerr = data.split("A2_rate_comp_lvl_1_ecc_ucerr=")[1].split(',')[0]
        A2_rate_comp_lvl_1_ecc_ucerr = hex_to_bin(A2_rate_comp_lvl_1_ecc_ucerr)
        A2_drr_comp_lvl_1_ecc_ucerr = data.split("A2_drr_comp_lvl_1_ecc_ucerr=")[1].split(',')[0]
        A2_drr_comp_lvl_1_ecc_ucerr = hex_to_bin(A2_drr_comp_lvl_1_ecc_ucerr)
        A2_iclass0_comp_lvl_1_ecc_ucerr = data.split("A2_iclass0_comp_lvl_1_ecc_ucerr=")[1].split(',')[0]
        A2_iclass0_comp_lvl_1_ecc_ucerr = hex_to_bin(A2_iclass0_comp_lvl_1_ecc_ucerr)
        A2_iclass1_comp_lvl_1_ecc_ucerr = data.split("A2_iclass1_comp_lvl_1_ecc_ucerr=")[1].split(',')[0]
        A2_iclass1_comp_lvl_1_ecc_ucerr = hex_to_bin(A2_iclass1_comp_lvl_1_ecc_ucerr)
        A2_iclass2_comp_lvl_1_ecc_ucerr = data.split("A2_iclass2_comp_lvl_1_ecc_ucerr=")[1].split(',')[0]
        A2_iclass2_comp_lvl_1_ecc_ucerr = hex_to_bin(A2_iclass2_comp_lvl_1_ecc_ucerr)
        A2_prio_comp_lvl_1_ecc_ucerr = data.split("A2_prio_comp_lvl_1_ecc_ucerr=")[1].split(',')[0]
        A2_prio_comp_lvl_1_ecc_ucerr = hex_to_bin(A2_prio_comp_lvl_1_ecc_ucerr)
        A2_dest_comp_lvl_1_ecc_ucerr = data.split("A2_dest_comp_lvl_1_ecc_ucerr=")[1].split(',')[0]
        A2_dest_comp_lvl_1_ecc_ucerr = hex_to_bin(A2_dest_comp_lvl_1_ecc_ucerr)
        A2_rate_comp_lvl_2_ecc_ucerr = data.split("A2_rate_comp_lvl_2_ecc_ucerr=")[1].split(',')[0]
        A2_rate_comp_lvl_2_ecc_ucerr = hex_to_bin(A2_rate_comp_lvl_2_ecc_ucerr)
        A2_drr_comp_lvl_2_ecc_ucerr = data.split("A2_drr_comp_lvl_2_ecc_ucerr=")[1].split(',')[0]
        A2_drr_comp_lvl_2_ecc_ucerr = hex_to_bin(A2_drr_comp_lvl_2_ecc_ucerr)
        A2_iclass0_comp_lvl_2_ecc_ucerr = data.split("A2_iclass0_comp_lvl_2_ecc_ucerr=")[1].split(',')[0]
        A2_iclass0_comp_lvl_2_ecc_ucerr = hex_to_bin(A2_iclass0_comp_lvl_2_ecc_ucerr)
        A2_iclass1_comp_lvl_2_ecc_ucerr = data.split("A2_iclass1_comp_lvl_2_ecc_ucerr=")[1].split(',')[0]
        A2_iclass1_comp_lvl_2_ecc_ucerr = hex_to_bin(A2_iclass1_comp_lvl_2_ecc_ucerr)
        A2_iclass2_comp_lvl_2_ecc_ucerr = data.split("A2_iclass2_comp_lvl_2_ecc_ucerr=")[1].split(',')[0]
        A2_iclass2_comp_lvl_2_ecc_ucerr = hex_to_bin(A2_iclass2_comp_lvl_2_ecc_ucerr)
        A2_prio_comp_lvl_2_ecc_ucerr = data.split("A2_prio_comp_lvl_2_ecc_ucerr=")[1].split(',')[0]
        A2_prio_comp_lvl_2_ecc_ucerr = hex_to_bin(A2_prio_comp_lvl_2_ecc_ucerr)
        A2_dest_comp_lvl_2_ecc_ucerr = data.split("A2_dest_comp_lvl_2_ecc_ucerr=")[1].split(',')[0]
        A2_dest_comp_lvl_2_ecc_ucerr = hex_to_bin(A2_dest_comp_lvl_2_ecc_ucerr)
        A2_rate_comp_lvl_3_ecc_ucerr = data.split("A2_rate_comp_lvl_3_ecc_ucerr=")[1].split(',')[0]
        A2_rate_comp_lvl_3_ecc_ucerr = hex_to_bin(A2_rate_comp_lvl_3_ecc_ucerr)
        A2_drr_comp_lvl_3_ecc_ucerr = data.split("A2_drr_comp_lvl_3_ecc_ucerr=")[1].split(',')[0]
        A2_drr_comp_lvl_3_ecc_ucerr = hex_to_bin(A2_drr_comp_lvl_3_ecc_ucerr)
        A2_iclass0_comp_lvl_3_ecc_ucerr = data.split("A2_iclass0_comp_lvl_3_ecc_ucerr=")[1].split(',')[0]
        A2_iclass0_comp_lvl_3_ecc_ucerr = hex_to_bin(A2_iclass0_comp_lvl_3_ecc_ucerr)
        A2_iclass1_comp_lvl_3_ecc_ucerr = data.split("A2_iclass1_comp_lvl_3_ecc_ucerr=")[1].split(',')[0]
        A2_iclass1_comp_lvl_3_ecc_ucerr = hex_to_bin(A2_iclass1_comp_lvl_3_ecc_ucerr)
        A2_iclass2_comp_lvl_3_ecc_ucerr = data.split("A2_iclass2_comp_lvl_3_ecc_ucerr=")[1].split(',')[0]
        A2_iclass2_comp_lvl_3_ecc_ucerr = hex_to_bin(A2_iclass2_comp_lvl_3_ecc_ucerr)
        A2_prio_comp_lvl_3_ecc_ucerr = data.split("A2_prio_comp_lvl_3_ecc_ucerr=")[1]
        A2_prio_comp_lvl_3_ecc_ucerr = hex_to_bin(A2_prio_comp_lvl_3_ecc_ucerr)
        data_value = A2_prio_comp_lvl_3_ecc_ucerr + A2_iclass2_comp_lvl_3_ecc_ucerr + A2_iclass1_comp_lvl_3_ecc_ucerr + A2_iclass0_comp_lvl_3_ecc_ucerr + A2_drr_comp_lvl_3_ecc_ucerr + A2_rate_comp_lvl_3_ecc_ucerr + A2_dest_comp_lvl_2_ecc_ucerr + A2_prio_comp_lvl_2_ecc_ucerr + A2_iclass2_comp_lvl_2_ecc_ucerr + A2_iclass1_comp_lvl_2_ecc_ucerr + A2_iclass0_comp_lvl_2_ecc_ucerr + A2_drr_comp_lvl_2_ecc_ucerr + A2_rate_comp_lvl_2_ecc_ucerr + A2_dest_comp_lvl_1_ecc_ucerr + A2_prio_comp_lvl_1_ecc_ucerr + A2_iclass2_comp_lvl_1_ecc_ucerr + A2_iclass1_comp_lvl_1_ecc_ucerr + A2_iclass0_comp_lvl_1_ecc_ucerr + A2_drr_comp_lvl_1_ecc_ucerr + A2_rate_comp_lvl_1_ecc_ucerr + A2_dest_comp_lvl_0_ecc_ucerr + A2_prio_comp_lvl_0_ecc_ucerr + A2_iclass2_comp_lvl_0_ecc_ucerr + A2_iclass1_comp_lvl_0_ecc_ucerr + A2_iclass0_comp_lvl_0_ecc_ucerr + A2_drr_comp_lvl_0_ecc_ucerr + A2_rate_comp_lvl_0_ecc_ucerr + A2_src_comp_ecc_ucerr
        data_value = format_hex_value(data_value)
        return data_value
    return (
            ":: A2_src_comp_ecc_ucerr="
            + data[-1]
            + ", A2_rate_comp_lvl_0_ecc_ucerr="
            + data[-2]
            + ", A2_drr_comp_lvl_0_ecc_ucerr="
            + data[-3]
            + ", A2_iclass0_comp_lvl_0_ecc_ucerr="
            + data[-4]
            + ", A2_iclass1_comp_lvl_0_ecc_ucerr="
            + data[-5]
            + ", A2_iclass2_comp_lvl_0_ecc_ucerr="
            + data[-6]
            + ", A2_prio_comp_lvl_0_ecc_ucerr="
            + data[-7]
            + ", A2_dest_comp_lvl_0_ecc_ucerr="
            + data[-8]
            + ", A2_rate_comp_lvl_1_ecc_ucerr="
            + data[-9]
            + ", A2_drr_comp_lvl_1_ecc_ucerr="
            + data[-10]
            + ", A2_iclass0_comp_lvl_1_ecc_ucerr="
            + data[-11]
            + ", A2_iclass1_comp_lvl_1_ecc_ucerr="
            + data[-12]
            + ", A2_iclass2_comp_lvl_1_ecc_ucerr="
            + data[-13]
            + ", A2_prio_comp_lvl_1_ecc_ucerr="
            + data[-14]
            + ", A2_dest_comp_lvl_1_ecc_ucerr="
            + data[-15]
            + ", A2_rate_comp_lvl_2_ecc_ucerr="
            + data[-16]
            + ", A2_drr_comp_lvl_2_ecc_ucerr="
            + data[-17]
            + ", A2_iclass0_comp_lvl_2_ecc_ucerr="
            + data[-18]
            + ", A2_iclass1_comp_lvl_2_ecc_ucerr="
            + data[-19]
            + ", A2_iclass2_comp_lvl_2_ecc_ucerr="
            + data[-20]
            + ", A2_prio_comp_lvl_2_ecc_ucerr="
            + data[-21]
            + ", A2_dest_comp_lvl_2_ecc_ucerr="
            + data[-22]
            + ", A2_rate_comp_lvl_3_ecc_ucerr="
            + data[-23]
            + ", A2_drr_comp_lvl_3_ecc_ucerr="
            + data[-24]
            + ", A2_iclass0_comp_lvl_3_ecc_ucerr="
            + data[-25]
            + ", A2_iclass1_comp_lvl_3_ecc_ucerr="
            + data[-26]
            + ", A2_iclass2_comp_lvl_3_ecc_ucerr="
            + data[-27]
            + ", A2_prio_comp_lvl_3_ecc_ucerr="
            + data[-28]
    )


def SCHED_MON_DEST_ID(data):
    if "=" in data:
        A2_sched_mon_dest_id_1 = data.split("A2_sched_mon_dest_id_1=")[1].split(
            ","
        )[0]
        A2_sched_mon_dest_id_1 = hex_to_bin(A2_sched_mon_dest_id_1)
        A2_sched_mon_dest_id_1 = format_data_length(A2_sched_mon_dest_id_1, 6)
        A2_sched_mon_dest_id_2 = data.split("A2_sched_mon_dest_id_2=")[1].split(',')
        A2_sched_mon_dest_id_2 = hex_to_bin(A2_sched_mon_dest_id_2)
        A2_sched_mon_dest_id_2 = format_data_length(A2_sched_mon_dest_id_2, 6)
        A2_sched_mon_ser_ing_if_1 = data.split("A2_sched_mon_ser_ing_if_1=")[1].split(',')[0]
        A2_sched_mon_ser_ing_if_1 = hex_to_bin(A2_sched_mon_ser_ing_if_1)
        A2_sched_mon_ser_ing_if_1 = format_data_length(A2_sched_mon_ser_ing_if_1, 3)
        A2_sched_mon_ser_ing_if_2 = data.split("A2_sched_mon_ser_ing_if_2=")[1]
        A2_sched_mon_ser_ing_if_2 = hex_to_bin(A2_sched_mon_ser_ing_if_2)
        A2_sched_mon_dest_id_2 = format_data_length(A2_sched_mon_dest_id_2, 3)
        data_value = A2_sched_mon_ser_ing_if_2 + A2_sched_mon_ser_ing_if_1 + A2_sched_mon_dest_id_2 + A2_sched_mon_dest_id_1
        data_value = format_hex_value(data_value)
        return data_value
    return (
            ":: A2_sched_mon_dest_id_1="
            + data[-6:]
            + ", A2_sched_mon_dest_id_2="
            + data[-14:-8]
            + ", A2_sched_mon_ser_ing_if_1="
            + data[-19:-16]
            + ", A2_sched_mon_ser_ing_if_2="
            + data[-23:-20]
    )


def SCHED_JOB_REQ_BARRIER_CONFIG(data):
    if "=" in data:
        A2_sched_gen_barrier_if1 = data.split("A2_sched_gen_barrier_if1=")[1].split(
            ","
        )[0]
        A2_sched_gen_barrier_if1 = hex_to_bin(A2_sched_gen_barrier_if1)
        A2_sched_gen_barrier_code = data.split("A2_sched_gen_barrier_code=")[1].split(',')
        A2_sched_gen_barrier_code = hex_to_bin(A2_sched_gen_barrier_code)
        A2_sched_gen_barrier_code = format_data_length(A2_sched_gen_barrier_code, 3)
        A2_sched_gen_barrier_njr_id = data.split("A2_sched_gen_barrier_njr_id=")[1].split(',')[0]
        A2_sched_gen_barrier_njr_id = hex_to_bin(A2_sched_gen_barrier_njr_id)
        A2_sched_gen_barrier_njr_id = format_data_length(A2_sched_gen_barrier_njr_id, 3)
        A2_sched_gen_barrier_if2 = data.split("A2_sched_gen_barrier_if2=")[1]
        A2_sched_gen_barrier_if2 = hex_to_bin(A2_sched_gen_barrier_if2)
        data_value = A2_sched_gen_barrier_if2 + A2_sched_gen_barrier_njr_id + A2_sched_gen_barrier_code + A2_sched_gen_barrier_if1
        data_value = format_hex_value(data_value)
        return data_value
    return (
            ":: A2_sched_gen_barrier_if1="
            + data[-1]
            + ", A2_sched_gen_barrier_code="
            + data[-4:-1]
            + ", A2_sched_gen_barrier_njr_id="
            + data[-7:-4]
            + ", A2_sched_gen_barrier_if2="
            + data[-8]
    )


def SCHED_RX_BARRIER_DATA_REG(data):
    if "=" in data:
        A2_sched_rx_barrier_vld = data.split("A2_sched_rx_barrier_vld=")[1].split(
            ","
        )[0]
        A2_sched_rx_barrier_vld = hex_to_bin(A2_sched_rx_barrier_vld)
        A2_sched_rx_barrier_code = data.split("A2_sched_rx_barrier_code=")[1].split(',')
        A2_sched_rx_barrier_code = hex_to_bin(A2_sched_rx_barrier_code)
        A2_sched_rx_barrier_code = format_data_length(A2_sched_rx_barrier_code, 3)
        A2_sched_rx_barrier_njr_id = data.split("A2_sched_rx_barrier_njr_id=")[1]
        A2_sched_rx_barrier_njr_id = hex_to_bin(A2_sched_rx_barrier_njr_id)
        A2_sched_rx_barrier_njr_id = format_data_length(A2_sched_rx_barrier_njr_id, 2)
        data_value = A2_sched_rx_barrier_njr_id + A2_sched_rx_barrier_code + A2_sched_rx_barrier_vld
        data_value = format_hex_value(data_value)
        return data_value
    return (
            ":: A2_sched_rx_barrier_vld="
            + data[-1]
            + ", A2_sched_rx_barrier_code="
            + data[-4:-1]
            + ", A2_sched_rx_barrier_njr_id="
            + data[-6:-4]
    )


def SCHED_RESPONSE_QUEUE_DATA_REG(data):
    if "=" in data:
        A2_sched_resp_queue_data = data.split("A2_sched_resp_queue_data=")[1].split(
            ","
        )[0]
        A2_sched_resp_queue_data = hex_to_bin(A2_sched_resp_queue_data)
        A2_sched_resp_queue_data = format_data_length(A2_sched_resp_queue_data, 26)
        A2_sched_resp_queue_tag = data.split("A2_sched_resp_queue_tag=")[1].split(
            ","
        )[0]
        A2_sched_resp_queue_tag = hex_to_bin(A2_sched_resp_queue_tag)
        A2_sched_resp_queue_tag = format_data_length(A2_sched_resp_queue_tag, 4)
        A2_sched_resp_queue_err = data.split("A2_sched_resp_queue_err=")[1]
        A2_sched_resp_queue_err = hex_to_bin(A2_sched_resp_queue_err)
        A2_sched_resp_queue_err = format_data_length(A2_sched_resp_queue_err, 2)
        data_value = A2_sched_resp_queue_err + A2_sched_resp_queue_tag + A2_sched_resp_queue_data
        data_value = format_hex_value(data_value)
        return data_value
    return (
            ":: A2_sched_resp_queue_data="
            + data[-26:]
            + ", A2_sched_resp_queue_tag="
            + data[-30:-26]
            + ", A2_sched_resp_queue_err="
            + data[-32:-30]
    )


def ID_POS2NEG_CR_TRANS(data):
    if "=" in data:
        A2_sid_pos2neg_src_cred = data.split("A2_sid_pos2neg_src_cred=")[1].split(
            ","
        )[0]
        A2_sid_pos2neg_src_cred = hex_to_bin(A2_sid_pos2neg_src_cred)
        A2_sid_pos2neg_src_cred = format_data_length(A2_sid_pos2neg_src_cred, 16)
        A2_did_pos2neg_dest_cred = data.split("A2_did_pos2neg_dest_cred=")[1]
        A2_did_pos2neg_dest_cred = hex_to_bin(A2_did_pos2neg_dest_cred)
        A2_did_pos2neg_dest_cred = format_data_length(A2_did_pos2neg_dest_cred, 16)
        data_value = A2_did_pos2neg_dest_cred + A2_sid_pos2neg_src_cred
        data_value = format_hex_value(data_value)
        return data_value
    return (
            ":: A2_sid_pos2neg_src_cred="
            + data[-16:]
            + ", A2_did_pos2neg_dest_cred="
            + data[-32:-16]
    )


def SCHED_NJR_EN_TBL(data):
    if "=" in data:
        A2_sched_njr_enable = data.split("A2_sched_njr_enable=")[1]
        A2_sched_njr_enable = hex_to_bin(A2_sched_njr_enable)
        data_value = "0" * 31 + A2_sched_njr_enable
        data_value = format_hex_value(data_value)
        return data_value
    return ":: A2_sched_njr_enable=" + data[-1]


def SCHED_CMD_QUEUE_CMD_REG(data):
    if "=" in data:
        A2_sched_node_reg_addr = data.split("A2_sched_node_reg_addr=")[1].split(",")[0]
        A2_sched_node_reg_addr = hex_to_bin(A2_sched_node_reg_addr)
        A2_sched_node_reg_addr = format_data_length(A2_sched_node_reg_addr, 3)
        A2_sched_comp_node_id = data.split("A2_sched_comp_node_id=")[1].split(",")[0]
        A2_sched_comp_node_id = hex_to_bin(A2_sched_comp_node_id)
        A2_sched_comp_node_id = format_data_length(A2_sched_comp_node_id, 14)
        A2_sched_is_parent = data.split("A2_sched_is_parent=")[1].split(",")[0]
        A2_sched_is_parent = hex_to_bin(A2_sched_is_parent)
        A2_sched_comp_type = data.split("A2_sched_comp_type=")[1].split(",")[0]
        A2_sched_comp_type = hex_to_bin(A2_sched_comp_type)
        A2_sched_comp_type = format_data_length(A2_sched_comp_type, 3)
        A2_sched_comp_lvl = data.split("A2_sched_comp_lvl=")[1].split(",")[0]
        A2_sched_comp_lvl = hex_to_bin(A2_sched_comp_lvl)
        A2_sched_comp_lvl = format_data_length(A2_sched_comp_lvl, 3)
        A2_sched_cmd_queue_tag = data.split("A2_sched_cmd_queue_tag=")[1].split(",")[0]
        A2_sched_cmd_queue_tag = hex_to_bin(A2_sched_cmd_queue_tag)
        A2_sched_cmd_queue_tag = format_data_length(A2_sched_cmd_queue_tag, 4)
        A2_sched_cmd_queue_op = data.split("A2_sched_cmd_queue_op=")[1].split(",")[0]
        A2_sched_cmd_queue_op = hex_to_bin(A2_sched_cmd_queue_op)
        A2_sched_cmd_queue_op = format_data_length(A2_sched_cmd_queue_op, 3)
        data_value = (
                A2_sched_cmd_queue_op
                + A2_sched_cmd_queue_tag
                + "0"
                + A2_sched_comp_lvl
                #            + "0"
                + A2_sched_comp_type
                + A2_sched_is_parent
                + A2_sched_comp_node_id
                + A2_sched_node_reg_addr
        )
        data_value = format_hex_value(data_value)
        return data_value

    return (
            ":: A2_sched_node_reg_addr="
            + bin_to_hex(data[-3:])
            + ", A2_sched_comp_node_id="
            + bin_to_hex(data[-17:-3])
            + ", A2_sched_is_parent="
            + bin_to_hex(data[-18])
            + ",A2_sched_comp_type="
            + bin_to_hex(data[-21:-18])
            + ", A2_sched_comp_lvl="
            + bin_to_hex(data[-24:-21])
            + ", A2_sched_cmd_queue_tag="
            + bin_to_hex(data[-29:-25])
            + ", A2_sched_cmd_queue_op="
            + bin_to_hex(data[-32:-29])
            + "\n"
            + "*" * 50
            + "\n"
    )


def SCHED_RATE_CLK_CONFIG(data):
    if "=" in data:
        A2_refill_tick_step_pos = data.split("A2_refill_tick_step_pos=")[1].split(",")[
            0
        ]
        A2_refill_tick_step_pos = hex_to_bin(A2_refill_tick_step_pos)
        A2_refill_tick_step_pos = format_data_length(A2_refill_tick_step_pos, 16)
        A2_refill_tick_step_neg = data.split("A2_refill_tick_step_neg=")[1]
        A2_refill_tick_step_neg = hex_to_bin(A2_refill_tick_step_neg)
        A2_refill_tick_step_neg = format_data_length(A2_refill_tick_step_neg, 16)
        data_value = A2_refill_tick_step_neg + A2_refill_tick_step_pos
        data_value = format_hex_value(data_value)
        return data_value
    return (
            ":: A2_refill_tick_step_pos="
            + bin_to_hex(data[-16:])
            + " A2_refill_tick_step_neg="
            + bin_to_hex(data[-32:-16])
    )


def SCHED_MTU_SRC_DEST_SIZE_TBL(data):
    if "=" in data:
        A2_job_req_max_src_creds = data.split("A2_job_req_max_src_creds=")[1].split(
            ","
        )[0]
        A2_job_req_max_src_creds = hex_to_bin(A2_job_req_max_src_creds)
        A2_job_req_max_src_creds = format_data_length(A2_job_req_max_src_creds, 16)
        A2_job_req_max_dest_creds = data.split("A2_job_req_max_dest_creds=")[1].split(
            ","
        )[0]
        A2_job_req_max_dest_creds = hex_to_bin(A2_job_req_max_dest_creds)
        A2_job_req_max_dest_creds = format_data_length(A2_job_req_max_dest_creds, 16)
        data_value = A2_job_req_max_dest_creds + A2_job_req_max_src_creds
        data_value = format_hex_value(data_value)
        return data_value
    return (
            ":: A2_job_req_max_src_creds="
            + bin_to_hex(data[-16:])
            + ", A2_job_req_max_dest_creds="
            + bin_to_hex(data[-32:-16])
    )


def SCHED_MTU_COST_CUTOFF_SIZE_TBL(data):
    if "=" in data:
        A2_job_req_max_cost = data.split("A2_job_req_max_cost=")[1].split(",")[0]
        A2_job_req_max_cost = hex_to_bin(A2_job_req_max_cost)
        A2_job_req_max_cost = format_data_length(A2_job_req_max_cost, 16)
        A2_sched_cutoff_credits = data.split("A2_sched_cutoff_credits=")[1].split(",")[
            0
        ]
        A2_sched_cutoff_credits = hex_to_bin(A2_sched_cutoff_credits)
        A2_sched_cutoff_credits = format_data_length(A2_sched_cutoff_credits, 16)
        data_value = A2_sched_cutoff_credits + A2_job_req_max_cost
        data_value = format_hex_value(data_value)
        return data_value
    return (
            ":: A2_job_req_max_cost="
            + bin_to_hex(data[-16:])
            + ", A2_sched_cutoff_credits="
            + bin_to_hex(data[-32:-16])
    )


def SCHED_CONFIG_0(data):
    if "=" in data:
        A2_sched_max_outstanding_jreq = data.split("A2_sched_max_outstanding_jreq=")[
            1
        ].split(",")[0]
        A2_sched_max_outstanding_jreq = hex_to_bin(A2_sched_max_outstanding_jreq)
        A2_sched_max_outstanding_jreq = format_data_length(
            A2_sched_max_outstanding_jreq, 5
        )
        A2_sched_dest_comp_lvl = data.split("A2_sched_dest_comp_lvl=")[1].split(",")[0]
        A2_sched_dest_comp_lvl = hex_to_bin(A2_sched_dest_comp_lvl)
        A2_sched_dest_comp_lvl = format_data_length(A2_sched_dest_comp_lvl, 3)
        A2_mon_njr_outstanding_jreq_status = data.split(
            "A2_mon_njr_outstanding_jreq_status="
        )[1].split(",")[0]
        A2_mon_njr_outstanding_jreq_status = hex_to_bin(
            A2_mon_njr_outstanding_jreq_status
        )
        A2_mon_njr_outstanding_jreq_status = format_data_length(
            A2_mon_njr_outstanding_jreq_status, 4
        )
        data_value = (
                A2_mon_njr_outstanding_jreq_status
                + A2_sched_dest_comp_lvl
                + A2_sched_max_outstanding_jreq
        )
        data_value = format_hex_value(data_value)
        return data_value
    return (
            ":: A2_sched_max_outstanding_jreq="
            + bin_to_hex(data[-5:])
            + ", A2_sched_dest_comp_lvl="
            + bin_to_hex(data[-8:-5])
            + ", A2_mon_njr_outstanding_jreq_status="
            + bin_to_hex(data[-12:-8])
            + "\n"
            + "*" * 50
    )


def SCHED_CMD_QUEUE_WDATA_REG(data):
    if "=" in data:
        A2_sched_wdata = data.split("A2_sched_wdata=")[1].split(",")[0]
        A2_sched_wdata = hex_to_bin(A2_sched_wdata)
        A2_sched_wdata = format_data_length(A2_sched_wdata, 26)
        A2_sched_byte_wmask = data.split("A2_sched_byte_wmask=")[1].split(",")[0]
        A2_sched_byte_wmask = hex_to_bin(A2_sched_byte_wmask)
        A2_sched_byte_wmask = format_data_length(A2_sched_byte_wmask, 4)
        data_value = A2_sched_byte_wmask + A2_sched_wdata
        data_value = format_hex_value(data_value)
        return data_value
    return (
            ":: A2_sched_wdata="
            + bin_to_hex(data[-26:])
            + ", A2_sched_byte_wmask="
            + bin_to_hex(data[-30:-26])
            + "\n"
    )


def SCHED_STATUS_REG(data):
    if "=" in data:
        A2_sched_resp_queue_depth = data.split("A2_sched_resp_queue_depth=")[1].split(
            ","
        )[0]
        A2_sched_resp_queue_depth = hex_to_bin(A2_sched_resp_queue_depth)
        A2_sched_resp_queue_depth = format_data_length(A2_sched_resp_queue_depth, 5)
        A2_schead_cmd_queue_depth = data.split("A2_schead_cmd_queue_depth=")[1].split(
            ","
        )[0]
        A2_schead_cmd_queue_depth = hex_to_bin(A2_schead_cmd_queue_depth)
        A2_schead_cmd_queue_depth = format_data_length(A2_schead_cmd_queue_depth, 5)
        A2_sched_barrier_queue_depth = data.split("A2_sched_barrier_queue_depth=")[
            1
        ].split(",")[0]
        A2_sched_barrier_queue_depth = hex_to_bin(A2_sched_barrier_queue_depth)
        A2_sched_barrier_queue_depth = format_data_length(
            A2_sched_barrier_queue_depth, 5
        )
        A2_outstanding_jreq_status = data.split("A2_outstanding_jreq_status=")[1]
        A2_outstanding_jreq_status = hex_to_bin(A2_outstanding_jreq_status)
        A2_outstanding_jreq_status = format_data_length(A2_outstanding_jreq_status, 5)
        data_value = (
                A2_outstanding_jreq_status
                + "00000"
                + A2_sched_barrier_queue_depth
                + "000"
                + A2_schead_cmd_queue_depth
                + "000"
                + A2_sched_resp_queue_depth
        )
        data_value = format_hex_value(data_value)
        return data_value
    return (
            ":: A2_sched_resp_queue_depth="
            + bin_to_hex(data[-5:])
            + ", A2_schead_cmd_queue_depth="
            + bin_to_hex(data[-13:-8])
            + ", A2_sched_barrier_queue_depth="
            + bin_to_hex(data[-21:-16])
            + " A2_outstanding_jreq_status="
            + bin_to_hex(data[-32:-27])
    )


# Following methods are for PSX/PCIe bit calculation


def bit_31_23_calculation(padded_binary):
    bit_31_23 = (
            padded_binary[-32]
            + padded_binary[-31]
            + padded_binary[-30]
            + padded_binary[-29]
            + padded_binary[-28]
            + padded_binary[-27]
            + padded_binary[-26]
            + padded_binary[-25]
            + padded_binary[-24]
    )

    hex_binary = hex(int(bit_31_23, 2))
    bit_31_23_val = "Reserved"
    bit_31_23_val = "reserved: ", hex_binary, ":", "(", bit_31_23_val, ")"
    return bit_31_23_val


def bit_22_9_calculation(padded_binary):
    bit_22_9 = (
            padded_binary[-23]
            + padded_binary[-22]
            + padded_binary[-21]
            + padded_binary[-20]
            + padded_binary[-19]
            + padded_binary[-18]
            + padded_binary[-17]
            + padded_binary[-16]
            + padded_binary[-15]
            + padded_binary[-14]
            + padded_binary[-13]
            + padded_binary[-12]
            + padded_binary[-11]
            + padded_binary[-10]
    )
    hex_binary = hex(int(bit_22_9, 2))
    hex_binary_split = hex_binary[-1] + hex_binary[-2]
    bit_22_9_val = "Entry of table or context to access"
    bit_22_9_value = "Entry=" + hex_binary
    return bit_22_9_value


def bit_8_7_calculation(padded_binary):
    bit_8_7 = padded_binary[-9] + padded_binary[-8]
    hex_binary = hex(int(bit_8_7, 2))
    bit_8_7_dict = {"00": "Reserved", "01": "CMD_WR", "10": "CMD_RD", "11": "Reserved"}
    bit_8_7_value = "op=" + hex_binary + "(" + bit_8_7_dict[bit_8_7] + ")"
    return bit_8_7_value


def bit_6_1_calculation(padded_binary):
    bit_6_1 = (
            padded_binary[-7]
            + padded_binary[-6]
            + padded_binary[-5]
            + padded_binary[-4]
            + padded_binary[-3]
            + padded_binary[-2]
    )
    hex_binary = hex(int(bit_6_1, 2))
    hex_binary_split = hex_binary[-2] + hex_binary[-1]
    bit_6_1_dict = {
        "10": "PCIE_BRIDGE0_FNC_STS",
        "11": "PCIE_BRIDGE0_ADDR_TRANS_WINDOWS",
        "12": "PCIE_BRIDGE0_FNC_CFG",
        "13": "PCIE_BRIDGE0_BAR_CFG",
        "14": "PCIE_BRIDGE1_FNC_STS",
        "15": "PCIE_BRIDGE1_ADDR_TRANS_WINDOWS",
        "16": "PCIE_BRIDGE1_FNC_CFG",
        "17": "PCIE_BRIDGE1_BAR_CFG",
        "18": "PCIE_BRIDGE2_FNC_STS",
        "19": "PCIE_BRIDGE2_ADDR_TRANS_WINDOWS",
        "1a": "PCIE_BRIDGE2_FNC_CFG",
        "1b": "PCIE_BRIDGE2_BAR_CFG",
        "1c": "PCIE_BRIDGE3_FNC_STS",
        "1d": "PCIE_BRIDGE3_ADDR_TRANS_WINDOWS",
        "1e": "PCIE_BRIDGE3_FNC_CFG",
        "1f": "PCIE_BRIDGE3_BAR_CFG",
        "20": "PSX_BRIDGE_A2C_APERTURE_REMAP",
        "21": "PSX_BRIDGE_A2C_APERTURE_CONFIG",
        "22": "PSX_BRIDGE_A2C_APERTURE_WINDOWS",
        "23": "PSX_BRIDGE_C2A_APERTURE_TABLE",
        "24": "PSX_BRIDGE_C2A_RAXID_TABLE",
        "25": "PSX_BRIDGE_C2A_WAXID_TABLE",
        "26": "PSX_BRIDGE_STASH_TABLE",
        "27": "PSX_BRIDGE_C2A_GIC_ADDR",
        "28": "PSX_BRIDGE_IRQ_CLIENT_CFG",
        "30": "PCIE_BRIDGE0_MSG_CFG",
        "31": "PCIE_BRIDGE0_MSG_CFG",
        "32": "PCIE_BRIDGE0_MSG_CFG",
        "33": "PCIE_BRIDGE0_MSG_CFG",
        "34": "PSX_BRIDGE_DDR_MAP_TABLE",
    }
    bit_6_1_value = "sel=" + hex_binary + "(" + bit_6_1_dict[hex_binary_split] + ")"
    return bit_6_1_value


def bit_0_calculation(padded_binary):
    bit_0_value = "busy=" + hex(int(padded_binary[-1], 2))
    return bit_0_value


# Following methods are for the decoding of the psx/pcie bridge address values from CDO to Text and vice versa
# Based on select value of particular register decoding the bridge
# If byteval includes x it's text to CDO conversion else it's only binary values


def hex_20_value(byteval):
    if "x" in byteval:
        cmd = byteval
        ap_remap_addr = bin(int(cmd.split("ap_remap_addr=")[1], 16)).replace("0b", "")
        data_value = hex(int(ap_remap_addr, 2))
        data_value = (
            data_value
            if len(data_value) == 10
            else "0x" + (10 - len(data_value)) * "0" + data_value.replace("0x", "")
        )
        return data_value
    hex_binary_22_0 = hex(int(byteval[-23:], 2))
    bit_22_0_value = " ap_remap_addr=" + hex_binary_22_0
    data_frame = [["ap_remap_addr", hex_binary_22_0]]
    data_frame = pd.DataFrame(data_frame)
    return data_frame, bit_22_0_value


def hex_21_value(byteval):
    if "x" in byteval:
        cmd = byteval.strip()
        axprot_1 = bin(int(cmd.split("axprot_1=")[1], 16)).replace("0b", "")
        xmti = bin(int(cmd.split("xmti=")[1].split(";axprot_1=")[0], 16)).replace(
            "0b", ""
        )
        xmti = format_data_length(xmti, 12)
        apt_type = bin(
            int(cmd.split("apt_type=")[1].split(";")[0].split(")")[1], 16)
        ).replace("0b", "")
        err_mode = cmd.split("err_mode=")[1].split(";")[0]
        err_mode = "0" if err_mode == "OK" else "1"
        if apt_type == "0":
            csi_dst_fifo = bin(
                int(cmd.split("csi_dst_fifo=")[1].split(")")[0], 16)
            ).replace("0b", "")
            csi_dst_fifo = format_data_length(csi_dst_fifo, 9)
            csi_dst = bin(
                int(CSI_SRC_DST[cmd.split(";csi_dest=")[1].split("(")[0]].value, 16)
            ).replace("0b", "")
            csi_dest = format_data_length(csi_dst, 5)
            requester = bin(
                int(cmd.split("requester=")[1].split(";csi_dest")[0], 16)
            ).replace("0b", "")
            requester = format_data_length(requester, 16)
            data = csi_dst_fifo + csi_dest + requester
        else:
            reserved = bin(
                int(cmd.split(";reserve=")[1].split(");apt_type=")[0], 16)
            ).replace("0b", "")
            reserved = format_data_length(reserved, 13)
            log2_num_window = bin(
                int(cmd.split("log2_num_window=")[1].split(";reserve=")[0], 16)
            ).replace("0b", "")
            log2_num_window = format_data_length(log2_num_window, 3)
            log2_win_size = bin(
                int(cmd.split("log2_win_size=")[1].split(";log2_num_window=")[0], 16)
            ).replace("0b", "")
            log2_win_size = format_data_length(log2_win_size, 5)
            base_win = bin(
                int(cmd.split("base_win=")[1].split(";log2_win_size=")[0], 16)
            ).replace("0b", "")
            base_win = format_data_length(base_win, 8)
            wrap = bin(int(cmd.split("wrap=")[1].split(";base_win=")[0], 16)).replace(
                "0b", ""
            )
            data = reserved + log2_num_window + log2_win_size + base_win + wrap
        data_value = axprot_1 + xmti + apt_type + data + err_mode
        data_value = hex(int(data_value, 2))
        data_value = (
            data_value
            if len(data_value) == 10
            else "0x" + (10 - len(data_value)) * "0" + data_value.replace("0x", "")
        )
        return data_value

    byteval = "0" * (64 - len(byteval)) + str(byteval) if len(byteval) < 64 else byteval
    hex_binary_0 = hex(int(byteval[-1], 2))
    if hex_binary_0 == "0x0":
        bit_0_value = "err_mode=OK"
    elif hex_binary_0 == "0x1":
        bit_0_value = "err_mode=SLVERR"
    hex_binary_30_1 = hex(int(byteval[-31:-1], 2))
    binary_30_1 = byteval[-31:-1]
    hex_binary_31 = hex(int(byteval[-32], 2))
    hex_binary_30_1_0 = hex_binary_30_1_8_1 = hex_binary_30_1_21_17 = hex_binary_30_1_30_22 = hex_binary_30_1_16_1 = hex_binary_30_1_16_14 = hex_binary_30_1_13_9 = "0x0"
    if byteval[-32] == "0":
        hex_binary_30_1_16_1 = hex(int(binary_30_1[-16:], 2))
        bit_30_1_16_1_value = "requester=" + hex_binary_30_1_16_1

        hex_binary_30_1_21_17 = hex(int(binary_30_1[-21:-16], 2))
        bit_30_1_21_17_value = (
                "csi_dest="
                + CSI_SRC_DST(hex_binary_30_1_21_17).name
                + "("
                + hex_binary_30_1_21_17
                + ")"
        )

        hex_binary_30_1_30_22 = hex(int(binary_30_1[-30:-21], 2))
        bit_30_1_30_22_value = "csi_dst_fifo=" + hex_binary_30_1_30_22

        bit_30_1_value = (
                "Type=Config Aperture("
                + bit_30_1_16_1_value
                + ";"
                + bit_30_1_21_17_value
                + ";"
                + bit_30_1_30_22_value
                + ")"
        )
        bit_31_value = "apt_type=(Config Space)" + hex_binary_31
    else:
        bit_31_value = "apt_type=(Mem/IO)" + hex_binary_31
        hex_binary_30_1_0 = hex(int(binary_30_1[-1], 2))
        bit_30_1_0_value = "wrap=" + hex_binary_30_1_0

        hex_binary_30_1_8_1 = hex(int(binary_30_1[-9:-1], 2))
        bit_30_1_8_1_value = "base_win=" + hex_binary_30_1_8_1

        hex_binary_30_1_13_9 = hex(int(binary_30_1[-14:-9], 2))
        bit_30_1_13_9_value = "log2_win_size=" + hex_binary_30_1_13_9

        hex_binary_30_1_16_14 = hex(int(binary_30_1[-17:-14], 2))
        bit_30_1_16_14_value = "log2_num_window=" + hex_binary_30_1_16_14

        hex_binary_30_1_29_17 = hex(int(binary_30_1[-30:-17], 2))
        bit_30_1_29_17_value = "reserve=" + hex_binary_30_1_29_17
        bit_30_1_value = (
                "Type=Mem/IO("
                + bit_30_1_0_value
                + ";"
                + bit_30_1_8_1_value
                + ";"
                + bit_30_1_13_9_value
                + ";"
                + bit_30_1_16_14_value
                + ";"
                + bit_30_1_29_17_value
                + ")"
        )

    hex_binary_43_32 = hex(int(byteval[-44:-32], 2))
    bit_43_32_value = "xmti=" + hex_binary_43_32

    hex_binary_44 = hex(int(byteval[-45], 2))
    bit_44_value = "axprot_1=" + hex_binary_44
    if byteval[-32] == "0":
        data_frame = [["axprot_1", hex_binary_44], ["xmti", hex_binary_43_32],
                      ["apt_type(CFG)", hex_binary_31],
                      ["csi_dst_fifo", hex_binary_30_1_30_22],
                      ["csi_dest",
                       f"{hex_binary_30_1_21_17}({CSI_SRC_DST(hex_binary_30_1_21_17).name})"],
                      ["requester", hex_binary_30_1_16_1],
                      ["err_mode", hex_binary_0]]
        requester = hex_binary_30_1_16_1
    else:
        data_frame = [["axprot_1", hex_binary_44], ["xmti", hex_binary_43_32],
                      ["apt_type(MEM)", hex_binary_31],
                      ["log2_num_window", hex_binary_30_1_16_14],
                      ["log2_win_size", hex_binary_30_1_13_9],
                      ["base_win", hex_binary_30_1_8_1],
                      ["wrap", hex_binary_30_1_0],
                      ["err_mode", hex_binary_0]]
        requester = hex_binary_30_1_8_1
    data_frame = pd.DataFrame(data_frame)
    data_frame.columns = ['A2C_APERTURE_CONFIG', f'APERTURE-{int(requester, 16)}']
    return data_frame, (
        bit_0_value,
        ";",
        bit_30_1_value,
        ";",
        bit_31_value,
        ";",
        bit_43_32_value,
        ";",
        bit_44_value,
    )


def hex_10_value(byteval):
    if "x" in byteval:
        cmd = byteval.strip()
        rsvd = bin(int(cmd.split("rsvd=")[1], 16)).replace("0b", "")
        msix_mask = bin(int(cmd.split("msix_mask=")[1].split(" rsvd")[0], 16)).replace(
            "0b", ""
        )
        evt_pend = bin(
            int(cmd.split("evt_pend=")[1].split(" msix_mask=")[0], 16)
        ).replace("0b", "")
        flr = bin(int(cmd.split("flr=")[1].split(" evt_pend=")[0], 16)).replace(
            "0b", ""
        )
        msi_enable = bin(int(cmd.split("msi_enable=")[1].split(" flr")[0], 16)).replace(
            "0b", ""
        )
        msix_enable = bin(
            int(cmd.split("msix_enable=")[1].split(" msi_enable=")[0], 16)
        ).replace("0b", "")
        bme = bin(int(cmd.split("bme=")[1].split(" msix_enable=")[0], 16)).replace(
            "0b", ""
        )
        data_value = rsvd + msix_mask + evt_pend + flr + msi_enable + msix_enable + bme
        data_value = hex(int(data_value, 2)).replace("0x", "")
        return create_hex_list(data_value, 8)

    hex_binary_0 = hex(int(byteval[-1], 2))
    bit_0_value = "bme=" + hex_binary_0

    hex_binary_1 = hex(int(byteval[-2], 2))
    bit_1_value = "msix_enable=" + hex_binary_1

    hex_binary_2 = hex(int(byteval[-3], 2))
    bit_2_value = "msi_enable=" + hex_binary_2

    hex_binary_3 = hex(int(byteval[-4], 2))
    bit_3_value = "flr=" + hex_binary_3

    hex_binary_4 = hex(int(byteval[-5], 2))
    bit_4_value = "evt_pend=" + hex_binary_4

    hex_binary_5 = hex(int(byteval[-6], 2))
    bit_5__value = "msix_mask=" + hex_binary_5

    hex_binary_6 = hex(int(byteval[-7], 2))
    bit_6_value = "rsvd=" + hex_binary_6

    return (
        bit_0_value,
        ";",
        bit_1_value,
        ";",
        bit_2_value,
        ";",
        bit_3_value,
        ";",
        bit_4_value,
        ";",
        bit_5__value,
        ";",
        bit_6_value,
    )


def hex_11_value(byteval):
    if "x" in byteval:
        cmd = byteval.strip()
        rsvd = bin(int(cmd.split("rsvd=")[1], 16)).replace("0b", "")
        rsvd = format_data_length(rsvd, 11)
        valid = bin(int(cmd.split("valid=")[1].split(";rsvd")[0], 16)).replace("0b", "")
        csi_dst = bin(
            int(CSI_SRC_DST[cmd.split(";csi_dst=")[1].split("(")[0]].value, 16)
        ).replace("0b", "")
        csi_dst = format_data_length(csi_dst, 5)
        csi_rro = bin(int(cmd.split("csi_rro=")[1].split(";csi_dst")[0], 16)).replace(
            "0b", ""
        )
        enc_mode = {
            "PCQ_AE_ADDR": "00",
            "PCQ_AE_APERTURE": "01",
            "PCQ_AE_AP_FUNC_BAR": "10",
        }
        addr_enc_mode = bin(
            int(enc_mode[cmd.split("addr_enc_mode=")[1].split("(")[0]], 16)
        ).replace("0b", "")
        addr_enc_mode = format_data_length(addr_enc_mode, 2)
        if addr_enc_mode == enc_mode["PCQ_AE_APERTURE"]:
            ap_id = bin(
                int(cmd.split("PCQ_AE_APERTURE(ap_id=")[1].split(";")[0], 16)
            ).replace("0b", "")
            ap_id = format_data_length(ap_id, 6)
            win_off = bin(int(cmd.split(";win_off=")[1].split(")")[0], 16)).replace(
                "0b", ""
            )
            win_off = format_data_length(win_off, 8)
            rsvd = "0" * 38
            addr_ap_afb = rsvd + ap_id + win_off
        elif addr_enc_mode == enc_mode["PCQ_AE_ADDR"]:
            addr_ap_afb = bin(
                int(cmd.split("addr_ap_afb=")[1].split(";")[0], 16)
            ).replace("0b", "")
            addr_ap_afb = format_data_length(addr_ap_afb, 52)
        else:
            ap_id = bin(
                int(cmd.split("PCQ_AE_AP_FUNC_BAR(ap_id=")[1].split(";")[0], 16)
            ).replace("0b", "")
            ap_id = format_data_length(ap_id, 6)
            win_off = bin(int(cmd.split("Pfunc_to_rfunc=")[1].split(")")[0], 16)).replace(
                "0b", ""
            )
            win_off = format_data_length(win_off, 13)
            rsvd = "0" * 33
            addr_ap_afb = rsvd + ap_id + win_off

        data_value = hex(
            int(rsvd + valid + csi_dst + csi_rro + addr_enc_mode + addr_ap_afb, 2)
        ).replace("0x", "")
        a = data_value
        data = " ".join(
            [a[-i - 8: -i if i else None] for i in range(0, len(a), 8)][::-1]
        )
        data = ["0x" + format_data_length(x, 8) for x in data.split(" ")][::-1]
        return data

    bitlength = len(byteval)
    byteval = "0" * (72 - len(byteval)) + str(byteval) if len(byteval) < 72 else byteval
    if len(byteval) >= 72:
        bit_0_51_value = byteval[-52:]
        hex_binary_52_53 = hex(int(byteval[-54:-52], 2))
        if byteval[-54:-52] == "00":
            bit_52_53_value = "addr_enc_mode=PCQ_AE_ADDR(" + hex_binary_52_53 + ")"
            list_1 = []
            list_2 = ["addr_ap_afb", hex_binary_52_53]
        elif byteval[-54:-52] == "01":
            bit_52_53_value = (
                    "addr_enc_mode=PCQ_AE_APERTURE(ap_id="
                    + hex(int(bit_0_51_value[-14:-8], 2))
                    + ";win_off="
                    + hex(int(bit_0_51_value[-8:], 2))
                    + ")"
            )
            list_1 = ['ap_id', hex(int(bit_0_51_value[-14:-8], 2))]
            list_2 = ['win_off', hex(int(bit_0_51_value[-8:], 2))]
        else:
            bit_52_53_value = (
                    "addr_enc_mode=PCQ_AE_AP_FUNC_BAR(ap_id="
                    + hex(int(bit_0_51_value[-19:-13], 2))
                    + ";Pfunc_to_rfunc="
                    + hex(int(bit_0_51_value[-13:], 2))
                    + ")"
            )
            list_1 = ['ap_id', hex(int(bit_0_51_value[-19:-13], 2))]
            list_2 = ['Pfunc_to_rfunc', hex(int(bit_0_51_value[-13:], 2))]

        hex_binary_54 = hex(int(byteval[-55], 2))
        bit_54_value = "csi_rro=" + hex_binary_54

        hex_binary_55_59 = hex(int(byteval[-60:-55], 2))
        bit_55_59_value = (
                "csi_dst="
                + CSI_SRC_DST(hex_binary_55_59).name
                + "("
                + hex_binary_55_59
                + ")"
        )

        hex_binary_60 = hex(int(byteval[-61], 2))
        bit_60_value = "valid=" + hex_binary_60
        if hex_binary_60 == '0x0':
            hex_binary_60 = "Invalid"
        hex_binary_61_71 = hex(int(byteval[-72:-61], 2))
        bit_61_71__value = "rsvd=" + hex_binary_61_71
        data_frame = [list_1, list_2,
                      ["addr_enc_mode", hex_binary_52_53],
                      ["csi_dst", f'{CSI_SRC_DST(hex_binary_55_59).name} ({hex_binary_55_59})'],
                      ["csi_rro", hex_binary_54],
                      ["valid", hex_binary_60],
                      ["rsvd", hex_binary_61_71]]
        data_frame = pd.DataFrame(data_frame)
        return data_frame, (
            bit_52_53_value,
            ";",
            bit_54_value,
            ";",
            bit_55_59_value,
            ";",
            bit_60_value,
            ";",
            bit_61_71__value,
        )
    else:
        return (
                "bit length is "
                + str(bitlength)
                + " which is less than expected bit length 72"
        )


def hex_12_value(byteval):
    if "x" in byteval:
        cmd = byteval
        valid = bin(int(cmd.split("valid=")[1], 16)).replace("0b", "")
        func_type = bin(
            int(cmd.split("func_type=")[1].split(";valid=")[0], 16)
        ).replace("0b", "")
        func_type = format_data_length(func_type, 5)
        data_value = hex(int(valid + func_type, 2)).replace("0x", "")
        data_value = "0x" + format_data_length(data_value, 8)
        return data_value

    hex_binary_0_4 = hex(int(byteval[-5:], 2))
    bit_0_4_value = "func_type=" + hex_binary_0_4

    hex_binary_5 = hex(int(byteval[-6], 2))
    bit_5_value = "valid=" + hex_binary_5
    if hex_binary_5 == '0x0':
        hex_binary_5 = "Invalid"
    data_frame = [["valid", hex_binary_5],
                  ["func_type", hex_binary_0_4]]
    data_frame = pd.DataFrame(data_frame)

    return data_frame, (bit_0_4_value, ";", bit_5_value)


def hex_13_value(byteval):
    if "x" in byteval:
        cmd = byteval
        valid = bin(
            int(cmd.split("valid=")[1].split(";log2_bar_size_m12")[0], 16)
        ).replace("0b", "")
        base_win = bin(int(cmd.split("base_win=")[1].split(";wrap=")[0], 16)).replace(
            "0b", ""
        )
        base_win = format_data_length(base_win, 8)
        log2_bar_size_m12 = bin(
            int(cmd.split("log2_bar_size_m12=")[1].split(";log2_n_win")[0], 16)
        ).replace("0b", "")
        log2_bar_size_m12 = format_data_length(log2_bar_size_m12, 6)
        log2_n_win = bin(
            int(cmd.split("log2_n_win=")[1].split(";log2_win_size_m12")[0], 16)
        ).replace("0b", "")
        log2_n_win = format_data_length(log2_n_win, 3)
        log2_win_size_m12 = bin(
            int(cmd.split("log2_win_size_m12=")[1].split(";base_win=")[0], 16)
        ).replace("0b", "")
        log2_win_size_m12 = format_data_length(log2_win_size_m12, 5)
        wrap = bin(int(cmd.split("wrap=")[1], 16)).replace("0b", "")
        data_value = hex(
            int(
                valid
                + log2_bar_size_m12
                + log2_n_win
                + log2_win_size_m12
                + base_win
                + wrap,
                2,
            )
        ).replace("0x", "")
        data_value = "0x" + format_data_length(data_value, 8)
        return data_value

    hex_binary_0 = hex(int(byteval[-1], 2))
    bit_0_value = "wrap=" + hex_binary_0

    hex_binary_1_8 = hex(int(byteval[-9:-1], 2))
    bit_1_8_value = "base_win=" + hex_binary_1_8

    hex_binary_9_13 = hex(int(byteval[-14:-9], 2))
    bit_9_13_value = "log2_win_size_m12=" + hex_binary_9_13

    hex_binary_14_16 = hex(int(byteval[-17:-14], 2))
    bit_14_16_value = "log2_n_win=" + hex_binary_14_16

    hex_binary_17_22 = hex(int(byteval[-23:-17], 2))
    bit_17_22_value = "log2_bar_size_m12=" + hex_binary_17_22

    hex_binary_23 = hex(int(byteval[-24], 2))
    bit_23_value = "valid=" + hex_binary_23
    if hex_binary_23 == '0x0':
        hex_binary_23 = "Invalid"
    data_frame = [["valid", hex_binary_23], ["log2_bar_size_m12", hex_binary_17_22],
                  ["log2_n_win", hex_binary_14_16],
                  ["log2_win_size_m12", hex_binary_9_13],
                  ["base_win", hex_binary_1_8],
                  ["wrap", hex_binary_0]]
    data_frame = pd.DataFrame(data_frame)
    # data_frame.columns = [f'PCIE0_BAR{int(hex_binary_1_8, 16)}_CFG', int(hex_binary_1_8, 16)]

    return data_frame, (
        bit_23_value,
        ";",
        bit_17_22_value,
        ";",
        bit_14_16_value,
        ";",
        bit_9_13_value,
        ";",
        bit_1_8_value,
        ";",
        bit_0_value,
    )


def hex_30_value(byteval):
    if "x" in byteval:
        cmd = byteval
        valid = bin(int(cmd.split("valid=")[1], 16)).replace("0b", "")
        func_type = bin(int(cmd.split("func_type=")[1].split("valid=")[0], 16)).replace(
            "0b", ""
        )
        func_type = format_data_length(func_type, 5)
        pcie_msg_code = bin(
            int(cmd.split("pcie_msg_code=")[1].split("func_type")[0], 16)
        ).replace("0b", "")
        pcie_msg_code = format_data_length(pcie_msg_code, 8)
        csi_dst = bin(
            int(CSI_SRC_DST[cmd.split("csi_dst=")[1].split("(")[0]].value, 16)
        ).replace("0b", "")
        csi_dst = format_data_length(csi_dst, 5)
        msg_cookie = bin(
            int(cmd.split("msg_cookie=")[1].split("csi_dst")[0], 16)
        ).replace("0b", "")
        msg_cookie = format_data_length(msg_cookie, 8)
        data_value = valid + func_type + pcie_msg_code + csi_dst + msg_cookie
        data_value = hex(int(data_value, 2)).replace("0x", "")
        return create_hex_list(data_value, 8)

    hex_binary_0_7 = hex(int(byteval[-8:], 2))
    bit_0_7_value = "msg_cookie=" + hex_binary_0_7

    hex_binary_8_12 = hex(int(byteval[-13:-8], 2))
    bit_8_12_value = (
            "csi_dst=" + CSI_SRC_DST(hex_binary_8_12).name + "(" + hex_binary_8_12 + ")"
    )

    hex_binary_13_20 = hex(int(byteval[-21:-13], 2))
    bit_13_20_value = "pcie_msg_code=" + hex_binary_13_20

    hex_binary_21_25 = hex(int(byteval[-26:-21], 2))
    bit_21_25_value = "func_type=" + hex_binary_21_25

    hex_binary_26 = hex(int(byteval[-27], 2))
    bit_26_value = "valid=" + hex_binary_26

    return (
        bit_0_7_value,
        ";",
        bit_8_12_value,
        ";",
        bit_13_20_value,
        ";",
        bit_21_25_value,
        ";",
        bit_26_value,
    )


def hex_22_value(byteval):
    if "x" in byteval:
        cmd = byteval
        if "MEM" in cmd:
            window_type = "0"
            requester = bin(int(cmd.split("requester=")[1].split(")")[0], 16)).replace(
                "0b", ""
            )
            requester = format_data_length(requester, 16)
            pasid = bin(int(cmd.split("pasid=")[1].split(";requester")[0], 16)).replace(
                "0b", ""
            )
            pasid = format_data_length(pasid, 23)
            window_base_index = bin(
                int(cmd.split("window_base_index=")[1].split(";pasid")[0], 16)
            ).replace("0b", "")
            window_base_index = format_data_length(window_base_index, 52)
            pcie_no_snoop = bin(
                int(cmd.split("pcie_no_snoop=")[1].split(";window_base_index")[0], 16)
            ).replace("0b", "")
            write_enable = bin(
                int(cmd.split("write_enable=")[1].split(";pcie_no_snoop")[0], 16)
            ).replace("0b", "")
            read_enable = bin(
                int(cmd.split("read_enable=")[1].split(";write_enable")[0], 16)
            ).replace("0b", "")
            csi_dst_fifo = bin(
                int(cmd.split("csi_dst_fifo=")[1].split(";read_enable")[0], 16)
            ).replace("0b", "")
            csi_dst_fifo = format_data_length(csi_dst_fifo, 9)
            csi_dst = bin(
                int(CSI_SRC_DST[cmd.split("csi_dest=")[1].split("(")[0]].value, 16)
            ).replace("0b", "")
            csi_dest = format_data_length(csi_dst, 5)
            data = (
                    requester
                    + pasid
                    + window_base_index
                    + pcie_no_snoop
                    + write_enable
                    + read_enable
                    + csi_dst_fifo
                    + csi_dest
                    + window_type
            )

        else:
            window_type = "1"
            reserved = bin(int(cmd.split("reserved=")[1], 16)).replace("0b", "")
            reserved = format_data_length(reserved, 90)
            csi_dst = bin(
                int(CSI_SRC_DST[cmd.split(";csi_dest=")[1].split("(")[0]].value, 16)
            ).replace("0b", "")
            csi_dest = format_data_length(csi_dst, 5)
            csi_dst_fifo = bin(
                int(cmd.split("csi_dst_fifo=")[1].split(";reserved")[0], 16)
            ).replace("0b", "")
            csi_dst_fifo = format_data_length(csi_dst_fifo, 9)
            data = reserved + csi_dst_fifo + csi_dest + window_type
        data_value = data
        data_value = hex(int(data_value, 2)).replace("0x", "")
        return create_hex_list(data_value, 8)
    byteval = (
        "0" * (104 - len(byteval)) + str(byteval) if len(byteval) < 104 else byteval
    )
    bit_0 = byteval[-1]
    if bit_0 == "0":
        hex_binary_5_1 = hex(int(byteval[-6:-1], 2))
        bit_5_1_value = (
                "csi_dest=" + CSI_SRC_DST(hex_binary_5_1).name + "(" + hex_binary_5_1 + ")"
        )

        hex_binary_6_14 = hex(int(byteval[-15:-6], 2))
        bit_6_14_value = "csi_dst_fifo=" + hex_binary_6_14

        hex_binary_15 = hex(int(byteval[-16], 2))
        bit_15_value = "read_enable=" + hex_binary_15

        hex_binary_16 = hex(int(byteval[-17], 2))
        bit_16_value = "write_enable=" + hex_binary_16

        hex_binary_17 = hex(int(byteval[-18], 2))
        bit_17_value = "pcie_no_snoop=" + hex_binary_17

        hex_binary_18_69 = hex(int(byteval[-70:-18], 2))
        bit_18_69_value = "window_base_index=" + hex_binary_18_69

        hex_binary_70_88 = hex(int(byteval[-93:-70], 2))
        bit_70_88_value = "pasid=" + hex_binary_70_88

        hex_binary_89_104 = hex(int(byteval[-108:-93], 2))
        bit_89_104_value = "requester=" + hex_binary_89_104
        data_frame = [["requester", hex_binary_89_104],
                      ["pasid", hex_binary_70_88],
                      ["window_base_index", hex_binary_18_69],
                      ["pcie_no_snoop", hex_binary_17],
                      ["write_enable", hex_binary_16],
                      ["read_enable", hex_binary_15],
                      ["csi_dst_fifo", hex_binary_6_14],
                      ["csi_dest", f"{CSI_SRC_DST(hex_binary_5_1).name} ({hex_binary_5_1})"]]
        data_frame = pd.DataFrame(data_frame, columns=[[f'A2C_APERTURE_WINDOW', '']])
        data_frame.columns = ['A2C_APERTURE_WINDOW', 'Value']
        return data_frame, (
            "Type=MEM(",
            bit_5_1_value,
            ";",
            bit_6_14_value,
            ";",
            bit_15_value,
            ";",
            bit_16_value,
            ";",
            bit_17_value,
            ";",
            bit_18_69_value,
            ";",
            bit_70_88_value,
            ";",
            bit_89_104_value + ")",
        )
    else:
        hex_binary_5_1 = hex(int(byteval[-6:-1], 2))
        bit_5_1_value = (
                "csi_dst=" + CSI_SRC_DST(hex_binary_5_1).name + "(" + hex_binary_5_1 + ")"
        )

        hex_binary_6_14 = hex(int(byteval[-15:-6], 2))
        bit_6_14_value = "csi_dst_fifo=" + hex_binary_6_14

        hex_binary_15_104 = hex(int(byteval[-105:-15], 2))
        bit_15_104_value = "reserved=" + hex_binary_15_104
        return (
            "Type=INTR(",
            bit_5_1_value,
            ";",
            bit_6_14_value,
            ";",
            bit_15_104_value + ")",
        )


def create_hex_list(a, n):
    """Create specific length hexadecimal value list from hexadecimal string values"""
    data = " ".join([a[-i - n: -i if i else None] for i in range(0, len(a), n)][::-1])
    return ["0x" + format_data_length(x, n) for x in data.split(" ")][::-1]


def hex_23_value(byteval):
    bit_92_91_dict = {
        "00": "C2A_EM_BDF",
        "01": "C2A_EM_FUNC_BAR_OFF",
        "10": "C2A_EM_FUNC_ADDR",
    }
    if "x" in byteval:
        cmd = byteval
        unordered_axi_id = bin(int(cmd.split("unordered_axi_id=")[1], 16)).replace(
            "0b", ""
        )
        unordered_axi_id = format_data_length(unordered_axi_id, 4)
        unordered_wr = bin(
            int(cmd.split("unordered_wr=")[1].split(";unordered_axi_id")[0], 16)
        ).replace("0b", "")
        stash_indx_from_csi_st = bin(
            int(cmd.split("stash_indx_from_csi_st=")[1].split(";unordered_wr")[0], 16)
        ).replace("0b", "")
        stash_indx = bin(
            int(cmd.split("stash_indx=")[1].split(";stash_indx_from_csi_st")[0], 16)
        ).replace("0b", "")
        stash_indx = format_data_length(stash_indx, 5)
        encoding_mode = cmd.split("encoding_mode=")[1].split(";stash_indx")[0]
        encoding_mode = dict((v, k) for k, v in bit_92_91_dict.items()).get(
            encoding_mode
        )
        encoding_mode = format_data_length(encoding_mode, 2)
        xmti_from_rq = bin(
            int(cmd.split("xmti_from_rq=")[1].split(";encoding_mode")[0], 16)).replace("0b", "")
        axi_base_page_idx = bin(
            int(cmd.split("axi_base_page_idx=")[1].split(";ap_xmti=")[0], 16)
        ).replace("0b", "")
        axi_base_page_idx = format_data_length(axi_base_page_idx, 39)
        ap_xmti = bin(
            int(cmd.split("ap_xmti=")[1].split(";xmti_from_rq")[0], 16)).replace("0b", "")
        ap_xmti = format_data_length(ap_xmti, 12)

        ap_size_pages = bin(
            int(cmd.split("ap_size_pages=")[1].split(";axi_base_page_idx")[0], 16)).replace("0b", "")
        ap_size_pages = format_data_length(ap_size_pages, 36)

        rp_completer = bin(
            int(cmd.split("rp_completer=")[1].split(";ap_size_pages=")[0], 16)
        ).replace("0b", "")
        rp_completer = format_data_length(rp_completer, 16)
        squash_err = bin(
            int(cmd.split("squash_err=")[1].split(";rp_completer=")[0], 16)
        ).replace("0b", "")
        axcache = bin(
            int(cmd.split("axcache=")[1].split(";squash_err=")[0], 16)
        ).replace("0b", "")
        axcache = format_data_length(axcache, 2)
        reserved = bin(int(cmd.split("Valid=")[1].split(";axcache=")[0], 16)).replace(
            "0b", ""
        )
        data_value = (
                unordered_axi_id
                + unordered_wr
                + stash_indx_from_csi_st
                + stash_indx
                + encoding_mode
                + xmti_from_rq
                + ap_xmti
                + axi_base_page_idx
                + ap_size_pages
                + rp_completer
                + squash_err
                + axcache
                + reserved
        )
        data_value = hex(int(data_value, 2)).replace("0x", "")
        return create_hex_list(data_value, 8)
    byteval = (
        "0" * (104 - len(byteval)) + str(byteval) if len(byteval) < 104 else byteval
    )
    hex_binary_0 = hex(int(byteval[-1], 2))

    bit_0_value = "Valid=" + hex_binary_0
    if hex_binary_0 == '0x0':
        hex_binary_0 = "Invalid"
    hex_binary_2_1 = hex(int(byteval[-3:-1], 2))
    bit_2_1_value = "axcache=" + hex_binary_2_1
    if byteval[-4] == "1":
        hex_binary_3 = hex(int(byteval[-4], 2))
        bit_3_value = "squash_err=" + hex_binary_3
    else:
        hex_binary_3 = hex(int(byteval[-4], 2))
        bit_3_value = "squash_err=" + hex_binary_3

    hex_binary_19_4 = hex(int(byteval[-20:-4], 2))
    bit_19_4_value = "rp_completer=" + hex_binary_19_4

    hex_binary_55_20 = hex(int(byteval[-56:-20], 2))
    bit_55_20_value = "ap_size_pages=" + hex_binary_55_20

    hex_binary_94_56 = hex(int(byteval[-95:-56], 2))
    bit_94_56_value = "axi_base_page_idx=" + hex_binary_94_56

    hex_binary_106_95 = hex(int(byteval[-107:-95], 2))
    bit_106_95_value = "ap_xmti=" + hex_binary_106_95

    hex_binary_107 = hex(int(byteval[-108], 2))
    bit_107_value = "xmti_from_rq=" + hex_binary_107

    hex_binary_109_108 = hex(int(byteval[-110:-108], 2))
    bit_109_108 = byteval[-110] + byteval[-109]
    bit_109_108_value = "encoding_mode=" + bit_92_91_dict[bit_109_108]

    hex_binary_114_110 = hex(int(byteval[-115:-110], 2))
    bit_114_110_value = "stash_indx=" + hex_binary_114_110

    hex_binary_115 = hex(int(byteval[-116], 2))
    bit_115_value = "stash_indx_from_csi_st=" + hex_binary_115

    hex_binary_116 = hex(int(byteval[-117], 2))
    bit_116_value = "unordered_wr=" + hex_binary_116

    hex_binary_120_117 = hex(int(byteval[-121:-117], 2))
    bit_120_117_value = "unordered_axi_id=" + hex_binary_120_117

    data_frame = [['Valid', hex_binary_0],
                  ["unordered_axi_id", hex_binary_120_117], ["unordered_wr", hex_binary_116],
                  ["stash_indx_from_csi_st", hex_binary_115],
                  ["stash_indx", hex_binary_114_110],
                  ["encoding_mode", f'{hex_binary_109_108} ({bit_92_91_dict[bit_109_108]})'],
                  ["ap_xmti", hex_binary_106_95],
                  ["axi_base_page_idx", hex_binary_94_56],
                  ['ap_size_pages', hex_binary_55_20],
                  ["rp_completer", hex_binary_19_4],
                  ["squash_err", hex_binary_3],
                  ["axcache", hex_binary_2_1],
                  ["reserved", hex_binary_0]]
    data_frame = pd.DataFrame(data_frame)

    return data_frame, (
        bit_0_value,
        ";",
        bit_2_1_value,
        ";",
        bit_3_value,
        ";",
        bit_19_4_value,
        ";",
        bit_55_20_value,
        ";",
        bit_94_56_value,
        ";",
        bit_106_95_value,
        ";",
        bit_107_value,
        ";",
        bit_109_108_value,
        ";",
        bit_114_110_value,
        ";",
        bit_115_value,
        ";",
        bit_116_value,
        ";",
        bit_120_117_value
    )


def hex_24_value(byteval):
    if "x" in byteval:
        cmd = byteval
        axid_0 = bin(int(cmd.split("axid_0=")[1].split(";axid_1=")[0], 16)).replace(
            "0b", ""
        )
        axid_0 = format_data_length(axid_0, 3)
        axid_1 = bin(int(cmd.split("axid_1=")[1].split(";axid_2")[0], 16)).replace(
            "0b", ""
        )
        axid_1 = format_data_length(axid_1, 3)
        axid_2 = bin(int(cmd.split("axid_2=")[1].split(";axid_3")[0], 16)).replace(
            "0b", ""
        )
        axid_2 = format_data_length(axid_2, 3)
        axid_3 = bin(int(cmd.split("axid_3=")[1].split(";axid_4")[0], 16)).replace(
            "0b", ""
        )
        axid_3 = format_data_length(axid_3, 3)
        axid_4 = bin(int(cmd.split("axid_4=")[1].split(";axid_5")[0], 16)).replace(
            "0b", ""
        )
        axid_4 = format_data_length(axid_4, 3)
        axid_5 = bin(int(cmd.split("axid_5=")[1], 16)).replace("0b", "")
        axid_5 = format_data_length(axid_5, 3)
        data_value = (
                "00000000"
                + "0"
                + axid_5
                + "0"
                + axid_4
                + "0"
                + axid_3
                + "0"
                + axid_2
                + "0"
                + axid_1
                + "0"
                + axid_0
        )
        data_value = hex(int(data_value, 2))
        data_value = (
            data_value
            if len(data_value) == 10
            else "0x" + (10 - len(data_value)) * "0" + data_value.replace("0x", "")
        )
        return data_value

    hex_binary_0 = hex(int(byteval[-1], 2))
    bit_0_value = "valid=" + hex_binary_0

    hex_binary_0_2 = hex(int(byteval[-3:], 2))
    bit_0_2_value = "axid_0=" + hex_binary_0_2

    hex_binary_3 = hex(int(byteval[-4], 2))
    bit_3_value = "reserved=" + hex_binary_3

    hex_binary_4_6 = hex(int(byteval[-7:-4], 2))
    bit_4_6_value = "axid_1=" + hex_binary_4_6

    hex_binary_7 = hex(int(byteval[-8], 2))
    bit_7_value = "reserved=" + hex_binary_7

    hex_binary_8_10 = hex(int(byteval[-11:-8], 2))
    bit_8_10_value = "axid_2=" + hex_binary_8_10

    hex_binary_11 = hex(int(byteval[-12], 2))
    bit_11_value = "reserved=" + hex_binary_11

    hex_binary_12_14 = hex(int(byteval[-15:-12], 2))
    bit_12_14_value = "axid_3=" + hex_binary_12_14

    hex_binary_15 = hex(int(byteval[-16], 2))
    bit_15_value = "reserved=" + hex_binary_15

    hex_binary_16_18 = hex(int(byteval[-19:-16], 2))
    bit_16_18_value = "axid_4=" + hex_binary_16_18

    hex_binary_19 = hex(int(byteval[-20], 2))
    bit_19_value = "reserved=" + hex_binary_19

    hex_binary_20_22 = hex(int(byteval[-23:-20], 2))
    bit_20_22_value = "axid_5=" + hex_binary_20_22

    hex_binary_23 = hex(int(byteval[-24], 2))
    bit_23_value = "reserved=" + hex_binary_23

    hex_binary_24_31 = hex(int(byteval[-32:-24], 2))
    bit_24_31_value = "reserved=" + hex_binary_24_31

    data_frame = [["axid_5", hex_binary_20_22], ["axid_4", hex_binary_16_18],
                  ["axid_3", hex_binary_12_14],
                  ["axid_2", hex_binary_8_10],
                  ["axid_1", hex_binary_4_6],
                  ["axid_0", hex_binary_0_2]]
    data_frame = pd.DataFrame(data_frame)

    return data_frame, (
        bit_0_2_value,
        ";",
        bit_4_6_value,
        ";",
        bit_8_10_value,
        ";",
        bit_12_14_value,
        ";",
        bit_16_18_value,
        ";",
        bit_20_22_value,
    )


def hex_25_value(byteval):
    if "x" in byteval:
        cmd = byteval
        axid_0 = bin(int(cmd.split("axid_0=")[1].split(";axid_1=")[0], 16)).replace(
            "0b", ""
        )
        axid_0 = format_data_length(axid_0, 3)
        axid_1 = bin(int(cmd.split("axid_1=")[1].split(";axid_2")[0], 16)).replace(
            "0b", ""
        )
        axid_1 = format_data_length(axid_1, 3)
        axid_2 = bin(int(cmd.split("axid_2=")[1].split(";axid_3")[0], 16)).replace(
            "0b", ""
        )
        axid_2 = format_data_length(axid_2, 3)
        axid_3 = bin(int(cmd.split("axid_3=")[1].split(";axid_4")[0], 16)).replace(
            "0b", ""
        )
        axid_3 = format_data_length(axid_3, 3)
        axid_4 = bin(int(cmd.split("axid_4=")[1].split(";axid_5")[0], 16)).replace(
            "0b", ""
        )
        axid_4 = format_data_length(axid_4, 3)
        axid_5 = bin(int(cmd.split("axid_5=")[1], 16)).replace("0b", "")
        axid_5 = format_data_length(axid_5, 3)
        data_value = (
                "00000000"
                + "0"
                + axid_5
                + "0"
                + axid_4
                + "0"
                + axid_3
                + "0"
                + axid_2
                + "0"
                + axid_1
                + "0"
                + axid_0
        )
        data_value = hex(int(data_value, 2))
        data_value = (
            data_value
            if len(data_value) == 10
            else "0x" + (10 - len(data_value)) * "0" + data_value.replace("0x", "")
        )
        return data_value

    hex_binary_0_2 = hex(int(byteval[-3:], 2))
    bit_0_2_value = "axid_0=" + hex_binary_0_2

    hex_binary_3 = hex(int(byteval[-4], 2))
    bit_3_value = " reserved=" + hex_binary_3

    hex_binary_4_6 = hex(int(byteval[-7:-4], 2))
    bit_4_6_value = "axid_1=" + hex_binary_4_6

    hex_binary_7 = hex(int(byteval[-8], 2))
    bit_7_value = " reserved=" + hex_binary_7

    hex_binary_8_10 = hex(int(byteval[-11:-8], 2))
    bit_8_10_value = "axid_2=" + hex_binary_8_10

    hex_binary_11 = hex(int(byteval[-12], 2))
    bit_11_value = " reserved=" + hex_binary_11

    hex_binary_12_14 = hex(int(byteval[-15:-12], 2))
    bit_12_14_value = "axid_3=" + hex_binary_12_14

    hex_binary_15 = hex(int(byteval[-16], 2))
    bit_15_value = " reserved=" + hex_binary_15

    hex_binary_16_18 = hex(int(byteval[-19:-16], 2))
    bit_16_18_value = "axid_4=" + hex_binary_16_18

    hex_binary_19 = hex(int(byteval[-20], 2))
    bit_19_value = " reserved=" + hex_binary_19

    hex_binary_20_22 = hex(int(byteval[-23:-20], 2))
    bit_20_22_value = "axid_5=" + hex_binary_20_22

    hex_binary_23 = hex(int(byteval[-24], 2))
    bit_23_value = " reserved=" + hex_binary_23

    hex_binary_24_31 = hex(int(byteval[-32:-24], 2))
    bit_24_31_value = " reserved=" + hex_binary_24_31

    data_frame = [["axid_5", hex_binary_20_22], ["axid_4", hex_binary_16_18],
                  ["axid_3", hex_binary_12_14],
                  ["axid_2", hex_binary_8_10],
                  ["axid_1", hex_binary_4_6],
                  ["axid_0", hex_binary_0_2]]
    data_frame = pd.DataFrame(data_frame)

    return data_frame, (
        bit_0_2_value,
        ";",
        bit_4_6_value,
        ";",
        bit_8_10_value,
        ";",
        bit_12_14_value,
        ";",
        bit_16_18_value,
        ";",
        bit_20_22_value,
    )


def hex_26_value(byteval):
    if "x" in byteval:
        cmd = byteval
        Ipiden = bin(int(cmd.split("Ipiden=")[1], 16)).replace("0b", "")
        Ipid = bin(int(cmd.split("Ipid=")[1].split(";Ipiden=")[0], 16)).replace("0b", "")
        Ipid = format_data_length(Ipid, 5)
        niden = bin(int(cmd.split("niden=")[1].split(";Ipid=")[0], 16)).replace("0b", "")
        nid = bin(int(cmd.split("nid=")[1].split(";niden=")[0], 16)).replace("0b", "")
        nid = format_data_length(nid, 11)
        snoop = bin(int(cmd.split("snoop=")[1].split(";nid=")[0], 16)).replace("0b", "")
        snoop = format_data_length(snoop, 4)
        domain = bin(int(cmd.split("domain=")[1].split(";snoop=")[0], 16)).replace(
            "0b", ""
        )
        domain = format_data_length(domain, 11)
        data_value = Ipiden + Ipid + niden + nid + snoop + domain
        data_value = hex(int(data_value, 2)).replace("0x", "")
        data_value = "0x" + format_data_length(data_value, 8)
        return data_value

    hex_binary_0_1 = hex(int(byteval[-2:], 2))
    bit_0_1_value = "domain=" + hex_binary_0_1

    hex_binary_2_5 = hex(int(byteval[-6:-2], 2))
    bit_2_5_value = "snoop=" + hex_binary_2_5

    hex_binary_4_6 = hex(int(byteval[-6:-4], 2))
    bit_4_6_value = "nid=" + hex_binary_4_6

    hex_binary_7_17 = hex(int(byteval[-18:-7], 2))
    bit_7_17_value = "niden=" + hex_binary_7_17

    hex_binary_18_22 = hex(int(byteval[-23:-18], 2))
    bit_18_22_value = "Ipid=" + hex_binary_18_22

    hex_binary_23 = hex(int(byteval[-24], 2))
    bit_23_value = "Ipiden=" + hex_binary_23

    return (
        bit_0_1_value,
        ";",
        bit_2_5_value,
        ";",
        bit_4_6_value,
        ";",
        bit_7_17_value,
        ";",
        bit_18_22_value,
        ";",
        bit_23_value,
    )


def hex_28_value(byteval):
    if "x" in byteval:
        cmd = byteval
        xmti_mask = bin(int(cmd.split("xmti_mask=")[1], 16)).replace("0b", "")
        xmti_mask = format_data_length(xmti_mask, 12)
        xmti_match = bin(
            int(cmd.split("xmti_match=")[1].split("xmti_mask")[0], 16)
        ).replace("0b", "")
        xmti_match = format_data_length(xmti_match, 12)

        irqs_owned = bin(
            int(cmd.split("irqs_owned=")[1].split("xmti_match=")[0], 16)
        ).replace("0b", "")
        irqs_owned = format_data_length(irqs_owned, 32)
        mode = "0" if "MSI" in cmd else "1"

        msi_addr = bin(int(cmd.split("msi_addr=")[1].split("mode=")[0], 16)).replace(
            "0b", ""
        )
        msi_addr = format_data_length(msi_addr, 48)

        msi_data = bin(
            int(cmd.split("msi_data=")[1].split("msi_addr=")[0], 16)
        ).replace("0b", "")
        msi_data = format_data_length(msi_data, 16)

        level_rsv = bin(
            int(cmd.split("level_rsv=")[1].split("msi_data=")[0], 16)
        ).replace("0b", "")
        level_rsv = format_data_length(level_rsv, 62)
        level_sel = bin(
            int(cmd.split("level_sel=")[1].split("level_rsv=")[0], 16)
        ).replace("0b", "")
        level_sel = format_data_length(level_sel, 2)

        data_value = (
                xmti_mask
                + xmti_match
                + irqs_owned
                + mode
                + msi_addr
                + msi_data
                + level_rsv
                + level_sel
        )
        data_value = hex(int(data_value, 2)).replace("0x", "")
        return create_hex_list(data_value, 8)

    hex_binary_0_1 = hex(int(byteval[-2:], 2))
    bit_0_1_value = "level_sel=" + hex_binary_0_1

    hex_binary_2_63 = hex(int(byteval[-64:-2], 2))
    bit_2_63_value = "level_rsv=" + hex_binary_2_63

    hex_binary_0_15 = hex(int(byteval[-16:], 2))
    bit_0_15_value = "msi_data=" + hex_binary_0_15

    hex_binary_16_63 = hex(int(byteval[-64:-16], 2))
    bit_16_63_value = "msi_addr=" + hex_binary_16_63

    hex_binary_64 = hex(int(byteval[-65], 2))
    if byteval[-65] == "0":
        bit_64_value = "mode=MSI" + hex_binary_64
    else:
        bit_64_value = "mode=LEVEL" + hex_binary_64

    hex_binary_65_96 = hex(int(byteval[-97:-65], 2))
    bit_65_96_value = "irqs_owned=" + hex_binary_65_96

    hex_binary_97_108 = hex(int(byteval[-109:-97], 2))
    bit_97_108_value = "xmti_match=" + hex_binary_97_108

    hex_binary_109_120 = hex(int(byteval[-121:-109], 2))
    bit_109_120_value = "xmti_mask=" + hex_binary_109_120

    return (
        bit_0_1_value,
        ";",
        bit_2_63_value,
        ";",
        bit_0_15_value,
        ";",
        bit_16_63_value,
        ";",
        bit_64_value,
        ";",
        bit_65_96_value,
        ";",
        bit_97_108_value,
        ";",
        bit_109_120_value,
    )


def hex_34_value(byteval):
    if "x" in byteval:
        cmd = byteval
        Rsvd4 = bin(int(cmd.split("Rsvd4=")[1], 16)).replace("0b", "")
        Rsvd4 = format_data_length(Rsvd4, 4)
        chan_id_3_to_base = bin(
            int(cmd.split("chan_id_3_to_base=")[1].split("Rsvd4=")[0], 16)
        ).replace("0b", "")
        chan_id_3_to_base = format_data_length(chan_id_3_to_base, 12)
        Rsvd3 = bin(
            int(cmd.split("Rsvd3=")[1].split("chan_id_3_to_base=")[0], 16)
        ).replace("0b", "")
        Rsvd3 = format_data_length(Rsvd3, 4)
        chan_id_2_to_base = bin(
            int(cmd.split("chan_id_2_to_base=")[1].split("Rsvd3=")[0], 16)
        ).replace("0b", "")
        chan_id_2_to_base = format_data_length(chan_id_2_to_base, 12)
        Rsvd2 = bin(
            int(cmd.split("Rsvd2=")[1].split("chan_id_2_to_base=")[0], 16)
        ).replace("0b", "")
        Rsvd2 = format_data_length(Rsvd2, 4)
        chan_id_1_to_base = bin(
            int(cmd.split("chan_id_1_to_base=")[1].split("Rsvd2=")[0], 16)
        ).replace("0b", "")
        chan_id_1_to_base = format_data_length(chan_id_1_to_base, 12)
        Rsvd1 = bin(
            int(cmd.split("Rsvd1=")[1].split("chan_id_1_to_base=")[0], 16)
        ).replace("0b", "")
        Rsvd1 = format_data_length(Rsvd1, 4)
        chan_id_0_to_base = bin(
            int(cmd.split("chan_id_0_to_base=")[1].split("Rsvd1=")[0], 16)
        ).replace("0b", "")
        chan_id_0_to_base = format_data_length(chan_id_0_to_base, 12)
        Rsvd0 = bin(
            int(cmd.split("Rsvd0=")[1].split("chan_id_0_to_base=")[0], 16)
        ).replace("0b", "")
        Rsvd0 = format_data_length(Rsvd0, 29)
        ddr0_path = bin(int(cmd.split("ddr0_path=")[1].split("Rsvd0")[0], 16)).replace(
            "0b", ""
        )
        ddr0_path = format_data_length(ddr0_path, 2)
        chan_id_0_is_ddr0 = bin(
            int(cmd.split("chan_id_0_is_ddr0=")[1].split("ddr0_path")[0], 16)
        ).replace("0b", "")
        data_value = (
                Rsvd4
                + chan_id_3_to_base
                + Rsvd3
                + chan_id_2_to_base
                + Rsvd2
                + chan_id_1_to_base
                + Rsvd1
                + chan_id_0_to_base
                + Rsvd0
                + ddr0_path
                + chan_id_0_is_ddr0
        )
        data_value = hex(int(data_value, 2)).replace("0x", "")
        return create_hex_list(data_value, 8)

    hex_binary_0 = hex(int(byteval[-1], 2))
    bit_0_value = "chan_id_0_is_ddr0=" + hex_binary_0

    hex_binary_1_2 = hex(int(byteval[-3:-1], 2))
    bit_1_2_value = "ddr0_path=" + hex_binary_1_2

    hex_binary_3_31 = hex(int(byteval[-32:-3], 2))
    bit_3_31_value = "Rsvd0=" + hex_binary_3_31

    hex_binary_32_43 = hex(int(byteval[-44:-32], 2))
    bit_32_43_value = "chan_id_0_to_base=" + hex_binary_32_43

    hex_binary_44_47 = hex(int(byteval[-48:-44], 2))
    bit_44_47_value = "Rsvd1=" + hex_binary_44_47

    hex_binary_48_59 = hex(int(byteval[-60:-48], 2))
    bit_48_59_value = "chan_id_1_to_base=" + hex_binary_48_59

    hex_binary_60_63 = hex(int(byteval[-64:-60], 2))
    bit_60_63_value = "Rsvd2=" + hex_binary_60_63

    hex_binary_64_75 = hex(int(byteval[-76:-64], 2))
    bit_64_75_value = "chan_id_2_to_base=" + hex_binary_64_75

    hex_binary_76_79 = hex(int(byteval[-80:-76], 2))
    bit_76_79_value = "Rsvd3=" + hex_binary_76_79

    hex_binary_80_91 = hex(int(byteval[-92:-80], 2))
    bit_80_91_value = "chan_id_3_to_base=" + hex_binary_80_91

    hex_binary_92_95 = hex(int(byteval[-96:-92], 2))
    bit_92_95_value = "Rsvd4=" + hex_binary_92_95

    return (
        bit_0_value,
        ";",
        bit_1_2_value,
        ";",
        bit_3_31_value,
        ";",
        bit_32_43_value,
        ";",
        bit_44_47_value,
        ";",
        bit_48_59_value,
        ";",
        bit_60_63_value,
        ";",
        bit_64_75_value,
        ";",
        bit_76_79_value,
        ";",
        bit_80_91_value,
        ";",
        bit_92_95_value,
    )


def HAH_FNNO_2_PFVFDCID_ENTRY_0(data):
    if "=" in data:
        dcid = data.split("dcid=")[1].split(
            ";"
        )[0]
        dcid = hex_to_bin(dcid)
        dcid = format_data_length(dcid, 4)
        vi_stride_id = data.split("vi_stride_id=")[1].split(
            ";"
        )[0]
        vi_stride_id = hex_to_bin(vi_stride_id)
        vi_stride_id = format_data_length(vi_stride_id, 3)
        en = data.split("en=")[1]
        en = hex_to_bin(en)
        data_value = en + vi_stride_id + dcid
        data_value = format_hex_value(data_value)
        return data_value
    return ":: dcid=" + hex(int(data[-4:], 2)) + ";vi_stride_id=" + hex(int(data[-7:-4], 2)) + ";en=" + hex(
        int(data[-8], 2))


def HAH_FNNO_2_PFVFDCID_ENTRY_1(data):
    if "=" in data:
        pasid_shift = data.split("pasid_shift=")[1].split(
            ";"
        )[0]
        pasid_shift = hex_to_bin(pasid_shift)
        pasid_shift = format_data_length(pasid_shift, 2)
        num_vi = data.split("num_vi=")[1].split(
            ";"
        )[0]
        num_vi = hex_to_bin(num_vi)
        num_vi = format_data_length(num_vi, 13)
        base_vi = data.split("base_vi=")[1]
        base_vi = hex_to_bin(base_vi)
        base_vi = format_data_length(base_vi, 13)
        data_value = base_vi + num_vi + pasid_shift
        data_value = format_hex_value(data_value)
        return data_value
    return ":: pasid_shift=" + hex(int(data[-2:], 2)) + ";num_vi=" + hex(
        int(data[-15:-2], 2)) + ";base_vi=" + bin_to_hex(data[-28:-15])


def HAH_FNNO_2_PFVFDCID_INST(data):
    if "=" in data:
        fn_no = data.split("fn_no=")[1].split(
            ";"
        )[0]
        fn_no = hex_to_bin(fn_no)
        fn_no = format_data_length(fn_no, 12)
        rw = data.split("rw=")[1].split(
            ";"
        )[0]
        rw = hex_to_bin(rw)
        data_value = rw + '0000000000000000000' + fn_no
        data_value = format_hex_value(data_value)
        return data_value
    return ":: fn_no=" + bin_to_hex(data[-13:]) + ";rw=" + bin_to_hex(data[-32])


def TCAM_ENTRY_0(data):
    if "=" in data:
        rw_mask = data.split("rw_mask=")[1].split(
            ";"
        )[0]
        rw_mask = hex_to_bin(rw_mask)
        rw = data.split("rw=")[1].split(
            ";"
        )[0]
        rw = hex_to_bin(rw)
        bar_mask = data.split("bar_mask=")[1].split(
            ";"
        )[0]
        bar_mask = hex_to_bin(bar_mask)
        bar_mask = format_data_length(bar_mask, 7)
        bar = data.split("bar=")[1].split(
            ";"
        )[0]
        bar = hex_to_bin(bar)
        bar = format_data_length(bar, 3)
        dcid = data.split("dcid=")[1].split(
            ";"
        )[0]
        dcid = hex_to_bin(dcid)
        dcid = format_data_length(dcid, 4)

        dcid_mask = data.split("dcid_mask=")[1].split(
            ";"
        )[0]
        dcid_mask = hex_to_bin(dcid_mask)
        dcid_mask = format_data_length(dcid_mask, 4)

        data_value = dcid_mask + dcid + bar + bar_mask + rw + rw_mask
        data_value = format_hex_value(data_value)
        return data_value
    return ":: rw_mask=" + bin_to_hex(data[-1]) + ";rw=" + bin_to_hex(data[-2]) + ";bar_mask=" + bin_to_hex(data[-8:-5]) \
           + ";bar=" + bin_to_hex(data[-11:-8]) + ";dcid=" + bin_to_hex(data[-17:-13]) + ";dcid_mask=" + bin_to_hex(
        data[-21:-17])


def TCAM_ENTRY_1(data):
    if "=" in data:
        bar_offset = data.split("bar_offset=")[1].split(
            ";"
        )[0]
        bar_offset = hex_to_bin(bar_offset)
        bar_offset = format_data_length(bar_offset, 25)
        data_value = bar_offset
        data_value = format_hex_value(data_value)
        return data_value
    return ":: bar_offset=" + bin_to_hex(data[-26:])


def TCAM_ENTRY_2(data):
    if "=" in data:
        bar_offset = data.split("bar_offset=")[1].split(
            ";"
        )[0]
        bar_offset = hex_to_bin(bar_offset)
        bar_offset = format_data_length(bar_offset, 25)
        data_value = bar_offset
        data_value = format_hex_value(data_value)
        return data_value
    return ":: bar_offset=" + bin_to_hex(data[-26:])


def TCAM_ENTRY_3(data):
    if "=" in data:
        smid = data.split("smid=")[1].split(
            ";"
        )[0]
        smid = hex_to_bin(smid)
        smid = format_data_length(smid, 12)

        smid_mask = data.split("smid_mask=")[1].split(
            ";"
        )[0]
        smid_mask = hex_to_bin(smid_mask)
        smid_mask = format_data_length(smid_mask, 12)
        pasidv = data.split("pasidv=")[1].split(
            ";"
        )[0]
        pasidv = hex_to_bin(pasidv)
        pasidv_mask = data.split("pasidv_mask=")[1]
        pasidv_mask = hex_to_bin(pasidv_mask)
        data_value = pasidv_mask + pasidv + smid_mask + smid
        data_value = format_hex_value(data_value)
        return data_value
    return ":: smid=" + bin_to_hex(data[-12:]) + ";smid_mask=" + bin_to_hex(data[-24:-12]) + ";pasidv=" + bin_to_hex(
        data[-25]) \
           + ";pasidv_mask=" + bin_to_hex(data[-26])


def TCAM_RESULT_0(data):
    if "=" in data:
        bar_offset = data.split("ap_base_lsb=")[1]
        bar_offset = hex_to_bin(bar_offset)
        bar_offset = format_data_length(bar_offset, 25)
        data_value = bar_offset
        data_value = format_hex_value(data_value)
        return data_value
    return ":: ap_base_lsb=" + bin_to_hex(data[-32:])


def TCAM_RESULT_1(data):
    if "=" in data:
        ap_base_msb = data.split("ap_base_msb=")[1].split(
            ";"
        )[0]
        ap_base_msb = hex_to_bin(ap_base_msb)
        ap_base_msb = format_data_length(ap_base_msb, 18)
        ap_size = data.split("ap_size=")[1].split(
            ";"
        )[0]
        ap_size = hex_to_bin(ap_size)
        ap_size = format_data_length(ap_size, 6)
        data_value = ap_size + '000000' + ap_base_msb
        data_value = format_hex_value(data_value)
        return data_value
    return ":: ap_base_msb=" + bin_to_hex(data[-19:]) + ";ap_size=" + bin_to_hex(data[-30:-24])


def TCAM_RESULT_2(data):
    if "=" in data:
        dst_id = data.split("dst_id=")[1].split(
            ";"
        )[0]
        dst_id = hex_to_bin(dst_id)
        dst_id = format_data_length(dst_id, 3)
        posted_en = data.split("posted_en=")[1].split(
            ";"
        )[0]
        posted_en = hex_to_bin(posted_en)
        md_lbn = data.split("md_lbn=")[1].split(
            ";"
        )[0]
        md_lbn = hex_to_bin(md_lbn)
        md_lbn = format_data_length(md_lbn, 4)
        en_wht = data.split("en_wht=")[1].split(
            ";"
        )[0]
        en_wht = hex_to_bin(en_wht)
        en_wht = format_data_length(en_wht, 2)
        en_whr = data.split("en_whr=")[1].split(
            ";"
        )[0]
        en_whr = hex_to_bin(en_whr)
        en_whr = format_data_length(en_whr, 2)
        so_idx = data.split("so_idx=")[1].split(
            ";"
        )[0]
        so_idx = hex_to_bin(so_idx)
        so_idx = format_data_length(so_idx, 4)
        en = data.split(";en=")[1]
        en = hex_to_bin(en)
        data_value = en + '00' + so_idx + en_whr + en_wht + md_lbn + posted_en + '0000000000000' + dst_id
        data_value = format_hex_value(data_value)
        return data_value
    return ":: dst_id=" + bin_to_hex(data[-3:]) + ";posted_en=" + bin_to_hex(data[-17]) + ";md_lbn=" + bin_to_hex(
        data[-21:-17]) + ";en_wht=" \
           + bin_to_hex(data[-23:-21]) + ";en_whr=" + bin_to_hex(data[-25:-23]) + ";so_idx=" + bin_to_hex(
        data[-29:-25]) + ";en=" + bin_to_hex(data[-32])


def TCAM_RESULT_3(data):
    if "=" in data:
        metadata_offset = data.split("metadata_offset=")[1].split(
            ";"
        )
        metadata_offset = hex_to_bin(metadata_offset)
        metadata_offset = format_data_length(metadata_offset, 16)
        data_value = metadata_offset
        data_value = format_hex_value(data_value)
        return data_value
    return ":: metadata_offset=" + bin_to_hex(data[-16:])


def TCAM_INST(data):
    if "=" in data:
        index = data.split("index=")[1].split(
            ";"
        )[0]
        index = hex_to_bin(index)
        index = format_data_length(index, 5)

        opcode = data.split("opcode=")[1]
        opcode = hex_to_bin(opcode)

        data_value = opcode + '00000000000000000000000000' + index
        data_value = format_hex_value(data_value)
        return data_value
    return ":: index=" + bin_to_hex(data[-6:]) + ";opcode=" + bin_to_hex(data[-32])


def TCAM_STATUS(data):
    if "=" in data:
        index = data.split("tcam_status=")[1].split(
            ";"
        )
        index = hex_to_bin(index)
        index = format_data_length(index, 5)

        data_value = index
        data_value = format_hex_value(data_value)
        return data_value
    return ":: tcam_status=" + bin_to_hex(data[-7:])


def multiple_dfs(writer, df_list, sheets, spaces, startrow=0, startcol=0):
    if df_list is not list:
        for dataframe in df_list:
            dataframe.to_excel(writer, sheet_name=sheets, startrow=startrow, startcol=startcol, index=False,
                               header=True)
            startrow = startrow + len(dataframe.index) + spaces + 1
    else:
        df_list.to_excel(writer, sheet_name=sheets, startrow=startrow, startcol=startcol)


def convert_c_file_to_cdo(input_file):
    """Convert config header file into cdo file"""
    cdo = input_file.split('.')[0] + '.cdo'
    cdo_file = open(cdo, 'w')
    try:
        file1 = open(input_file, "r")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found {e}")
    for f in file1:
        if 'Xil_Out32' in f:
            f = f.replace('Xil_Out32', 'write').replace('(', ' ').replace(')', ' ').replace(';', '').replace(',',
                                                                                                             ' ').split(
                '//')[0].lower().strip() + '\n'
            cdo_file.write(f)
    cdo_file.close()
    return cdo


def eqdma_bit_4_1_calculation(padded_binary):
    bit_6_1 = (
            padded_binary[-5]
            + padded_binary[-4]
            + padded_binary[-3]
            + padded_binary[-2]
    )
    hex_binary = hex(int(bit_6_1, 2))
    hex_binary_split = hex_binary.replace('0x', '')
    bit_6_1_dict = {
        "0": "QDMA_CTXT_SELC_DEC_SW",
        "1": "Reserved",
        "2": "QDMA_CTXT_SELC_DEC_HW",
        "3": "Reserved",
        "4": "QDMA_CTXT_SELC_DEC_CR",
        "5": "Reserved",
        "6": "QDMA_CTXT_SELC_WRB",
        "7": "QDMA_CTXT_SELC_PFTCH",
        "8": "QDMA_CTXT_SELC_INT_COAL",
        "9": "QDMA_CTXT_SELC_FMAP_CFG",
        "a": "Reserved",
        "b": "QDMA_CTXT_SELC_TIMER",
        "c": "QDMA_CTXT_SELC_FMAP",
        "d": "Reserved",
        "e": "QDMA_CTXT_SELC_C2H_DROP",
        "f": "QDMA_CTXT_SELC_CSI_PROF"
    }
    bit_6_1_value = "sel=" + hex_binary + "(" + bit_6_1_dict[hex_binary_split] + ")"
    return bit_6_1_value


def eqdma_bit_6_5_calculation(padded_binary):
    bit_6_5 = padded_binary[-7] + padded_binary[-6]
    hex_binary = hex(int(bit_6_5, 2))
    bit_6_5_dict = {"00": "QDMA_CTXT_CMD_CLR", "01": "QDMA_CTXT_CMD_WR", "10": "QDMA_CTXT_CMD_RD",
                    "11": "QDMA_CTXT_CMD_INV"}
    bit_6_5_value = "op=" + hex_binary + "(" + bit_6_5_dict[bit_6_5] + ")"
    return bit_6_5_value


def eqdma_bit_19_7_calculation(padded_binary):
    bit_19_7 = (padded_binary[-20]
                + padded_binary[-19]
                + padded_binary[-18]
                + padded_binary[-17]
                + padded_binary[-16]
                + padded_binary[-15]
                + padded_binary[-14]
                + padded_binary[-13]
                + padded_binary[-12]
                + padded_binary[-11]
                + padded_binary[-10]
                + padded_binary[-9]
                + padded_binary[-8]
                )
    hex_binary = hex(int(bit_19_7, 2))
    bit_19_7_value = "Qid=" + hex_binary
    return bit_19_7_value


def eqdma_bit_31_20_calculation(padded_binary):
    bit_31_20 = (
            padded_binary[-32]
            + padded_binary[-31]
            + padded_binary[-30]
            + padded_binary[-29]
            + padded_binary[-28]
            + padded_binary[-27]
            + padded_binary[-26]
            + padded_binary[-25]
            + padded_binary[-24]
            + padded_binary[-23]
            + padded_binary[-22]
            + padded_binary[-21]
    )

    hex_binary = hex(int(bit_31_20, 2))
    bit_31_20_val = "Reserved"
    bit_31_20_val = "reserved: ", hex_binary, ":", "(", bit_31_20_val, ")"
    return bit_31_20_val


def eqdma_bit_0_calculation(padded_binary):
    bit_0_value = "busy=" + hex(int(padded_binary[-1], 2))
    return bit_0_value


def eqdma_get_data(count, Lines, register):
    """
    This method get and decode data for 8 registers of psx/pcie bridge and return values with specific register
    """
    base_add = '0xb4480000'
    value = ""
    Count_0 = count - 1
    line1 = data8 = data7 = data6 = data5 = data4 = data3 = data2 = data1 = ""
    for i in range(7, -1, -1):
        if re.search(r"480844", Lines[Count_0 - 1], re.IGNORECASE):
            add = re.search(r"480844", Lines[Count_0 - 1], re.IGNORECASE).start()
        if "mask_poll" not in Lines[Count_0 - 1] and len(Lines[Count_0 - 1]) != 0 \
                and f"480844 " not in Lines[Count_0 - 1]:
            data = Lines[Count_0 - 1].replace("\n", "").split(" ")
            data = [i for i in data if i]
            offset_val = data[1]
            add_val = data[2].replace("0x", "")
            offset = hex(int(offset_val, 16) - int(base_add, 16))
            if str(offset) == "0x804" and not data1:
                data1 = add_val
            elif str(offset) == "0x808" and not data2:
                data2 = add_val
            elif str(offset) == "0x80c" and not data3:
                data3 = add_val
            elif str(offset) == "0x810" and not data4:
                data4 = add_val
            elif str(offset) == "0x814" and not data5:
                data5 = add_val
            elif str(offset) == "0x818" and not data6:
                data6 = add_val
            elif str(offset) == "0x81c" and not data7:
                data7 = add_val
            elif str(offset) == "0x820" and not data8:
                data8 = add_val
            else:
                break
            line1 = (
                    data8 + data7 + data6 + data5 + data4 + data3 + data2 + data1
            )
            register = "\n" + str(Count_0) + "-->" + Lines[Count_0 - 1] + register
            value = convert_hex_binary(line1)
            Count_0 = Count_0 - 1
        else:
            break
    return register, value


def hex_f_value(byteval):
    if "=" in byteval:
        csi_dst_id = byteval.split("csi_dst_id=")[1].split(";")[0]
        csi_dst_id = hex_to_bin(csi_dst_id)
        csi_dst_id = format_data_length(csi_dst_id, 5)

        rsvd = byteval.split("rsvd=")[1].split(";")[0]
        rsvd = hex_to_bin(rsvd)
        rsvd = format_data_length(rsvd, 4)

        csi_dst_fifo_id = byteval.split("wrb_csi_fifo_id=")[1].split(";")[0]
        csi_dst_fifo_id = hex_to_bin(csi_dst_fifo_id)
        csi_dst_fifo_id = format_data_length(csi_dst_fifo_id, 9)

        dsc_csi_fifo_id = byteval.split("dsc_csi_fifo_id=")[1].split(";")[0]
        dsc_csi_fifo_id = hex_to_bin(dsc_csi_fifo_id)
        dsc_csi_fifo_id = format_data_length(dsc_csi_fifo_id, 9)

        req_vc = byteval.split("req_vc=")[1].split(";")[0]
        req_vc = hex_to_bin(req_vc)
        req_vc = format_data_length(req_vc, 4)

        rc_id = byteval.split("rc_id=")[1].split(";")[0]
        rc_id = hex_to_bin(rc_id)
        rc_id = format_data_length(rc_id, 6)
        data_value = csi_dst_id + rsvd + csi_dst_fifo_id + dsc_csi_fifo_id + req_vc + rc_id
        data_value = format_hex_value(data_value)
        return data_value
    hex_binary_0_5, bit_0_5_value = get_value(byteval[-6:], "rc_id")
    hex_binary_9_6, bit_9_6_value = get_value(byteval[-10:-6], "req_vc")
    hex_binary_31_28, bit_31_28_value = get_value(byteval[-32:-28], "rsvd")
    hex_binary_28_19, bit_28_19_value = get_value(byteval[-28:-19], "wrb_csi_fifo_id")
    hex_binary_19_10, bit_19_10_value = get_value(byteval[-19:-10], "dsc_csi_fifo_id")
    hex_binary_36_32, bit_36_32_value = get_value(byteval[-37:-32], "csi_dst_id")
    data_frame = [["csi_dst_id", CSI_SRC_DST(hex_binary_36_32).name],
                  ["rsvd", hex_binary_31_28],
                  ["wrb_csi_fifo_id", hex_binary_28_19],
                  ["dsc_csi_fifo_id", hex_binary_19_10],
                  ["req_vc", hex_binary_9_6],
                  ["rc_id", hex_binary_0_5]]
    data_frame = pd.DataFrame(data_frame)
    return data_frame, (
        bit_36_32_value, ";",
        bit_31_28_value, ";",
        bit_28_19_value,
        ";",
        bit_19_10_value,
        ";",
        bit_9_6_value,
        ";",
        bit_0_5_value
    )


def hex_c_value(byteval):
    if "=" in byteval:
        qid_base0 = byteval.split("qid_base0=")[1].split(";")[0]
        qid_base0 = hex_to_bin(qid_base0)
        qid_base0 = format_data_length(qid_base0, 13)
        rsv0 = byteval.split("rsv0=")[1].split(";")[0]
        rsv0 = hex_to_bin(rsv0)
        rsv0 = format_data_length(rsv0, 4)

        qid_cnt0 = byteval.split("qid_cnt0=")[1].split(";")[0]
        qid_cnt0 = hex_to_bin(qid_cnt0)
        qid_cnt0 = format_data_length(qid_cnt0, 14)

        rsv1 = byteval.split("rsv1=")[1].split(";")[0]
        rsv1 = hex_to_bin(rsv1)
        rsv1 = format_data_length(rsv1, 2)

        qid_base1 = byteval.split("qid_base1=")[1].split(";")[0]
        qid_base1 = hex_to_bin(qid_base1)
        qid_base1 = format_data_length(qid_base1, 13)

        rsv2 = byteval.split("rsv2=")[1].split(";")[0]
        rsv2 = hex_to_bin(rsv2)
        rsv2 = format_data_length(rsv2, 3)

        qid_cnt1 = byteval.split("qid_cnt1=")[1].split(";")[0]
        qid_cnt1 = hex_to_bin(qid_cnt1)
        qid_cnt1 = format_data_length(qid_cnt1, 14)

        rsv3 = byteval.split("rsv3=")[1]
        rsv3 = hex_to_bin(rsv3)
        rsv3 = format_data_length(rsv3, 2)

        data_value = rsv3 + qid_cnt1 + rsv2 + qid_base1 + rsv1 + qid_cnt0 + rsv0 + qid_base0
        data_value = format_hex_value(data_value)
        return data_value
    hex_binary_0_12 = hex(int(byteval[-13:], 2))
    bit_0_13_value = "qid_base0=" + hex_binary_0_12

    hex_binary_13_15 = hex(int(byteval[-16:-13], 2))
    bit_13_15_value = (
            "rsv0=" + hex_binary_13_15
    )

    hex_binary_16_29 = hex(int(byteval[-30:-16], 2))
    bit_16_29_value = "qid_cnt0=" + hex_binary_16_29

    hex_binary_30_31 = hex(int(byteval[-32:-30], 2))
    bit_30_31_value = "rsv1=" + hex_binary_30_31

    hex_binary_32_44 = hex(int(byteval[-45:-32], 2))
    bit_33_44_value = "qid_base1=" + hex_binary_32_44

    hex_binary_46_47 = hex(int(byteval[-48:-45], 2))
    bit_46_47_value = "rsv2=" + hex_binary_46_47

    hex_binary_48_61 = hex(int(byteval[-62:-48], 2))
    bit_48_61_value = "qid_cnt1=" + hex_binary_48_61

    hex_binary_62_63 = hex(int(byteval[-64:-62], 2))
    bit_62_63_value = "rsv3=" + hex_binary_62_63

    data_frame = [["qid_base0", hex_binary_0_12],
                  ["rsv0", hex_binary_13_15],
                  ["qid_cnt0", hex_binary_16_29],
                  ["rsv1", hex_binary_30_31],
                  ["qid_base1", hex_binary_32_44],
                  ["rsv2", hex_binary_46_47],
                  ["qid_cnt1", hex_binary_48_61],
                  ["rsv3", hex_binary_62_63]]
    data_frame = pd.DataFrame(data_frame)
    return data_frame, (
        bit_0_13_value,
        ";",
        bit_13_15_value,
        ";",
        bit_16_29_value,
        ";",
        bit_30_31_value,
        ";",
        bit_33_44_value,
        ";",
        bit_46_47_value,
        ";",
        bit_48_61_value,
        ";",
        bit_62_63_value
    )


def hex_eqdma_4_value(byteval):
    if "=" in byteval:
        reserved = byteval.split("Reserved=")[1].split(";")[0]
        reserved = hex_to_bin(reserved)
        reserved = format_data_length(reserved, 16)
        credt = byteval.split("credt=")[1]
        credt = hex_to_bin(credt)
        credt = format_data_length(credt, 16)
        data_value = credt + reserved
        data_value = format_hex_value(data_value)
        return data_value
    hex_binary_0_16 = hex(int(byteval[-16:], 2))
    bit_0_16_value = "Reserved=" + hex_binary_0_16

    hex_binary_31_16 = hex(int(byteval[-32:-16], 2))
    bit_16_31_value = (
            "credt=" + hex_binary_31_16
    )

    data_frame = [["Reserved", hex_binary_0_16],
                  ["credt", hex_binary_31_16]]
    data_frame = pd.DataFrame(data_frame)
    return data_frame, (
        bit_0_16_value,
        ";",
        bit_16_31_value
    )


def hex_eqdma_a_value(byteval):
    if "=" in byteval:
        credt = byteval.split("m2m_qstate=")[1]
        credt = hex_to_bin(credt)
        data_value = credt
        data_value = format_hex_value(data_value)
        return data_value
    m2m_qstate = hex(int(byteval[-1], 2))
    m2m_qstate_value = "m2m_qstate=" + m2m_qstate
    data_frame = [["m2m_qstate", m2m_qstate]]
    data_frame = pd.DataFrame(data_frame)
    return data_frame, (m2m_qstate_value)


def hex_eqdma_9_value(byteval):
    if "=" in byteval:
        intc_cidx_upd_off = byteval.split("intc_cidx_upd_off=")[1].split(";")[0]
        intc_cidx_upd_off = hex_to_bin(intc_cidx_upd_off)
        intc_cidx_upd_off = format_data_length(intc_cidx_upd_off, 17)
        cmpt_cidx_upd_off = byteval.split("cmpt_cidx_upd_off=")[1].split(";")[0]
        cmpt_cidx_upd_off = hex_to_bin(cmpt_cidx_upd_off)
        cmpt_cidx_upd_off = format_data_length(cmpt_cidx_upd_off, 17)
        dsc_pidx_upd_off = byteval.split("dsc_pidx_upd_off=")[1].split(";")[0]
        dsc_pidx_upd_off = hex_to_bin(dsc_pidx_upd_off)
        dsc_pidx_upd_off = format_data_length(dsc_pidx_upd_off, 17)
        qspc_start_off = byteval.split("qspc_start_off=")[1].split(";")[0]
        qspc_start_off = hex_to_bin(qspc_start_off)
        qspc_start_off = format_data_length(qspc_start_off, 20)
        strides_per_func = byteval.split("strides_per_func=")[1].split(";")[0]
        strides_per_func = hex_to_bin(strides_per_func)
        strides_per_func = format_data_length(strides_per_func, 4)
        stride_size = byteval.split("stride_size=")[1].split(";")[0]
        stride_size = hex_to_bin(stride_size)
        stride_size = format_data_length(stride_size, 4)
        tot_func = byteval.split("tot_func=")[1].split(";")[0]
        tot_func = hex_to_bin(tot_func)
        tot_func = format_data_length(tot_func, 13)
        start_func = byteval.split("start_func=")[1].split(";")[0]
        start_func = hex_to_bin(start_func)
        start_func = format_data_length(start_func, 12)
        data_value = intc_cidx_upd_off + cmpt_cidx_upd_off + dsc_pidx_upd_off + qspc_start_off + \
                     strides_per_func + stride_size + tot_func + start_func
        data_value = format_hex_value(data_value)
        return data_value
    start_func_hex, start_func_str = get_value(byteval[-12:], "start_func")
    tot_func_hex, tot_func_str = get_value(byteval[-25:-12], "tot_func")
    stride_size_hex, stride_size_str = get_value(byteval[-29:-25], "stride_size")
    strides_per_func_hex, strides_per_func_str = get_value(byteval[-33:-29], "strides_per_func")
    qspc_start_off_hex, qspc_start_off_str = get_value(byteval[-53:-33], "qspc_start_off")
    dsc_pidx_upd_off_hex, dsc_pidx_upd_off_str = get_value(byteval[-70:-53], "dsc_pidx_upd_off")
    cmpt_cidx_upd_off_hex, cmpt_cidx_upd_off_str = get_value(byteval[-87:-70], "cmpt_cidx_upd_off")
    intc_cidx_upd_off_hex, intc_cidx_upd_off_str = get_value(byteval[-104:-70], "intc_cidx_upd_off")
    data_frame = [["start_func", start_func_hex],
                  ["tot_func", tot_func_hex],
                  ["stride_size", stride_size_hex],
                  ["strides_per_func", strides_per_func_hex],
                  ["qspc_start_off", qspc_start_off_hex],
                  ["dsc_pidx_upd_off", dsc_pidx_upd_off_hex],
                  ["cmpt_cidx_upd_off", cmpt_cidx_upd_off_hex],
                  ["intc_cidx_upd_off", intc_cidx_upd_off_hex]
                  ]
    data_frame = pd.DataFrame(data_frame)
    return data_frame, (intc_cidx_upd_off_str, ";",
                        cmpt_cidx_upd_off_str, ";",
                        dsc_pidx_upd_off_str, ";",
                        qspc_start_off_str, ";",
                        strides_per_func_str, ";",
                        stride_size_str, ";",
                        tot_func_str, ";",
                        start_func_str)


def get_value(data, data_str):
    bin_to_hex_data = hex(int(data, 2))
    return bin_to_hex_data, f"{data_str}={bin_to_hex_data}"


def hex_eqdma_8_value(byteval):
    if "=" in byteval:
        vld = byteval.split("vld=")[1].split(";")[0]
        vld = hex_to_bin(vld)
        vec = byteval.split("vec=")[1].split(";")[0]
        vec = hex_to_bin(vec)
        vec = format_data_length(vec, 11)
        rsv1 = byteval.split("rsv1=")[1].split(";")[0]
        rsv1 = hex_to_bin(rsv1)
        int_st = byteval.split("int_st=")[1].split(";")[0]
        int_st = hex_to_bin(int_st)
        color = byteval.split("color=")[1].split(";")[0]
        color = hex_to_bin(color)
        baddr_4k = byteval.split("baddr_4k=")[1].split(";")[0]
        baddr_4k = hex_to_bin(baddr_4k)
        baddr_4k = format_data_length(baddr_4k, 52)
        page_size = byteval.split("page_size=")[1].split(";")[0]
        page_size = hex_to_bin(page_size)
        page_size = format_data_length(page_size, 3)
        pidx = byteval.split("pidx=")[1].split(";")[0]
        pidx = hex_to_bin(pidx)
        pidx = format_data_length(pidx, 12)
        at = byteval.split("at=")[1].split(";")[0]
        at = hex_to_bin(at)
        pasid = byteval.split("pasid=")[1].split(";")[0]
        pasid = hex_to_bin(pasid)
        pasid = format_data_length(pasid, 20)
        pasid_en = byteval.split("pasid_en=")[1].split(";")[0]
        pasid_en = hex_to_bin(pasid_en)
        cdm_prof_id = byteval.split("cdm_prof_id=")[1].split(";")[0]
        cdm_prof_id = hex_to_bin(cdm_prof_id)
        cdm_prof_id = format_data_length(cdm_prof_id, 5)
        fnc = byteval.split("fnc=")[1].split(";")[0]
        fnc = hex_to_bin(fnc)
        fnc = format_data_length(fnc, 12)
        client_id = byteval.split("client_id=")[1].split(";")[0]
        client_id = hex_to_bin(client_id)
        client_id = format_data_length(client_id, 4)

        lgcy_int_en = byteval.split("lgcy_int_en=")[1].split(";")[0]
        lgcy_int_en = hex_to_bin(lgcy_int_en)
        asserted = byteval.split("asserted=")[1].split(";")[0]
        asserted = hex_to_bin(asserted)
        rsv = byteval.split("rsv=")[1]
        rsv = hex_to_bin(rsv)
        rsv = format_data_length(rsv, 35)
        data_value = rsv + asserted + lgcy_int_en + client_id + fnc + cdm_prof_id + pasid_en + pasid + at + pidx + page_size + baddr_4k + \
                     color + int_st + rsv1 + vec + vld
        data_value = format_hex_value(data_value)
        return data_value
    vld_hex, vld_str = get_value(byteval[-1], "vld")
    vec_hex, vce_str = get_value(byteval[-12:-1], "vec")
    rsv1_hex, rsv1_str = get_value(byteval[-13], "rsv1")
    int_st_hex, int_st_str = get_value(byteval[-14], "int_st")
    color_hex, color_str = get_value(byteval[-15], "color")
    baddr_4k_hex, baddr_4k_str = get_value(byteval[-67:-15], "baddr_4k")
    page_size_hex, page_size_str = get_value(byteval[-70:-67], "page_size")
    pidx_hex, pidx_str = get_value(byteval[-82:-70], "pidx")
    at_hex, at_str = get_value(byteval[-83], "at")
    pasid_hex, pasid_str = get_value(byteval[-103:-83], "pasid")
    pasid_en_hex, pasid_en_str = get_value(byteval[-104], "pasid_en")
    cdm_prof_id_hex, cdm_prof_id_str = get_value(byteval[-109:-104], "cdm_prof_id")
    fnc_hex, fnc_str = get_value(byteval[-121:-109], "fnc")
    client_id_hex, client_id_str = get_value(byteval[-124:-121], "client_id")
    lgcy_int_en_hex, lgcy_int_en_str = get_value(byteval[-126], "lgcy_int_en")
    asserted_hex, asserted_str = get_value(byteval[-127], "asserted")
    rsv_hex, rsv_str = get_value(byteval[-160:-127], "rsv")

    data_frame = [["vld", vld_hex],
                  ["vec", vec_hex],
                  ["rsv1", rsv1_hex],
                  ["int_st", int_st_hex],
                  ["color", color_hex],
                  ["baddr_4k", baddr_4k_hex],
                  ["page_size", page_size_hex],
                  ["pidx", pidx_hex],
                  ["at", at_hex],
                  ["pasid", pasid_hex],
                  ["pasid_en", pasid_en_hex],
                  ["cdm_prof_id", cdm_prof_id_hex],
                  ["fnc", fnc_hex],
                  ["pidx", pidx_hex],
                  ["client_id", client_id_hex],
                  ["lgcy_int_en", lgcy_int_en_hex],
                  ["asserted", asserted_hex],
                  ["rsv", rsv_hex]]
    data_frame = pd.DataFrame(data_frame)
    return data_frame, (
        vld_str,
        ";",
        vce_str,
        ";",
        rsv1_str,
        ";",
        int_st_str,
        ";",
        color_str, ";", baddr_4k_str, ";", page_size_str, ";", pidx_str, ";", at_str, ";", pasid_str, ";", pasid_en_str,
        ";",
        cdm_prof_id_str,
        ";",
        fnc_str,
        ";",
        client_id_str, ";", lgcy_int_en_str, ";", asserted_str, ";", rsv_str
    )


def hex_eqdma_6_value(byteval):
    if "=" in byteval:
        pidx = byteval.split("pidx=")[1].split(";")[0]
        pidx = hex_to_bin(pidx)
        pidx = format_data_length(pidx, 16)
        cidx = byteval.split("cidx=")[1].split(";")[0]
        cidx = hex_to_bin(cidx)
        cidx = format_data_length(cidx, 16)
        valid = byteval.split("valid=")[1].split(";")[0]
        valid = hex_to_bin(valid)
        en_stat_desc = byteval.split("en_stat_desc=")[1].split(";")[0]
        en_stat_desc = hex_to_bin(en_stat_desc)
        en_int = byteval.split("en_int=")[1].split(";")[0]
        en_int = hex_to_bin(en_int)
        trig_mode = byteval.split("trig_mode=")[1].split(";")[0]
        trig_mode = hex_to_bin(trig_mode)
        trig_mode = format_data_length(trig_mode, 3)
        counter_ix = byteval.split("counter_ix=")[1].split(";")[0]
        counter_ix = hex_to_bin(counter_ix)
        counter_ix = format_data_length(counter_ix, 4)
        timer_ix = byteval.split("timer_ix=")[1].split(";")[0]
        timer_ix = hex_to_bin(timer_ix)
        timer_ix = format_data_length(timer_ix, 4)
        int_st = byteval.split("int_st=")[1].split(";")[0]
        int_st = hex_to_bin(int_st)
        int_st = format_data_length(int_st, 2)
        user_trig_pend = byteval.split("user_trig_pend=")[1].split(";")[0]
        user_trig_pend = hex_to_bin(user_trig_pend)
        isr_done = byteval.split("isr_done=")[1].split(";")[0]
        isr_done = hex_to_bin(isr_done)
        color = byteval.split("color=")[1].split(";")[0]
        color = hex_to_bin(color)
        err = byteval.split("err=")[1].split(";")[0]
        err = hex_to_bin(err)
        err = format_data_length(err, 2)
        qsize_ix = byteval.split("qsize_ix=")[1].split(";")[0]
        qsize_ix = hex_to_bin(qsize_ix)
        qsize_ix = format_data_length(qsize_ix, 4)
        baddr4_high = byteval.split("baddr4_high=")[1].split(";")[0]
        baddr4_high = hex_to_bin(baddr4_high)
        baddr4_high = format_data_length(baddr4_high, 58)
        baddr4_low = byteval.split("baddr4_low=")[1].split(";")[0]
        baddr4_low = hex_to_bin(baddr4_low)
        baddr4_low = format_data_length(baddr4_low, 4)
        desc_size = byteval.split("desc_size=")[1].split(";")[0]
        desc_size = hex_to_bin(desc_size)
        desc_size = format_data_length(desc_size, 2)
        full_upd = byteval.split("full_upd=")[1].split(";")[0]
        full_upd = hex_to_bin(full_upd)
        ovf_chk_dis = byteval.split("ovf_chk_dis=")[1].split(";")[0]
        ovf_chk_dis = hex_to_bin(ovf_chk_dis)
        vec = byteval.split("vec=")[1].split(";")[0]
        vec = hex_to_bin(vec)
        vec = format_data_length(vec, 11)
        rsv0 = byteval.split("rsv0=")[1].split(";")[0]
        rsv0 = hex_to_bin(rsv0)
        rsv0 = format_data_length(rsv0, 5)
        int_aggr = byteval.split("int_aggr=")[1].split(";")[0]
        int_aggr = hex_to_bin(int_aggr)
        vio = byteval.split("vio=")[1].split(";")[0]
        vio = hex_to_bin(vio)
        dir_c2h = byteval.split("dir_c2h=")[1].split(";")[0]
        dir_c2h = hex_to_bin(dir_c2h)
        vio_eop = byteval.split("vio_eop=")[1].split(";")[0]
        vio_eop = hex_to_bin(vio_eop)
        sh_cmpt = byteval.split("sh_cmpt=")[1].split(";")[0]
        sh_cmpt = hex_to_bin(sh_cmpt)
        client_id = byteval.split("client_id=")[1].split(";")[0]
        client_id = hex_to_bin(client_id)
        client_id = format_data_length(client_id, 4)
        qdm_csi_prof_id = byteval.split("qdm_csi_prof_id=")[1].split(";")[0]
        qdm_csi_prof_id = hex_to_bin(qdm_csi_prof_id)
        qdm_csi_prof_id = format_data_length(qdm_csi_prof_id, 5)
        at = byteval.split("at=")[1].split(";")[0]
        at = hex_to_bin(at)
        pasid = byteval.split("pasid=")[1].split(";")[0]
        pasid = hex_to_bin(pasid)
        pasid = format_data_length(pasid, 20)
        pasid_en = byteval.split("pasid_en=")[1].split(";")[0]
        pasid_en = hex_to_bin(pasid_en)
        tph = byteval.split("tph=")[1].split(";")[0]
        tph = hex_to_bin(tph)
        tph = format_data_length(tph, 11)
        fnc_id = byteval.split("fnc_id=")[1].split(";")[0]
        fnc_id = hex_to_bin(fnc_id)
        fnc_id = format_data_length(fnc_id, 12)
        msi_en = byteval.split("msi_en=")[1].split(";")[0]
        msi_en = hex_to_bin(msi_en)
        lgcy_irq_on = byteval.split("lgcy_irq_on=")[1].split(";")[0]
        lgcy_irq_on = hex_to_bin(lgcy_irq_on)
        rsv = byteval.split("rsv=")[1]
        rsv = hex_to_bin(rsv)
        rsv = format_data_length(rsv, 20)
        data_value = rsv + lgcy_irq_on + msi_en + fnc_id + tph + pasid_en + pasid + at + qdm_csi_prof_id + client_id + sh_cmpt + vio_eop + dir_c2h + vio + int_aggr + rsv0 + vec + ovf_chk_dis + full_upd + baddr4_high + baddr4_low + desc_size + qsize_ix + err + color + isr_done + user_trig_pend + int_st + timer_ix + counter_ix + trig_mode + en_int + en_stat_desc + valid + cidx + pidx
        data_value = format_hex_value(data_value)
        return data_value

    pidx_hex, pidx_str = get_value(byteval[-16:], "pidx")
    cidx_hex, cidx_str = get_value(byteval[-32:-16], "cidx")
    valid_hex, valid_str = get_value(byteval[-33], "valid")
    en_stat_desc_hex, en_stat_desc_str = get_value(byteval[-34], "en_stat_desc")
    en_int_hex, en_int_str = get_value(byteval[-35], "en_int")
    trig_mode_hex, trig_mode_str = get_value(byteval[-38:-35], "trig_mode")
    counter_ix_hex, counter_ix_str = get_value(byteval[-42:-38], "counter_ix")
    timer_ix_hex, timer_ix_str = get_value(byteval[-46:-42], "timer_ix")
    int_st_hex, int_st_str = get_value(byteval[-48:-46], "int_st")
    user_trig_pend_hex, user_trig_pend_str = get_value(byteval[-49], "user_trig_pend")
    isr_done_hex, isr_done_str = get_value(byteval[-50], "isr_done")
    color_hex, color_str = get_value(byteval[-51], "color")
    err_hex, err_str = get_value(byteval[-53:-52], "err")
    desc_size_hex, desc_size_str = get_value(byteval[-59:-57], "desc_size")
    qsize_ix_hex, qsize_ix_str = get_value(byteval[-56:-53], "qsize_ix")
    baddr4_high_hex, baddr4_high_str = get_value(byteval[-121:-64], "baddr4_high")
    baddr4_low_hex, baddr4_low_str = get_value(byteval[-63:-59], "baddr4_low")
    full_upd_hex, full_upd_str = get_value(byteval[-122], "full_upd")
    ovf_chk_dis_upd_hex, ovf_chk_dis_str = get_value(byteval[-123], "ovf_chk_dis")
    vec_hex, vec_str = get_value(byteval[-134:-123], "vec")
    rsv0_hex, rsv0_str = get_value(byteval[-139:-134], "rsv0")
    int_aggr_hex, int_aggr_str = get_value(byteval[-140], "int_aggr")
    vio_hex, vio_str = get_value(byteval[-141], "vio")
    dir_c2h_hex, dir_c2h_str = get_value(byteval[-142], "dir_c2h")
    vio_eop_hex, vio_eop_str = get_value(byteval[-143], "vio_eop")
    sh_cmpt_hex, sh_cmpt_str = get_value(byteval[-144], "sh_cmpt")
    client_id_hex, client_id_str = get_value(byteval[-147:-144], "client_id")
    qdm_csi_prof_id_hex, qdm_csi_prof_id_str = get_value(byteval[-153:-148], "qdm_csi_prof_id")
    at_hex, at_str = get_value(byteval[-154], "at")
    pasid_hex, pasid_str = get_value(byteval[-174:-154], "pasid")
    pasid_en_hex, pasid_en_str = get_value(byteval[-175], "pasid_en")
    tph_hex, tph_str = get_value(byteval[-186:-175], "tph")
    fnc_id_hex, fnc_id_str = get_value(byteval[-198:-187], "fnc_id")
    msi_en_hex, msi_en_str = get_value(byteval[-199], "msi_en")
    lgcy_irq_on_hex, lgcy_irq_on_str = get_value(byteval[-200], "lgcy_irq_on")
    rsv_hex, rsv_str = get_value(byteval[-218:-200], "rsv")

    data_frame = [["pidx", pidx_hex],
                  ["cidx", cidx_hex],
                  ["valid", valid_hex],
                  ["en_stat_desc", en_stat_desc_hex],
                  ["en_int", en_int_hex],
                  ["trig_mode", trig_mode_hex],
                  ["counter_ix", counter_ix_hex],
                  ["timer_ix", timer_ix_hex],
                  ["int_st", int_st_hex],
                  ["user_trig_pend", user_trig_pend_hex],
                  ["isr_done", isr_done_hex],
                  ["color", color_hex],
                  ["qsize_ix", qsize_ix_hex],
                  ["err", err_hex],
                  ["desc_size", desc_size_hex],
                  ["baddr4_low", baddr4_low_hex],
                  ["baddr4_high", baddr4_high_hex],
                  ["full_upd", full_upd_hex],
                  ["ovf_chk_dis_upd_", ovf_chk_dis_upd_hex],
                  ["vec", vec_hex],
                  ["rsv0", rsv0_hex],
                  ["int_aggr", int_aggr_hex],
                  ["vio", vio_hex],
                  ["dir_c2h", dir_c2h_hex],
                  ["vio_eop", vio_eop_hex],
                  ["sh_cmpt", sh_cmpt_hex],
                  ["client_id", client_id_hex],
                  ["qdm_csi_prof_id", qdm_csi_prof_id_hex],
                  ["at", at_hex],
                  ["pasid", pasid_hex],
                  ["pasid_en", pasid_en_hex],
                  ["tph", tph_hex],
                  ["fnc_id", fnc_id_hex],
                  ["msi_en", msi_en_hex],
                  ["lgcy_irq_on", lgcy_irq_on_hex],
                  ["rsv", rsv_hex]
                  ]
    data_frame = pd.DataFrame(data_frame)
    return data_frame, (
        pidx_str,
        ";",
        cidx_str,
        ";",
        valid_str,
        ";",
        en_stat_desc_str,
        ";",
        en_int_str, ";", trig_mode_str, ";", counter_ix_str, ";", timer_ix_str, ";", int_st_str, ";",
        user_trig_pend_str,
        ";", isr_done_str,
        ";",
        color_str, ";", err_str, ";", desc_size_str,
        ";",
        qsize_ix_str,
        ";",
        baddr4_low_str, ";", full_upd_str, ";", ovf_chk_dis_str, ";", vec_str, ";", rsv0_str, ";", int_aggr_str, ";",
        vio_str, ";", dir_c2h_str, ";", vio_eop_str, ";", sh_cmpt_str, ";", client_id_str, ";", qdm_csi_prof_id_str,
        ";",
        at_str, ";", pasid_str, ";", pasid_en_str, ";", tph_str, ";", fnc_id_str, ";", msi_en_str, ";",
        lgcy_irq_on_str, ";", rsv_str
    )


def hex_eqdma_7_value(byteval):
    if "=" in byteval:
        buf_sz_ix = byteval.split("buf_sz_ix=")[1].split(";")[0]
        buf_sz_ix = hex_to_bin(buf_sz_ix)
        buf_sz_ix = format_data_length(buf_sz_ix, 5)
        client_id = byteval.split("client_id=")[1].split(";")[0]
        client_id = hex_to_bin(client_id)
        client_id = format_data_length(client_id, 4)
        var_desc = byteval.split("var_desc=")[1].split(";")[0]
        var_desc = hex_to_bin(var_desc)
        virtio = byteval.split("virtio=")[1].split(";")[0]
        virtio = hex_to_bin(virtio)
        num_pfch = byteval.split("num_pfch=")[1].split(";")[0]
        num_pfch = hex_to_bin(num_pfch)
        num_pfch = format_data_length(num_pfch, 6)
        pfch_need = byteval.split("pfch_need=")[1].split(";")[0]
        pfch_need = hex_to_bin(pfch_need)
        pfch_need = format_data_length(pfch_need, 6)
        rsvd = byteval.split("rsvd=")[1].split(";")[0]
        rsvd = hex_to_bin(rsvd)
        rsvd = format_data_length(rsvd, 4)
        err = byteval.split("err=")[1].split(";")[0]
        err = hex_to_bin(err)
        pfch_en = byteval.split("pfch_en=")[1].split(";")[0]
        pfch_en = hex_to_bin(pfch_en)
        pfch = byteval.split("pfch=")[1].split(";")[0]
        pfch = hex_to_bin(pfch)
        sw_crdt = byteval.split("sw_crdt=")[1].split(";")[0]
        sw_crdt = hex_to_bin(sw_crdt)
        sw_crdt = format_data_length(sw_crdt, 16)
        valid = byteval.split("valid=")[1]
        valid = hex_to_bin(valid)
        data_value = valid + sw_crdt + pfch + pfch_en + err + rsvd + pfch_need + num_pfch + virtio + var_desc + client_id + buf_sz_ix
        data_value = format_hex_value(data_value)
        return data_value
    buf_sz_ix_hex, buf_sz_ix_str = get_value(byteval[-4:], "buf_sz_ix")
    client_id_hex, client_id_str = get_value(byteval[-8:-4], "client_id")
    var_desc_hex, var_desc_str = get_value(byteval[-9], "var_desc")
    virtio_hex, virtio_str = get_value(byteval[-10], "virtio")
    num_pfch_hex, num_pfch_str = get_value(byteval[-16:-10], "num_pfch")
    pfch_need_hex, pfch_need_str = get_value(byteval[-22:-16], "pfch_need")
    rsvd_hex, rsvd_str = get_value(byteval[-26:-22], "rsvd")
    err_hex, err_str = get_value(byteval[-27], "err")
    pfch_en_hex, pfch_en_str = get_value(byteval[-28], "pfch_en")
    pfch_hex, pfch_str = get_value(byteval[-29], "pfch")
    sw_crdt_hex, sw_crdt_str = get_value(byteval[-45:-29], "sw_crdt")
    valid_hex, valid_str = get_value(byteval[-46], "valid")
    data_frame = [["buf_sz_ix", buf_sz_ix_hex],
                  ["client_id", client_id_hex],
                  ["var_desc", var_desc_hex],
                  ["virtio", virtio_hex],
                  ["num_pfch", num_pfch_hex],
                  ["pfch_need", pfch_need_hex],
                  ["rsvd", rsvd_hex],
                  ["err", err_hex],
                  ["pfch_en", pfch_en_hex],
                  ["pfch", pfch_hex],
                  ["sw_crdt", sw_crdt_hex],
                  ["valid", valid_hex]]
    data_frame = pd.DataFrame(data_frame)
    return data_frame, (
        buf_sz_ix_str,
        ";",
        client_id_str,
        ";",
        var_desc_str,
        ";",
        virtio_str,
        ";",
        num_pfch_str, ";", pfch_need_str, ";", rsvd_str, ";", err_str, ";", pfch_en_str, ";", pfch_str, ";",
        sw_crdt_str,
        ";", valid_str)


def hex_eqdma_2_value(byteval):
    if "=" in byteval:
        cidx = byteval.split("cidx=")[1].split(";")[0]
        cidx = hex_to_bin(cidx)
        cidx = format_data_length(cidx, 16)
        crd_use = byteval.split("crd_use=")[1].split(";")[0]
        crd_use = hex_to_bin(crd_use)
        crd_use = format_data_length(crd_use, 16)
        reserved = byteval.split("Reserved=")[1].split(";")[0]
        reserved = hex_to_bin(reserved)
        reserved = format_data_length(reserved, 8)
        dsc_pnd = byteval.split("dsc_pnd=")[1].split(";")[0]
        dsc_pnd = hex_to_bin(dsc_pnd)
        idl_stp_b = byteval.split("idl_stp_b=")[1].split(";")[0]
        idl_stp_b = hex_to_bin(idl_stp_b)
        evt_pnd = byteval.split("evt_pnd=")[1].split(";")[0]
        evt_pnd = hex_to_bin(evt_pnd)
        fetch_pnd = byteval.split("fetch_pnd=")[1].split(";")[0]
        fetch_pnd = hex_to_bin(fetch_pnd)
        fetch_pnd = format_data_length(fetch_pnd, 8)
        data_value = '0' + fetch_pnd + evt_pnd + idl_stp_b + dsc_pnd + reserved + crd_use + cidx
        data_value = format_hex_value(data_value)
        return data_value
    cidx_hex, cidx_str = get_value(byteval[-16:], "cidx")
    crd_use_hex, crd_use_str = get_value(byteval[-32:-16], "crd_use")
    reserved_hex, reserved_str = get_value(byteval[-40:-32], "Reserved")
    dsc_pnd_hex, dsc_pnd_str = get_value(byteval[-41], "dsc_pnd")
    idl_stp_b_hex, idl_stp_str = get_value(byteval[-42], "idl_stp_b")
    evt_pnd_hex, evt_pnd_str = get_value(byteval[-43], "evt_pnd")
    fetch_pnd_hex, fetch_pnd_str = get_value(byteval[-47:-43], "fetch_pnd")
    res_hex, res_str = get_value(byteval[-48], "Reserved")
    data_frame = [["cidx", cidx_hex],
                  ["crd_use", crd_use_hex],
                  ["Reserved", reserved_hex],
                  ["dsc_pnd", dsc_pnd_hex],
                  ["idl_stp_b", idl_stp_b_hex],
                  ["pfch_need", evt_pnd_hex],
                  ["fetch_pnd", fetch_pnd_hex],
                  ["Reserved", res_hex]]
    data_frame = pd.DataFrame(data_frame)
    return data_frame, (
        cidx_str,
        ";",
        crd_use_str,
        ";",
        reserved_str,
        ";",
        dsc_pnd_str,
        ";",
        idl_stp_str, ";", evt_pnd_str, ";", fetch_pnd_str, ";", res_str)


def hex_eqdma_0_value(byteval):
    if "=" in byteval:
        pidx = byteval.split("pidx=")[1].split(";")[0]
        pidx = hex_to_bin(pidx)
        pidx = format_data_length(pidx, 16)
        irq_arm = byteval.split("irq_arm=")[1].split(";")[0]
        irq_arm = hex_to_bin(irq_arm)
        fnc = byteval.split("fnc=")[1].split(";")[0]
        fnc = hex_to_bin(fnc)
        fnc = format_data_length(fnc, 12)
        qen = byteval.split("qen=")[1].split(";")[0]
        qen = hex_to_bin(qen)
        fcrd_en = byteval.split("fcrd_en=")[1].split(";")[0]
        fcrd_en = hex_to_bin(fcrd_en)
        wbi_chk = byteval.split("wbi_chk=")[1].split(";")[0]
        wbi_chk = hex_to_bin(wbi_chk)
        wbi_intvl_en = byteval.split("wbi_intvl_en=")[1].split(";")[0]
        wbi_intvl_en = hex_to_bin(wbi_intvl_en)
        at = byteval.split("at=")[1].split(";")[0]
        at = hex_to_bin(at)
        fetch_max = byteval.split("fetch_max=")[1].split(";")[0]
        fetch_max = hex_to_bin(fetch_max)
        fetch_max = format_data_length(fetch_max, 4)
        dis_qinv_on_err = byteval.split("dis_qinv_on_err=")[1].split(";")[0]
        dis_qinv_on_err = hex_to_bin(dis_qinv_on_err)
        f_in_order = byteval.split("f_in_order=")[1].split(";")[0]
        f_in_order = hex_to_bin(f_in_order)
        err_irq_snt = byteval.split("err_irq_snt=")[1].split(";")[0]
        err_irq_snt = hex_to_bin(err_irq_snt)
        rng_sz = byteval.split("rng_sz=")[1].split(";")[0]
        rng_sz = hex_to_bin(rng_sz)
        rng_sz = format_data_length(rng_sz, 4)
        dsc_sz = byteval.split("dsc_sz=")[1].split(";")[0]
        dsc_sz = hex_to_bin(dsc_sz)
        dsc_sz = format_data_length(dsc_sz, 3)
        wbk_en = byteval.split("wbk_en=")[1].split(";")[0]
        wbk_en = hex_to_bin(wbk_en)
        irq_en = byteval.split("irq_en=")[1].split(";")[0]
        irq_en = hex_to_bin(irq_en)
        irq_no_last = byteval.split("irq_no_last=")[1].split(";")[0]
        irq_no_last = hex_to_bin(irq_no_last)
        err = byteval.split("err=")[1].split(";")[0]
        err = hex_to_bin(err)
        err = format_data_length(err, 2)
        err_wb_sent = byteval.split("err_wb_sent=")[1].split(";")[0]
        err_wb_sent = hex_to_bin(err_wb_sent)
        irq_req = byteval.split("irq_req=")[1].split(";")[0]
        irq_req = hex_to_bin(irq_req)
        dsc_base = byteval.split("dsc_base=")[1].split(";")[0]
        dsc_base = hex_to_bin(dsc_base)
        dsc_base = format_data_length(dsc_base, 64)
        vec = byteval.split("vec=")[1].split(";")[0]
        vec = hex_to_bin(vec)
        vec = format_data_length(vec, 11)
        int_aggr = byteval.split("int_aggr=")[1].split(";")[0]
        int_aggr = hex_to_bin(int_aggr)
        dis_intr_on_vf = byteval.split("dis_intr_on_vf=")[1].split(";")[0]
        dis_intr_on_vf = hex_to_bin(dis_intr_on_vf)
        virtio_en = byteval.split("virtio_en=")[1].split(";")[0]
        virtio_en = hex_to_bin(virtio_en)
        irq_byp = byteval.split("irq_byp=")[1].split(";")[0]
        irq_byp = hex_to_bin(irq_byp)
        pasid = byteval.split("pasid=")[1].split(";")[0]
        pasid = hex_to_bin(pasid)
        pasid = format_data_length(pasid, 20)
        pasid_en = byteval.split("pasid_en=")[1].split(";")[0]
        pasid_en = hex_to_bin(pasid_en)
        virtio_dsc_base = byteval.split("virtio_dsc_base=")[1].split(";")[0]
        virtio_dsc_base = hex_to_bin(virtio_dsc_base)
        virtio_dsc_base = format_data_length(virtio_dsc_base, 64)
        client_id = byteval.split("client_id=")[1].split(";")[0]
        client_id = hex_to_bin(client_id)
        client_id = format_data_length(client_id, 4)
        qdm_csi_prof_id = byteval.split("qdm_csi_prof_id=")[1].split(";")[0]
        qdm_csi_prof_id = hex_to_bin(qdm_csi_prof_id)
        qdm_csi_prof_id = format_data_length(qdm_csi_prof_id, 5)
        tph = byteval.split("tph=")[1].split(";")[0]
        tph = hex_to_bin(tph)
        tph = format_data_length(tph, 11)
        c2h_st = byteval.split("c2h_st=")[1].split(";")[0]
        c2h_st = hex_to_bin(c2h_st)
        cdx_int_prof_id = byteval.split("cdx_int_prof_id=")[1].split(";")[0]
        cdx_int_prof_id = hex_to_bin(cdx_int_prof_id)
        cdx_int_prof_id = format_data_length(cdx_int_prof_id, 4)
        infer_mem_spc = byteval.split("infer_mem_spc=")[1].split(";")[0]
        infer_mem_spc = hex_to_bin(infer_mem_spc)
        rc_id = byteval.split("rc_id=")[1].split(";")[0]
        rc_id = hex_to_bin(rc_id)
        rc_id = format_data_length(rc_id, 6)
        oneshot_en = byteval.split("oneshot_en=")[1].split(";")[0]
        oneshot_en = hex_to_bin(oneshot_en)
        intr_asserted = byteval.split("intr_asserted=")[1]
        intr_asserted = hex_to_bin(intr_asserted)
        data_value = intr_asserted + oneshot_en + rc_id + infer_mem_spc + cdx_int_prof_id + c2h_st + tph + \
                     qdm_csi_prof_id + client_id + virtio_dsc_base + pasid_en + pasid + irq_byp + virtio_en + \
                     dis_intr_on_vf + int_aggr + vec + dsc_base + irq_req + err_wb_sent + err + irq_no_last + \
                     irq_en + wbk_en + dsc_sz + rng_sz + err_irq_snt + f_in_order + dis_qinv_on_err + fetch_max + \
                     at + wbi_intvl_en + wbi_chk + fcrd_en + qen + fnc + irq_arm + pidx
        data_value = format_hex_value(data_value)
        return data_value
    pidx_hex, pidx_str = get_value(byteval[-16:], "pidx")
    irq_arm_hex, irq_arm_str = get_value(byteval[-17], "irq_arm")
    fnc_hex, fnc_str = get_value(byteval[-29:-17], "fnc")
    qen_hex, qen_str = get_value(byteval[-30], "qen")
    fcrd_en_hex, fcrd_en_str = get_value(byteval[-31], "fcrd_en")
    wbi_chk_hex, wbi_chk_str = get_value(byteval[-32], "wbi_chk")
    wbi_intvl_en_hex, wbi_intvl_en_str = get_value(byteval[-33], "wbi_intvl_en")
    at_hex, at_str = get_value(byteval[-34], "at")
    fetch_max_hex, fetch_max_str = get_value(byteval[-38:-34], "fetch_max")
    dis_qinv_on_err_hex, dis_qinv_on_err_str = get_value(byteval[-39], "dis_qinv_on_err")
    f_in_order_hex, f_in_order_str = get_value(byteval[-40], "f_in_order")
    err_irq_snt_hex, err_irq_snt_str = get_value(byteval[-41], "err_irq_snt")
    rng_sz_hex, rng_sz_str = get_value(byteval[-45:-41], "rng_sz")
    dsc_sz_hex, dsc_sz_str = get_value(byteval[-48:-45], "dsc_sz")
    wbk_en_hex, wbk_en_str = get_value(byteval[-49], "wbk_en")
    irq_en_hex, irq_en_str = get_value(byteval[-50], "irq_en")
    irq_no_last_hex, irq_no_last_str = get_value(byteval[-51], "irq_no_last")
    err_hex, err_str = get_value(byteval[-53:-51], "err")
    err_wb_sent_hex, err_wb_sent_str = get_value(byteval[-54], "err_wb_sent")
    irq_req_hex, irq_req_str = get_value(byteval[-55], "irq_req")
    dsc_base_hex, dsc_base_str = get_value(byteval[-119:-55], "dsc_base")
    vec_hex, vec_str = get_value(byteval[-130:-119], "vec")
    int_aggr_hex, int_aggr_str = get_value(byteval[-131], "int_aggr")
    dis_intr_on_vf_hex, dis_intr_on_vf_str = get_value(byteval[-132], "dis_intr_on_vf")
    virtio_en_hex, virtio_en_str = get_value(byteval[-133], "virtio_en")
    irq_byp_hex, irq_byp_str = get_value(byteval[-134], "irq_byp")
    pasid_hex, pasid_str = get_value(byteval[-154:-134], "pasid")
    pasid_en_hex, pasid_en_str = get_value(byteval[-155], "pasid_en")
    virtio_dsc_base_hex, virtio_dsc_base_str = get_value(byteval[-219:-155], "virtio_dsc_base")
    client_id_hex, client_id_str = get_value(byteval[-223:-219], "client_id")
    qdm_csi_prof_id_hex, qdm_csi_prof_id_str = get_value(byteval[-228:-223], "qdm_csi_prof_id")
    tph_hex, tph_str = get_value(byteval[-239:-228], "tph")
    c2h_st_hex, c2h_st_str = get_value(byteval[-240], "c2h_st")
    cdx_int_prof_id_hex, cdx_int_prof_id_str = get_value(byteval[-244:-240], "cdx_int_prof_id")
    infer_mem_spc_hex, infer_mem_spc_str = get_value(byteval[-245], "infer_mem_spc")
    rc_id_hex, rc_id_str = get_value(byteval[-251:-245], "rc_id")
    oneshot_en_hex, oneshot_en_str = get_value(byteval[-252], "oneshot_en")
    intr_asserted_hex, intr_asserted_str = get_value(byteval[-253], "intr_asserted")
    data_frame = [["pidx", pidx_hex],
                  ["irq_arm", irq_arm_hex],
                  ["fnc", fnc_hex],
                  ["qen", qen_hex],
                  ["fcrd_en", fcrd_en_hex],
                  ["wbi_chk", wbi_chk_hex],
                  ["wbi_intvl_en", wbi_intvl_en_hex],
                  ["at", at_hex],
                  ["fetch_max", fetch_max_hex],
                  ["dis_qinv_on_err", dis_qinv_on_err_hex],
                  ["f_in_order", f_in_order_hex],
                  ["err_irq_snt", err_irq_snt_hex],
                  ["rng_sz", rng_sz_hex],
                  ["dsc_sz", dsc_sz_hex],
                  ["wbk_en", wbk_en_hex],
                  ["irq_en", irq_en_hex],
                  ["irq_no_last", irq_no_last_hex],
                  ["err", err_hex],
                  ["err_wb_sent", err_wb_sent_hex],
                  ["irq_req", irq_req_hex],
                  ["dsc_base", dsc_base_hex],
                  ["vec", vec_hex],
                  ["int_aggr", int_aggr_hex],
                  ["dis_intr_on_vf", dis_intr_on_vf_hex],
                  ["virtio_en", virtio_en_hex],
                  ["irq_byp", irq_byp_hex],
                  ["pasid", pasid_hex],
                  ["pasid_en", pasid_en_hex],
                  ["virtio_dsc_base", virtio_dsc_base_hex],
                  ["client_id", client_id_hex],
                  ["qdm_csi_prof_id", qdm_csi_prof_id_hex],
                  ["tph", tph_hex],
                  ["c2h_st", c2h_st_hex],
                  ["cdx_int_prof_id", cdx_int_prof_id_hex],
                  ["infer_mem_spc", infer_mem_spc_hex],
                  ["rc_id", rc_id_hex],
                  ["oneshot_en", oneshot_en_hex],
                  ["intr_asserted", intr_asserted_hex],
                  ]
    data_frame = pd.DataFrame(data_frame)
    return data_frame, (
        pidx_str, ";", irq_arm_str, ";", fnc_str, ";", qen_str, ";", fcrd_en_str, ";", wbi_chk_str, ";",
        wbi_intvl_en_str,
        ";", at_str, ";", fetch_max_str, ";", dis_qinv_on_err_str, ";", f_in_order_str, ";", err_irq_snt_str,
        ";", rng_sz_str, ";", dsc_sz_str, ";", wbk_en_str, ";", irq_en_str, ";", irq_no_last_str, ";", err_str,
        ";", err_wb_sent_str, ";", irq_req_str, ";", dsc_base_str, ";", vec_str, ";", int_aggr_str, ";",
        dis_intr_on_vf_str,
        ";", virtio_en_str, ";", irq_byp_str, ";", pasid_str, ";", pasid_en_str, ";", virtio_dsc_base_str, ";",
        client_id_str,
        ";", qdm_csi_prof_id_str, ";", tph_str, ";", c2h_st_str, ";", cdx_int_prof_id_str, ";", infer_mem_spc_str,
        ";", rc_id_str, ";", oneshot_en_str, ";", intr_asserted_str)


def QDMA_DMAP_SEL_INT_CIDX(byteval):
    if "=" in byteval:
        reserved = byteval.split("Reserved=")[1].split(";")[0]
        reserved = hex_to_bin(reserved)
        reserved = format_data_length(reserved, 16)
        ring_idx = byteval.split("ring_idx=")[1].split(";")[0]
        ring_idx = hex_to_bin(ring_idx)
        ring_idx = format_data_length(ring_idx, 16)
        sw_cidx = byteval.split("sw_cidx=")[1].split(";")[0]
        sw_cidx = hex_to_bin(sw_cidx)
        sw_cidx = format_data_length(sw_cidx, 8)
        data_value = reserved + ring_idx + sw_cidx
        data_value = format_hex_value(data_value)
        return data_value
    reserved_hex, reserved_str = get_value(byteval[-32:-24], "Reserved")
    ring_idx_hex, ring_idx_str = get_value(byteval[-24:-16], "ring_idx")
    sw_cidx_hex, sw_cidx_str = get_value(byteval[-16:], "sw_cidx")
    data_frame = [["Reserved", reserved_hex],
                  ["ring_idx", ring_idx_hex],
                  ["sw_cidx", sw_cidx_hex]]
    data_frame = pd.DataFrame(data_frame)
    return data_frame, (
        reserved_str,
        ";",
        ring_idx_str,
        ";",
        sw_cidx_str)


def QDMA_DMAP_SEL_DSC_PIDX(byteval):
    if "=" in byteval:
        reserved = byteval.split("Reserved=")[1].split(";")[0]
        reserved = hex_to_bin(reserved)
        reserved = format_data_length(reserved, 15)
        irq_arm = byteval.split("irq_arm=")[1].split(";")[0]
        irq_arm = hex_to_bin(irq_arm)
        dsc_pidx = byteval.split("dsc_pidx=")[1].split(";")[0]
        dsc_pidx = hex_to_bin(dsc_pidx)
        dsc_pidx = format_data_length(dsc_pidx, 16)
        data_value = reserved + irq_arm + dsc_pidx
        data_value = format_hex_value(data_value)
        return data_value
    reserved_hex, reserved_str = get_value(byteval[-32:-17], "Reserved")
    irq_arm_hex, irq_arm_str = get_value(byteval[-17], "irq_arm")
    dsc_pidx_hex, dsc_pidx_str = get_value(byteval[-16:], "dsc_pidx")
    data_frame = [["Reserved", reserved_hex],
                  ["irq_arm", irq_arm_hex],
                  ["sw_cidx", dsc_pidx_hex]]
    data_frame = pd.DataFrame(data_frame)
    return data_frame, (
        reserved_str,
        ";",
        irq_arm_str,
        ";",
        dsc_pidx_str)


def QDMA_DMAP_SEL_CMPT_CIDX(byteval):
    if "=" in byteval:
        reserved = byteval.split("Reserved=")[1].split(";")[0]
        reserved = hex_to_bin(reserved)
        reserved = format_data_length(reserved, 3)
        irq_en_wrb = byteval.split("irq_en_wrb=")[1].split(";")[0]
        irq_en_wrb = hex_to_bin(irq_en_wrb)
        en_sts_desc_wrb = byteval.split("en_sts_desc_wrb=")[1].split(";")[0]
        en_sts_desc_wrb = hex_to_bin(en_sts_desc_wrb)
        trigger_mode = byteval.split("trigger_mode=")[1].split(";")[0]
        trigger_mode = hex_to_bin(trigger_mode)
        trigger_mode = format_data_length(trigger_mode, 3)
        c2h_timer_cnt_index = byteval.split("c2h_timer_cnt_index=")[1].split(";")[0]
        c2h_timer_cnt_index = hex_to_bin(c2h_timer_cnt_index)
        c2h_timer_cnt_index = format_data_length(c2h_timer_cnt_index, 4)
        c2h_count_threshold = byteval.split("c2h_count_threshold=")[1].split(";")[0]
        c2h_count_threshold = hex_to_bin(c2h_count_threshold)
        c2h_count_threshold = format_data_length(c2h_count_threshold, 4)
        wrb_cidx = byteval.split("wrb_cidx=")[1]
        wrb_cidx = hex_to_bin(wrb_cidx)
        wrb_cidx = format_data_length(wrb_cidx, 16)
        data_value = reserved + irq_en_wrb + en_sts_desc_wrb + trigger_mode + c2h_timer_cnt_index + c2h_count_threshold + wrb_cidx
        data_value = format_hex_value(data_value)
        return data_value
    reserved_hex, reserved_str = get_value(byteval[-32:-29], "Reserved")
    irq_en_wrb_hex, irq_en_wrb_str = get_value(byteval[-29], "irq_en_wrb")
    en_sts_desc_wrb_hex, en_sts_desc_wrb_str = get_value(byteval[-29], "en_sts_desc_wrb")
    trigger_mode_hex, trigger_mode_str = get_value(byteval[-27:-24], "trigger_mode")
    c2h_timer_cnt_index_hex, c2h_timer_cnt_index_str = get_value(byteval[-20:-16], "c2h_timer_cnt_index")
    c2h_count_threshold_hex, c2h_count_threshold_str = get_value(byteval[-16:], "c2h_count_threshold")
    wrb_cidx_hex, wrb_cidx_str = get_value(byteval[-27:-24], "wrb_cidx")
    data_frame = [["Reserved", reserved_hex],
                  ["irq_en_wrb", irq_en_wrb_hex],
                  ["en_sts_desc_wrb", en_sts_desc_wrb_hex],
                  ["trigger_mode", trigger_mode_hex],
                  ["c2h_timer_cnt_index", c2h_timer_cnt_index_hex],
                  ["wrb_cidx", wrb_cidx_hex]]
    data_frame = pd.DataFrame(data_frame)
    return data_frame, (
        reserved_str, ";",
        irq_en_wrb_str, ";",
        en_sts_desc_wrb_str, ";",
        trigger_mode_str, ";",
        c2h_timer_cnt_index_str, ";",
        en_sts_desc_wrb_str, ";",
        c2h_count_threshold_str, ";",
        wrb_cidx_str)


def CDX_CDM_CSI_NPR_DST_FIFO_CFG0(byteval):
    if "=" in byteval:
        reserved = byteval.split("Reserved=")[1].split(";")[0]
        reserved = hex_to_bin(reserved)
        reserved = format_data_length(reserved, 15)
        irq_arm = byteval.split("irq_arm=")[1].split(";")[0]
        irq_arm = hex_to_bin(irq_arm)
        dsc_pidx = byteval.split("dsc_pidx=")[1].split(";")[0]
        dsc_pidx = hex_to_bin(dsc_pidx)
        dsc_pidx = format_data_length(dsc_pidx, 16)
        data_value = reserved + irq_arm + dsc_pidx
        data_value = format_hex_value(data_value)
        return data_value
    reserved_hex, reserved_str = get_value(byteval[-32:-28], "rsvd")
    sched_dest_id_hex, sched_dest_id_str = get_value(byteval[-28:-23], "sched_dest_id")
    sink_id_hex, sink_id_str = get_value(byteval[-23:-21], "sink_id")
    dst_fifo_id_hex, dst_fifo_id_str = get_value(byteval[-21:-14], "dst_fifo_id")
    init_crdt_hex, init_crdt_str = get_value(byteval[-14:-4], "init_crdt")
    thresh_hex, thresh_str = get_value(byteval[-4:], "thresh")
    data_frame = [["Reserved", reserved_hex],
                  ["irq_arm", sched_dest_id_hex],
                  ["sink_id", sink_id_hex],
                  ["dst_fifo_id", dst_fifo_id_hex],
                  ["init_crdt", init_crdt_hex],
                  ["thresh", thresh_hex]]
    data_frame = pd.DataFrame(data_frame)
    return data_frame, (
        reserved_str, ";",
        sched_dest_id_str, ";",
        sink_id_str, ";",
        dst_fifo_id_str, ";",
        init_crdt_str, ";",
        thresh_str)


def CDX_CDM_CSI_PR_DST_FIFO_CFG0(byteval):
    reserved_hex, reserved_str = get_value(byteval[-32:-23], "rsvd")
    sink_id_hex, sink_id_str = get_value(byteval[-23:-21], "sink_id")
    dst_fifo_id_hex, dst_fifo_id_str = get_value(byteval[-21:-14], "dst_fifo_id")
    init_crdt_hex, init_crdt_str = get_value(byteval[-14:-4], "init_crdt")
    thresh_hex, thresh_str = get_value(byteval[-4:], "thresh")
    data_frame = [["Reserved", reserved_hex],
                  ["sink_id", sink_id_hex],
                  ["dst_fifo_id", dst_fifo_id_hex],
                  ["init_crdt", init_crdt_hex],
                  ["thresh", thresh_hex]]
    data_frame = pd.DataFrame(data_frame)
    return data_frame, (
        reserved_str, ";",
        sink_id_str, ";",
        dst_fifo_id_str, ";",
        init_crdt_str, ";",
        thresh_str)


def CDX_CDM_M2ST_FIFO_CRDT_CFG(byteval):
    reserved_hex, reserved_str = get_value(byteval[-32:-16], "rsvd")
    cfg_fifo_crdt_hex, cfg_fifo_crdt_str = get_value(byteval[-16:], "cfg_fifo_crdt")
    data_frame = [["Reserved", reserved_hex],
                  ["cfg_fifo_crdt", cfg_fifo_crdt_hex]]
    data_frame = pd.DataFrame(data_frame)
    return data_frame, (
        reserved_str, ";",
        cfg_fifo_crdt_str)


def CDX_CDM_M2ST_DST_CRDT_CFG(byteval):
    reserved_hex, reserved_str = get_value(byteval[-32:-16], "rsvd")
    pkt_crd_en_hex, pkt_crd_en_str = get_value(byteval[-18], "pkt_crd_en")
    inf_crd_en_hex, inf_crd_en_str = get_value(byteval[-17], "inf_crd_en")
    cfg_dst_crdt_hex, cfg_dst_crdt_str = get_value(byteval[-16:], "cfg_dst_crdt")
    data_frame = [
        ["Reserved", reserved_hex],
        ["pkt_crd_en", pkt_crd_en_hex],
        ["inf_crd_en", inf_crd_en_hex],
        ["cfg_dst_crdt", cfg_dst_crdt_hex]]
    data_frame = pd.DataFrame(data_frame)
    return data_frame, (
        reserved_str, ";",
        pkt_crd_en_str, ";",
        inf_crd_en_str, ";",
        cfg_dst_crdt_str)


def CDX_C2H_VC_TO_CLIENT(byteval):
    ch7_hex, ch7_str = get_value(byteval[-32:-28], "ch7")
    ch6_hex, ch6_str = get_value(byteval[-28:-24], "ch6")
    ch5_hex, ch5_str = get_value(byteval[-24:-20], "ch5")
    ch4_hex, ch4_str = get_value(byteval[-20:-16], "ch4")
    ch3_hex, ch3_str = get_value(byteval[-16:-12], "ch3")
    ch2_hex, ch2_str = get_value(byteval[-12:-8], "ch2")
    ch1_hex, ch1_str = get_value(byteval[-8:-4], "ch1")
    ch0_hex, ch0_str = get_value(byteval[-4:], "ch0")
    data_frame = [
        ["ch7", ch7_hex],
        ["ch6", ch6_hex],
        ["ch5", ch5_hex],
        ["ch4", ch4_hex],
        ["ch3", ch3_hex],
        ["ch2", ch2_hex],
        ["ch1", ch1_hex],
        ["ch0", ch0_hex]]
    data_frame = pd.DataFrame(data_frame)
    return data_frame, (
        ch7_str, ";",
        ch6_str, ";",
        ch5_str, ";",
        ch4_str, ";",
        ch3_str, ";",
        ch2_str, ";",
        ch1_str, ";",
        ch0_str)


def CDX_ST2M_CLIENT_TO_VC(byteval):
    rsvd_hex, rsvd_str = get_value(byteval[-32:-16], "rsvd")
    cdm_dpu1_hex, cdm_dpu1_str = get_value(byteval[-16:-12], "cdm_dpu1")
    cdm_dpu0_hex, cdm_dpu0_str = get_value(byteval[-12:-8], "cdm_dpu0")
    cdm_fab1_hex, cdm_fab1_str = get_value(byteval[-8:-4], "cdm_fab1")
    cdm_fab0_hex, cdm_fab0_str = get_value(byteval[-4:], "cdm_fab0")
    data_frame = [
        ["rsvd", rsvd_hex],
        ["cdm_dpu1", cdm_dpu1_hex],
        ["cdm_dpu0", cdm_dpu0_hex],
        ["cdm_fab1", cdm_fab1_hex],
        ["cdm_fab0", cdm_fab0_hex]
    ]
    data_frame = pd.DataFrame(data_frame)
    return data_frame, (
        rsvd_str, ";",
        cdm_dpu1_str, ";",
        cdm_dpu0_str, ";",
        cdm_fab1_str, ";",
        cdm_fab0_str,)


def Reserved(byteval):
    rsvd_hex, rsvd_str = get_value(byteval[-32:], "rsvd")
    data_frame = [
        ["rsvd", rsvd_hex]
    ]
    data_frame = pd.DataFrame(data_frame)
    return data_frame, (
        rsvd_str)


def QDMA_GLBL_TRQ_ERR_MSK(byteval):
    rsvd_hex, rsvd_str = get_value(byteval[-32:], "mask")
    data_frame = [
        ["mask", rsvd_hex]
    ]
    data_frame = pd.DataFrame(data_frame)
    return data_frame, (
        rsvd_str)


def CDX_CDM_M2M_INT_PROF_TBL_A0(byteval):
    wr_csi_dst_fifo_hex, wr_csi_dst_fifo_str = get_value(byteval[-32:-23], "wr_csi_dst_fifo")
    rd_csi_dst_fifo_hex, rd_csi_dst_fifo_str = get_value(byteval[-23:-14], "rd_csi_dst_fifo")
    client_id_hex, client_id_str = get_value(byteval[-14:-10], "client_id")
    req_vc_hex, req_vc_str = get_value(byteval[-10:-6], "req_vc")
    rc_id_hex, rc_id_str = get_value(byteval[-6:], "rc_id")
    data_frame = [
        ["wr_csi_dst_fifo", wr_csi_dst_fifo_hex],
        ["rd_csi_dst_fifo", rd_csi_dst_fifo_hex],
        ["client_id_fifo", client_id_hex],
        ["req_vc_fifo", req_vc_hex],
        ["rc_id", rc_id_hex],
    ]
    data_frame = pd.DataFrame(data_frame)
    return data_frame, (
        wr_csi_dst_fifo_str, ";",
        rd_csi_dst_fifo_str, ";",
        client_id_str, ";",
        req_vc_str, ";",
        rc_id_str, ";"
    )


def Config_Block_Identifier(byteval):
    identifier_hex, identifier_str = get_value(byteval[-32:-20], "identifier")
    Config_block_identifier_hex, Config_block_identifier_str = get_value(byteval[-20:-16], "Config_block_identifier")
    reserved_hex, reserved_str = get_value(byteval[-16:-8], "reserved")
    version_hex, version_str = get_value(byteval[-8:], "version")
    data_frame = [
        ["identifier", identifier_hex],
        ["Config_block_identifier", Config_block_identifier_hex],
        ["reserved", reserved_hex],
        ["version", version_hex],
    ]
    data_frame = pd.DataFrame(data_frame)
    return data_frame, (
        identifier_str, ";",
        Config_block_identifier_str, ";",
        reserved_str, ";",
        version_str
    )


def Config_Block_System_ID(byteval):
    reserved_hex, reserved_str = get_value(byteval[-32:-20], "reserved")
    inst_type_hex, inst_type_str = get_value(byteval[-20:-16], "inst_type")
    system_id_hex, system_id_str = get_value(byteval[-16:-8], "system_id")
    data_frame = [
        ["reserved", reserved_hex],
        ["inst_type", inst_type_hex],
        ["reserved", system_id_hex],
    ]
    data_frame = pd.DataFrame(data_frame)
    return data_frame, (
        reserved_str, ";",
        inst_type_str, ";",
        system_id_str
    )


def Config_Block_Scratch(byteval):
    rsvd_hex, rsvd_str = get_value(byteval[-32:], "scratch")
    data_frame = [
        ["scratch", rsvd_hex]
    ]
    data_frame = pd.DataFrame(data_frame)
    return data_frame, (
        rsvd_str)


def QDMA_GLBL2_DBG_MATCH_PAT(byteval):
    rsvd_hex, rsvd_str = get_value(byteval[-32:], "pattern")
    data_frame = [
        ["pattern", rsvd_hex]
    ]
    data_frame = pd.DataFrame(data_frame)
    return data_frame, (
        rsvd_str)


def QDMA_GLBL_RNG_SZ_1(byteval):
    rsvd_hex, rsvd_str = get_value(byteval[-32:-16], "reserved")
    ring_size_hex, ring_size_str = get_value(byteval[-16:], "ring_size")
    data_frame = [
        ["pattern", rsvd_hex],
        ["ring_size", ring_size_hex]
    ]
    data_frame = pd.DataFrame(data_frame)
    return data_frame, (
        rsvd_str, ";",
        ring_size_str)


def QDMA_GLBL2_IDENTIFIER(byteval):
    identifier_hex, identifier_str = get_value(byteval[-32:-8], "identifier")
    version_hex, version_str = get_value(byteval[-8:], "version")
    data_frame = [
        ["identifier", identifier_hex],
        ["version", version_hex],
    ]
    data_frame = pd.DataFrame(data_frame)
    return data_frame, (
        identifier_str, ";",
        version_str
    )


def QDMA_GLBL2_CHANNEL_INST(byteval):
    reserved_hex, reserved_str = get_value(byteval[-32:-5], "reserved")
    cmpt_en_hex, cmpt_en_str = get_value(byteval[-5], "cmpt_en")
    dsc_eng_en_hex, dsc_eng_en_str = get_value(byteval[-4], "dsc_eng_en")
    m2m_en_hex, m2m_en_str = get_value(byteval[-3], "m2m_en")
    h2c_st_en_hex, h2c_st_en_str = get_value(byteval[-2], "h2c_st_en")
    c2h_st_en_hex, c2h_st_en_str = get_value(byteval[-1], "c2h_st_en")
    data_frame = [
        ["reserved", reserved_hex],
        ["cmpt_en", cmpt_en_hex],
        ["dsc_eng_en", dsc_eng_en_hex],
        ["m2m_en", m2m_en_hex],
        ["h2c_st_en", h2c_st_en_hex],
        ["c2h_st_en", c2h_st_en_hex],
    ]
    data_frame = pd.DataFrame(data_frame)
    return data_frame, (
        reserved_str, ";",
        cmpt_en_str, ";",
        dsc_eng_en_str, ";",
        m2m_en_str, ";",
        h2c_st_en_str, ";",
        c2h_st_en_str
    )


def QDMA_GLBL2_CHANNEL_QDMA_CAP(byteval):
    reserved_hex, reserved_str = get_value(byteval[-32:-14], "reserved")
    multiq_max_hex, multiq_max_str = get_value(byteval[-14:], "multiq_max")
    data_frame = [
        ["reserved", reserved_hex],
        ["multiq_max", multiq_max_hex],
    ]
    data_frame = pd.DataFrame(data_frame)
    return data_frame, (
        reserved_str, ";",
        multiq_max_str
    )


def QDMA_GLBL2_DBG_MATCH_SEL(byteval):
    reserved_hex, reserved_str = get_value(byteval[-32:-20], "reserved")
    match_sel_hex, match_sel_str = get_value(byteval[-20:-12], "match_sel")
    dbg1_sel_hex, dbg1_sel_str = get_value(byteval[-12:-6], "dbg1_sel")
    dbg0_sel_hex, dbg0_sel_str = get_value(byteval[-6:], "dbg0_sel")
    data_frame = [
        ["reserved", reserved_hex],
        ["match_sel", match_sel_hex],
        ["multiq_max", dbg1_sel_hex],
        ["multiq_max", dbg0_sel_hex],
    ]
    data_frame = pd.DataFrame(data_frame)
    return data_frame, (
        reserved_str, ";",
        match_sel_str, ";",
        dbg1_sel_str, ";",
        dbg0_sel_str
    )


def CDM_RFAB_RRU_CHNL_ALLOC(byteval):
    if "=" in byteval:
        reserved = byteval.split("rsvd=")[1].split(";")[0]
        reserved = hex_to_bin(reserved)
        reserved = format_data_length(reserved, 10)
        dsc_eng_num_blk = byteval.split("dsc_eng_num_blk=")[1].split(";")[0]
        dsc_eng_num_blk = hex_to_bin(dsc_eng_num_blk)
        dsc_eng_num_blk = format_data_length(dsc_eng_num_blk, 3)
        dsc_eng_blk_idx = byteval.split("dsc_eng_blk_idx=")[1].split(";")[0]
        dsc_eng_blk_idx = hex_to_bin(dsc_eng_blk_idx)
        dsc_eng_blk_idx = format_data_length(dsc_eng_blk_idx, 3)
        rsvd1 = byteval.split("rsvd1=")[1].split(";")[0]
        rsvd1 = hex_to_bin(rsvd1)
        rsvd1 = format_data_length(rsvd1, 2)
        m2st_num_blk = byteval.split("m2st_num_blk=")[1].split(";")[0]
        m2st_num_blk = hex_to_bin(m2st_num_blk)
        m2st_num_blk = format_data_length(m2st_num_blk, 3)
        m2st_blk_idx = byteval.split("m2st_blk_idx=")[1].split(";")[0]
        m2st_blk_idx = hex_to_bin(m2st_blk_idx)
        m2st_blk_idx = format_data_length(m2st_blk_idx, 3)
        rsvd0 = byteval.split("rsvd0=")[1].split(";")[0]
        rsvd0 = hex_to_bin(rsvd0)
        rsvd0 = format_data_length(rsvd0, 2)
        m2m_num_blk = byteval.split("m2m_num_blk=")[1].split(";")[0]
        m2m_num_blk = hex_to_bin(m2m_num_blk)
        m2m_num_blk = format_data_length(m2m_num_blk, 3)
        m2m_blk_idx = byteval.split("m2m_blk_idx=")[1].split(";")[0]
        m2m_blk_idx = hex_to_bin(m2m_blk_idx)
        m2m_blk_idx = format_data_length(m2m_blk_idx, 3)
        data_value = reserved + dsc_eng_num_blk + dsc_eng_blk_idx + rsvd1 + m2st_num_blk + m2st_blk_idx + rsvd0 + \
                     m2m_num_blk + m2m_blk_idx
        data_value = format_hex_value(data_value)
        return data_value
    reserved_hex, reserved_str = get_value(byteval[-32:-22], "rsvd")
    dsc_eng_num_blk_hex, dsc_eng_num_blk_str = get_value(byteval[-22:-19], "dsc_eng_num_blk")
    dsc_eng_blk_idx_hex, dsc_eng_blk_idx_str = get_value(byteval[-19:-16], "dsc_eng_blk_idx")
    rsvd1_hex, rsvd1_str = get_value(byteval[-16:-14], "rsvd1")
    m2st_num_blk_hex, m2st_num_blk_str = get_value(byteval[-14:-11], "m2st_num_blk")
    m2st_blk_idx_hex, m2st_blk_idx_str = get_value(byteval[-11:-8], "m2st_blk_idx")
    rsvd0_hex, rsvd0_str = get_value(byteval[-8:-6], "rsvd0")
    m2m_num_blk_hex, m2m_num_blk_str = get_value(byteval[-6:-3], "m2m_num_blk")
    m2m_blk_idx_hex, m2m_blk_idx_str = get_value(byteval[-3:], "m2m_blk_idx")
    data_frame = [["rsvd	", reserved_hex],
                  ["dsc_eng_num_blk", dsc_eng_num_blk_hex],
                  ["dsc_eng_blk_idx", dsc_eng_blk_idx_hex],
                  ["rsvd1", rsvd1_hex],
                  ["m2st_num_blk", m2st_num_blk_hex],
                  ["m2st_blk_idx", m2st_blk_idx_hex],
                  ["rsvd0", rsvd0_hex],
                  ["m2m_num_blk", m2m_num_blk_hex],
                  ["m2m_blk_idx", m2m_blk_idx_hex]]
    data_frame = pd.DataFrame(data_frame)
    return data_frame, (
        reserved_str, ";",
        dsc_eng_num_blk_str, ";",
        dsc_eng_blk_idx_str, ";",
        rsvd1_str, ";",
        m2st_num_blk_str, ";",
        m2st_blk_idx_str, ";",
        rsvd0_str, ";",
        m2m_num_blk_str, ";",
        m2m_blk_idx_str)
