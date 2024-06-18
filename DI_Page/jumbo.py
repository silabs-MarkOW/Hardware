import read_table

registers = '''Offset Name Type Description
0x000 CAL RO CRC of DI-page and calibration temperature
0x004 MODULEINFO RO Module trace information
0x008 MODXOCAL RO Module Crystal Oscillator Calibration
0x020 EXTINFO RO External Component description
0x028 EUI48L RO EUI48 OUI and Unique identifier
0x02C EUI48H RO OUI
0x030 CUSTOMINFO RO Custom information
0x034 MEMINFO RO Flash page size and misc. chip information
0x040 UNIQUEL RO Low 32 bits of device unique number
0x044 UNIQUEH RO High 32 bits of device unique number
0x048 MSIZE RO Flash and SRAM Memory size in kB
0x04C PART RO Part description
0x050 DEVINFOREV RO Device information page revision
0x054 EMUTEMP RO EMU Temperature Calibration Information
0x060 ADC0CAL0 RO ADC0 calibration register 0
0x064 ADC0CAL1 RO ADC0 calibration register 1
0x068 ADC0CAL2 RO ADC0 calibration register 2
0x06C ADC0CAL3 RO ADC0 calibration register 3
0x080 HFRCOCAL0 RO HFRCO Calibration Register (4 MHz)
0x08C HFRCOCAL3 RO HFRCO Calibration Register (7 MHz)
0x098 HFRCOCAL6 RO HFRCO Calibration Register (13 MHz)
0x09C HFRCOCAL7 RO HFRCO Calibration Register (16 MHz)
0x0A0 HFRCOCAL8 RO HFRCO Calibration Register (19 MHz)
0x0A8 HFRCOCAL10 RO HFRCO Calibration Register (26 MHz)
0x0AC HFRCOCAL11 RO HFRCO Calibration Register (32 MHz)
0x0B0 HFRCOCAL12 RO HFRCO Calibration Register (38 MHz)
0x0E0 AUXHFRCOCAL0 RO AUXHFRCO Calibration Register (4 MHz)
0x0EC AUXHFRCOCAL3 RO AUXHFRCO Calibration Register (7 MHz)
0x0F8 AUXHFRCOCAL6 RO AUXHFRCO Calibration Register (13 MHz)
0x0FC AUXHFRCOCAL7 RO AUXHFRCO Calibration Register (16 MHz)
0x100 AUXHFRCOCAL8 RO AUXHFRCO Calibration Register (19 MHz)
0x108 AUXHFRCOCAL10 RO AUXHFRCO Calibration Register (26 MHz)
0x10C AUXHFRCOCAL11 RO AUXHFRCO Calibration Register (32 MHz)
0x110 AUXHFRCOCAL12 RO AUXHFRCO Calibration Register (38 MHz)
0x140 VMONCAL0 RO VMON Calibration Register 0
0x144 VMONCAL1 RO VMON Calibration Register 1
0x148 VMONCAL2 RO VMON Calibration Register 2
0x158 IDAC0CAL0 RO IDAC0 Calibration Register 0
0x15C IDAC0CAL1 RO IDAC0 Calibration Register 1
0x168 DCDCLNVCTRL0 RO DCDC Low-noise VREF Trim Register 0
0x16C DCDCLPVCTRL0 RO DCDC Low-power VREF Trim Register 0
0x170 DCDCLPVCTRL1 RO DCDC Low-power VREF Trim Register 1
0x174 DCDCLPVCTRL2 RO DCDC Low-power VREF Trim Register 2
0x178 DCDCLPVCTRL3 RO DCDC Low-power VREF Trim Register 3
0x17C DCDCLPCMPHYSSEL0 RO DCDC LPCMPHYSSEL Trim Register 0
0x180 DCDCLPCMPHYSSEL1 RO DCDC LPCMPHYSSEL Trim Register 1
0x184 VDAC0MAINCAL RO VDAC0 Cals for Main Path
0x188 VDAC0ALTCAL RO VDAC0 Cals for Alternate Path
0x18C VDAC0CH1CAL RO VDAC0 CH1 Error Cal
0x190 OPA0CAL0 RO OPA0 Calibration Register for DRIVESTRENGTH 0, INCBW=1
0x194 OPA0CAL1 RO OPA0 Calibration Register for DRIVESTRENGTH 1, INCBW=1
0x198 OPA0CAL2 RO OPA0 Calibration Register for DRIVESTRENGTH 2, INCBW=1
0x19C OPA0CAL3 RO OPA0 Calibration Register for DRIVESTRENGTH 3, INCBW=1
0x1A0 OPA1CAL0 RO OPA1 Calibration Register for DRIVESTRENGTH 0, INCBW=1
0x1A4 OPA1CAL1 RO OPA1 Calibration Register for DRIVESTRENGTH 1, INCBW=1
0x1A8 OPA1CAL2 RO OPA1 Calibration Register for DRIVESTRENGTH 2, INCBW=1
0x1AC OPA1CAL3 RO OPA1 Calibration Register for DRIVESTRENGTH 3, INCBW=1
0x1B0 OPA2CAL0 RO OPA2 Calibration Register for DRIVESTRENGTH 0, INCBW=1
0x1B4 OPA2CAL1 RO OPA2 Calibration Register for DRIVESTRENGTH 1, INCBW=1
0x1B8 OPA2CAL2 RO OPA2 Calibration Register for DRIVESTRENGTH 2, INCBW=1
0x1BC OPA2CAL3 RO OPA2 Calibration Register for DRIVESTRENGTH 3, INCBW=1
0x1C0 CSENGAINCAL RO Cap Sense Gain Adjustment
0x1D0 OPA0CAL4 RO OPA0 Calibration Register for DRIVESTRENGTH 0, INCBW=0
0x1D4 OPA0CAL5 RO OPA0 Calibration Register for DRIVESTRENGTH 1, INCBW=0
0x1D8 OPA0CAL6 RO OPA0 Calibration Register for DRIVESTRENGTH 2, INCBW=0
0x1DC OPA0CAL7 RO OPA0 Calibration Register for DRIVESTRENGTH 3, INCBW=0
0x1E0 OPA1CAL4 RO OPA1 Calibration Register for DRIVESTRENGTH 0, INCBW=0
0x1E4 OPA1CAL5 RO OPA1 Calibration Register for DRIVESTRENGTH 1, INCBW=0
0x1E8 OPA1CAL6 RO OPA1 Calibration Register for DRIVESTRENGTH 2, INCBW=0
0x1EC OPA1CAL7 RO OPA1 Calibration Register for DRIVESTRENGTH 3, INCBW=0
0x1F0 OPA2CAL4 RO OPA2 Calibration Register for DRIVESTRENGTH 0, INCBW=0
0x1F4 OPA2CAL5 RO OPA2 Calibration Register for DRIVESTRENGTH 1, INCBW=0
0x1F8 OPA2CAL6 RO OPA2 Calibration Register for DRIVESTRENGTH 2, INCBW=0
0x1FC OPA2CAL7 RO OPA2 Calibration Register for DRIVESTRENGTH 3, INCBW=0
'''

