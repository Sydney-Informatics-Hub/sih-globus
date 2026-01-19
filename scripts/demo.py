#!/usr/bin/env python3
"""
Test and demo script for Globus group administration tools.
Shows examples of how to use the tools without requiring real group IDs.
"""

import os
import sys
import tempfile
import subprocess

def demo_bulk_invite():
    """Demonstrate the bulk invite functionality."""
    print("=== Bulk Invite Demo ===")
    print("This demonstrates how to invite multiple users to a group.\n")
    
    # Create a temporary users file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        demo_users = [
            "# Demo users file",
            "demo.user1@example.com",
            "demo.user2@university.edu", 
            "demo.user3@institution.org"
        ]
        f.write('\n'.join(demo_users))
        users_file = f.name
    
    print(f"Created demo users file: {users_file}")
    print("Contents:")
    with open(users_file, 'r') as f:
        for line_num, line in enumerate(f, 1):
            print(f"  {line_num}: {line.rstrip()}")
    
    print("\nExample commands you could run:")
    print(f"  # Dry run to see what would happen:")
    print(f"  ./scripts/bulk_invite.py DEMO_GROUP_ID --users-file {users_file} --dry-run --verbose")
    print()
    print(f"  # Actually invite users as members:")
    print(f"  ./scripts/bulk_invite.py DEMO_GROUP_ID --users-file {users_file} --role member")
    print()
    print(f"  # Invite specific users as managers:")
    print(f"  ./scripts/bulk_invite.py DEMO_GROUP_ID --users demo.user1@example.com demo.user2@university.edu --role manager")
    
    # Clean up
    os.unlink(users_file)
    print(f"\nCleaned up temporary file: {users_file}")

def demo_group_admin():
    """Demonstrate the group admin functionality."""
    print("\n=== Group Admin Demo ===")
    print("This demonstrates various group administration tasks.\n")
    
    print("Example commands you could run:")
    print("  # List all your groups:")
    print("  ./scripts/globus-admin list")
    print("  # OR: ./scripts/group_admin.py list")
    print()
    print("  # Show group information:")
    print("  ./scripts/globus-admin info YOUR_GROUP_ID")
    print("  # OR: ./scripts/group_admin.py info YOUR_GROUP_ID")
    print()
    print("  # Show all group members:")
    print("  ./scripts/globus-admin members YOUR_GROUP_ID")
    print("  # OR: ./scripts/group_admin.py members YOUR_GROUP_ID")
    print()
    print("  # Export group data for backup:")
    print("  ./scripts/group_admin.py export YOUR_GROUP_ID --output backup.json")
    print()
    print("  # Bulk remove users:")
    print("  ./scripts/group_admin.py bulk-remove YOUR_GROUP_ID --users user1 user2 user3")

def check_login_status():
    """Check if user is logged into Globus."""
    print("\n=== Login Status Check ===")
    try:
        result = subprocess.run(['globus', 'whoami'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ You are logged into Globus!")
            print(f"  Identity: {result.stdout.strip()}")
            return True
        else:
            print("✗ You are not logged into Globus.")
            print("  Run: globus login")
            return False
    except FileNotFoundError:
        print("✗ Globus CLI not found in PATH")
        return False
    except Exception as e:
        print(f"✗ Error checking login status: {e}")
        return False

def show_quick_start():
    """Show quick start guide."""
    print("\n=== Quick Start Guide ===")
    print("To get started with group administration:")
    print()
    print("1. Login to Globus:")
    print("   globus login")
    print()
    print("2. List your groups to get group IDs:")
    print("   ./scripts/globus-admin list")
    print()
    print("3. Create a users file with the people you want to invite:")
    print("   cp scripts/users.txt my_team.txt")
    print("   # Edit my_team.txt with actual email addresses")
    print()
    print("4. Test with a dry run:")
    print("   ./scripts/globus-admin invite YOUR_GROUP_ID --users-file my_team.txt --dry-run")
    print()
    print("5. If it looks good, run the actual invitation:")
    print("   ./scripts/globus-admin invite YOUR_GROUP_ID --users-file my_team.txt --role member")
    print()
    print("For more help:")
    print("   ./scripts/globus-admin help")
    print("   cat scripts/README.md")

def main():
    print("Globus Group Administration - Demo & Test Script")
    print("=" * 50)
    
    # Check login status
    logged_in = check_login_status()
    
    # Show demos
    demo_bulk_invite()
    demo_group_admin()
    show_quick_start()
    
    if not logged_in:
        print("\n" + "!" * 50)
        print("IMPORTANT: You need to login to Globus first!")
        print("Run: globus login")
        print("!" * 50)

if __name__ == "__main__":
    main()