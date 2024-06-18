import read_table

registers = '''Offset Name Type Description
0x000 INFO R DI Information
0x004 PART R Part Info
0x008 MEMINFO R Memory Info
0x00C MSIZE R Memory Size
0x010 PKGINFO R Misc Device Info
0x014 CUSTOMINFO R Custom Part Info
0x018 SWFIX R SW Fix Register
0x01C SWCAPA0 R Software Restriction
0x020 SWCAPA1 R Software Restriction
0x028 EXTINFO R External Component Info
0x040 EUI48L R EUI 48 Low
0x044 EUI48H R EUI 48 High
0x048 EUI64L R EUI64 Low
0x04C EUI64H R EUI64 High
0x050 CALTEMP R Calibration Temperature Information
0x054 EMUTEMP R EMU Temperature Sensor Calibration Information
0x058 HFRCODPLLCALn R HFRCODPLL Calibration
0x0A0 HFRCOEM23CALn R HFRCOEM23 Calibration
0x130 MODULENAME0 R Module Name Information
0x134 MODULENAME1 R Module Name Information
0x138 MODULENAME2 R Module Name Information
0x13C MODULENAME3 R Module Name Information
0x140 MODULENAME4 R Module Name Information
0x144 MODULENAME5 R Module Name Information
0x148 MODULENAME6 R Module Name Information
0x14C MODULEINFO R Module Information
0x150 MODXOCAL R Module External Oscillator Calibration Information
0x180 IADC0GAIN0 R IADC Gain Calibration
0x184 IADC0GAIN1 R IADC Gain Calibration
0x188 IADC0OFFSETCAL0 R IADC Offset Calibration
0x18C IADC0NORMALOFFSETCAL0 R IADC Offset Calibration
0x190 IADC0NORMALOFFSETCAL1 R IADC Offset Calibration
0x194 IADC0HISPDOFFSETCAL0 R IADC Offset Calibration
0x1FC LEGACY R Legacy Device Info
0x25C RTHERM R Thermistor Calibration
'''

fields = '''INFO
31:24 DEVINFOREV 0x7 R DI Page Version
23:16 PRODREV 0x0 R Production Revision
15:0 CRC 0x0 R CRC
PART
29:24 FAMILY 0x0 R Device Family
23:22 Reserved To ensure compatibility with future devices, always write Reserved bits to their reset value, unless otherwise stated. More information in 1.2 Conventions
21:16 FAMILYNUM 0x0 R Device Family
15:0 DEVICENUM 0x0 R Device Number
MEMINFO
31:16 DILEN 0x0 R Length of DI Page
15:8 UDPAGESIZE 0x0 R User Data Page Size
7:0 FLASHPAGESIZE 0x0 R Flash Page Size
MSIZE
26:16 SRAM 0x0 R Sram Size
15:0 FLASH 0x0 R Flash Size
PKGINFO
23:16 PINCOUNT 0x0 R Pin Count
15:8 PKGTYPE 0x0 R Package Type
7:0 TEMPGRADE 0x0 R Temperature Grade
CUSTOMINFO
31:16 PARTNO 0x0 R Part Number
SWFIX
31:0 RSV 0xFFFFFFFF R Reserved
SWCAPA0
21:20 SRI 0x0 R RAIL Capability
17:16 CONNECT 0x0 R Connect Capability
13:12 BTSMART 0x0 R Bluetooth Smart Capability
9:8 RF4CE 0x0 R RF4CE Capability
5:4 THREAD 0x0 R Thread Capability
1:0 ZIGBEE 0x0 R Zigbee Capability
SWCAPA1
2 GWEN 0x0 R Gateway Gateway enabled part
1 NCPEN 0x0 R NCP Network co-processor enabled part. NCP only if RFMCUEN = 0
0 RFMCUEN 0x0 R RF-MCU
EXTINFO
23:16 REV 0x0 R Revision
15:8 CONNECTION 0x0 R Connection
0 SPI SPI control interface
255 NONE No interface
7:0 TYPE 0x0 R Type
EUI48L
31:24 OUI48L 0x0 R OUI48L Lower Octet of EUI48 Organizationally Unique Identifier
23:0 UNIQUEID 0x0 R Unique ID
EUI48H
31:16 RESERVED 0xFFFF R RESERVED
15:0 OUI48H 0x0 R OUI48H
EUI64L
31:0 UNIQUEL 0x0 R UNIQUEL
EUI64H
31:8 OUI64 0x0 R OUI64 24-bit OUI identifier
7:0 UNIQUEH 0x0 R UNIQUEH
CALTEMP
7:0 TEMP 0x0 R Cal Temp
EMUTEMP
10:2 EMUTEMPROOM 0x0 R Emu Room Temperature
HFRCODPLLCALn
31:28 IREFTC 0x0 R Tempco Trim
27:26 CMPSEL 0x0 R Comparator Load Select
25:24 CLKDIV 0x0 R Locally Divide HFRCO Clock Output
23:21 CMPBIAS 0x0 R Comparator Bias Current
20:16 FREQRANGE 0x0 R Frequency Range
15 LDOHP 0x0 R LDO High Power Mode
13:8 FINETUNING 0x0 R Fine Tuning Value
6:0 TUNING 0x0 R Tuning Value
MODULENAME0
31:24 MODCHAR4 0xFF R Fourth character of Module Name, 0xFF = unwritten, 0x00 = character not used in name
23:16 MODCHAR3 0xFF R Third character of Module Name, 0xFF = unwritten, 0x00 = character not used in name
15:8 MODCHAR2 0xFF R Second character of Module Name, 0xFF = unwritten, 0x00 = character not used in name
7:0 MODCHAR1 0xFF R First character of Module Name, 0xFF = unwritten, 0x00 = character not used in name
MODULENAME1
31:24 MODCHAR8 0xFF R Character of Module Name, 0xFF = unwritten, 0x00 = character not used in name
23:16 MODCHAR7 0xFF R Character of Module Name, 0xFF = unwritten, 0x00 = character not used in name
15:8 MODCHAR6 0xFF R Character of Module Name, 0xFF = unwritten, 0x00 = character not used in name
7:0 MODCHAR5 0xFF R Character of Module Name, 0xFF = unwritten, 0x00 = character not used in name
MODULENAME2
31:24 MODCHAR12 0xFF R Character of Module Name, 0xFF = unwritten, 0x00 = character not used in name
23:16 MODCHAR11 0xFF R Character of Module Name, 0xFF = unwritten, 0x00 = character not used in name
15:8 MODCHAR10 0xFF R Character of Module Name, 0xFF = unwritten, 0x00 = character not used in name
7:0 MODCHAR9 0xFF R Character of Module Name, 0xFF = unwritten, 0x00 = character not used in name
'''

