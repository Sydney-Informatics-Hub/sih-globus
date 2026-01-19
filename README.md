# SIH Globus toolkit 

## Resources 

- [CLI reference docs](https://docs.globus.org/cli/reference/)
- [Installation](https://docs.globus.org/cli/#installation)
- [Enable tab completion](https://docs.globus.org/cli/#tab-completion)

## Administrative Tools

This repository contains wrapper scripts to simplify common Globus group administration tasks:

### Quick Start

1. **Login to Globus:**
```bash
globus login
```

2. **Use the admin helper:**
```bash
# List all your groups
./scripts/globus-admin list

# Show group members
./scripts/globus-admin members GROUP_ID

# Bulk invite users
./scripts/globus-admin invite GROUP_ID --users-file scripts/users.txt --role member
```

3. **Run the demo to see examples:**
```bash
./scripts/demo.py
```

### Available Scripts

- **`scripts/globus-admin`** - Main administrative helper with easy commands
- **`scripts/bulk_invite.py`** - Bulk invite users to groups
- **`scripts/group_admin.py`** - Comprehensive group management
- **`scripts/demo.py`** - Demo and testing script
- **`scripts/users.txt`** - Example users file template

See [scripts/README.md](scripts/README.md) for detailed documentation and examples.

## Manual Commands

For direct CLI usage, manage invitations to a Globus group: 

```bash
globus group invite --help
globus group member invite --help
```
