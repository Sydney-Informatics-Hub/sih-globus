# Troubleshooting Guide

## Common Issues

### Authentication Problems

**Globus Login Fails**
```bash
# Check session status
globus session show

# Re-authenticate
globus logout
globus login
```

**Token Expired**
```bash
globus session update
```

### Script Errors

**Permission Denied**
```bash
chmod +x scripts/*.py scripts/globus-admin
```

**Python Module Not Found**
```bash
# Ensure you're in the right environment
which python
pip list | grep globus
```

### Group Management Issues

**User Already Exists**
- Check current group membership first
- Use bulk-remove then re-invite with new role

**Identity Not Found** 
- Verify email addresses
- Use --provision flag for external users
- Check institutional identity policies

## Getting Help

1. Use `--help` flag on any script
2. Check verbose output with `--verbose`
3. Review the [Common Workflows](../workflows/common-tasks.md)
4. Submit issues on GitHub

---

*This guide will be expanded as more issues are identified.*