if '__main__' == __name__ :
    offsets = read_table.get_offsets(registers)
    print('    offsets = %s'%(offsets.__str__()))
    bits = read_table.get_bits(fields)
    print('    bits = %s'%(bits.__str__()))
else :
    offsets = {'INFO': 0, 'PART': 4, 'MEMINFO': 8, 'MSIZE': 12, 'PKGINFO': 16, 'CUSTOMINFO': 20, 'SWFIX': 24, 'SWCAPA0': 28, 'SWCAPA1': 32, 'EXTINFO': 40, 'EUI48L': 64, 'EUI48H': 68, 'EUI64L': 72, 'EUI64H': 76, 'CALTEMP': 80, 'EMUTEMP': 84, 'HFRCODPLLCALn': 88, 'HFRCOEM23CALn': 160, 'MODULENAME0': 304, 'MODULENAME1': 308, 'MODULENAME2': 312, 'MODULENAME3': 316, 'MODULENAME4': 320, 'MODULENAME5': 324, 'MODULENAME6': 328, 'MODULEINFO': 332, 'MODXOCAL': 336, 'IADC0GAIN0': 384, 'IADC0GAIN1': 388, 'IADC0OFFSETCAL0': 392, 'IADC0NORMALOFFSETCAL0': 396, 'IADC0NORMALOFFSETCAL1': 400, 'IADC0HISPDOFFSETCAL0': 404, 'LEGACY': 508, 'RTHERM': 604}
    bits = {'INFO': {'DEVINFOREV': '31:24', 'PRODREV': '23:16', 'CRC': '15:0'}, 'PART': {'FAMILY': '29:24', 'Reserved': '23:22', 'FAMILYNUM': '21:16', 'DEVICENUM': '15:0'}, 'MEMINFO': {'DILEN': '31:16', 'UDPAGESIZE': '15:8', 'FLASHPAGESIZE': '7:0'}, 'MSIZE': {'SRAM': '26:16', 'FLASH': '15:0'}, 'PKGINFO': {'PINCOUNT': '23:16', 'PKGTYPE': '15:8', 'TEMPGRADE': '7:0'}, 'CUSTOMINFO': {'PARTNO': '31:16'}, 'SWFIX': {'RSV': '31:0'}, 'SWCAPA0': {'SRI': '21:20', 'CONNECT': '17:16', 'BTSMART': '13:12', 'RF4CE': '9:8', 'THREAD': '5:4', 'ZIGBEE': '1:0'}, 'SWCAPA1': {'GWEN': '2', 'NCPEN': '1', 'RFMCUEN': '0'}, 'EXTINFO': {'REV': '23:16', 'CONNECTION': '15:8', 'SPI': '0', 'NONE': '255', 'TYPE': '7:0'}, 'EUI48L': {'OUI48L': '31:24', 'UNIQUEID': '23:0'}, 'EUI48H': {'RESERVED': '31:16', 'OUI48H': '15:0'}, 'EUI64L': {'UNIQUEL': '31:0'}, 'EUI64H': {'OUI64': '31:8', 'UNIQUEH': '7:0'}, 'CALTEMP': {'TEMP': '7:0'}, 'EMUTEMP': {'EMUTEMPROOM': '10:2'}, 'HFRCODPLLCALn': {'IREFTC': '31:28', 'CMPSEL': '27:26', 'CLKDIV': '25:24', 'CMPBIAS': '23:21', 'FREQRANGE': '20:16', 'LDOHP': '15', 'FINETUNING': '13:8', 'TUNING': '6:0'}, 'MODULENAME0': {'MODCHAR4': '31:24', 'MODCHAR3': '23:16', 'MODCHAR2': '15:8', 'MODCHAR1': '7:0'}, 'MODULENAME1': {'MODCHAR8': '31:24', 'MODCHAR7': '23:16', 'MODCHAR6': '15:8', 'MODCHAR5': '7:0'}, 'MODULENAME2': {'MODCHAR12': '31:24', 'MODCHAR11': '23:16', 'MODCHAR10': '15:8', 'MODCHAR9': '7:0'}}
