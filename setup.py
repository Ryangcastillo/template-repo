#!/usr/bin/env python3
"""
Setup script for CMS development environment.
"""

import os
import sys
import subprocess
from pathlib import Path


def run_command(cmd, description):
    """Run a shell command with error handling."""
    print(f"📦 {description}...")
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"✅ {description} completed")
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        return False
    return True


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")


def setup_virtual_environment():
    """Set up virtual environment and install dependencies."""
    venv_path = Path("venv")
    
    if not venv_path.exists():
        if not run_command(f"{sys.executable} -m venv venv", "Creating virtual environment"):
            return False
    
    # Determine activate script path based on OS
    if os.name == 'nt':  # Windows
        activate_script = venv_path / "Scripts" / "activate"
        pip_cmd = str(venv_path / "Scripts" / "pip")
    else:  # Unix/Linux/MacOS
        activate_script = venv_path / "bin" / "activate"
        pip_cmd = str(venv_path / "bin" / "pip")
    
    # Install dependencies
    if not run_command(f"{pip_cmd} install --upgrade pip", "Upgrading pip"):
        return False
    
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies"):
        return False
    
    print(f"""
🎉 Virtual environment setup complete!

To activate the environment:
  Source: source {activate_script}  # Unix/Linux/MacOS
  Windows: {activate_script}

To run tests:
  python run_tests.py

To start development:
  1. Activate the virtual environment
  2. Set up your database (see docs/environment.md)
  3. Run the application
""")
    return True


def install_pre_commit_hooks():
    """Install pre-commit hooks for code quality."""
    try:
        # Check if pre-commit is available
        subprocess.run(["pre-commit", "--version"], 
                      capture_output=True, check=True)
        
        if run_command("pre-commit install", "Installing pre-commit hooks"):
            print("✅ Pre-commit hooks installed")
            return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  pre-commit not available, skipping hooks installation")
    
    return False


def create_env_file():
    """Create .env file from template if it doesn't exist."""
    env_file = Path(".env")
    env_template = Path(".env.example")
    
    if not env_file.exists():
        if env_template.exists():
            run_command("cp .env.example .env", "Creating .env file from template")
        else:
            # Create basic .env file
            with open(".env", "w") as f:
                f.write("""# CMS Environment Variables
DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_URL=sqlite:///cms.db

# Optional: Context7 API Key
# CONTEXT7_API_KEY=your-api-key-here
""")
            print("✅ Created basic .env file")
    else:
        print("✅ .env file already exists")


def main():
    """Main setup function."""
    print("🚀 Setting up Python CMS development environment...")
    
    # Check Python version
    check_python_version()
    
    # Set up virtual environment
    if not setup_virtual_environment():
        print("❌ Failed to set up virtual environment")
        sys.exit(1)
    
    # Install pre-commit hooks
    install_pre_commit_hooks()
    
    # Create environment file
    create_env_file()
    
    print("""
🎯 Setup complete! Next steps:

1. Read the documentation:
   - docs/environment.md - Development environment
   - docs/architecture.md - System architecture
   - docs/developer-guidelines.md - TDD practices

2. Run tests to verify setup:
   python run_tests.py

3. Start developing with TDD:
   - Write failing test (Red)
   - Write minimal code (Green) 
   - Refactor (Blue)

4. Follow the AI Agent Contract:
   - All changes must follow .aiconfig.md rules
   - Use Context7 MCP: include 'use context7' in AI prompts
   - Commit with proper prefixes: Refactor|Fix|Add|Update|Remove|Docs|Spec

Happy coding! 🎉
""")


if __name__ == "__main__":
    main()