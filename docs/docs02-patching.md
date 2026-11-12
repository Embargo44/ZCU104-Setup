# 02 - Patching Vivado (Critical)

Vivado 2020.1 has a bug that breaks IP generation. So we must apply two official AMD patches to VIVADO. **If you skip the patches, the hardware build will fail.**

## 1. Install Vivado

1.  Open the extracted Vivado folder and right-click `xsetup.exe` -> **Run as Administrator**.
2.  When it fails to connect to the internet to check for updates, click **Ignore**.
3.  **Select Install Type:** Vivado.
    *   *Why:* We only need Vivado and Vivado HLS, not the full Vitis software stack.
4.  **Select Edition:** Vivado HL WebPACK.
    *   *Why:* This is the free, license-free edition.
5.  **Select Components:** 
    *   Check `Design Tools -> Vivado Design Suite -> Vivado`.
        *   *Why:* The core synthesis tool and HLS.
    *   Check `Devices -> Production Devices -> SoCs -> Zynq UltraScale+ MPSoC`.
        *   *Why:* The exact chip family on the ZCU104.
    *   Uncheck everything else (7 Series, UltraScale, Vitis).
        *   *Why:* Saves ~20 GB of disk space and cuts install time.
6.  **Install Path:** Set to a short root path like `C:\Vivado\`.
    *   *Why:* Vivado has a 260-character Windows path limit. Deeply nested build files will crash the synthesis if installed deep in a user folder.
7.  Let it install (takes 45–90 minutes). Leave "Install Cable Drivers" checked.

## 2. Patch 1: Y2K22 Bug Fix

This patch fixes the HLS IP export bug that causes the build to fail.

1.  Locate `y2k22_patch-1.2.zip`.
2.  Extract the contents directly into your Vivado root folder (`C:\Vivado\`).
    *   **Verify:** You should have a folder path `C:\Vivado\y2k22_patch\patch.py`.
3.  Open Command Prompt and run the patch using Vivado's bundled Python:
    ```cmd
    cd /d C:\Vivado
    Vivado\2020.1\tps\win64\python-2.7.16\python.exe y2k22_patch\patch.py