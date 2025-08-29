# AI Dataset Health ZOS

AI dataset health scoring for IBM z/OS via z/0SMF (Db2-free). ONNX inference runs on Linux on Z; writes PDSE/GDG reports.

## Features

- **File Listing**: List all files in the repository for analysis and inventory

## Quick start

```bash
# Install the package in development mode
pip install -e .

# Run health check using the console script
ai-dataset-health-zos --health .

# Or run directly with Python module (development)
PYTHONPATH=src python -m ai_dataset_health_zos.cli --health .
```

## Usage

### Health Analysis

```bash
# Using the installed console script
ai-dataset-health-zos --health .
ai-dataset-health-zos --health /path/to/repository

# Development mode (without installation)
PYTHONPATH=src python -m ai_dataset_health_zos.cli --health .
```

### List Repository Files (Legacy)

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
- `LICENSE` - Apache-2.0 license file

## License

License: Apache-2.0 (see LICENSE). Docs under CC BY 4.0.
