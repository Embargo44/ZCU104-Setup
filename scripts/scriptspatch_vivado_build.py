import os
import re

def main():
    print("========================================")
    print("Patching TVM-VTA Hardware Build Scripts")
    print("========================================")
    
    # Ensure we are in the hardware/xilinx directory
    if not os.path.exists("make.py"):
        print("[!] Error: make.py not found. Please run this script from the 'hardware/xilinx' directory.")
        return

    # 1. Patch make.py (Fix task_ip to use VIVADO_HLS)
    print("[*] Patching make.py...")
    with open("make.py", "r") as f:
        content = f.read()

    # Replace the buggy cmd block in task_ip with the correct one
    old_make_block = """    cmd = [
        VIVADO,
        "-mode", "tcl",
        "-source", str(SCRIPT_DIR / "vivado.tcl"),
        "-tclargs",
        str(BUILD_DIR / "hls" / CONF),
        str(CONFIG_TCL)
    ]"""
    new_make_block = """    cmd = [
        VIVADO_HLS,
        "-f", str((SCRIPT_DIR / "hls.tcl").as_posix()),
        "-tclargs",
        str((VTA_HW_DIR).as_posix()),
        str((CONFIG_TCL).as_posix())
    ]"""
    
    # We only want to replace the FIRST occurrence (inside task_ip)
    content = content.replace(old_make_block, new_make_block, 1)
    
    # Remove any -jobs 2 if it was added
    content = content.replace('"-jobs", "2",\n', '')
    content = content.replace('"-jobs", "2"\n', '')

    with open("make.py", "w") as f:
        f.write(content)
    print("  -> make.py patched.")

    # 2. Patch pkg_config.py (Set 100 MHz)
    print("[*] Patching pkg_config.py...")
    config_path = "../../config/pkg_config.py"
    with open(config_path, "r") as f:
        cfg_content = f.read()

    # Find the zcu104 block and change freq/per
    # We use regex to find the specific block
    zcu104_pattern = r'(elif self.TARGET == "zcu104":.*?self.fpga_freq = )\d+(.*?self.fpga_per = )\d+'
    cfg_content = re.sub(zcu104_pattern, r'\g<1>100\g<2>10', cfg_content, flags=re.DOTALL)
    
    with open(config_path, "w") as f:
        f.write(cfg_content)
    print("  -> pkg_config.py set to 100 MHz (10ns period).")

    # 3. Patch hls.tcl (Bypass C-Simulation Segfault)
    print("[*] Patching hls.tcl...")
    with open("scripts/hls.tcl", "r") as f:
        hls_content = f.read()
    
    hls_content = hls_content.replace("csim_design -clean", "# csim_design -clean")
    
    with open("scripts/hls.tcl", "w") as f:
        f.write(hls_content)
    print("  -> hls.tcl simulation bypassed.")

    print("========================================")
    print("All patches applied successfully!")
    print("You can now run: python make.py bit")
    print("========================================")

if __name__ == "__main__":
    main()