# VTA on ZCU104 — Setup Guide

Configuring Apache TVM - VTA on a Xilinx ZCU104 FPGA

## Setup Overview

### Phase 1: Environment Prep
Download the **Vivado 2020.1** toolchain. install utilities ( balenaEtcher). The host environment is also set up on **WSL (Ubuntu)**.

### Phase 2: Patching Vivado (Critical)
For Vivado 2020.1 to work for us we apply **2** patches to it (Y2K22 and AR75516). BOTH CRITICAL. Without them, the hardware build will fail to generate IP cores.

### Phase 3: Source Acquisition (Patching Critical)
Clone the **tvm-vta** hardware fork. **Patch the Python script (`make.py`)** to fix Windows path logic and HLS generation. The official repo uses a Linux-only Makefile.

### Phase 4: Bitstream Generation (Patching Critical)
Edit `pkg_config.py` to set the clock to **100 MHz**. Run the patched build script in Vivado. It compiles the hardware and generates the `vta.bit` file.

### Phase 5: Board Setup
Flash the PYNQ v2.7 image to the SD card. Boot the ZCU104. Compile the VTA runtime on the board using CMake 3.27.7, and start the RPC server.

### Phase 6: Hardware Loading
Upload the `.bit` and `.hwh` files to the board. Load them with PYNQ.

### Phase 7: Host Compiler
Build the main Apache TVM compiler in WSL. 

### Phase 8: Execution


---

## The 3-Part Build Architecture

We require compiling three separate pieces in three different environments:

1. **The Hardware (Windows):** The `.bit` file is generated using Vivado. This is the physical FPGA circuit.
2. **The Board Runtime (ZCU104 Linux):** The `libvta.so` driver and TVM runtime are compiled on the board's ARM processor so it can talk to the FPGA and receive data.
3. **The Host Compiler (WSL Linux):** The full TVM compiler is built on the laptop 

## Critical Modifications Checklist

- [ ] **PYNQ Version:** Must use v2.7 (v3.x/v4.x require newer Vivado).
- [ ] **Vivado Installer:** Must use the 35.51 GB "All OS Installer" (.tar.gz), not the web installer.
- [ ] **Vivado Patches:** Y2K22 and AR75516 patches are mandatory.
- [ ] **`make.py` Fix:** `task_ip` must use `VIVADO_HLS` and `hls.tcl`.
- [ ] **Clock Speed:** `pkg_config.py` must be changed from 333 to 100 MHz.
- [ ] **File Naming:** `vta.bit` and `vta.hwh` must have matching names.
- [ ] **FPGA Manager:** If overlay load hangs, use `Ctrl+C`, NEVER `kill -9`.

---

## Documentation Index

- [00 - Downloads](docs/00-downloads.md)
- [01 - Environment Prep](docs/01-environment.md)
- [02 - Patching Vivado](docs/02-patching.md)
- [03 - Source Acquisition](docs/03-source.md)
- [04 - Bitstream Generation](docs/04-bitstream.md)
- [05 - Board Setup](docs/05-board-setup.md)
- [06 - Hardware Loading](docs/06-loading.md)
- [07 - Host Compiler](docs/07-host-compiler.md)
- [08 - Execution](docs/08-execution.md)