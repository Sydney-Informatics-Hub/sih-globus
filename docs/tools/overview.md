# Administrative Tools Overview

Scripts here are to be used by administrators for managing groups, collections, monitoring transfers. 

## Main Interface

The primary entry point for all administrative operations:

```bash
./scripts/globus-admin <command> [options]
```

**Available Commands:**

| Command | Purpose | Example |
|---------|---------|---------|
| `list` | Show all your groups | `./scripts/globus-admin list` |
| `info` | Display group details | `./scripts/globus-admin info GROUP_ID` |
| `members` | List group members | `./scripts/globus-admin members GROUP_ID` |
| `invite` | Bulk invite users | `./scripts/globus-admin invite GROUP_ID --users-file users.txt` |
| `help` | Show usage information | `./scripts/globus-admin help` |

## Transfer Monitoring Tool (`monitor_transfers.py`)

**Purpose**: Export transfer data to CSV format with comprehensive filtering options.

**Key Features**:
- Export all transfer data to CSV format
- Filter by status, collection, time range, and labels
- Real-time monitoring with watch mode
- Complete transfer details including retry counts and owner information

**Usage Examples**:

| Purpose | Example |
|---------|---------|
| Export all transfers to CSV | `python3 scripts/monitor_transfers.py > transfers.csv` |
| Real-time monitoring | `python3 scripts/monitor_transfers.py --watch --interval 30` |
| Filter by status | `python3 scripts/monitor_transfers.py --status FAILED` |
| Filter by collection | `python3 scripts/monitor_transfers.py --collection UUID` |
| Limit results | `python3 scripts/monitor_transfers.py --limit 50` |

## Bulk invite (`bulk_invite.py`)

**Purpose**: Invite multiple users to a Globus group simultaneously.

**Key Features**:
- Read users from file or command line
- Support for different roles (member, manager, admin)
- Dry-run mode for testing
- Identity provisioning
- Detailed error reporting

**Usage Examples**:
```bash
# From file
./scripts/bulk_invite.py GROUP_ID --users-file team.txt --role member

# From command line
./scripts/bulk_invite.py GROUP_ID --users user1@domain.com user2@domain.com --role manager

# With dry run
./scripts/bulk_invite.py GROUP_ID --users-file team.txt --dry-run --verbose
```

## Group Administration (`group_admin.py`)

**Purpose**: Comprehensive group management operations.

**Key Features**:
- List and inspect groups
- Member management
- Data export for backups
- Bulk removal operations

**Usage Examples**:
```bash
# List all groups
./scripts/group_admin.py list

# Export group data
./scripts/group_admin.py export GROUP_ID --output backup.json

# Bulk remove users
./scripts/group_admin.py bulk-remove GROUP_ID --users user1 user2
```

## Transfer Monitoring (`monitor_transfers.py`)

**Purpose**: Monitor, analyze, and report on Globus transfer activities with comprehensive CSV output for data analysis.

**Key Features**:
- Real-time transfer monitoring
- CSV export for analysis and reporting
- Comprehensive transfer statistics (owner, timing, file counts, error rates)
- Filtering by status, collection, time range, and labels
- Performance optimization with caching
- Support for both transfers and deletion tasks

**Usage Examples**:
```bash
# Export all transfers to CSV for analysis
./scripts/monitor_transfers.py > transfer_report.csv

# Monitor specific collection in real-time
./scripts/monitor_transfers.py --collection COLLECTION_ID --watch

# Generate failed transfer report
./scripts/monitor_transfers.py --status FAILED > failed_transfers.csv

# Track transfers from last week
./scripts/monitor_transfers.py --requested-after $(date -d '7 days ago' +%Y-%m-%d)

# Monitor deletion tasks
./scripts/monitor_transfers.py --type DELETE --verbose

# Fast monitoring without endpoint name resolution
./scripts/monitor_transfers.py --no-names --limit 500
```

**CSV Output Columns**:
- Transfer identification: `task_id`, `status`, `type`, `label`
- User information: `initiated_by`, `owner_email` 
- Timing: `request_time`, `completion_time`
- Endpoints: `source_endpoint`, `dest_endpoint`
- Progress: `files_total`, `files_transferred`, `bytes_total`, `bytes_transferred`
- Performance: `speed_mbps`
- Error tracking: `faults`, `retries`, `failed_subtasks`, `succeeded_subtasks`

## Common Options

All scripts support these common patterns:

### Input Methods
- **File-based**: `--users-file users.txt`
- **Command-line**: `--users user1 user2 user3`

### Safety Features
- **Dry-run**: `--dry-run` (show what would happen)
- **Verbose**: `--verbose` (detailed output)
- **Validation**: Syntax and permission checking

### Output Formats
- **Human-readable**: Default text output
- **JSON**: `--format json` (where supported)
- **Export**: Structured data files

## Error Handling

The scripts provide some error handling. You will see the following error commands: 

### Authentication Errors
```bash
MissingLoginError: Please run 'globus login'
```

### Permission Errors
```bash
HTTP 403: Insufficient permissions for group operation
```

### User Not Found
```bash
✗ Failed: user@domain.com - Identity not found
```

### Network Issues
```bash
Connection timeout - please check network connectivity
```