fields = '''PART
31:24 PROD_REV RO Production revision as unsigned integer
23:16 DEVICE_FAMILY RO Device Family
15:0 DEVICE_NUMBER RO Part number as unsigned integer (e.g. 233 for EFR32BG1P233F256GM48-B0)
HFRCOCAL0
31:28 VREFTC RO HFRCO Temperature Coefficient Trim on Comparator Reference
27 FINETUNINGEN RO HFRCO enable reference for fine tuning
26:25 CLKDIV RO HFRCO Clock Output Divide
24 LDOHP RO HFRCO LDO High Power Mode
23:21 CMPBIAS RO HFRCO Comparator Bias Current
20:16 FREQRANGE RO HFRCO Frequency Range
13:8 FINETUNING RO HFRCO Fine Tuning Value
6:0 TUNING RO HFRCO Tuning Value
HFRCOCAL1
31:28 VREFTC RO HFRCO Temperature Coefficient Trim on Comparator Reference
27 FINETUNINGEN RO HFRCO enable reference for fine tuning
26:25 CLKDIV RO HFRCO Clock Output Divide
24 LDOHP RO HFRCO LDO High Power Mode
23:21 CMPBIAS RO HFRCO Comparator Bias Current
20:16 FREQRANGE RO HFRCO Frequency Range
13:8 FINETUNING RO HFRCO Fine Tuning Value
6:0 TUNING RO HFRCO Tuning Value
HFRCOCAL2
31:28 VREFTC RO HFRCO Temperature Coefficient Trim on Comparator Reference
27 FINETUNINGEN RO HFRCO enable reference for fine tuning
26:25 CLKDIV RO HFRCO Clock Output Divide
24 LDOHP RO HFRCO LDO High Power Mode
23:21 CMPBIAS RO HFRCO Comparator Bias Current
20:16 FREQRANGE RO HFRCO Frequency Range
13:8 FINETUNING RO HFRCO Fine Tuning Value
6:0 TUNING RO HFRCO Tuning Value
HFRCOCAL3
31:28 VREFTC RO HFRCO Temperature Coefficient Trim on Comparator Reference
27 FINETUNINGEN RO HFRCO enable reference for fine tuning
26:25 CLKDIV RO HFRCO Clock Output Divide
24 LDOHP RO HFRCO LDO High Power Mode
23:21 CMPBIAS RO HFRCO Comparator Bias Current
20:16 FREQRANGE RO HFRCO Frequency Range
13:8 FINETUNING RO HFRCO Fine Tuning Value
6:0 TUNING RO HFRCO Tuning Value
HFRCOCAL4
31:28 VREFTC RO HFRCO Temperature Coefficient Trim on Comparator Reference
27 FINETUNINGEN RO HFRCO enable reference for fine tuning
26:25 CLKDIV RO HFRCO Clock Output Divide
24 LDOHP RO HFRCO LDO High Power Mode
23:21 CMPBIAS RO HFRCO Comparator Bias Current
20:16 FREQRANGE RO HFRCO Frequency Range
13:8 FINETUNING RO HFRCO Fine Tuning Value
6:0 TUNING RO HFRCO Tuning Value
HFRCOCAL5
31:28 VREFTC RO HFRCO Temperature Coefficient Trim on Comparator Reference
27 FINETUNINGEN RO HFRCO enable reference for fine tuning
26:25 CLKDIV RO HFRCO Clock Output Divide
24 LDOHP RO HFRCO LDO High Power Mode
23:21 CMPBIAS RO HFRCO Comparator Bias Current
20:16 FREQRANGE RO HFRCO Frequency Range
13:8 FINETUNING RO HFRCO Fine Tuning Value
6:0 TUNING RO HFRCO Tuning Value
HFRCOCAL6
31:28 VREFTC RO HFRCO Temperature Coefficient Trim on Comparator Reference
27 FINETUNINGEN RO HFRCO enable reference for fine tuning
26:25 CLKDIV RO HFRCO Clock Output Divide
24 LDOHP RO HFRCO LDO High Power Mode
23:21 CMPBIAS RO HFRCO Comparator Bias Current
20:16 FREQRANGE RO HFRCO Frequency Range
13:8 FINETUNING RO HFRCO Fine Tuning Value
6:0 TUNING RO HFRCO Tuning Value
HFRCOCAL7
31:28 VREFTC RO HFRCO Temperature Coefficient Trim on Comparator Reference
27 FINETUNINGEN RO HFRCO enable reference for fine tuning
26:25 CLKDIV RO HFRCO Clock Output Divide
24 LDOHP RO HFRCO LDO High Power Mode
23:21 CMPBIAS RO HFRCO Comparator Bias Current
20:16 FREQRANGE RO HFRCO Frequency Range
13:8 FINETUNING RO HFRCO Fine Tuning Value
6:0 TUNING RO HFRCO Tuning Value
HFRCOCAL8
31:28 VREFTC RO HFRCO Temperature Coefficient Trim on Comparator Reference
27 FINETUNINGEN RO HFRCO enable reference for fine tuning
26:25 CLKDIV RO HFRCO Clock Output Divide
24 LDOHP RO HFRCO LDO High Power Mode
23:21 CMPBIAS RO HFRCO Comparator Bias Current
20:16 FREQRANGE RO HFRCO Frequency Range
13:8 FINETUNING RO HFRCO Fine Tuning Value
6:0 TUNING RO HFRCO Tuning Value
HFRCOCAL9
31:28 VREFTC RO HFRCO Temperature Coefficient Trim on Comparator Reference
27 FINETUNINGEN RO HFRCO enable reference for fine tuning
26:25 CLKDIV RO HFRCO Clock Output Divide
24 LDOHP RO HFRCO LDO High Power Mode
23:21 CMPBIAS RO HFRCO Comparator Bias Current
20:16 FREQRANGE RO HFRCO Frequency Range
13:8 FINETUNING RO HFRCO Fine Tuning Value
6:0 TUNING RO HFRCO Tuning Value
HFRCOCAL10
31:28 VREFTC RO HFRCO Temperature Coefficient Trim on Comparator Reference
27 FINETUNINGEN RO HFRCO enable reference for fine tuning
26:25 CLKDIV RO HFRCO Clock Output Divide
24 LDOHP RO HFRCO LDO High Power Mode
23:21 CMPBIAS RO HFRCO Comparator Bias Current
20:16 FREQRANGE RO HFRCO Frequency Range
13:8 FINETUNING RO HFRCO Fine Tuning Value
6:0 TUNING RO HFRCO Tuning Value
HFRCOCAL11
31:28 VREFTC RO HFRCO Temperature Coefficient Trim on Comparator Reference
27 FINETUNINGEN RO HFRCO enable reference for fine tuning
26:25 CLKDIV RO HFRCO Clock Output Divide
24 LDOHP RO HFRCO LDO High Power Mode
23:21 CMPBIAS RO HFRCO Comparator Bias Current
20:16 FREQRANGE RO HFRCO Frequency Range
13:8 FINETUNING RO HFRCO Fine Tuning Value
6:0 TUNING RO HFRCO Tuning Value
HFRCOCAL12
31:28 VREFTC RO HFRCO Temperature Coefficient Trim on Comparator Reference
27 FINETUNINGEN RO HFRCO enable reference for fine tuning
26:25 CLKDIV RO HFRCO Clock Output Divide
24 LDOHP RO HFRCO LDO High Power Mode
23:21 CMPBIAS RO HFRCO Comparator Bias Current
20:16 FREQRANGE RO HFRCO Frequency Range
13:8 FINETUNING RO HFRCO Fine Tuning Value
6:0 TUNING RO HFRCO Tuning Value
HFRCOCAL13
31:28 VREFTC RO HFRCO Temperature Coefficient Trim on Comparator Reference
27 FINETUNINGEN RO HFRCO enable reference for fine tuning
26:25 CLKDIV RO HFRCO Clock Output Divide
24 LDOHP RO HFRCO LDO High Power Mode
23:21 CMPBIAS RO HFRCO Comparator Bias Current
20:16 FREQRANGE RO HFRCO Frequency Range
13:8 FINETUNING RO HFRCO Fine Tuning Value
6:0 TUNING RO HFRCO Tuning Value
'''

