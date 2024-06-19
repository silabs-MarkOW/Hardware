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
0x050 CALTEMP R Calibration Temperature
0x054 EMUTEMP R EMU Temp
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
0x198 IADC0HISPDOFFSETCAL1 R IADC Offset Calibration
0x1FC LEGACY R Legacy Device Info
0x25C RTHERM R Thermistor Calibration
0x264 FENOTCHCAL R FENOTCH Calibration
'''

fields = '''INFO
31:24 DEVINFOREV 0x7 R DI Page Version
23:16 PRODREV 0x0 R Production Revision
15:0 CRC 0x0 R CRC
PART
29:24 FAMILY 0x0 R Device Family
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
'''

if '__main__' == __name__ :
    offsets = read_table.get_offsets(registers)
    print('    offsets = %s'%(offsets.__str__()))
    bits = read_table.get_bits(fields)
    print('    bits = %s'%(bits.__str__()))
else :
    offsets = {'INFO': 0, 'PART': 4, 'MEMINFO': 8, 'MSIZE': 12, 'PKGINFO': 16, 'CUSTOMINFO': 20, 'SWFIX': 24, 'SWCAPA0': 28, 'SWCAPA1': 32, 'EXTINFO': 40, 'EUI48L': 64, 'EUI48H': 68, 'EUI64L': 72, 'EUI64H': 76, 'CALTEMP': 80, 'EMUTEMP': 84, 'HFRCODPLLCALn': 88, 'HFRCOEM23CALn': 160, 'MODULENAME0': 304, 'MODULENAME1': 308, 'MODULENAME2': 312, 'MODULENAME3': 316, 'MODULENAME4': 320, 'MODULENAME5': 324, 'MODULENAME6': 328, 'MODULEINFO': 332, 'MODXOCAL': 336, 'IADC0GAIN0': 384, 'IADC0GAIN1': 388, 'IADC0OFFSETCAL0': 392, 'IADC0NORMALOFFSETCAL0': 396, 'IADC0NORMALOFFSETCAL1': 400, 'IADC0HISPDOFFSETCAL0': 404, 'IADC0HISPDOFFSETCAL1': 408, 'LEGACY': 508, 'RTHERM': 604, 'FENOTCHCAL': 612}
    bits = {'INFO': {'DEVINFOREV': '31:24', 'PRODREV': '23:16', 'CRC': '15:0'}, 'PART': {'FAMILY': '29:24', 'FAMILYNUM': '21:16', 'DEVICENUM': '15:0'}, 'MEMINFO': {'DILEN': '31:16', 'UDPAGESIZE': '15:8', 'FLASHPAGESIZE': '7:0'}, 'MSIZE': {'SRAM': '26:16', 'FLASH': '15:0'}, 'PKGINFO': {'PINCOUNT': '23:16', 'PKGTYPE': '15:8', 'TEMPGRADE': '7:0'}}
