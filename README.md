# VTA on ZCU104 — Setup Guide

Configuring Apache TVM - VTA on a Xilinx ZCU104 FPGA

## Setup Overview

### Phase 1: Environment Prep
Download the **Vivado 2020.1** toolchain. Install utilities (balenaEtcher). The host environment is set up on **WSL (Ubuntu)**.

### Phase 2: Patching Vivado (Critical)
For Vivado 2020.1 to work for us we apply **2** patches to it (Y2K22 and AR75516). BOTH CRITICAL. Without them, the hardware build will fail to generate IP cores.

### Phase 3: Source Acquisition (Patching Critical)
Clone the **tvm-vta** hardware fork. **Patch the Python script (`make.py`)** to fix Windows path logic and HLS generation. The official repo uses a Linux-only Makefile.

### Phase 4: Bitstream Generation (Patching Critical)
Edit `pkg_config.py` to set the clock to **100 MHz** (freq=100, period=10). Bypass the HLS C-Simulation segfault by commenting out `csim_design` in `hls.tcl`. Manually find and rename the `.hwh` file.

### Phase 5: Board Setup
Flash the PYNQ v2.7 image to the SD card. Boot the ZCU104. Extract CMake 3.27.7 on the board. Compile the VTA runtime and driver on the board. **Use `ultra96_sample.json` to force the PYNQ driver symbols to compile.**

### Phase 6: Hardware Loading
Upload the `.bit` and `.hwh` files to the board. Load them with PYNQ.

### Phase 7: Host Compiler
Build Apache TVM (v0.15.0) in WSL using contained LLVM 17. Patch TVM's CMake files to fix a `zstd` static linking error.

### Phase 8: Execution
Compile custom C++ inference binary (`run_fpga.cpp`) directly on the board, explicitly including `pynq_driver.cc` in the `g++` command to resolve hardware symbols.

---

## The 3-Part Build Architecture

1. **The Hardware (Windows):** The `.bit` file is generated using Vivado.
2. **The Board Runtime (ZCU104 Linux):** The `libvta.so` driver and TVM runtime are compiled on the board's ARM processor.
3. **The Host Compiler (WSL Linux):** The full TVM compiler is built on the laptop.

## Critical Modifications Checklist

- [ ] **PYNQ Version:** Must use v2.7.
- [ ] **Vivado Installer:** Must use the 35.51 GB "All OS Installer" (.tar.gz), installed to `C:\Vivado` to avoid path limits.
- [ ] **Vivado Patches:** Y2K22 and AR75516 patches.
- [ ] **`make.py` Fix:** `task_ip` must use `VIVADO_HLS` and `hls.tcl`. 
- [ ] **HLS Segfault:** Comment out `csim_design -clean` in `hls.tcl`.
- [ ] **Clock Speed:** `pkg_config.py` must have `fpga_freq = 100` and `fpga_per = 10`.
- [ ] **TVM Version:** Use `v0.15.0`.
- [ ] **LLVM Version:** Must use contained LLVM 17.
- [ ] **Zstd Linker Fix:** Patch `FindLLVM.cmake` to use `libzstd_shared`.
- [ ] **Board JSON:** Use `ultra96_sample.json` to force `libvta.so` to compile the PYNQ driver.
- [ ] **File Naming:** `vta.bit` and `vta.hwh` must have matching names.
- [ ] **FPGA Manager:** If overlay load hangs, use `Ctrl+C`, NEVER `kill -9`.

---

## Documentation Index

- [00 - Downloads](docs/docs00-downloads.md)
- [01 - Environment Prep](docs/docs01-environment_prep.md)
- [02 - Patching Vivado](docs/docs02-patching.md)
- [03 - Source Acquisition](docs/docs03-source.md)
- [04 - Bitstream Generation](docs/docs04-bitstream.md)
- [05 - Board Setup](docs/docs05-board-setup.md)
- [06 - Hardware Loading](docs/docs06-loading.md)
- [07 - Host Compiler](docs/docs07-host-compiler.md)
- [08 - Execution](docs/docs08-execution.md)



jns