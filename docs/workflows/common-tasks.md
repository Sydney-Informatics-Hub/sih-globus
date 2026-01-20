# Common Workflows

This guide covers typical administrative tasks and how to accomplish them efficiently.

## Team Onboarding

### Scenario: Adding New Team Members

**Goal**: Invite multiple new employees to your project group.

**Steps**:

1. **Prepare user list**:
   ```bash
   cat > new_team_q1_2026.txt << EOF
   alice.smith@company.com
   bob.jones@company.com
   carol.brown@company.com
   EOF
   ```

2. **Test the invitation**:
   ```bash
   ./scripts/globus-admin invite PROJECT_GROUP_ID \
     --users-file new_team_q1_2026.txt \
     --role member \
     --dry-run \
     --verbose
   ```

3. **Execute the invitation**:
   ```bash
   ./scripts/globus-admin invite PROJECT_GROUP_ID \
     --users-file new_team_q1_2026.txt \
     --role member \
     --provision
   ```

4. **Verify the results**:
   ```bash
   ./scripts/globus-admin members PROJECT_GROUP_ID
   ```

## Group Maintenance

### Scenario: Regular Group Audit

**Goal**: Review group membership and export data for compliance.

**Steps**:

1. **Export current state**:
   ```bash
   DATE=$(date +%Y%m%d)
   ./scripts/group_admin.py export GROUP_ID --output "audit_${DATE}.json"
   ```

2. **Review group information**:
   ```bash
   ./scripts/globus-admin info GROUP_ID
   ./scripts/globus-admin members GROUP_ID
   ```

3. **Generate member list**:
   ```bash
   ./scripts/group_admin.py members GROUP_ID | tee "members_${DATE}.txt"
   ```

### Scenario: Removing Inactive Users

**Goal**: Clean up group membership by removing users who are no longer active.

**Steps**:

1. **Identify users to remove** (manual process or from HR system):
   ```bash
   cat > inactive_users.txt << EOF
   former.employee@company.com
   contractor.finished@external.com
   EOF
   ```

2. **Remove users**:
   ```bash
   ./scripts/group_admin.py bulk-remove GROUP_ID --users-file inactive_users.txt
   ```

3. **Verify removal**:
   ```bash
   ./scripts/globus-admin members GROUP_ID
   ```

## Role Management

### Scenario: Promoting Users

**Goal**: Promote existing members to managers or admins.

**Current State**: Users are members  
**Desired State**: Users are managers

**Steps**:

1. **List current members**:
   ```bash
   ./scripts/globus-admin members GROUP_ID > current_members.txt
   ```

2. **Identify users to promote**:
   ```bash
   cat > promote_to_manager.txt << EOF
   senior.dev@company.com
   team.lead@company.com
   EOF
   ```

3. **Remove them first** (Globus requires removal before role change):
   ```bash
   ./scripts/group_admin.py bulk-remove GROUP_ID --users-file promote_to_manager.txt
   ```

4. **Re-add with new role**:
   ```bash
   ./scripts/globus-admin invite GROUP_ID \
     --users-file promote_to_manager.txt \
     --role manager
   ```

## External Collaboration

### Scenario: Adding External Partners

**Goal**: Add collaborators from other institutions.

**Considerations**:
- External users may not have existing Globus identities
- Need identity provisioning
- Different institutional authentication

**Steps**:

1. **Prepare external user list**:
   ```bash
   cat > external_collaborators.txt << EOF
   # University partners
   prof.smith@partner-university.edu
   researcher.jones@research-institute.org
   
   # Industry partners
   contact@partner-company.com
   EOF
   ```

2. **Invite with identity provisioning**:
   ```bash
   ./scripts/globus-admin invite COLLABORATION_GROUP_ID \
     --users-file external_collaborators.txt \
     --role member \
     --provision \
     --verbose
   ```

3. **Follow up on failures** (manual verification may be needed):
   - Check email addresses for typos
   - Contact users to ensure they complete registration
   - Verify institutional access policies

## Bulk Operations

### Scenario: Large User Import

**Goal**: Import 100+ users efficiently and safely.

**Strategy**: Break into smaller batches to manage errors.

**Steps**:

1. **Split large user list**:
   ```bash
   split -l 20 all_users.txt batch_
   # Creates: batch_aa, batch_ab, batch_ac, etc.
   ```

2. **Process each batch**:
   ```bash
   for batch in batch_*; do
     echo "Processing $batch..."
     ./scripts/globus-admin invite GROUP_ID \
       --users-file "$batch" \
       --role member \
       --provision \
       --verbose
     sleep 2  # Brief pause between batches
   done
   ```

3. **Collect results**:
   ```bash
   ./scripts/globus-admin members GROUP_ID > final_members.txt
   wc -l final_members.txt  # Count total members
   ```

## Automation Integration

### Scenario: CI/CD Integration

**Goal**: Automate group management with external systems.

**GitHub Actions Example**:
```yaml
name: Update Group Membership
on:
  push:
    paths: ['team-members.txt']

jobs:
  update-group:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Install Globus CLI
      run: pipx install globus-cli
    - name: Authenticate
      run: echo "${{ secrets.GLOBUS_TOKEN }}" | globus login --stdin
    - name: Update group
      run: |
        ./scripts/globus-admin invite ${{ secrets.GROUP_ID }} \
          --users-file team-members.txt \
          --role member
```

### Scenario: Scheduled Maintenance

**Goal**: Regular group cleanup via cron job.

**Cron Script** (`/scripts/maintenance.sh`):
```bash
#!/bin/bash
DATE=$(date +%Y%m%d)
GROUP_ID="your-group-id"

# Export current state
./scripts/group_admin.py export $GROUP_ID --output "backup_${DATE}.json"

# Run any scheduled updates
# (could read from HR system, LDAP, etc.)

# Log results
echo "Maintenance completed: $DATE" >> maintenance.log
```

**Crontab Entry**:
```bash
# Run weekly maintenance on Sundays at 2 AM
0 2 * * 0 /path/to/sih-globus/scripts/maintenance.sh
```

## Error Recovery

### Common Issues and Solutions

**Authentication Expired**:
```bash
globus session show  # Check status
globus login         # Re-authenticate if needed
```

**Partial Failures in Bulk Operations**:
1. Check the error messages for patterns
2. Extract successful users vs. failed users
3. Retry failed users with corrections
4. Use `--verbose` to get detailed error information

**Identity Provisioning Issues**:
1. Verify email addresses are correct
2. Check if users need to complete Globus registration
3. Ensure institutional policies allow external identities

---

**Related Documentation**:
- [Bulk Invite Details](../tools/bulk-invite.md)
- [Group Management](../tools/group-admin.md)
- [Troubleshooting Guide](../reference/troubleshooting.md)