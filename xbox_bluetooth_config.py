import os, sys, re, shutil, subprocess, datetime

if os.geteuid() != 0:
    sys.exit("This script must be run as root (use sudo)")

path = "/var/lib/bluetooth"
target = "[ConnectionParameters]\nMinInterval=6\nMaxInterval=9\nLatency=44\nTimeout=216\n"
xbox_name = "Name=Xbox Wireless Controller"

def find_controllers(name):
    result = []
    for root, _, files in os.walk(path):
        for file in files:
            if file == "info":
                with open(os.path.join(root, file), "r") as f:
                    contents = f.read()
                    if name in contents:
                        result.append(os.path.join(root, file))
    return result

def choose_device():
    devices = find_controllers("Name=")
    print("Available devices:")
    for i, device in enumerate(devices, start=1):
        with open(device, "r") as f:
            contents = f.read()
            name = re.search(r'Name=(.+)', contents).group(1)
        mac_address = os.path.basename(os.path.dirname(device))
        print(f"{i}. {name} ({mac_address})")
    print(f"{len(devices)+1}. Manually enter a MAC address")
    print(f"{len(devices)+2}. Cancel")
    choice = int(input("Enter the number corresponding to your choice: "))
    if choice == len(devices) + 1:
        mac_address = input("Enter the device MAC address: ")
        controller_address = input("Enter the Xbox controller MAC address: ")
        return os.path.join(path, mac_address, controller_address, "info")
    elif choice == len(devices) + 2:
        sys.exit("No changes made. Exiting.")
    else:
        return devices[choice-1]


def restore_from_backup():
    backup_files = [f for f in os.listdir() if f.endswith(".info")]
    if len(backup_files) == 0:
        print("No backup files found.")
        return
    print("Available backup files:")
    for i, backup_file in enumerate(backup_files, start=1):
        print(f"{i}. {backup_file}")
    choice = int(input("Enter the number corresponding to the backup file you want to restore: "))
    chosen_backup = backup_files[choice - 1]
    controller_address = chosen_backup.split("_")[0]
    mac_address = os.path.dirname(os.path.dirname(os.path.realpath(chosen_backup)))
    info_path = os.path.join(path, mac_address, controller_address, "info")
    shutil.copy(chosen_backup, info_path)
    print(f"Configuration restored from backup: {chosen_backup}")
    subprocess.run(["systemctl", "restart", "bluetooth.service"])
    print("Bluetooth service restarted")

print("WARNING: This script may introduce issues and comes with no warranties.")
acknowledge = input("Type 'yes' to confirm you understand: ")
if acknowledge.lower() != 'yes': sys.exit()
restore = input("Do you want to restore the configuration from a backup? [y/N]: ")
if restore.lower() == 'y':
    restore_from_backup()
    sys.exit()

xbox_controllers = find_controllers(xbox_name)
if len(xbox_controllers) > 0:
    print("Found Xbox controller(s):")
    for controller in xbox_controllers:
        print(f"  {controller}")
    configure = input("Do you want to configure the found Xbox controller(s)? [Y/n]: ")
    if configure.lower() == 'n':
        chosen_device = choose_device()
        xbox_controllers = [chosen_device]
else:
    chosen_device = choose_device()
    xbox_controllers = [chosen_device]

restart = input("Do you want to restart the Bluetooth service after updating the configuration? [Y/n]: ")
for controller in xbox_controllers:
    with open(controller, "r") as f:
        contents = f.read()
    backup_path = f"{os.getcwd()}/{os.path.basename(os.path.dirname(controller))}_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.info"
    shutil.copy(controller, backup_path)
    with open(controller, "w") as f:
        f.write(re.sub(r'(?<=\[ConnectionParameters\]\n)(.*\n)*', target, contents))
    print(f"Configuration file backed up to: {backup_path}")

if restart.lower() != 'n':
    subprocess.run(["systemctl", "restart", "bluetooth.service"])
    print("Bluetooth configuration updated successfully")

