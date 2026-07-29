#!/usr/bin/env python3
import argparse
import subprocess
import sys

def run_command(cmd, cwd=None):
    try:
        result = subprocess.run(cmd, cwd=cwd, check=True, text=True, capture_output=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error executing {' '.join(cmd)}: {e}", file=sys.stderr)
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr, file=sys.stderr)
        sys.exit(1)

def status():
    print("--- Git Status ---")
    run_command(['git', 'status'])

def diff():
    print("--- Git Diff ---")
    run_command(['git', 'diff'])

def commit(message, files):
    print("--- Staging Files ---")
    run_command(['git', 'add'] + files)
    print("--- Committing ---")
    run_command(['git', 'commit', '-m', message])

def push(branch):
    print("--- Pushing to Remote ---")
    run_command(['git', 'push', 'origin', branch])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Git Manager Script")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Status
    status_parser = subparsers.add_parser('status', help="Check git status")
    
    # Diff
    diff_parser = subparsers.add_parser('diff', help="Check git diff")
    
    # Commit
    commit_parser = subparsers.add_parser('commit', help="Add files and commit")
    commit_parser.add_argument('-m', '--message', required=True, help="Commit message")
    commit_parser.add_argument('files', nargs='+', help="Files to add")
    
    # Push
    push_parser = subparsers.add_parser('push', help="Push to remote")
    push_parser.add_argument('-b', '--branch', required=True, help="Branch to push to")

    args = parser.parse_args()

    if args.command == 'status':
        status()
    elif args.command == 'diff':
        diff()
    elif args.command == 'commit':
        commit(args.message, args.files)
    elif args.command == 'push':
        push(args.branch)
