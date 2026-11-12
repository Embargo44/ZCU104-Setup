# 03 - Source Acquisition

We do not use the official Apache TVM repository for the hardware build. We use a community fork (`l0r3m1psum/tvm-vta`) because it includes a Python build script (`make.py`) that correctly handles Windows file paths.

## 1. Clone the Fork

Open Command Prompt and clone the specific commit that is known to work:

```cmd

git clone https://github.com/l0r3m1psum/tvm-vta.git
cd tvm-vta
git checkout 15f28aa
```
*(Note: You will see a "detached HEAD" warning. This is normal and expected.)*

## 2. Fix the Build Script (`make.py`)

Out of the box, `make.py` has bugs that break the build on Windows. It calls the main Vivado binary for the HLS step instead of `vivado_hls`.

1. Open `hardware/xilinx/make.py` in Notepad.
2. Find the `task_ip()` function.
3. Replace its `cmd` block with this exact code:

```python
    cmd = [
        VIVADO_HLS,
        "-f", str((SCRIPT_DIR / "hls.tcl").as_posix()),
        "-tclargs",
        str((VTA_HW_DIR).as_posix()),
        str((CONFIG_TCL).as_posix())
    ]
```

