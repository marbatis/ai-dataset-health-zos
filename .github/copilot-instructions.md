# AI Dataset Health ZOS

AI dataset health scoring for IBM z/OS via z/OSMF (Db2-free). ONNX inference runs on Linux on Z; writes PDSE/GDG reports.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Environment Setup
- Python 3.12+ required (tested with Python 3.12.3)
- No external dependencies - uses Python standard library only
- `python3 --version` - verify Python installation
- `which python3` - confirm Python location

### Repository Setup
- `git clone https://github.com/marbatis/ai-dataset-health-zos.git`
- `cd ai-dataset-health-zos`
- Repository uses standard Python structure with executable scripts

### Build and Run
- **No build step required** - Python scripts run directly
- Make scripts executable: `chmod +x list_files.py`
- Run file listing tool:
  - Current directory: `python3 list_files.py`
  - Specific path: `python3 list_files.py /path/to/directory` 
  - As executable: `./list_files.py`
  - From different directory: `python3 /path/to/repo/list_files.py /target/path`

### Testing and Validation
- **No test framework configured** - manual validation required
- Validate syntax: `python3 -m py_compile list_files.py`
- Test scenarios:
  - Small repository: `python3 list_files.py` (executes in ~0.03 seconds)
  - Large directories: `python3 list_files.py /usr/lib/python3` (executes in ~2-3 seconds for 12,000+ files)
  - Empty directories: handled gracefully with "No files found" message
  - Invalid paths: handled gracefully, shows resolved path attempt
- **CRITICAL VALIDATION**: Always run complete user scenarios after making changes:
  1. `python3 list_files.py` - list current repository files
  2. `./list_files.py /tmp` - test as executable with different path
  3. Verify output shows numbered file list with total count

### Performance Expectations
- File listing execution times (NEVER CANCEL):
  - Small repositories (1-10 files): <0.1 seconds
  - Medium repositories (100-1,000 files): <0.5 seconds  
  - Large directories (10,000+ files): 2-3 seconds
  - **No timeout concerns** - all operations complete quickly

## Key Projects and Files

### Repository Structure
```
.
├── LICENSE              # MIT license
├── README.md           # Project documentation
└── list_files.py       # File listing tool (main functionality)
```

### Core Functionality
- **list_files.py**: Main tool for repository file analysis
  - Lists all files recursively, excluding .git directory
  - Accepts optional directory path argument
  - Outputs numbered list with total file count
  - Uses pathlib.Path for cross-platform compatibility
  - Error handling for invalid paths and empty directories

### Python Modules Used
- `os` - file system operations
- `sys` - command line arguments and error handling
- `pathlib` - modern path handling

## Validation Requirements

### Manual Testing Steps
1. **Basic functionality**: `python3 list_files.py` - must show current repository files
2. **Path argument**: `python3 list_files.py /usr` - must handle external directories
3. **Executable mode**: `./list_files.py` - must work as standalone script
4. **Error handling**: `python3 list_files.py /nonexistent` - must handle gracefully
5. **Empty directory**: Create empty dir and test - must show "No files found"

### Code Quality
- **No linting tools configured** - manual code review required
- Python syntax validation: `python3 -m py_compile list_files.py`
- **No external dependencies** - uses only Python standard library
- **No requirements.txt or setup.py** - no dependency management needed

### Expected Output Format
```
Listing files in repository: /full/path/to/directory
--------------------------------------------------
 1. LICENSE
 2. README.md
 3. list_files.py

Total files: 3
```

## Development Guidelines

### Adding New Features
- Maintain Python standard library only approach
- Follow existing error handling patterns
- Test with various directory sizes and structures
- Ensure cross-platform Path handling using pathlib
- Always test as both `python3 script.py` and `./script.py`

### Common Tasks
- **Repository analysis**: Use `python3 list_files.py` to inventory files
- **Directory comparison**: Compare file lists between different paths
- **File counting**: Quick file count for any directory structure

### No CI/CD Configuration
- **No GitHub workflows present** - manual testing required
- **No automated linting or testing** - validate changes manually
- Recommended validation sequence:
  1. Syntax check: `python3 -m py_compile filename.py`
  2. Manual testing with multiple scenarios
  3. Verify executable permissions and shebang

### Troubleshooting
- **"No module named..."**: This project uses only standard library - check Python installation
- **Permission denied**: Run `chmod +x list_files.py` to make executable
- **Path not found**: Script handles gracefully, verify target directory exists
- **Unexpected output**: Verify Python 3.12+ is being used

## Current Development Status
- **Early stage repository** with core file listing functionality
- **No external dependencies** - ready to run immediately after clone
- **Manual testing approach** - no automated test suite configured
- **Single core feature** - file listing and repository analysis tool

Always run the complete manual validation scenarios after making any changes to ensure functionality remains intact.