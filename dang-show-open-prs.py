#!/usr/bin/python3

import argparse
import json
import os
from shutil import which
import subprocess

if not which("gh"):
    print("gh CLI required to run this script, aborting")
    exit(1)


parser = argparse.ArgumentParser(
        prog="Open PR Lister",
        description="Uses the gh CLI to pull all open PRs under one root directory"
        )
parser.add_argument('-d', '--directory')
args = parser.parse_args()

default_dir = "."

root_dir = args.directory

if not root_dir:
    root_dir = default_dir
    print('No PROJECT_ROOT_DIR set, defaulting to current directory')

def project_is_github_repo(path:os.DirEntry) -> bool:
    files = os.scandir(path)

    if not files:
        return False

    for file in files:
        if file.name == ".git":
            return True

    return False

def print_prs_for_project(path:os.DirEntry):
    process_result = subprocess.run(["gh", "pr", "list", "--json", "url,title,author"], cwd=path, capture_output=True)

    if process_result.returncode != 0:
        print("Failed to pull list for " + path.name)
        return


    pr_data = process_result.stdout
    json_data = json.loads(pr_data)

    if not json_data:
        return

    print(path.name + ":\n")
    for pr in json_data:
        print(f"* {pr['url']} ({pr['author'].get('name', 'bot')}): {pr['title']}")

    print("") # newline

github_projects = [dir for dir in os.scandir(root_dir) if dir.is_dir() and project_is_github_repo(dir)]

if not github_projects:
    print("No projects found")
    exit(1)

print("") # newline

for dir in github_projects:
    print_prs_for_project(dir)





