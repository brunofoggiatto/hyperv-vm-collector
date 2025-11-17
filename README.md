# Hyper-V VM Collector

A Python script that collects virtual machine (VM) information from multiple **Hyper-V** servers via **WinRM**.

## Features

- Connects to multiple hosts using WinRM (NTLM authentication)  
- Lists each VM’s name, state, RAM, CPU count, and IP addresses  
- Displays a unified (cluster-like) overview of all VMs  
- Simple configuration through a `config.json` file  

## Requirements

- Python 3.8 or higher  
- `pywinrm` module  

```bash
pip install -r requirements.txt
