# 01 - Environment Prep

Before installing Vivado, we must prepare the host environment and extract the toolchain.

## 1. WSL (Windows Subsystem for Linux)
Install Ubuntu 22.04 via PowerShell (`wsl --install -d Ubuntu-22.04`). Then run:
```bash
sudo apt update
sudo apt install -y git cmake gcc g++ python3 python3-pip