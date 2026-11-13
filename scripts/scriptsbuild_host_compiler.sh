#!/bin/bash
set -e

echo "========================================"
echo "Building TVM Host Compiler for VTA"
echo "========================================"

# 1. Install Dependencies (Bypass Ubuntu 24.04 pip restrictions)
echo "[*] Installing system dependencies..."
sudo apt update
sudo apt install -y git cmake gcc g++ python3 python3-pip libzstd-dev
sudo apt install -y python3-numpy python3-decorator python3-pytest python3-attr python3-psutil python3-scipy

# 2. Download and Contain LLVM 17
echo "[*] Downloading LLVM 17..."
cd ~
if [ ! -d "llvm-17-contained" ]; then
    wget https://github.com/llvm/llvm-project/releases/download/llvmorg-17.0.6/clang+llvm-17.0.6-x86_64-linux-gnu-ubuntu-22.04.tar.xz
    tar -xf clang+llvm-17.0.6-x86_64-linux-gnu-ubuntu-22.04.tar.xz
    mv clang+llvm-17.0.6-x86_64-linux-gnu-ubuntu-22.04 llvm-17-contained
    rm clang+llvm-17.0.6-x86_64-linux-gnu-ubuntu-22.04.tar.xz
else
    echo "[*] LLVM 17 already downloaded."
fi

# 3. Clone TVM v0.15.0
echo "[*] Cloning TVM v0.15.0..."
if [ ! -d "tvm" ]; then
    git clone --recursive --branch v0.15.0 https://github.com/apache/tvm tvm
else
    echo "[*] TVM folder already exists. Skipping clone."
fi

# 4. Patch Zstd Linker Bug
echo "[*] Patching FindLLVM.cmake for shared zstd..."
cd ~/tvm
# Revert any previous patches to be safe
git checkout cmake/utils/FindLLVM.cmake || true
sed -i 's/zstd::libzstd_static/zstd::libzstd_shared/g' cmake/utils/FindLLVM.cmake

# 5. Configure and Build
echo "[*] Configuring and building TVM. This will take 15-40 minutes..."
mkdir -p build
cd build
cmake .. -DUSE_LLVM="$HOME/llvm-17-contained/bin/llvm-config" -DUSE_VTA_FSIM=ON
make -j4

# 6. Add to bashrc
echo "[*] Adding TVM to PYTHONPATH in ~/.bashrc..."
if ! grep -q "TVM_LIBRARY_PATH" ~/.bashrc; then
    echo 'export PYTHONPATH=$HOME/tvm/python:$PYTHONPATH' >> ~/.bashrc
    echo 'export TVM_LIBRARY_PATH=$HOME/tvm/build' >> ~/.bashrc
fi

echo "========================================"
echo "Host Compiler Build Complete!"
echo "Please run: source ~/.bashrc"
echo "========================================"