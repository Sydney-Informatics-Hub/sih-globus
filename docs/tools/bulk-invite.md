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
uinkey1@sydney.edu.au
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
  --users user1@example.com user2@university.edu user3@company.org
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

## Examples

### New Team Onboarding

```bash
# Create team file
cat > new_hires_q1.txt << EOF
alice.smith@company.com
bob.jones@company.com
carol.brown@company.com
EOF

# Test first
./scripts/bulk_invite.py team-group-id \
  --users-file new_hires_q1.txt \
  --role member \
  --dry-run \
  --verbose

# Execute if looks good
./scripts/bulk_invite.py team-group-id \
  --users-file new_hires_q1.txt \
  --role member \
  --provision
```

### Promote Existing Members

```bash
# Promote specific users to managers
./scripts/bulk_invite.py project-group-id \
  --users senior.dev@company.com team.lead@company.com \
  --role manager
```

### External Collaborators

```bash
# Add external users with identity provisioning
./scripts/bulk_invite.py collaboration-group-id \
  --users external1@partner.org external2@university.edu \
  --role member \
  --provision
```

## Output Examples

### Successful Operation

```
Inviting 3 user(s) to group abc123-group-id with role 'member'
  ✓ Success: user1@example.com
  ✓ Success: user2@university.edu  
  ✓ Success: user3@company.org

Summary: 3 successful, 0 failed
```

### With Errors

```
Inviting 3 user(s) to group abc123-group-id with role 'member'
  ✓ Success: user1@example.com
  ✗ Failed: baduser@nowhere.com - Identity not found
  ✓ Success: user3@company.org

Summary: 2 successful, 1 failed
```

### Dry Run Mode

```
Inviting 3 user(s) to group abc123-group-id with role 'member'
DRY RUN - No actual invitations will be sent
  [DRY RUN] Inviting: user1@example.com
  [DRY RUN] Inviting: user2@university.edu
  [DRY RUN] Inviting: user3@company.org

Summary: 3 successful, 0 failed
```

## Error Handling

### Common Errors

**Identity Not Found**
```
✗ Failed: user@domain.com - Identity not found
```
*Solution*: Use `--provision` flag or verify email address

**Insufficient Permissions**
```
✗ Failed: HTTP 403 - Insufficient permissions
```
*Solution*: Verify you have admin/manager role in the group

**Already a Member**
```
✗ Failed: user@domain.com - Already a member
```
*Solution*: Remove from error list or use group management tools

### Best Practices

!!! tip "Safety First"
    - Always use `--dry-run` before actual execution
    - Start with small batches to test permissions
    - Keep backups of user lists

!!! info "File Management"
    - Use descriptive filenames: `spring2026_students.txt`
    - Include dates in bulk operations
    - Comment your user files for context

!!! warning "Identity Provisioning"
    - Only use `--provision` when necessary
    - Verify external email addresses
    - Understand your organization's identity policies

## Integration with Other Tools

### With Group Admin

```bash
# Export current members first
./scripts/group_admin.py export GROUP_ID --output before_invite.json

# Bulk invite
./scripts/bulk_invite.py GROUP_ID --users-file new_users.txt --role member

# Verify changes
./scripts/group_admin.py members GROUP_ID
```

### With CI/CD

```yaml
# Example GitHub Action
- name: Invite new team members
  run: |
    ./scripts/bulk_invite.py ${{ secrets.GROUP_ID }} \
      --users-file .github/new_members.txt \
      --role member \
      --provision
```

---

**Related:**
- [Group Management](group-admin.md)
- [Common Workflows](../workflows/common-tasks.md)
- [Troubleshooting](../reference/troubleshooting.md)