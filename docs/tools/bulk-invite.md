# Bulk Invite Tool

The bulk invite script allows you to invite multiple users to a Globus group in a single operation.

## Basic Usage

```bash
./scripts/bulk_invite.py GROUP_ID [OPTIONS]
```

## Input Methods

### From File

Create a users file with one email address per line:

```bash
# users.txt 
# comment lines skipped
# empty lines ignored
unikey1@sydney.edu.au
unikey2@sydney.edu.au
unikey3@sydney.edu.au
```

Then run:
```bash
./scripts/bulk_invite.py abc123-group-id --users-file users.txt
```

### From Command Line

```bash
./scripts/bulk_invite.py abc123-group-id \
  --users unikey1@sydney.edu.au unikey2@sydney.edu.au unikey3@sydney.edu.au
```

## Options Reference

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--users-file FILE` | `-f` | File containing user list | None |
| `--users USER [USER...]` | `-u` | Space-separated users | None |
| `--role ROLE` | `-r` | Role to assign | `member` |
| `--provision` | `-p` | Provision identities if missing | False |
| `--dry-run` | `-d` | Show actions without executing | False |
| `--verbose` | `-v` | Detailed output | False |

## Role Types

| Role | Permissions | Use Case |
|------|-------------|----------|
| `member` | Basic group access | Regular users |
| `manager` | Can manage members | Team leads |
| `admin` | Full group control | Administrators |
