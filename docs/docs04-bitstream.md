# 04 - Bitstream Generation

Before building, we must configure the hardware for 100 MHz and bypass a Vivado simulation crash.

## 1. Configure the 100 MHz Clock

By default, the VTA design targets 333 MHz. We use 100 MHz for stability and faster build times.

1. Open `config/pkg_config.py` in Notepad.
2. Find the `zcu104` block (around line 150).
3. Change the frequency and period variables:
```python
self.fpga_freq = 100
self.fpga_per = 10
```
*(Note: `fpga_per` is the period in nanoseconds. 10ns = 100 MHz).*

## 2. Bypass the Crashing C-Simulation (Critical)

Vivado 2020.1's HLS simulation crashes with a `SIGSEGV` error on modern Windows machines. We must skip it.

1. Open `hardware/xilinx/scripts/hls.tcl` in Notepad.
2. Find the line `csim_design -clean` (around line 89).
3. Comment it out by adding a `#`:
```tcl
# csim_design -clean
```

## 3. Run the Build

1. Open Command Prompt and navigate to the build directory:
   
2. Set the Vivado PATH:
   
3. Ensure the ZCU104 configuration is active:
  
   ```
4. Run the build:
    python make.py bit



## 4. Locate the Files

The `.bit` file is exported to:
`build\hardware\xilinx\vivado\zcu104_1x16_i8w8a32_15_15_18_17\export\vta.bit`

**Critical:** The build script does not automatically copy the `.hwh` (hardware handoff) file to the export folder. 
1. Search the `vivado` build folder for `*.hwh` 
3. Rename it to `vta.hwh` so it matches the `.bit` file.