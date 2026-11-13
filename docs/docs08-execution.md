# 08 - Execution & Custom Binaries

Running your own custom C++ binaries on the board requires manually linking against the PYNQ driver. 

## 1. Compile Custom C++ on the Board

If you write a custom C++ program (like `run_fpga.cpp`) that uses the VTA API, you cannot simply link against `libvta.so` because the hardware symbols are sometimes left undefined. You must explicitly compile the `pynq_driver.cc` source file into your executable.

Run this exact `g++` command on the board:

```bash
cd /home/xilinx/jupyter_notebooks
g++ -std=c++17 -O2 run_fpga.cpp -o run_fpga \
  -I tvm/3rdparty/vta-hw/include \
  -I tvm/include \
  -I tvm/3rdparty/vta-hw/src/pynq \
  tvm/3rdparty/vta-hw/src/pynq/pynq_driver.cc \
  -L /home/xilinx/jupyter_notebooks/tvm/build -ltvm_runtime -lvta \
  -Wl,-rpath,/home/xilinx/jupyter_notebooks/tvm/build
```

*Why this works:* By adding `tvm/3rdparty/vta-hw/src/pynq/pynq_driver.cc` directly to the compiler command, we bypass TVM's broken CMake logic and link the memory-mapped hardware functions directly into your binary.

## 2. Run the Binary

Execute your newly compiled program with your test data:
```bash
sudo ./run_fpga my_program.bin test.data
```

(The fpga test setup I have is only for me. Find your own ways to test it)