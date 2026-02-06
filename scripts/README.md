# Globus Group Administration Scripts

This directory contains wrapper scripts to simplify common Globus group administration tasks.

## Scripts

### 1. `bulk_invite.py` - Bulk User Invitations

Invite multiple users to a Globus group at once.

**Usage:**
```bash
# Invite users from a file
python3 bulk_invite.py GROUP_ID --users-file users.txt --role member

# Invite specific users
python3 bulk_invite.py GROUP_ID --users user1@example.com user2@institution.edu --role manager

# Dry run to see what would happen
python3 bulk_invite.py GROUP_ID --users-file users.txt --dry-run --verbose

# Provision identities if they don't exist
python3 bulk_invite.py GROUP_ID --users-file users.txt --provision
```

**Options:**
- `--users-file, -f`: File containing usernames/emails (one per line)
- `--users, -u`: Space-separated list of usernames/emails
- `--role, -r`: Role to assign (member, manager, admin) [default: member]
- `--provision, -p`: Provision identities if they don't exist
- `--dry-run, -d`: Show what would be done without executing
- `--verbose, -v`: Verbose output

### 2. `group_admin.py` - Comprehensive Group Management

Multi-purpose tool for group administration tasks.

**Usage:**
```bash
# List all groups you belong to
python3 group_admin.py list

# Show detailed group information
python3 group_admin.py info GROUP_ID

# Show all group members
python3 group_admin.py members GROUP_ID

# Bulk remove users from a group
python3 group_admin.py bulk-remove GROUP_ID --users-file remove_users.txt
python3 group_admin.py bulk-remove GROUP_ID --users user1 user2 user3

# Export group data to JSON
python3 group_admin.py export GROUP_ID --output group_backup.json
```

### 3. `monitor_transfers.py` - Transfer Monitoring & Analysis

Monitor and analyze Globus transfer tasks with comprehensive CSV output for reporting and analysis.

**Usage:**
```bash
# Export all transfers to CSV file
python3 monitor_transfers.py > transfers.csv

# Monitor transfers for a specific collection
python3 monitor_transfers.py --collection ddb59aef-6d04-11e5-ba46-22000b92c6ec

# Show only active transfers
python3 monitor_transfers.py --status ACTIVE

# Show only failed transfers with verbose details
python3 monitor_transfers.py --status FAILED --verbose

# Monitor by task type (transfers vs deletions)
python3 monitor_transfers.py --type TRANSFER
python3 monitor_transfers.py --type DELETE

# Filter by time range
python3 monitor_transfers.py --requested-after 2026-01-01
python3 monitor_transfers.py --requested-before 2026-02-01

# Filter by label pattern
python3 monitor_transfers.py --label "backup*"

# Real-time monitoring with auto-refresh
python3 monitor_transfers.py --watch --interval 30

# Use endpoint IDs instead of names for faster performance
python3 monitor_transfers.py --no-names
```

**CSV Output Format:**
The script outputs comprehensive transfer data in CSV format with these columns:
- `task_id`: Unique transfer task identifier
- `status`: ACTIVE, SUCCEEDED, FAILED, or INACTIVE
- `type`: TRANSFER or DELETE
- `initiated_by`: Name of person who started the transfer
- `owner_email`: Email address of the initiator
- `label`: User-provided task label
- `request_time`: When transfer was requested (YYYY-MM-DD HH:MM:SS UTC)
- `completion_time`: When transfer completed (if finished)
- `source_endpoint`: Source collection name or ID
- `dest_endpoint`: Destination collection name or ID
- `files_total`: Total number of files
- `files_transferred`: Files successfully transferred
- `bytes_total`: Total data size in bytes
- `bytes_transferred`: Bytes successfully transferred
- `speed_mbps`: Transfer speed in megabits per second
- `faults`: Number of faults/errors encountered
- `retries`: Number of subtasks currently retrying
- `failed_subtasks`: Number of failed subtasks
- `succeeded_subtasks`: Number of successful subtasks

