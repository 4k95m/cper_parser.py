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



print("CPER Raw data parser\n")



raw = input("CPER Raw data: ")

sig_start = raw[0:8] # 4
revision = raw[8:12] # 2
sig_end = raw[12:20] # 4
sec_cnt = raw[20:24] # 2
err_sev = raw[24:32] # 4
valid_bits = raw[32:40] # 4
rec_len = raw[40:48] # 4
timestmp = raw[48:64] # 8
pf_id = raw[64:96] # 16
part_id = raw[96:128] # 16
crea_id = raw[128:160] # 16
notif_type = raw[160:192] # 16
rec_id = raw[192:208] # 8
flags = raw[208:216] # 4
persis_info = raw[216:232] # 8
resv = raw[232:256] # 12
sec_desc = raw[256:] # Nx72

sec_sev = sec_desc[-48:-40]
fru_txt = sec_desc[-40:]
fru_txt_ascii = bytearray.fromhex(fru_txt).decode()

rec_header = \
        "Signature Start   : " + sig_start + " (" + bytearray.fromhex(sig_start).decode() + ")" + "\n" + \
        "Revision          : " + revision + "\n" + \
        "Signature End     : " + sig_end + "\n" + \
        "Section Count     : " + sec_cnt + "\n" + \
        "Error Severity    : " + err_sev + "\n" + \
        "Validation Bits   : " + valid_bits + "\n" + \
        "Record Length     : " + rec_len + "\n" + \
        "Timestamp         : " + bcd_parser(timestmp) + "\n" + \
        "Platform ID       : " + pf_id + "\n" + \
        "Partition ID      : " + part_id + "\n" + \
        "Creator ID        : " + crea_id + "\n" + \
        "Notification Type : " + notif_type + "\n" + \
        "Record ID         : " + rec_id + "\n" + \
        "Flags             : " + flags + "\n" + \
        "Persistence Info  : " + persis_info + "\n" + \
        "Reserved [ZERO]   : " + resv + "\n"
        
descriptor = \
        "- Section Severity: " + sec_sev + "\n" + \
        "- FRU Text (Hex)  : " + fru_txt + "\n" + \
        "- FRU Text (Ascii): " + fru_txt_ascii

print("\nCPER Parse result:")
print("\nRaw data length: "+ str(int(len(raw)/2)) + "\n")
print("[Record Header]")
print(rec_header)
print("\n[Section Descriptor]")
print(descriptor)

