# CPER_parser.py
This python script parses a CPER (Common Platform Error Record) formatted raw data that is contained in an error event log provided by WHEA-Logger.
You can read the CPER documentation at [https://uefi.org/sites/default/files/resources/UEFI_Spec_2_2_D.pdf](https://uefi.org/sites/default/files/resources/UEFI_Spec_2_2_D.pdf)
>## This script can... (for now)
>- Parse the **record header**
>- Parse **multiple section descriptors** 

> ##  This script canNOT... (for now)
> - Parse **raw data of each sections**

# Usage
Simply run the script and copy/paste the raw data you want to read.


# Disclaimer
The script has been tested with CPER from my own event logs and CPER that were posted on the internet. At this moment, the script is still incomplete and is **only capable of parsing the record header and section descriptors.** Although I will try my best to implement a parsing function for raw data of each section, I cannot guarantee the completion. <br>Also, please be aware that **the parse result may contain inaccurate results. It is highly recommended that you check the result by yourself.**<br>Feedbacks are very much welcome.
