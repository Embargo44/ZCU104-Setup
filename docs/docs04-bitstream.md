# 04 - Bitstream Generation



## 1. Bypass HLS Segfault (Critical)
Vivado 2020.1's HLS simulation crashes with a `SIGSEGV` error on modern Windows machines. We must skip it.
1. Open `hardware/xilinx/scripts/hls.tcl`.
2. Find `csim_design -clean` (line ~89).
3. Comment it out:
```tcl
# csim_design -clean
```

## 2. Run Build
```cmd
cd /d C:\Users\LordFasha23\Work\CS_Files\FPGA\tvm-vta\hardware\xilinx
set PATH=C:\Vivado\Vivado\2020.1\bin;%PATH%
copy /y ..\..\config\zcu104_sample.json ..\..\config\vta_config.json
python make.py bit
```



 When it finishes, look for `impl_1 finished`. (it tends to get stuck here, waiting for this process. to check if the process is dead, check cpu usage by vivado. If it isnt using the cpu that means the process is dead)

 Also if the bit stream generation has any problems, its recomended you turn every other process on the laptop off.

## 3. Locate Files
The `.bit` is in `export\vta.bit`. 
**Critical:** The build script does not copy the `.hwh` file. Search the `vivado` build folder for `*.hwh` (usually `vta_wrapper.hwh`), copy it to `export`, and rename it to `vta.hwh`.