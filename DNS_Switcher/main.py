import platform
import subprocess
import re

def find_interface():
    def windows():
        try:
            r = subprocess.run(
                ["netsh", "interface", "ipv4", "show", "interfaces"],
                capture_output=True,
                text=True,
                shell=True
            )
            interfaces = r.stdout
            for line in interfaces.splitlines():
                if "Connected" in line:
                    match = re.search(r"^\s*(\S+)\s+", line)
                    if match:
                        return match.group(1)
        except subprocess.CalledProcessError as e:
            print("ERROR: ", e)
            return None

    def linux():
        try:
            r = subprocess.run(
                ["nmcli", "-t", "-f", "NAME,DEVICE,STATE", "con", "show", "--active"],
                capture_output=True,
                text=True
            )
            connections = r.stdout            
            for line in connections.splitlines():
                parts = line.split(":")
                if parts[2] == "activated":
                    return parts[0]
        except subprocess.CalledProcessError as e:
            print("ERROR: ", e)
            return None

    if platform.system() == "Linux":
        return linux()
    elif platform.system() == "Windows":
        return windows()
    else:
        print("Unsupported Operating System")
        return None

def change_dns(prim_dns, sec_dns):
    def linux(p, s):
        interface = find_interface()
        if interface:
            try:
                subprocess.run(
                    ["nmcli", "con", "mod", interface, "ipv4.dns", f"{p} {s}" if s else p],
                    check=True
                )
                subprocess.run(
                    ["nmcli", "con", "up", interface],
                    check=True
                )
            except subprocess.CalledProcessError as e:
                print(f"ERROR: {e}")

    def windows(p, s):
        interface = find_interface()
        if interface:
            try:
                subprocess.run(
                    ["netsh", "interface", "ipv4", "set", "dns", f"name={interface}", "static", p],
                    check=True,
                    shell=True
                )
                if s:
                    subprocess.run(
                        ["netsh", "interface", "ipv4", "add", "dns", f"name={interface}", "static", s, "index=2"],
                        check=True,
                        shell=True
                    )
            except subprocess.CalledProcessError as e:
                print("ERROR: ", e)

    if platform.system() == "Linux":
        linux(prim_dns, sec_dns)
    elif platform.system() == "Windows":
        windows(prim_dns, sec_dns)
    else:
        print("Unsupported Operating System")

def main():
    dns = {
    'Cloudflare': ["1.1.1.1", "1.0.0.1"],
    'Google': ['8.8.8.8', '8.8.4.4'],
    'OpenDNS': ['208.67.222.222', '208.67.220.220'],
    'Quad9': ['9.9.9.9', '149.112.112.112'],
    'Comodo Secure DNS': ['8.26.56.26', '8.20.247.20'],
    'CleanBrowsing': ['185.228.168.9', '185.228.169.9'],
    'Yandex': ['77.88.8.8', '77.88.8.1'],
    'Neustar': ['156.154.70.1', '156.154.71.1'],
    'Verisign': ['64.6.64.6', '64.6.65.6']
}

    print("Select a pre-defined DNS or enter a custom DNS:")
    for i, (provider, addresses) in enumerate(dns.items(), 1):
        print(f"{i}. {provider} (Primary: {addresses[0]}, Secondary: {addresses[1]})")
    print(f"{len(dns) + 1}. Enter Custom DNS")

    try:
        choice = int(input("\nEnter your choice (number): "))

        if 1 <= choice <= len(dns):
            selected_dns = list(dns.values())[choice - 1]
            prim, sec = selected_dns[0], selected_dns[1]
            provider = list(dns.keys())[choice - 1]
        elif choice == len(dns) + 1:
            prim = input("Enter the primary DNS: ")
            sec = input("Enter the secondary DNS (or leave blank for none): ")
            provider = "Custom DNS"
        else:
            print("Invalid choice. Exiting.")
            return

        change_dns(prim, sec)

        print(f"Switched to {provider} (Primary: {prim}, Secondary: {sec}) DNS")

    except ValueError:
        print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()
