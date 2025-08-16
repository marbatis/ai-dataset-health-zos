# AI Dataset Health ZOS

AI dataset health scoring for IBM z/OS via z/0SMF (Db2-free). ONNX inference runs on Linux on Z; writes PDSE/GDG reports.

## Features

- **File Listing**: List all files in the repository for analysis and inventory

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

### Options

```python
from list_files import list_repository_files

# Include only text files
list_repository_files(include=['**/*.txt'])

# Exclude test directories
list_repository_files(exclude=['tests/**'])

# Limit search depth
list_repository_files(max_depth=1)

# Include hidden files
list_repository_files(include_hidden=True)
```


## Files

- `list_files.py` - Tool to list all files in the repository
- `README.md` - This documentation file  
- `LICENSE` - MIT license file
