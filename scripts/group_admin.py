#!/usr/bin/env python3
"""
Comprehensive Globus group administration tool.
Provides easy-to-use commands for common group management tasks.
"""

import argparse
import subprocess
import sys
import json
from datetime import datetime

def run_globus_command(cmd, output_format="json"):
    """Run a globus CLI command and return the result."""
    try:
        full_cmd = f"globus --format {output_format} {cmd}"
        result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            if output_format == "json":
                try:
                    return True, json.loads(result.stdout), ""
                except json.JSONDecodeError:
                    return True, result.stdout, ""
            else:
                return True, result.stdout, ""
        return False, "", result.stderr
    except Exception as e:
        return False, "", str(e)

def list_groups():
    """List all groups the user belongs to."""
    success, data, error = run_globus_command("group list")
    if not success:
        print(f"Error listing groups: {error}")
        return
    
    if isinstance(data, list):
        print(f"Found {len(data)} group(s):")
        for group in data:
            print(f"  • {group.get('name', 'N/A')} (ID: {group.get('id', 'N/A')})")
            print(f"    Role: {group.get('my_role', 'N/A')}")
    else:
        print(data)

def show_group_members(group_id):
    """Show all members of a group."""
    success, data, error = run_globus_command(f"group member list {group_id}")
    if not success:
        print(f"Error listing group members: {error}")
        return
    
    if isinstance(data, list):
        print(f"Group {group_id} has {len(data)} member(s):")
        for member in data:
            status = member.get('status', 'N/A')
            role = member.get('role', 'N/A')
            username = member.get('username', 'N/A')
            print(f"  • {username} - {role} ({status})")
    else:
        print(data)

def show_group_info(group_id):
    """Show detailed information about a group."""
    success, data, error = run_globus_command(f"group show {group_id}")
    if not success:
        print(f"Error getting group info: {error}")
        return
    
    if isinstance(data, dict):
        print(f"Group Information:")
        print(f"  Name: {data.get('name', 'N/A')}")
        print(f"  ID: {data.get('id', 'N/A')}")
        print(f"  Description: {data.get('description', 'N/A')}")
        print(f"  Visibility: {data.get('visibility', 'N/A')}")
        print(f"  Join Policy: {data.get('join_policy', 'N/A')}")
    else:
        print(data)

def bulk_remove_users(group_id, users):
    """Remove multiple users from a group."""
    print(f"Removing {len(users)} user(s) from group {group_id}")
    
    successful = 0
    failed = 0
    
    for user in users:
        success, stdout, stderr = run_globus_command(f"group member remove {group_id} {user}", "text")
        
        if success:
            successful += 1
            print(f"  ✓ Removed: {user}")
        else:
            failed += 1
            print(f"  ✗ Failed to remove: {user} - {stderr}")
    
    print(f"Summary: {successful} removed, {failed} failed")

def export_group_data(group_id, output_file=None):
    """Export group information and member list to JSON."""
    # Get group info
    success_info, group_info, error_info = run_globus_command(f"group show {group_id}")
    if not success_info:
        print(f"Error getting group info: {error_info}")
        return
    
    # Get member list
    success_members, members, error_members = run_globus_command(f"group member list {group_id}")
    if not success_members:
        print(f"Error getting members: {error_members}")
        return
    
    export_data = {
        "exported_at": datetime.now().isoformat(),
        "group_info": group_info,
        "members": members
    }
    
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2)
        print(f"Group data exported to {output_file}")
    else:
        print(json.dumps(export_data, indent=2))

def main():
    parser = argparse.ArgumentParser(description='Globus Group Administration Tool')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List groups
    subparsers.add_parser('list', help='List all groups you belong to')
    
    # Show group info
    info_parser = subparsers.add_parser('info', help='Show group information')
    info_parser.add_argument('group_id', help='Group ID')
    
    # Show group members
    members_parser = subparsers.add_parser('members', help='Show group members')
    members_parser.add_argument('group_id', help='Group ID')
    
    # Bulk remove users
    remove_parser = subparsers.add_parser('bulk-remove', help='Remove multiple users from group')
    remove_parser.add_argument('group_id', help='Group ID')
    remove_parser.add_argument('--users-file', '-f', help='File containing list of users to remove')
    remove_parser.add_argument('--users', '-u', nargs='+', help='Space-separated list of users to remove')
    
    # Export group data
    export_parser = subparsers.add_parser('export', help='Export group data to JSON')
    export_parser.add_argument('group_id', help='Group ID')
    export_parser.add_argument('--output', '-o', help='Output file (default: stdout)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == 'list':
        list_groups()
    elif args.command == 'info':
        show_group_info(args.group_id)
    elif args.command == 'members':
        show_group_members(args.group_id)
    elif args.command == 'bulk-remove':
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
            print("Error: No users specified")
            sys.exit(1)
        
        bulk_remove_users(args.group_id, users)
    elif args.command == 'export':
        export_group_data(args.group_id, args.output)

if __name__ == "__main__":
    main()