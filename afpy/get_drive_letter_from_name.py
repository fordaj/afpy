import sys
import platform
import argparse

def windows(drive_name):
    import win32api #pip install pywin32
    
    for drive in win32api.GetLogicalDriveStrings().split('\000'):
        if not drive:
            continue
        vol_name = win32api.GetVolumeInformation(drive)[0]
        if vol_name == drive_name:
            return drive
    return None

def mac_linux(drive_name):
    import subprocess
    import os

    if platform.system() == "Darwin":
        mount_cmd = ["mount"]
    else:  # Linux
        mount_cmd = ["lsblk", "-o", "MOUNTPOINT,LABEL", "-J"]

    try:
        output = subprocess.check_output(mount_cmd, universal_newlines=True)
    except Exception:
        return None

    # macOS parsing
    if platform.system() == "Darwin":
        for line in output.splitlines():
            if f" on " in line and f"{drive_name}" in line:
                # line format: /dev/disk2s1 on /Volumes/MyDVD (hfs, local, nodev, nosuid, journaled)
                parts = line.split(" on ")
                if len(parts) > 1:
                    mount_point = parts[1].split(" ")[0]
                    return mount_point
    else:  # Linux parsing
        import json
        try:
            blk = json.loads(output)
            for dev in blk.get("blockdevices", []):
                mountpoint = dev.get("mountpoint")
                label = dev.get("label")
                if mountpoint and label == drive_name:
                    return mountpoint
                # also check children
                for child in dev.get("children", []):
                    if child.get("mountpoint") and child.get("label") == drive_name:
                        return child.get("mountpoint")
        except json.JSONDecodeError:
            return None

    return None

def find_drive(drive_name):
    system = platform.system()
    if system == "Windows":
        return windows(drive_name)
    else:
        print("WARNING UNTESTED")
        return mac_linux(drive_name)

def main():
    parser = argparse.ArgumentParser(description="Find drive path by volume name")
    parser.add_argument("--drive-name", required=True, help="Volume label of the drive")
    args = parser.parse_args()

    path = find_drive(args.drive_name)
    if path:
        print(path)
    else:
        print(f"Drive '{args.drive_name}' not found", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
