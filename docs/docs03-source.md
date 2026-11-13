# 03 - Source Acquisition

## 1. Configure 100 MHz Clock
Open `config/pkg_config.py`. Find the `zcu104` block (around line 150). Change the frequency and period variables:
```python
self.fpga_freq = 100
self.fpga_per = 10
```


## 2. Clone the Fork
We use the `l0r3m1psum/tvm-vta` fork because the official repo's Makefile breaks on Windows paths.
```cmd
git clone https://github.com/l0r3m1psum/tvm-vta.git
cd tvm-vta
git checkout 15f28aa
```

## 3. Fix `make.py`
Open `hardware/xilinx/make.py`. Find the `task_ip()` function and replace its `cmd` block with:
```python
    cmd = [
        VIVADO_HLS,
        "-f", str((SCRIPT_DIR / "hls.tcl").as_posix()),
        "-tclargs",
        str((VTA_HW_DIR).as_posix()),
        str((CONFIG_TCL).as_posix())
    ]
```




**You can also run the script fromm - scripts/patch_vivado_build.py to do this all for you**
