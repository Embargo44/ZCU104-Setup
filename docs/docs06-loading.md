# 06 - Hardware Loading

Before running any code, the FPGA must be configured with the bitstream.

## 1. Upload the Bitstream
Use the Jupyter web interface to upload both `vta.bit` and `vta.hwh` into the `/home/xilinx/jupyter_notebooks/` folder.

## 2. Load the Overlay
Open a Jupyter Terminal on the board and run:

```bash
cd /home/xilinx/jupyter_notebooks/
python3 -c "from pynq import Overlay; Overlay('vta.bit'); print('100 MHz VTA Loaded!')"
```

If you get an error saying `Unable to find metadata for bitstream`, ensure the `.hwh` file is in the exact same folder and has the exact same base name as the `.bit` file.