**Options:**
- `--collection, -c`: Collection/endpoint UUID to monitor
- `--status, -s`: Filter by status (ACTIVE, INACTIVE, SUCCEEDED, FAILED) - can use multiple times
- `--type, -t`: Filter by task type (TRANSFER, DELETE)
- `--label`: Filter by task label pattern
- `--requested-after`: Show tasks requested after this time (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
- `--requested-before`: Show tasks requested before this time (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
- `--limit, -l`: Maximum number of tasks to retrieve (default: 1000)
- `--verbose, -v`: Include additional technical details
- `--watch, -w`: Continuously refresh the display
- `--interval, -i`: Refresh interval in seconds for watch mode (default: 30)
- `--no-names`: Show endpoint IDs instead of names for faster performance

## Setup

1. Make scripts executable:
```bash
chmod +x bulk_invite.py group_admin.py monitor_transfers.py
```

2. Create a users file for bulk operations:
```bash
cp users.txt my_users.txt
# Edit my_users.txt with actual usernames/emails
```

3. Ensure you're logged into Globus:
```bash
globus login
```

## Examples

### Scenario 1: Onboarding New Team Members
```bash
# Create users.txt with new team member emails
echo "newuser1@company.com" >> new_team.txt
echo "newuser2@company.com" >> new_team.txt

# Invite them as members with identity provisioning
python3 bulk_invite.py abc123-group-id --users-file new_team.txt --role member --provision
```

### Scenario 2: Promoting Users to Managers
```bash
# Create a file with existing members to promote
python3 group_admin.py members abc123-group-id  # Check current members
echo "experienced.user@company.com" >> promote.txt

# Remove them first, then re-add as managers
python3 group_admin.py bulk-remove abc123-group-id --users-file promote.txt
python3 bulk_invite.py abc123-group-id --users-file promote.txt --role manager
```

### Scenario 3: Group Audit and Backup
```bash
# Export current group state
python3 group_admin.py export abc123-group-id --output backup_$(date +%Y%m%d).json

# Show current members
python3 group_admin.py members abc123-group-id
```

### Scenario 4: Transfer Monitoring and Analysis
```bash
# Export all recent transfers for analysis
python3 monitor_transfers.py > all_transfers_$(date +%Y%m%d).csv

# Monitor active transfers in real-time during a large data migration
python3 monitor_transfers.py --status ACTIVE --watch --interval 5

# Generate a report of failed transfers for troubleshooting
python3 monitor_transfers.py --status FAILED --limit 100 > failed_transfers.csv

# Monitor transfers for a specific research collection
python3 monitor_transfers.py --collection ddb59aef-6d04-11e5-ba46-22000b92c6ec > collection_transfers.csv

# Check transfer activity from the last week
python3 monitor_transfers.py --requested-after $(date -d '7 days ago' +%Y-%m-%d) > weekly_transfers.csv

# Monitor deletion tasks specifically
python3 monitor_transfers.py --type DELETE --verbose

# Track transfers with specific labels (e.g., backup operations)
python3 monitor_transfers.py --label "backup*" --status ACTIVE --status SUCCEEDED
```

### Scenario 5: Data Analysis and Reporting
```bash
# Create comprehensive transfer report for leadership
python3 monitor_transfers.py --limit 5000 > monthly_transfer_report.csv

# Import into spreadsheet for analysis:
# - Open monthly_transfer_report.csv in Excel/Google Sheets
# - Create pivot tables for transfer success rates by user
# - Analyze transfer volumes and speeds over time
# - Identify frequently failing endpoints

# Monitor specific user's transfer activity
python3 monitor_transfers.py | grep "user@institution.edu"

# Check for any stuck or long-running transfers
python3 monitor_transfers.py --status ACTIVE --requested-before $(date -d '1 day ago' +%Y-%m-%d)
```

## Tips

- Always use `--dry-run` first to verify what will happen
- Keep backups of group data before making bulk changes
- Use meaningful filenames for user lists (e.g., `new_students_2026.txt`)
- The scripts handle errors gracefully and provide summaries
- Use `--verbose` for detailed output during operations
- Export transfer data to CSV for analysis in spreadsheets or data analysis tools
- Use `--watch` mode for real-time monitoring during active data migrations
- The `--no-names` option improves performance when monitoring large numbers of transfers
- Combine multiple status filters (e.g., `--status ACTIVE --status FAILED`) for custom views
- Use time filters to generate reports for specific periods