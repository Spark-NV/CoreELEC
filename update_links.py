import os
import re

# Define the files to be updated for Kodi and Settings links
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

# Define the CoreELEC directory
coreelec_dir = os.path.dirname(os.path.abspath(__file__))

# Define functions to update Kodi and Settings links
def update_kodi_link():
    new_string = input("Enter the new kodi version hash/string: ")
    for file_path in kodi_files_to_update:
        with open(os.path.join(coreelec_dir, file_path), "r") as f:
            content = f.read()
        # Use regular expressions to find the old string
        pattern = r'PKG_VERSION="(.*?)"'
        old_string = re.findall(pattern, content)[0]
        content = content.replace(f'PKG_VERSION="{old_string}"', f'PKG_VERSION="{new_string}"')
        with open(os.path.join(coreelec_dir, file_path), "w") as f:
            f.write(content)
    print(f"\033[1m\nKodi/XBMC links/Hash's updated\033[0m\nNew string: \033[32m{new_string}\033[0m\nOld string: \033[31m{old_string}\033[0m\n")

def update_settings_link():
    new_string = input("Enter the new settings version hash/string: ")
    for file_path in settings_files_to_update:
        with open(os.path.join(coreelec_dir, file_path), "r") as f:
            content = f.read()
        # Use regular expressions to find the old string
        pattern = r'PKG_VERSION="(.*?)"'
        old_string = re.findall(pattern, content)[0]
        content = content.replace(f'PKG_VERSION="{old_string}"', f'PKG_VERSION="{new_string}"')
        with open(os.path.join(coreelec_dir, file_path), "w") as f:
            f.write(content)
    print(f"\033[1m\nSettings links/Hash's updated\033[0m\nNew string: \033[32m{new_string}\033[0m\nOld string: \033[31m{old_string}\033[0m\n")

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
    choice = input("Choose an option:\n1. Update Kodi hash/link\n2. Update Settings hash/link\n3. Show current kodi hash/link\n4. Show current settings hash/link\n")
    if choice == "1":
        update_kodi_link()
        break
    elif choice == "2":
        update_settings_link()
        break
    elif choice == "3":
        show_current_hash()
        break
    elif choice == "4":
        show_current_settings_hash()
        break
    else:
        print("Invalid choice. Please try again.")