if '__main__' == __name__ :
    offsets = read_table.get_offsets(registers)
    print('    offsets = %s'%(offsets.__str__()))
    bits = read_table.get_bits(fields)
    print('    bits = %s'%(bits.__str__()))
else :
    offsets = {'CAL': 0, 'MODULEINFO': 4, 'MODXOCAL': 8, 'EXTINFO': 32, 'EUI48L': 40, 'EUI48H': 44, 'CUSTOMINFO': 48, 'MEMINFO': 52, 'UNIQUEL': 64, 'UNIQUEH': 68, 'MSIZE': 72, 'PART': 76, 'DEVINFOREV': 80, 'EMUTEMP': 84, 'ADC0CAL0': 96, 'ADC0CAL1': 100, 'ADC0CAL2': 104, 'ADC0CAL3': 108, 'HFRCOCAL0': 128, 'HFRCOCAL3': 140, 'HFRCOCAL6': 152, 'HFRCOCAL7': 156, 'HFRCOCAL8': 160, 'HFRCOCAL10': 168, 'HFRCOCAL11': 172, 'HFRCOCAL12': 176, 'AUXHFRCOCAL0': 224, 'AUXHFRCOCAL3': 236, 'AUXHFRCOCAL6': 248, 'AUXHFRCOCAL7': 252, 'AUXHFRCOCAL8': 256, 'AUXHFRCOCAL10': 264, 'AUXHFRCOCAL11': 268, 'AUXHFRCOCAL12': 272, 'VMONCAL0': 320, 'VMONCAL1': 324, 'VMONCAL2': 328, 'IDAC0CAL0': 344, 'IDAC0CAL1': 348, 'DCDCLNVCTRL0': 360, 'DCDCLPVCTRL0': 364, 'DCDCLPVCTRL1': 368, 'DCDCLPVCTRL2': 372, 'DCDCLPVCTRL3': 376, 'DCDCLPCMPHYSSEL0': 380, 'DCDCLPCMPHYSSEL1': 384, 'VDAC0MAINCAL': 388, 'VDAC0ALTCAL': 392, 'VDAC0CH1CAL': 396, 'OPA0CAL0': 400, 'OPA0CAL1': 404, 'OPA0CAL2': 408, 'OPA0CAL3': 412, 'OPA1CAL0': 416, 'OPA1CAL1': 420, 'OPA1CAL2': 424, 'OPA1CAL3': 428, 'OPA2CAL0': 432, 'OPA2CAL1': 436, 'OPA2CAL2': 440, 'OPA2CAL3': 444, 'CSENGAINCAL': 448, 'OPA0CAL4': 464, 'OPA0CAL5': 468, 'OPA0CAL6': 472, 'OPA0CAL7': 476, 'OPA1CAL4': 480, 'OPA1CAL5': 484, 'OPA1CAL6': 488, 'OPA1CAL7': 492, 'OPA2CAL4': 496, 'OPA2CAL5': 500, 'OPA2CAL6': 504, 'OPA2CAL7': 508}
    bits = {'PART': {'PROD_REV': '31:24', 'DEVICE_FAMILY': '23:16', 'DEVICE_NUMBER': '15:0'}, 'HFRCOCAL0': {'VREFTC': '31:28', 'FINETUNINGEN': '27', 'CLKDIV': '26:25', 'LDOHP': '24', 'CMPBIAS': '23:21', 'FREQRANGE': '20:16', 'FINETUNING': '13:8', 'TUNING': '6:0'}, 'HFRCOCAL1': {'VREFTC': '31:28', 'FINETUNINGEN': '27', 'CLKDIV': '26:25', 'LDOHP': '24', 'CMPBIAS': '23:21', 'FREQRANGE': '20:16', 'FINETUNING': '13:8', 'TUNING': '6:0'}, 'HFRCOCAL2': {'VREFTC': '31:28', 'FINETUNINGEN': '27', 'CLKDIV': '26:25', 'LDOHP': '24', 'CMPBIAS': '23:21', 'FREQRANGE': '20:16', 'FINETUNING': '13:8', 'TUNING': '6:0'}, 'HFRCOCAL3': {'VREFTC': '31:28', 'FINETUNINGEN': '27', 'CLKDIV': '26:25', 'LDOHP': '24', 'CMPBIAS': '23:21', 'FREQRANGE': '20:16', 'FINETUNING': '13:8', 'TUNING': '6:0'}, 'HFRCOCAL4': {'VREFTC': '31:28', 'FINETUNINGEN': '27', 'CLKDIV': '26:25', 'LDOHP': '24', 'CMPBIAS': '23:21', 'FREQRANGE': '20:16', 'FINETUNING': '13:8', 'TUNING': '6:0'}, 'HFRCOCAL5': {'VREFTC': '31:28', 'FINETUNINGEN': '27', 'CLKDIV': '26:25', 'LDOHP': '24', 'CMPBIAS': '23:21', 'FREQRANGE': '20:16', 'FINETUNING': '13:8', 'TUNING': '6:0'}, 'HFRCOCAL6': {'VREFTC': '31:28', 'FINETUNINGEN': '27', 'CLKDIV': '26:25', 'LDOHP': '24', 'CMPBIAS': '23:21', 'FREQRANGE': '20:16', 'FINETUNING': '13:8', 'TUNING': '6:0'}, 'HFRCOCAL7': {'VREFTC': '31:28', 'FINETUNINGEN': '27', 'CLKDIV': '26:25', 'LDOHP': '24', 'CMPBIAS': '23:21', 'FREQRANGE': '20:16', 'FINETUNING': '13:8', 'TUNING': '6:0'}, 'HFRCOCAL8': {'VREFTC': '31:28', 'FINETUNINGEN': '27', 'CLKDIV': '26:25', 'LDOHP': '24', 'CMPBIAS': '23:21', 'FREQRANGE': '20:16', 'FINETUNING': '13:8', 'TUNING': '6:0'}, 'HFRCOCAL9': {'VREFTC': '31:28', 'FINETUNINGEN': '27', 'CLKDIV': '26:25', 'LDOHP': '24', 'CMPBIAS': '23:21', 'FREQRANGE': '20:16', 'FINETUNING': '13:8', 'TUNING': '6:0'}, 'HFRCOCAL10': {'VREFTC': '31:28', 'FINETUNINGEN': '27', 'CLKDIV': '26:25', 'LDOHP': '24', 'CMPBIAS': '23:21', 'FREQRANGE': '20:16', 'FINETUNING': '13:8', 'TUNING': '6:0'}, 'HFRCOCAL11': {'VREFTC': '31:28', 'FINETUNINGEN': '27', 'CLKDIV': '26:25', 'LDOHP': '24', 'CMPBIAS': '23:21', 'FREQRANGE': '20:16', 'FINETUNING': '13:8', 'TUNING': '6:0'}, 'HFRCOCAL12': {'VREFTC': '31:28', 'FINETUNINGEN': '27', 'CLKDIV': '26:25', 'LDOHP': '24', 'CMPBIAS': '23:21', 'FREQRANGE': '20:16', 'FINETUNING': '13:8', 'TUNING': '6:0'}, 'HFRCOCAL13': {'VREFTC': '31:28', 'FINETUNINGEN': '27', 'CLKDIV': '26:25', 'LDOHP': '24', 'CMPBIAS': '23:21', 'FREQRANGE': '20:16', 'FINETUNING': '13:8', 'TUNING': '6:0'}}
