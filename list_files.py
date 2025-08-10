#!/usr/bin/env python3
"""
AI Dataset Health ZOS - File Listing Tool

This script lists files in the repository for the AI dataset health scoring tool
for IBM z/OS via z/0SMF.
"""

import os
import sys
from pathlib import Path


def list_repository_files(repo_path="."):
    """
    List all files in the repository.
    
    Args:
        repo_path (str): Path to the repository (default: current directory)
    
    Returns:
        list: List of file paths relative to the repository root
    """
    repo_path = Path(repo_path).resolve()
    files = []
    
    # Walk through all files in the repository
    for root, dirs, filenames in os.walk(repo_path):
        # Skip .git directory
        if '.git' in dirs:
            dirs.remove('.git')
        
        for filename in filenames:
            file_path = Path(root) / filename
            # Get path relative to repository root
            relative_path = file_path.relative_to(repo_path)
            files.append(str(relative_path))
    
    return sorted(files)


def main():
    """Main function to list repository files."""
    try:
        # Get repository path from command line or use current directory
        repo_path = sys.argv[1] if len(sys.argv) > 1 else "."
        
        print(f"Listing files in repository: {Path(repo_path).resolve()}")
        print("-" * 50)
        
        files = list_repository_files(repo_path)
        
        if files:
            for i, file_path in enumerate(files, 1):
                print(f"{i:2}. {file_path}")
            print(f"\nTotal files: {len(files)}")
        else:
            print("No files found in the repository.")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()