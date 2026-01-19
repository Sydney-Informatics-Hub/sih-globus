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

## Setup

1. Make scripts executable:
```bash
chmod +x bulk_invite.py group_admin.py
```

2. Create a users file:
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

## Tips

- Always use `--dry-run` first to verify what will happen
- Keep backups of group data before making bulk changes
- Use meaningful filenames for user lists (e.g., `new_students_2026.txt`)
- The scripts handle errors gracefully and provide summaries
- Use `--verbose` for detailed output during operations