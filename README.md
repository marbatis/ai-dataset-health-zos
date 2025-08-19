# AI Dataset Health ZOS

AI dataset health scoring for IBM z/OS via z/0SMF (Db2-free). ONNX inference runs on Linux on Z; writes PDSE/GDG reports.

## Features

- **File Listing**: List all files in the repository for analysis and inventory

## Quick start

```bash
# list files
python list_files.py .

# run the health report (empty-file score)
python list_files.py --health .
```

## Usage

### List Repository Files

```bash
# List files in current directory
python3 list_files.py

# List files in specific repository path
python3 list_files.py /path/to/repository

# Run as executable
./list_files.py
```

## Files

- `list_files.py` - Tool to list all files in the repository
- `README.md` - This documentation file  
- `LICENSE` - MIT license file
