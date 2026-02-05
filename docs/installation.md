# Installation

## Prerequisites

- Python 3.8 or higher
- pipx (recommended for Globus CLI installation)

## Install Globus CLI

The Globus CLI is the foundation for all administrative tools.

### Using pipx (Recommended)

`pipx` installs tools in a self-contained environment, so they won't interfere with your other Python packages

```bash
# Install pipx if not already available
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# Install Globus CLI
pipx install globus-cli
```

### Using uv

Use `uv tool` to install it in a self-contained environment:

```bash
uv tool install globus-cli
```

### Using pip

```bash
pip install globus-cli
```

## Verify Installation

```bash
globus version
```

Expected output:
```
Installed version:  3.41.0
Latest version:     3.41.0

You are running the latest version of the Globus CLI
```

## Install Administrative Tools

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/sih-globus.git
   cd sih-globus
   ```

2. **Make scripts executable:**
   ```bash
   chmod +x scripts/*.py scripts/globus-admin
   ```

3. **Install optional dependencies:**
   ```bash
   pip install black flake8  # For development
   ```

## Enable Tab Completion

Add to your shell configuration file (`.bashrc`, `.zshrc`, etc.):

```bash
eval "$(_GLOBUS_COMPLETE=bash_source globus)"
```

## Verify Setup

Run the demo script to verify everything is working:

```bash
./scripts/demo.py
```

!!! tip "Path Setup"
    If you want to use the tools from anywhere, add the scripts directory to your PATH:
    ```bash
    export PATH="$PATH:/path/to/sih-globus/scripts"
    ```

## Troubleshooting

### Command Not Found

If `globus` command is not found after installation:

1. Ensure pipx bin directory is in PATH:
   ```bash
   pipx ensurepath
   source ~/.bashrc  # or ~/.zshrc
   ```

2. Verify installation location:
   ```bash
   pipx list
   which globus
   ```

### Permission Errors

If scripts aren't executable:
```bash
chmod +x scripts/globus-admin scripts/*.py
```

---

Next: [Quick Start Guide](quickstart.md)
