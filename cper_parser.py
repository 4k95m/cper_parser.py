import re



def byte_parse(str):
    split_text = re.split("(..)", str)
    split_text = split_text[1::2]
    split_text.reverse()
    return "".join(split_text)



def bcd_parser(bcd):
    century = str(int(bcd[-2:], 16))
    year = str(int(bcd[-4:-2], 16))
    month = str(int(bcd[-6:-4], 16))
    day = str(int(bcd[-8:-6], 16))
    hour = str(int(bcd[-12:-10], 16))
    minite = str(int(bcd[-14:-12], 16))
    sec = str(int(bcd[-16:-14], 16))

    date = century+year+"/"+month+"/"+day+" "+hour+":"+minite+":"+sec+" (UTC)"

    return date



def severity(sev):
    sev = byte_parse(sev)
    if sev == "00000000":
        sev_str = f"Recoverable)"
    elif sev == "00000001":
        sev_str = f"Fatal"
    elif sev == "00000002":
        sev_str = f"Corrected"
    elif sev == "00000003":
        sev_str = f"Informational"
    else:
        sev_str = "Unknown severity"
    return sev_str



def validbits_parser(valid_bits):
    vb_bin = f"{int(valid_bits, 16):0>32b}"
    valids = []
    if vb_bin[-1]=="1":
        valids.append("Platform ID")
    if vb_bin[-2]=="1":
        valids.append("Timestamp")
    if vb_bin[-3]=="1":
        valids.append("Partition ID")

    return "Valid values in: "+", ".join(valids)



print("CPER Raw data parser\n")

raw = input("CPER Raw data: ")

sig_start = raw[0:8] # 4
revision = byte_parse(raw[8:12]) # 2
sig_end = raw[12:20] # 4
sec_cnt = int(byte_parse(raw[20:24])) # 2
err_sev = raw[24:32] # 4
valid_bits = byte_parse(raw[32:40]) # 4
rec_len = raw[40:48] # 4
timestmp = raw[48:64] # 8
pf_id = raw[64:96] # 16
part_id = raw[96:128] # 16
crea_id = raw[128:160] # 16
notif_type = raw[160:192] # 16
rec_id = raw[192:208] # 8
flags = byte_parse(raw[208:216]) # 4
persis_info = raw[216:232] # 8
resv = raw[232:256] # 12

sec_desc_list = []
for i in range(sec_cnt):
    start = 256+i*144
    end = start+144
    sec_desc_list.append(raw[start:end])

def sec_desc_parser(sec_desc):
    sec_off = sec_desc[0:8] # 4
    sec_len = sec_desc[8:16] # 4
    sec_rev = sec_desc[16:20] # 2
    sec_valid = sec_desc[20:22] # 1
    sec_resv = sec_desc[22:24] # 2
    sec_flags = sec_desc[24:32] # 4
    sec_type = sec_desc[32:64] # 16
    fru_id = sec_desc[64:96] # 16
    sec_sev = sec_desc[96:104] # 8
    fru_txt = sec_desc[104:144] # 20
    fru_txt_ascii = bytearray.fromhex(fru_txt).decode()

    descriptor = \
            "- Section Offset  : " + str(int(byte_parse(sec_off), 16)) + "\n" + \
            "- Section Length  : " + str(int(byte_parse(sec_len), 16)) + "\n" + \
            "- Section Revision: " + sec_rev + "\n" + \
            "- Section ValidBit: " + sec_valid + "\n" + \
            "- Reserved [ZERO] : " + sec_resv + "\n" + \
            "- Flags           : " + sec_flags + "\n" + \
            "- Section Types   : " + sec_type + "\n" + \
            "- FRU Id          : " + fru_id + "\n" + \
            "- Section Severity: " + severity(sec_sev) + "\n" + \
            "- FRU Text (Hex)  : " + fru_txt + "\n" + \
            "- FRU Text (Ascii): " + fru_txt_ascii

    return descriptor

rec_header = \
        "- Signature Start   : " + sig_start + " (" + bytearray.fromhex(sig_start).decode() + ")" + "\n" + \
        "- Revision          : " + byte_parse(revision) + "\n" + \
        "- Signature End     : " + sig_end + "\n" + \
        "- Section Count     : " + str(sec_cnt) + "\n" + \
        "- Error Severity    : " + severity(err_sev) + "\n" + \
        "- Validation Bits   : " + validbits_parser(valid_bits) + "\n" + \
        "- Record Length     : " + str(int(byte_parse(rec_len), 16)) + "\n" + \
        "- Timestamp         : " + bcd_parser(timestmp) +"\n" + \
        "- Platform ID       : " + pf_id + "\n" + \
        "- Partition ID      : " + part_id + "\n" + \
        "- Creator ID        : " + crea_id + "\n" + \
        "- Notification Type : " + notif_type + "\n" + \
        "- Record ID         : " + rec_id + "\n" + \
        "- Flags             : " + flags + "\n" + \
        "- Persistence Info  : " + persis_info + "\n" + \
        "- Reserved [ZERO]   : " + resv + "\n"



print("\n####################")
print("CPER Parse result")
print("\nRaw data length: "+ str(int(len(raw)/2)))
print("####################\n")
print("\n###################")
print("[Record Header]")
print("###################")
print(rec_header)
print("\n#########################")
print("[Section Descriptors]")
print("#########################")
for sec_desc in sec_desc_list:
    print(sec_desc_parser(sec_desc))
    print("\n")


print("Section 1 (Raw)  :\n" + raw[400:])
print("\nPartial parse result:")
print("Section 1 (Ascii):\n" + bytearray.fromhex(raw[-40:]).decode())



