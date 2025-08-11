# AI Dataset Health for IBM z/OS

AI dataset health scoring for IBM z/OS via z/OSMF (Db2-free). ONNX inference runs on Linux on Z; writes PDSE/GDG reports.

**ALWAYS follow these instructions first and only fallback to search or bash commands when you encounter unexpected information that does not match the info here.**

## Current Repository State

**CRITICAL**: This repository is currently in early development stage with minimal codebase. Only README.md and LICENSE files exist.

- Do NOT attempt to build, test, or run code - no source code exists yet
- Do NOT look for package.json, requirements.txt, Makefile, or other build files - they do not exist
- Do NOT search for CI/CD workflows - none exist yet

## Working Effectively

### Repository Exploration
- View repository contents: `ls -la` shows only README.md and LICENSE
- Read project description: `cat README.md` provides the project overview
- Check git history: `git log --oneline` shows initial commits only

### Future Development Preparation
When source code is added to this repository, typical IBM z/OS and Linux development patterns suggest:

#### Expected Technology Stack (Based on Project Description)
- **Target Platform**: IBM z/OS mainframe systems
- **Inference Platform**: Linux on Z (s390x architecture)
- **AI Framework**: ONNX (Open Neural Network Exchange)
- **Data Access**: z/OSMF (IBM z/OS Management Facility) - Db2-free approach
- **Output Format**: PDSE (Partitioned Data Set Extended) and GDG (Generation Data Groups)

#### Anticipated Development Setup (When Code Exists)
- Expect Python-based implementation for ONNX inference
- Likely requirements.txt or pyproject.toml for Python dependencies
- Possible Docker containers for Linux on Z deployment
- JCL (Job Control Language) files for z/OS batch processing
- Configuration files for z/OSMF REST API access

### Validation Steps (When Code Exists)
- **NEVER CANCEL**: AI model training/inference can take 30+ minutes. Set timeout to 60+ minutes
- **NEVER CANCEL**: z/OS job submission and retrieval can take 10+ minutes. Set timeout to 20+ minutes
- Test ONNX model loading and inference on sample data
- Validate z/OSMF connectivity and authentication
- Verify PDSE/GDG output generation and formatting
- Test on actual s390x Linux environment when possible

## Project Structure (Expected)
Based on the project description, anticipate these components when developed:

```
/
├── README.md                    # Project documentation
├── LICENSE                      # MIT License
├── requirements.txt            # Python dependencies (ONNX, requests, etc.)
├── src/                        # Source code
│   ├── inference/              # ONNX inference engine
│   ├── zosmf/                  # z/OSMF REST API client
│   ├── dataset_health/         # Health scoring algorithms
│   └── output/                 # PDSE/GDG report generation
├── models/                     # ONNX model files
├── config/                     # Configuration files
├── jcl/                        # JCL for z/OS batch processing
├── docker/                     # Container definitions for Linux on Z
└── tests/                      # Unit and integration tests
```

## Common Tasks (When Code Exists)

### Environment Setup
- Install Python 3.8+ with s390x support for Linux on Z
- Install ONNX runtime for s390x: `pip install onnxruntime`
- Configure z/OSMF connection credentials
- Set up SSL certificates for mainframe connectivity

### Development Workflow
- Run unit tests: `python -m pytest tests/` (expected 5-10 minutes runtime)
- Lint code: `flake8 src/` or `pylint src/`
- Type check: `mypy src/`
- Test ONNX models: Load and run inference on sample datasets
- Validate z/OSMF connectivity: Test REST API calls with authentication

### Deployment Considerations
- **Linux on Z**: Deploy inference containers on s390x architecture
- **z/OS Integration**: Submit JCL jobs for dataset processing
- **Network Security**: Ensure proper SSL/TLS for z/OSMF communication
- **Performance**: Monitor inference latency and memory usage on mainframe resources

## Important Notes

### Mainframe-Specific Considerations
- EBCDIC vs ASCII encoding issues when transferring data
- z/OS dataset naming conventions (44-character limit)
- JCL job scheduling and resource allocation
- Security considerations for mainframe access (RACF, ACF2, Top Secret)

### Development Limitations
- **Cannot test on actual mainframe**: Development environment limitations
- **s390x emulation**: May need QEMU for architecture-specific testing
- **z/OSMF sandbox**: Require access to IBM z/OS system for full testing

## Repository History
- **Initial State**: README.md and LICENSE only
- **Next Steps**: Await source code implementation based on project description

## Contact and Resources
- Review IBM z/OSMF REST API documentation
- Consult ONNX documentation for s390x deployment
- Reference IBM z/OS dataset management guides for PDSE/GDG handling