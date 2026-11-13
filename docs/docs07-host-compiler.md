# 07 - Host Compiler (WSL)

## 1. Install Dependencies
Ubuntu 24.04 blocks `pip install`. Use `apt`:
```bash
sudo apt update
sudo apt install -y git cmake gcc g++ python3 python3-pip libzstd-dev
sudo apt install -y python3-numpy python3-decorator python3-pytest python3-attr python3-psutil python3-scipy
```

## 2. Download and Contain LLVM 17
(Since TVM-VTA uses LLVM 15, i am assuming that that is what th euser has set up. If you already have LLVM 17 just use that. **Note:** the same version **CAN'T** be used for both)

System LLVM 15 causes CMake to hard-crash. Download and contain LLVM 17: 
```bash
cd ~/Desktop/Temp
wget https://github.com/llvm/llvm-project/releases/download/llvmorg-17.0.6/clang+llvm-17.0.6-x86_64-linux-gnu-ubuntu-22.04.tar.xz
tar -xf clang+llvm-17.0.6-x86_64-linux-gnu-ubuntu-22.04.tar.xz
mv clang+llvm-17.0.6-x86_64-linux-gnu-ubuntu-22.04 llvm-17-contained
```

## 3. Clone Stable TVM
The `main` branch removed `config.cmake`. Use `v0.15.0`:
```bash
cd ~/Desktop/Temp
git clone --recursive --branch v0.15.0 https://github.com/apache/tvm tvm
cd tvm
```

## 4. Patch Zstd Linker Bug (Critical)
LLVM 17 forces a static `libzstd.a` which breaks the `-fPIC` linker. Patch TVM's CMake:
```bash
sed -i 's/zstd::libzstd_static/zstd::libzstd_shared/g' cmake/utils/FindLLVM.cmake
```

## 5. Configure and Build
WSL may freeze due to OOM during build. If this happens, run `wsl --shutdown` from Windows CMD, restart WSL, and resume with `make -j4`.
```bash
cd ~/Desktop/Temp/tvm
mkdir -p build && cd build
cmake .. -DUSE_LLVM=/home/lordfasha23/Desktop/Temp/llvm-17-contained/bin/llvm-config -DUSE_VTA_FSIM=ON
make -j4
```

## 6. Set Environment Variables
Add these to `~/.bashrc` or run them manually before executing scripts:
```bash
export PYTHONPATH=$HOME/Desktop/Temp/tvm/python:$PYTHONPATH
export TVM_LIBRARY_PATH=$HOME/Desktop/Temp/tvm/build
```