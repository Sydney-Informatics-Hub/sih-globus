#!/usr/bin/env python3
"""
Bulk invite users to a Globus group from a file or list.
Simplifies the process of inviting multiple users at once.
"""

import argparse
import subprocess
import sys
from pathlib import Path
import json

def run_globus_command(cmd):
    """Run a globus CLI command and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def invite_user(group_id, identity, role="member", provision=False):
    """Invite a single user to the group."""
    cmd = f"globus group member invite --role {role}"
    if provision:
        cmd += " --provision-identity"
    cmd += f" {group_id} {identity}"
    
    success, stdout, stderr = run_globus_command(cmd)
    return success, stdout, stderr

def main():
    parser = argparse.ArgumentParser(description='Bulk invite users to a Globus group')
    parser.add_argument('group_id', help='Globus group ID')
    parser.add_argument('--users-file', '-f', help='File containing list of users (one per line)')
    parser.add_argument('--users', '-u', nargs='+', help='Space-separated list of usernames/IDs')
    parser.add_argument('--role', '-r', choices=['member', 'manager', 'admin'], 
                       default='member', help='Role for invited users')
    parser.add_argument('--provision', '-p', action='store_true', 
                       help='Provision identities if they don\'t exist')
    parser.add_argument('--dry-run', '-d', action='store_true', 
                       help='Show what would be done without executing')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Collect users from file or command line
    users = []
    if args.users_file:
        try:
            with open(args.users_file, 'r') as f:
                users.extend([line.strip() for line in f if line.strip()])
        except FileNotFoundError:
            print(f"Error: File {args.users_file} not found")
            sys.exit(1)
    
    if args.users:
        users.extend(args.users)
    
    if not users:
        print("Error: No users specified. Use --users-file or --users")
        sys.exit(1)
    
    print(f"Inviting {len(users)} user(s) to group {args.group_id} with role '{args.role}'")
    if args.dry_run:
        print("DRY RUN - No actual invitations will be sent")
    
    successful = 0
    failed = 0
    
    for user in users:
        if args.verbose or args.dry_run:
            print(f"  {'[DRY RUN] ' if args.dry_run else ''}Inviting: {user}")
        
        if not args.dry_run:
            success, stdout, stderr = invite_user(args.group_id, user, args.role, args.provision)
            
            if success:
                successful += 1
                if args.verbose:
                    print(f"    ✓ Success: {user}")
            else:
                failed += 1
                print(f"    ✗ Failed: {user} - {stderr.strip()}")
        else:
            successful += 1
    
    print(f"\nSummary: {successful} successful, {failed} failed")
    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()