# 07 - Host Compiler (WSL)

The host laptop needs the Apache TVM compiler to translate AI models into VTA-specific instructions. 

## 1. Install Dependencies

Open your WSL (Ubuntu) terminal and install the build tools and compression libraries:
```bash
sudo apt update
sudo apt install -y git cmake gcc g++ python3 python3-pip libzstd-dev
sudo apt install -y python3-numpy python3-decorator python3-pytest python3-attr python3-psutil python3-scipy
```

## 2. Download and Contain LLVM 17  
(optionally if you have LLVM already, just use that. But the TVM version uses LLVM 15, so the same version can't be used for both)

Modern TVM requires LLVM 17. Ubuntu's default repositories only have LLVM 15. We download a pre-built binary and contain it in a specific folder:

```bash
cd ~/Desktop
wget https://github.com/llvm/llvm-project/releases/download/llvmorg-17.0.6/clang+llvm-17.0.6-x86_64-linux-gnu-ubuntu-22.04.tar.xz
tar -xf clang+llvm-17.0.6-x86_64-linux-gnu-ubuntu-22.04.tar.xz
mv clang+llvm-17.0.6-x86_64-linux-gnu-ubuntu-22.04 llvm-17-contained
```

## 3. Clone TVM (Stable Version)

The `main` branch of TVM removed the `config.cmake` file. We must use the stable `v0.15.0` release.

```bash
cd ~/Desktop
git clone --recursive --branch v0.15.0 https://github.com/apache/tvm tvm
cd tvm
```

## 4. Patch the LLVM CMake File (Critical)

LLVM 17 forces TVM to link against a static `libzstd.a` file, which fails with a `-fPIC` relocation error on Ubuntu. We must patch TVM's CMake file to use the shared `.so` library instead:

```bash
sed -i 's/zstd::libzstd_static/zstd::libzstd_shared/g' cmake/utils/FindLLVM.cmake
```

## 5. Configure and Build

```bash
cd ~/Desktop/tvm
mkdir -p build
cd build

cmake .. \
  -DUSE_LLVM=/home/lordfasha23/Desktop/llvm-17-contained/bin/llvm-config \
  -DUSE_VTA_FSIM=ON

make -j4
```

## 6. Verify

Once the build finishes, test that the Python bindings work:
```bash
export PYTHONPATH=$HOME/Desktop/tvm/python:$PYTHONPATH
export TVM_LIBRARY_PATH=$HOME/Desktop/tvm/build
python3 -c "import tvm; print(tvm.__version__)"
```