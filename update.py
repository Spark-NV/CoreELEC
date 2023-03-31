import os
import re
import sys
from github import Github

KODI_REPO_NAME = 'Spark-NV/xbmc'
KODI_BRANCH_NAME = 'aml-5.4-20.1'
SETTINGS_REPO_NAME = 'Spark-NV/service.coreelec.settings'
SETTINGS_BRANCH_NAME = 'coreelec-20'
coreelec_dir = os.path.dirname(os.path.abspath(__file__))

kodi_files_to_update = [
    "./projects/Amlogic-ce/packages/mediacenter/kodi/package.mk",
    "./projects/Amlogic-ce/devices/Amlogic-ne/packages/mediacenter/kodi/package.mk",
    "./packages/mediacenter/kodi/package.mk",
]

settings_files_to_update = [
    "./projects/Amlogic-ce/packages/mediacenter/CoreELEC-settings/package.mk",
    "./projects/Amlogic-ce/devices/Amlogic-ne/packages/mediacenter/CoreELEC-settings/package.mk",
    "./packages/mediacenter/LibreELEC-settings/package.mk",
]

def update_kodi_version():
    new_version = input("Enter new Kodi version number (e.g. 22.5 or 22.5.1): ")
    version_parts = new_version.split(".")

    major = int(version_parts[0])
    minor = 0

    if len(version_parts) > 1:
        minor_parts = ".".join(version_parts[1:]).split(".")
        minor = int(minor_parts[0])
        if len(minor_parts) > 1:
            minor += float("." + ".".join(minor_parts[1:]))

    with open("./distributions/CoreELEC/version", "r") as f:
        lines = f.readlines()

    old_major, old_minor = None, None
    for i in range(len(lines)):
        if "OS_MAJOR=" in lines[i]:
            old_major = lines[i].strip().split("=")[-1]
            lines[i] = '  OS_MAJOR="{}"\n'.format(major)
        elif "OS_MINOR=" in lines[i]:
            old_minor = lines[i].strip().split("=")[-1]
            lines[i] = '  OS_MINOR="{}"\n'.format(minor)

    with open("./distributions/CoreELEC/version", "w") as f:
        f.writelines(lines)

    if old_major and old_minor:
        print("\nUpdated Kodi version from \033[1;31m{}.{}\033[0m to \033[1;32m{}.{}\033[0m\n".format(old_major.strip('"'), old_minor.strip('"'), major, minor))
    elif old_major:
        print("\nUpdated Kodi version from \033[1;31m{}\033[0m to \033[1;32m{}.{}\033[0m\n".format(old_major.strip('"'), major, minor))
    else:
        print("\nUpdated Kodi version to \033[1;32m{}.{}\033[0m\n".format(major, minor))


def update_settings_links():
    g = Github()
    repo = g.get_repo(SETTINGS_REPO_NAME)
    latest_commit = repo.get_branch(SETTINGS_BRANCH_NAME).commit
    latest_commit_hash = latest_commit.sha

    for file_path in settings_files_to_update:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        with open(file_path, 'w') as f:
            for line in lines:
                if 'PKG_VERSION=' in line:
                    f.write(f'PKG_VERSION="{latest_commit_hash}"\n')
                else:
                    f.write(line)

def update_kodi_links():
    g = Github()
    repo = g.get_repo(KODI_REPO_NAME)
    latest_commit = repo.get_branch(KODI_BRANCH_NAME).commit
    latest_commit_hash = latest_commit.sha

    for file_path in kodi_files_to_update:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        with open(file_path, 'w') as f:
            for line in lines:
                if 'PKG_VERSION=' in line:
                    f.write(f'PKG_VERSION="{latest_commit_hash}"\n')
                else:
                    f.write(line)

def show_current_hash():
    hash_string = None
    matching_files = []
    for i, file_path in enumerate(kodi_files_to_update):
        with open(os.path.join(coreelec_dir, file_path), "r") as f:
            content = f.read()
        # Use regular expressions to find the hash string
        pattern = r'PKG_VERSION="(.*?)"'
        current_hash_string = re.findall(pattern, content)[0]
        if hash_string is None:
            hash_string = current_hash_string
            matching_files.append(file_path)
        elif current_hash_string == hash_string:
            matching_files.append(file_path)
        else:
            print(f"\n{file_path} \033[31mDOES NOT MATCH\033[0m PKG_VERSION={current_hash_string}")
    if len(matching_files) == len(kodi_files_to_update):
        print(f"\nPKG_VERSION= \033[31m{hash_string}\033[0m\n")
    else:
        for file_path in matching_files:
            print(f"\n{file_path} \033[32m=\033[0m PKG_VERSION={hash_string}")

def show_current_settings_hash():
    hash_string = None
    matching_files = []
    for i, file_path in enumerate(settings_files_to_update):
        with open(os.path.join(coreelec_dir, file_path), "r") as f:
            content = f.read()
        # Use regular expressions to find the hash string
        pattern = r'PKG_VERSION="(.*?)"'
        current_hash_string = re.findall(pattern, content)[0]
        if hash_string is None:
            hash_string = current_hash_string
            matching_files.append(file_path)
        elif current_hash_string == hash_string:
            matching_files.append(file_path)
        else:
            print(f"\n{file_path} \033[31mDOES NOT MATCH\033[0m PKG_VERSION={current_hash_string}")
    if len(matching_files) == len(settings_files_to_update):
        print(f"\nPKG_VERSION= \033[31m{hash_string}\033[0m\n")
    else:
        for file_path in matching_files:
            print(f"\n{file_path} \033[32m=\033[0m PKG_VERSION={hash_string}")

while True:
    choice = input("Choose an option:\n1. Update Kodi hash/link\n2. Update Settings hash/link\n3. Show current kodi hash/link\n4. Show current settings hash/link\n5. Update CoreELEC version\n6. Exit\n")
    if choice == "1":
        print("Updating Kodi links...")
        update_kodi_links()
        print("Kodi links updated successfully.")
    elif choice == "2":
        print("Updating Settings links...")
        update_kodi_links()
        print("Settings links updated successfully.")
    elif choice == "3":
        show_current_hash()
    elif choice == "4":
        show_current_settings_hash()
    elif choice == "5":
        update_kodi_version()
    elif choice == "6":
        print("Exiting...")
        sys.exit()
    else:
        print("Invalid choice. Please try again.")
