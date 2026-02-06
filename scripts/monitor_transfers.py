#!/usr/bin/env python3
"""
Monitor transfers to and from a Globus collection.
Shows active and recent transfer tasks with detailed status information.
"""

import argparse
import subprocess
import sys
import json
import time
import csv
import io
from datetime import datetime, timedelta
from pathlib import Path

def run_globus_command(cmd):
    """Run a globus CLI command and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def get_transfer_tasks(collection_id=None, status_filter=None, task_type=None, limit=1000, 
                      requested_after=None, requested_before=None, label_filter=None):
    """Get transfer tasks, optionally filtered by various parameters."""
    cmd = f"globus task list --format json --limit {limit}"
    
    if status_filter:
        # Handle multiple status filters
        if isinstance(status_filter, list):
            for status in status_filter:
                cmd += f" --filter-status {status}"
        else:
            cmd += f" --filter-status {status_filter}"
    
    if task_type:
        cmd += f" --filter-type {task_type}"
    
    if requested_after:
        cmd += f" --filter-requested-after '{requested_after}'"
    
    if requested_before:
        cmd += f" --filter-requested-before '{requested_before}'"
    
    if label_filter:
        cmd += f" --filter-label '{label_filter}'"
    
    success, stdout, stderr = run_globus_command(cmd)
    if not success:
        print(f"Error getting transfer tasks: {stderr}")
        return []
    
    try:
        data = json.loads(stdout)
        # Globus CLI returns data in a "DATA" field
        tasks = data.get("DATA", []) if isinstance(data, dict) else data
        
        # Debug: Check what we're getting
        if tasks and not isinstance(tasks[0], dict):
            print(f"Warning: Expected task dictionaries but got {type(tasks[0])}: {tasks[0]}")
            return []
        
        if collection_id:
            # Filter tasks involving the specified collection
            filtered_tasks = []
            for task in tasks:
                if (task.get('source_endpoint_id') == collection_id or 
                    task.get('destination_endpoint_id') == collection_id):
                    filtered_tasks.append(task)
            return filtered_tasks
        return tasks
    except json.JSONDecodeError as e:
        print(f"Error parsing transfer task data: {e}")
        print(f"Raw output: {stdout}")
        return []


def get_user_info(user_id, cache):
    """Get cached user information."""
    if user_id not in cache:
        cmd = f"globus get-identities --format json {user_id}"
        success, stdout, stderr = run_globus_command(cmd)
        if success:
            try:
                data = json.loads(stdout)
                identities = data.get("identities", [])
                if identities:
                    identity = identities[0]
                    cache[user_id] = {
                        "name": identity.get("name", ""),
                        "username": identity.get("username", user_id),
                        "email": identity.get("email", "")
                    }
                else:
                    cache[user_id] = {"name": "", "username": user_id, "email": ""}
            except json.JSONDecodeError:
                cache[user_id] = {"name": "", "username": user_id, "email": ""}
        else:
            cache[user_id] = {"name": "", "username": user_id, "email": ""}
    return cache[user_id]


def get_collection_info(collection_id, cache):
    """Get cached collection information."""
    if collection_id not in cache:
        cmd = f"globus endpoint show --format json {collection_id}"
        success, stdout, stderr = run_globus_command(cmd)
        if success:
            try:
                data = json.loads(stdout)
                cache[collection_id] = data.get('display_name', collection_id)
            except json.JSONDecodeError:
                cache[collection_id] = collection_id
        else:
            cache[collection_id] = collection_id
    return cache[collection_id]


def format_timestamp(timestamp_str):
    """Format ISO timestamp to readable format."""
    if not timestamp_str:
        return ""
    try:
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S UTC')
    except:
        return timestamp_str

def format_size(bytes_count):
    """Format byte count in human-readable form."""
    if not bytes_count:
        return "0 B"
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_count < 1024.0:
            return f"{bytes_count:.1f} {unit}"
        bytes_count /= 1024.0
    return f"{bytes_count:.1f} PB"

def output_csv(tasks, show_collection_names, user_cache, collection_cache):
    """Output tasks in CSV format."""
    fieldnames = [
        'task_id', 'status', 'type', 'initiated_by', 'owner_email', 'label',
        'request_time', 'completion_time', 'source_endpoint', 'dest_endpoint',
        'files_total', 'files_transferred', 'bytes_total', 'bytes_transferred',
        'speed_mbps', 'faults', 'retries', 'failed_subtasks', 'succeeded_subtasks'
    ]
    
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()
    
    for task in tasks:
        # Get owner info
        owner_id = task.get('owner_id')
        owner_info = get_user_info(owner_id, user_cache) if owner_id else {"name": "", "email": ""}
        
        # Get endpoint names if requested
        source_name = dest_name = ""
        if show_collection_names:
            source_id = task.get('source_endpoint_id')
            dest_id = task.get('destination_endpoint_id')
            if source_id:
                source_name = get_collection_info(source_id, collection_cache)
            if dest_id:
                dest_name = get_collection_info(dest_id, collection_cache)
        else:
            source_name = task.get('source_endpoint_id', '')
            dest_name = task.get('destination_endpoint_id', '')
        
        # Calculate speed in Mbps
        speed_bps = task.get('effective_bytes_per_second', 0)
        speed_mbps = (speed_bps * 8) / (1024 * 1024) if speed_bps else 0
        
        row = {
            'task_id': task.get('task_id', ''),
            'status': task.get('status', ''),
            'type': task.get('type', 'TRANSFER'),
            'initiated_by': owner_info.get('name') or owner_info.get('username', ''),
            'owner_email': owner_info.get('email', ''),
            'label': task.get('label', ''),
            'request_time': format_timestamp(task.get('request_time')),
            'completion_time': format_timestamp(task.get('completion_time')),
            'source_endpoint': source_name,
            'dest_endpoint': dest_name,
            'files_total': task.get('files', 0),
            'files_transferred': task.get('files_transferred', 0),
            'bytes_total': task.get('bytes', 0),
            'bytes_transferred': task.get('bytes_transferred', 0),
            'speed_mbps': f"{speed_mbps:.2f}" if speed_mbps > 0 else "0",
            'faults': task.get('faults', 0),
            'retries': task.get('subtasks_retrying', 0),
            'failed_subtasks': task.get('subtasks_failed', 0),
            'succeeded_subtasks': task.get('subtasks_succeeded', 0)
        }
        writer.writerow(row)

def print_detailed_task_info(task, verbose=False, show_collection_names=True, user_cache=None):
    """Print comprehensive information about a transfer task in human-readable format."""
    if user_cache is None:
        user_cache = {}
    
    task_id = task.get('task_id', 'Unknown')
    status = task.get('status', 'Unknown')
    label = task.get('label') or 'No label'
    task_type = task.get('type', 'TRANSFER')
    
    # Get owner information 
    owner_id = task.get('owner_id')
    if owner_id and owner_id not in user_cache:
        user_cache[owner_id] = get_user_info(owner_id)
    owner_info = user_cache.get(owner_id, {"username": owner_id}) if owner_id else {"username": "Unknown"}
    owner_display = owner_info.get('name') or owner_info.get('username', 'Unknown')
    
    # Status with emoji and color
    status_display = {
        'ACTIVE': '🔄 ACTIVE (In Progress)',
        'SUCCEEDED': '✅ SUCCEEDED (Completed)',
        'FAILED': '❌ FAILED (Error)',
        'INACTIVE': '⏸️ INACTIVE (Paused/Stopped)'
    }.get(status, f'❓ {status}')
    
    # Timing information
    request_time = format_timestamp(task.get('request_time'))
    completion_time = format_timestamp(task.get('completion_time')) if task.get('completion_time') else 'Not completed'
    
    # Transfer statistics
    files = task.get('files', 0)
    files_transferred = task.get('files_transferred', 0)
    bytes_total = task.get('bytes', 0)
    bytes_transferred = task.get('bytes_transferred', 0)
    bytes_per_second = task.get('effective_bytes_per_second', 0)
    
    # Retry and error information
    faults = task.get('faults', 0)
    subtasks_total = task.get('subtasks_total', 0)
    subtasks_succeeded = task.get('subtasks_succeeded', 0)
    subtasks_pending = task.get('subtasks_pending', 0)
    subtasks_retrying = task.get('subtasks_retrying', 0)
    subtasks_failed = task.get('subtasks_failed', 0)
    
    # Source and destination
    source_id = task.get('source_endpoint_id')
    dest_id = task.get('destination_endpoint_id')
    
    if show_collection_names and (source_id or dest_id):
        if source_id:
            source_info = get_collection_info(source_id)
            source_name = source_info.get('display_name', source_id)
        else:
            source_name = 'Unknown'
            
        if dest_id:
            dest_info = get_collection_info(dest_id)
            dest_name = dest_info.get('display_name', dest_id)
        else:
            dest_name = 'Unknown'
    else:
        source_name = source_id or 'Unknown'
        dest_name = dest_id or 'Unknown'
    
    # Print comprehensive information
    print(f"\\n{'='*80}")
    print(f"TASK: {task_id} | TYPE: {task_type}")
    print(f"STATUS: {status_display}")
    print(f"INITIATED BY: {owner_display}")
    print(f"LABEL: {label}")
    print(f"{'='*80}")
    
    # Timing
    print(f"⏰ TIMING:")
    print(f"  Requested:  {request_time}")
    print(f"  Completed:  {completion_time}")
    
    if status == 'ACTIVE' and bytes_per_second and bytes_total > bytes_transferred:
        remaining_bytes = bytes_total - bytes_transferred
        eta_seconds = remaining_bytes / bytes_per_second
        eta = format_duration(eta_seconds)
        print(f"  ETA:        {eta}")
    
    # Transfer details
    print(f"\\n📂 TRANSFER DETAILS:")
    if task_type == 'TRANSFER':
        print(f"  Source:      {source_name}")
        print(f"  Destination: {dest_name}")
    else:
        print(f"  Endpoint:    {source_name or dest_name}")
    
    # File and size information
    print(f"\\n📊 PROGRESS:")
    if files > 0:
        file_percent = (files_transferred / files * 100) if files > 0 else 0
        print(f"  Files:       {files_transferred:,} / {files:,} ({file_percent:.1f}%)")
    
    if bytes_total > 0:
        size_percent = (bytes_transferred / bytes_total * 100) if bytes_total > 0 else 0
        print(f"  Data Size:   {format_size(bytes_transferred)} / {format_size(bytes_total)} ({size_percent:.1f}%)")
    elif bytes_transferred > 0:
        print(f"  Data Size:   {format_size(bytes_transferred)} transferred")
    
    if bytes_per_second > 0:
        print(f"  Speed:       {format_size(bytes_per_second)}/s")
    
    # Error and retry information
    if faults > 0 or subtasks_retrying > 0 or subtasks_failed > 0:
        print(f"\\n⚠️  ISSUES & RETRIES:")
        if faults > 0:
            print(f"  Faults:      {faults:,}")
        if subtasks_retrying > 0:
            print(f"  Retrying:    {subtasks_retrying:,} subtasks")
        if subtasks_failed > 0:
            print(f"  Failed:      {subtasks_failed:,} subtasks")
    
    # Subtask breakdown (if available and verbose)
    if verbose and subtasks_total > 0:
        print(f"\\n🔍 SUBTASK BREAKDOWN:")
        print(f"  Total:       {subtasks_total:,}")
        print(f"  Succeeded:   {subtasks_succeeded:,}")
        print(f"  Pending:     {subtasks_pending:,}")
        print(f"  Retrying:    {subtasks_retrying:,}")
        print(f"  Failed:      {subtasks_failed:,}")
    
    # Additional technical details for verbose mode
    if verbose:
        print(f"\\n🔧 TECHNICAL DETAILS:")
        print(f"  Task ID:     {task_id}")
        if owner_info.get('email'):
            print(f"  Owner Email: {owner_info['email']}")
        if source_id:
            print(f"  Source ID:   {source_id}")
        if dest_id and task_type == 'TRANSFER':
            print(f"  Dest ID:     {dest_id}")
        
        # Additional flags and settings
        if task.get('encrypt_data'):
            print(f"  Encryption:  Enabled")
        if task.get('verify_checksum'):
            print(f"  Checksum:    Verified")
        if task.get('preserve_timestamp'):
            print(f"  Timestamps:  Preserved")
    
    return user_cache

def monitor_transfers(collection_id, status_filter, task_type, label_filter, requested_after, 
                     requested_before, limit, verbose, watch, watch_interval, show_names):
    """Main monitoring function."""
    
    user_cache = {}
    collection_cache = {}
    
    while True:
        try:
            tasks = get_transfer_tasks(
                collection_id=collection_id,
                status_filter=status_filter,
                task_type=task_type,
                limit=limit,
                requested_after=requested_after,
                requested_before=requested_before,
                label_filter=label_filter
            )
            
            if not tasks:
                if not watch:
                    print("task_id,status,type,initiated_by,owner_email,label,request_time,completion_time,source_endpoint,dest_endpoint,files_total,files_transferred,bytes_total,bytes_transferred,speed_mbps,faults,retries,failed_subtasks,succeeded_subtasks")
                return
            
            output_csv(tasks, show_names, user_cache, collection_cache)
            
            if not watch:
                break
                
            time.sleep(watch_interval)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            if not watch:
                sys.exit(1)
            time.sleep(watch_interval)

def main():
    parser = argparse.ArgumentParser(
        description='Monitor Globus transfers to and from a collection',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Monitor all transfers
  python3 monitor_transfers.py
  
  # Monitor transfers for a specific collection
  python3 monitor_transfers.py --collection ddb59aef-6d04-11e5-ba46-22000b92c6ec
  
  # Monitor all transfers (shows comprehensive details for up to 1000 tasks)
  python3 monitor_transfers.py
  
  # Monitor transfers for a specific collection
  python3 monitor_transfers.py --collection ddb59aef-6d04-11e5-ba46-22000b92c6ec
  
  # Monitor only active transfers with verbose technical details
  python3 monitor_transfers.py --status ACTIVE --verbose
  
  # Show recent failed transfers with full details
  python3 monitor_transfers.py --status FAILED --limit 20 --verbose
  
  # Monitor transfers by label pattern
  python3 monitor_transfers.py --label "backup*" --verbose
  
  # Show transfers from the last 24 hours
  python3 monitor_transfers.py --requested-after $(date -d '1 day ago' +%Y-%m-%d)
  
  # Monitor only DELETE tasks that are active or failed
  python3 monitor_transfers.py --type DELETE --status ACTIVE --status FAILED
  
  # Watch mode for real-time monitoring (updates every 30 seconds)
  python3 monitor_transfers.py --watch --interval 30
        """
    )
    
    parser.add_argument('--collection', '-c', 
                       help='Collection/endpoint UUID to monitor')
    parser.add_argument('--status', '-s', 
                       choices=['ACTIVE', 'INACTIVE', 'SUCCEEDED', 'FAILED'],
                       action='append',
                       help='Filter by transfer status (can be used multiple times)')
    parser.add_argument('--type', '-t',
                       choices=['TRANSFER', 'DELETE'],
                       help='Filter by task type')
    parser.add_argument('--label', 
                       help='Filter by task label pattern')
    parser.add_argument('--requested-after',
                       help='Filter tasks requested after this time (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)')
    parser.add_argument('--requested-before',
                       help='Filter tasks requested before this time (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)')
    parser.add_argument('--limit', '-l', type=int, default=1000,
                       help='Maximum number of tasks to retrieve (default: 1000)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Include additional technical details')
    parser.add_argument('--watch', '-w', action='store_true',
                       help='Watch mode - continuously refresh')
    parser.add_argument('--interval', '-i', type=int, default=30,
                       help='Refresh interval in seconds (default: 30)')
    parser.add_argument('--no-names', action='store_true',
                       help='Show endpoint IDs instead of names for faster retrieval')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.limit < 1:
        print("Error: --limit must be at least 1", file=sys.stderr)
        sys.exit(1)
    
    if args.interval < 1:
        print("Error: --interval must be at least 1 second", file=sys.stderr)
        sys.exit(1)
    
    # Check Globus CLI availability
    success, _, _ = run_globus_command("globus --help")
    if not success:
        print("Error: Globus CLI not found. Please install and configure the Globus CLI.", file=sys.stderr)
        print("See: https://docs.globus.org/cli/", file=sys.stderr)
        sys.exit(1)
    
    try:
        monitor_transfers(
            collection_id=args.collection,
            status_filter=args.status,
            task_type=args.type,
            label_filter=args.label,
            requested_after=args.requested_after,
            requested_before=args.requested_before,
            limit=args.limit,
            verbose=args.verbose,
            watch=args.watch,
            watch_interval=args.interval,
            show_names=not args.no_names
        )
    except KeyboardInterrupt:
        print("\nMonitoring stopped.", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()