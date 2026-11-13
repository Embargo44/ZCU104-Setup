# 05 - Board Setup

## 1. Flash and Boot
Flash PYNQ v2.7 to the SD card. Insert into ZCU104. Set SW6 to `ON, OFF, OFF, OFF`. Connect Ethernet and power. Ping `192.168.2.99`.

## 2. Upload and Extract CMake
Upload the `tvm` folder and `cmake-3.27.7-linux-aarch64.tar.gz` to `/home/xilinx/jupyter_notebooks/`.
```bash
cd /home/xilinx/jupyter_notebooks/
tar -xzvf cmake-3.27.7-linux-aarch64.tar.gz
```

## 3. The Smart Build Script
Create `board_build_vta.sh` in `~/tvm` on the board:
```bash
#!/bin/bash
set -e
cd "$(dirname "$0")"

if [ ! -d "build" ] || [ ! -f "build/libtvm_runtime.so" ]; then
    echo "[!] First-time build detected. Running full compile..."
    mkdir -p build
    cd build
    cp ../cmake/config.cmake .
    echo 'set(USE_VTA_FPGA ON)' >> config.cmake
    /home/xilinx/jupyter_notebooks/cmake-3.27.7-linux-aarch64/bin/cmake ..
    make runtime vta -j2
else
    echo "[*] Existing build found. Incremental patch build..."
    cd build
    make runtime vta -j2
fi
echo "Build complete!"
```

## 4. The "Ultra96" JSON Hack (Critical)
If checking `libvta.so` with `nm -D` results in `U VTADeviceAlloc` (undefined reference), the PYNQ driver was not compiled correctly. 
Fix it by replacing the board config with the Ultra96 one and rebuilding:
```bash
cd /home/xilinx/jupyter_notebooks/tvm
cp 3rdparty/vta-hw/config/ultra96_sample.json 3rdparty/vta-hw/config/vta_config.json
rm -rf build
./board_build_vta.sh
```
*Why:* The Ultra96 config forces CMake to compile the `pynq_driver.cc` file, resolving the memory mapping symbols.

## 5. Start RPC Server
```bash
cd /home/xilinx/jupyter_notebooks/tvm
sudo ./apps/vta_rpc/start_rpc_server.sh
```




**You can also run the script from - scripts/board_build_vta.sh to do this all for you**
