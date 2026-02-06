# Quick Start

Get up and running with the Globus administrative tools in minutes.

## 1. Authentication

First, authenticate with Globus using your institutional credentials:

```bash
globus login
```

This will:

- Open a browser window
- Redirect to University of Sydney/Okta login
- Generate authentication tokens
- Store credentials locally

## 2. Verify Login

Check your authentication status:

```bash
globus whoami
```

Expected output:
```
gsam0138@sydney.edu.au
```

## 3. Explore Your Groups

List all groups you have access to:

```bash
./scripts/globus-admin list
```

Example output:
```
Found 3 group(s):
  • University of Sydney (ID: d3f8880c-3693-11f0-9974-0affcae2cfad)
    Role: member
  • USYD RDS Endpoint Activity Monitors (ID: aba55772-a8a2-11f0-831a-0affcae2cfad)
    Role: manager
  • AARNet Subscription Managers (ID: 35c91839-46bc-11f0-b5c4-0e8dfaec7d97)
    Role: admin
```

## 4. First Bulk Invitation

Let's invite users to a group:

### Create a Users File

```bash
# Create a file with email addresses
cat > my_team.txt << EOF
user1@example.com
user2@university.edu
user3@company.org
EOF
```

### Test with Dry Run

```bash
./scripts/globus-admin invite YOUR_GROUP_ID \
  --users-file my_team.txt \
  --role member \
  --dry-run \
  --verbose
```

### Execute the Invitation

If the dry run looks good:

```bash
./scripts/globus-admin invite YOUR_GROUP_ID \
  --users-file my_team.txt \
  --role member
```

## 5. Group Management Tasks

### Show Group Details

```bash
./scripts/globus-admin info YOUR_GROUP_ID
```

### List Group Members

```bash
./scripts/globus-admin members YOUR_GROUP_ID
```

### Export Group Data

```bash
./scripts/group_admin.py export YOUR_GROUP_ID --output backup.json
```

## Common Workflows

### Team Onboarding

```bash
# 1. Create team file
echo "newuser@company.com" >> new_team.txt

# 2. Test invitation
./scripts/globus-admin invite GROUP_ID --users-file new_team.txt --dry-run

# 3. Execute with identity provisioning
./scripts/globus-admin invite GROUP_ID --users-file new_team.txt --provision
```

### Group Audit

```bash
# Export current state
./scripts/group_admin.py export GROUP_ID --output audit_$(date +%Y%m%d).json

# Review members
./scripts/globus-admin members GROUP_ID

# Check group settings
./scripts/globus-admin info GROUP_ID
```

## Help & Documentation

Get help on any command:

```bash
./scripts/globus-admin help
./scripts/bulk_invite.py --help
./scripts/group_admin.py --help
```
