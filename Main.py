import customtkinter
import datetime
import json
import platform
import psutil
import cpuinfo
import GPUtil
import socket
import subprocess
import sys
import os
import datetime
import sqlite3
from subprocess import call
import logging

OUTPUT_JSON_PATH = "output/output.json"
OUTPUT_TXT_PATH = 'output/output.txt'

# Initialize logging
logging.basicConfig(filename='config/app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')


def show_output():
    call(["python3", "output/output.py"])


def add_log_entry(log_string):
    """
    Function to add an entry to the log file with a timestamp.

    Args:
    log_string (str): The string to be logged.

    Returns:
    None
    """
    logging.info(log_string)

# Function to save data to JSON file
def save_to_json(data):
    # Saving to JSON file
    with open(OUTPUT_JSON_PATH, 'a') as json_file:
        if isinstance(data, dict):
            # Convert dictionary to JSON string
            json_string = json.dumps(data, indent=4)
            # Exclude lines starting with "//"
            filtered_data = [line for line in json_string.split('\n') if not line.strip().startswith("//")]
            json_file.write('\n'.join(filtered_data))
        else:
            # If data is not a dictionary, just write it to the file
            if "\\n\\n" in data:
                data = data.split("\\n\\n")
                json_file.write('\n'.join(data))
            else:
                json.dump(data, json_file, indent=4)
        json_file.write('\n')

    # Saving to TXT file
    with open(OUTPUT_TXT_PATH, 'a') as txt_file:
        if isinstance(data, dict):
            # Convert dictionary to string
            data_str = json.dumps(data, indent=4)
        else:
            data_str = str(data)
        txt_file.write(data_str + '\n')
# Function to append comments to JSON file
def append_comment(comment):
    with open(OUTPUT_JSON_PATH, 'a') as json_file:
        json_file.write(f"// {comment}\n")

# Functions to retrieve system information

# 1. Operating System Information
def get_os_info():
    append_comment("Operating System Information")
    try:
        system_name = platform.system()
        system_version = platform.version()
        system_architecture = platform.architecture()
        os_info = {"system_name": system_name, "system_version": system_version, "system_architecture": system_architecture}
        save_to_json(os_info)
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

# 2. CPU Information
def get_cpu_info():
    append_comment("CPU Information")
    try:
        cpu_info = cpuinfo.get_cpu_info()
        save_to_json(cpu_info)
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

# 3. Memory Information
def get_memory_info():
    append_comment("Memory Information")
    try:
        memory_info = dict(psutil.virtual_memory()._asdict())
        save_to_json(memory_info)
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

# 4. Disk Information
def get_disk_info():
    append_comment("Disk Information")
    try:
        disk_info = psutil.disk_partitions()
        save_to_json(disk_info)
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

# 5. GPU Information
def get_gpu_info():
    append_comment("GPU Information")
    try:
        gpus = GPUtil.getGPUs()
        gpu_info = []
        for gpu in gpus:
            gpu_info.append({
                "name": gpu.name,
                "memory": gpu.memoryTotal,
                "id": gpu.id
            })
        save_to_json(gpu_info)
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

# 6. IP Address
def get_ip_address():
    append_comment("IP Address")
    try:
        ip_address = socket.gethostbyname(socket.gethostname())
        save_to_json({"ip_address": ip_address})
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

# 7. MAC Address
def get_mac_address():
    append_comment("MAC Address")
    try:
        mac_addresses = {}
        for interface, addresses in psutil.net_if_addrs().items():
            if interface != 'lo':
                mac_address = [address.address for address in addresses if address.family == psutil.AF_LINK]
                if mac_address:
                    mac_addresses[interface] = mac_address[0]
        save_to_json(mac_addresses)
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

# 8. Network Interfaces
def get_network_interfaces():
    append_comment("Network Interfaces")
    try:
        network_interfaces = psutil.net_if_addrs()
        save_to_json(network_interfaces)
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

# 9. Network Speed
def get_network_speed():
    append_comment("Network Speed")
    try:
        network_speed = psutil.net_if_stats()
        save_to_json(network_speed)
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

# 10. Environment Variables
def get_environment_variables():
    append_comment("Environment Variables")
    try:
        environment_variables = dict(os.environ)
        save_to_json(environment_variables)
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

# 11. System Paths
def get_system_paths():
    append_comment("System Paths")
    try:
        system_paths = sys.path
        save_to_json(system_paths)
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

# 12. Python Version
def get_python_version():
    append_comment("Python Version")
    try:
        python_version = sys.version
        save_to_json({"python_version": python_version})
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

# 13. Installed Packages
def get_installed_packages():
    append_comment("Installed Packages")
    try:
        installed_packages = [package.strip() for package in subprocess.check_output([sys.executable, "-m", "pip", "list"]).decode('utf-8').split('\n')[2:]]
        save_to_json(installed_packages)
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

# 14. Running Processes
def get_running_processes():
    append_comment("Running Processes")
    try:
        running_processes = [p.as_dict(attrs=['pid', 'name']) for p in psutil.process_iter()]
        save_to_json(running_processes)
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

# 15. CPU Usage
def get_cpu_usage():
    append_comment("CPU Usage")
    try:
        cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
        save_to_json(cpu_usage)
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

# 16. Memory Usage
def get_memory_usage():
    append_comment("Memory Usage")
    try:
        memory_usage = psutil.virtual_memory().percent
        save_to_json({"memory_usage_percent": memory_usage})
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

# 17. Disk Usage
def get_disk_usage():
    append_comment("Disk Usage")
    try:
        disk_usage = psutil.disk_usage('/')
        save_to_json(disk_usage._asdict())
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

# 18. Network Usage
def get_network_usage():
    append_comment("Network Usage")
    try:
        network_usage = psutil.net_io_counters()._asdict()
        save_to_json(network_usage)
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

# 19. Filesystem Type
def get_filesystem_type():
    append_comment("Filesystem Type")
    try:
        filesystem_type = platform.system()
        save_to_json({"filesystem_type": filesystem_type})
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

# 20. System Boot Time
def get_boot_time():
    append_comment("System Boot Time")
    try:
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        save_to_json({"boot_time": boot_time})
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

# 21. Logged-in Users
def get_users():
    append_comment("Logged-in Users")
    try:
        users = psutil.users()
        user_info = [{"username": user.name, "terminal": user.terminal, "host": user.host, "started": datetime.datetime.fromtimestamp(user.started).strftime("%Y-%m-%d %H:%M:%S")} for user in users]
        save_to_json(user_info)
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

# 22. System Uptime
def get_system_uptime():
    append_comment("System Uptime")
    try:
        uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())
        save_to_json({"uptime": str(uptime)})
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

# 23. Battery Information
def get_battery_info():
    append_comment("Battery Information")
    try:
        battery = psutil.sensors_battery()
        if battery is not None:
            battery_info = {
                "percent": battery.percent,
                "power_plugged": battery.power_plugged
            }
            save_to_json(battery_info)
        else:
            save_to_json({"error": "No battery found"})
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

# 24. Display Information
def get_display_info():
    append_comment("Display Information")
    try:
        if platform.system() == 'Darwin':  # macOS
            display_info = subprocess.check_output(['system_profiler', 'SPDisplaysDataType']).decode('utf-8')
        elif platform.system() == 'Windows':  # Windows
            display_info = subprocess.check_output(['wmic', 'path', 'win32_videocontroller', 'get', '/format:list']).decode('utf-8')
        else:
            display_info = "Not available for this platform."
        save_to_json({"display_info": display_info})
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

""" # 25. BIOS/UEFI Information
def get_bios_info():
    append_comment("BIOS/UEFI Information")
    try:
        if platform.system() == 'Darwin':  # macOS
            from Foundation import NSBundle

            def get_system_firmware():
                io_registry_entry_children = NSBundle.mainBundle().infoDictionary().get("IORegistryEntryChildren")
                if io_registry_entry_children:
                    for entry in io_registry_entry_children:
                        if entry.get("firmware-aci"):
                            return entry.get("firmware-aci")
                return None

            system_firmware = get_system_firmware()
            if system_firmware:
                bios_info = {
                    "BIOS Vendor": system_firmware.get("manufacturer"),
                    "BIOS Version": system_firmware.get("version"),
                    "BIOS Release Date": system_firmware.get("releaseDate"),
                }
                save_to_json(bios_info)
            else:
                save_to_json({"error": "Unable to retrieve BIOS information. No firmware-aci entry found."})
        elif platform.system() == 'Windows':  # Windows
            bios_info = {}
            bios_info["BIOS Vendor"] = subprocess.check_output("wmic bios get manufacturer /value", shell=True, text=True).strip().split('=')[1]
            bios_info["BIOS Version"] = subprocess.check_output("wmic bios get smbiosbiosversion /value", shell=True, text=True).strip().split('=')[1]
            bios_info["BIOS Release Date"] = subprocess.check_output("wmic bios get releasedate /value", shell=True, text=True).strip().split('=')[1]
            save_to_json(bios_info)
        else:
            save_to_json({"error": "BIOS information retrieval is not supported on this platform."})
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})
 """
# 26. Motherboard Information
def get_motherboard_info():
    append_comment("Motherboard Information")
    try:
        if platform.system() == 'Darwin':  # macOS
            motherboard_info = subprocess.check_output(['system_profiler', 'SPHardwareDataType']).decode('utf-8')
        elif platform.system() == 'Windows':  # Windows
            motherboard_info = subprocess.check_output("wmic baseboard get /format:list", shell=True, text=True)
        else:
            motherboard_info = "Not available for this platform."
        save_to_json({"motherboard_info": motherboard_info})
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

# 27. Network Configuration
def get_network_configuration():
    append_comment("Network Configuration")
    try:
        if platform.system() == 'Darwin':  # macOS
            network_config = subprocess.check_output(['ifconfig']).decode('utf-8')
        elif platform.system() == 'Windows':  # Windows
            network_config = subprocess.check_output("ipconfig /all", shell=True, text=True)
        else:
            network_config = "Not available for this platform."
        save_to_json({"network_configuration": network_config})
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

# 28. Installed Software (macOS)
def get_installed_software():
    append_comment("Installed Software")
    try:
        if platform.system() == 'Darwin':  # macOS
            installed_software = subprocess.check_output(['system_profiler', 'SPApplicationsDataType']).decode('utf-8')
            installed_software = installed_software.replace("\\n", "\n")
            if "\n\n" in installed_software:
                installed_software = installed_software.split("\n\n")
        else:
            installed_software = "Not available for this platform."
        save_to_json({"installed_software": installed_software})
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

# 29. Filesystem Usage
def get_filesystem_usage():
    append_comment("Filesystem Usage")
    try:
        filesystem_usage = subprocess.check_output(['df', '-h']).decode('utf-8')
        save_to_json({"filesystem_usage": filesystem_usage})
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

# 30. USB Devices (macOS)
def get_usb_devices():
    append_comment("USB Devices")
    try:
        if platform.system() == 'Darwin':  # macOS
            usb_devices = subprocess.check_output(['system_profiler', 'SPUSBDataType']).decode('utf-8')
        else:
            usb_devices = "Not available for this platform."
        save_to_json({"usb_devices": usb_devices})
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

# 31. System Events (macOS)
def get_system_events():
    append_comment("System Events (Example: System logs)")
    try:
        if platform.system() == 'Darwin':  # macOS
            system_events = subprocess.check_output(['syslog']).decode('utf-8').splitlines()[-10:]
            system_events = "\n".join(system_events)
        else:
            system_events = "Not available for this platform."
        save_to_json({"system_events": system_events})
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

# 32. Audio Devices
def get_audio_devices():
    append_comment("Audio Devices")
    try:
        if platform.system() == 'Darwin':  # macOS
            audio_devices = subprocess.check_output(['system_profiler', 'SPAudioDataType']).decode('utf-8')
        elif platform.system() == 'Windows':  # Windows
            audio_devices = subprocess.check_output("wmic sounddev get /format:list", shell=True, text=True)
        else:
            audio_devices = "Not available for this platform."
        save_to_json({"audio_devices": audio_devices})
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

# Additional Functions

# 33. Additional System Hardware Information - Graphics Card
def get_graphics_card_info():
    append_comment("Graphics Card Information")
    try:
        if platform.system() == 'Darwin':  # macOS
            graphics_info = subprocess.check_output(['system_profiler', 'SPDisplaysDataType']).decode('utf-8')
        elif platform.system() == 'Windows':  # Windows
            graphics_info = subprocess.check_output("wmic path win32_videocontroller get /format:list", shell=True, text=True)
        else:
            graphics_info = "Not available for this platform."
        save_to_json({"graphics_card_info": graphics_info})
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

# 34. Additional System Hardware Information - Storage Devices
def get_storage_devices_info():
    append_comment("Storage Devices Information")
    try:
        if platform.system() == 'Darwin':  # macOS
            storage_info = subprocess.check_output(['system_profiler', 'SPStorageDataType']).decode('utf-8')
        elif platform.system() == 'Windows':  # Windows
            storage_info = subprocess.check_output("wmic diskdrive get /format:list", shell=True, text=True)
        else:
            storage_info = "Not available for this platform."
        save_to_json({"storage_devices_info": storage_info})
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

# 35. DNS Settings
def get_dns_settings():
    append_comment("DNS Settings")
    try:
        if platform.system() == 'Darwin':  # macOS
            dns_settings = subprocess.check_output(['scutil --dns']).decode('utf-8')
        elif platform.system() == 'Windows':  # Windows
            dns_settings = subprocess.check_output("ipconfig /all", shell=True, text=True)
        else:
            dns_settings = "Not available for this platform."
        save_to_json({"dns_settings": dns_settings})
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

# 36. Gateway Information
def get_gateway_info():
    append_comment("Gateway Information")
    try:
        if platform.system() == 'Darwin':  # macOS
            gateway_info = subprocess.check_output(['netstat', '-nr']).decode('utf-8')
        elif platform.system() == 'Windows':  # Windows
            gateway_info = subprocess.check_output("ipconfig", shell=True, text=True)
        else:
            gateway_info = "Not available for this platform."
        save_to_json({"gateway_info": gateway_info})
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

# 37. DHCP Lease Information
def get_dhcp_lease():
    append_comment("DHCP Lease Information")
    try:
        if platform.system() == 'Darwin':  # macOS
            dhcp_lease = subprocess.check_output(['ipconfig', 'getpacket', 'en0']).decode('utf-8')
        elif platform.system() == 'Windows':  # Windows
            dhcp_lease = subprocess.check_output("ipconfig /all", shell=True, text=True)
        else:
            dhcp_lease = "Not available for this platform."
        save_to_json({"dhcp_lease": dhcp_lease})
    except Exception as e:
        save_to_json({"error": str(e)})
        add_log_entry({"error": str(e)})

# 38. Get Google Chrome History
def get_chrome_history():
    append_comment("Google Chrome History")
    try:
        if os.name == 'nt':  # Windows
            app_data_path = os.getenv('LOCALAPPDATA')
            chrome_path = os.path.join(app_data_path, 'Google', 'Chrome', 'User Data', 'Default', 'History')
        else:  # macOS
            chrome_path = os.path.expanduser('~/Library/Application Support/Google/Chrome/Default/History')

        connection = sqlite3.connect(chrome_path)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM urls')
        rows = cursor.fetchall()

        history = []
        for row in rows:
            history.append({
                "url": row[1],
                "title": row[2],
                "visit_count": row[3],
                "last_visit_time": row[4]
            })
        
        save_to_json({"chrome_history": history})
        connection.close()
    except Exception as e:
        save_to_json({"chrome_history_error": str(e)})
        add_log_entry({"error": str(e)})

# 39. Get Brave Browser History
def get_brave_history():
    append_comment("Brave Browser History")
    try:
        if os.name == 'nt':  # Windows
            app_data_path = os.getenv('LOCALAPPDATA')
            brave_path = os.path.join(app_data_path, 'BraveSoftware', 'Brave-Browser', 'User Data', 'Default', 'History')
        else:  # macOS
            brave_path = os.path.expanduser('~/Library/Application Support/BraveSoftware/Brave-Browser/Default/History')

        connection = sqlite3.connect(brave_path)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM urls')
        rows = cursor.fetchall()

        history = []
        for row in rows:
            history.append({
                "url": row[1],
                "title": row[2],
                "visit_count": row[3],
                "last_visit_time": row[4]
            })
        
        save_to_json({"brave_history": history})
        connection.close()
    except Exception as e:
        save_to_json({"brave_history_error": str(e)})
        add_log_entry({"error": str(e)})

# 40. Get Microsoft Edge History
def get_edge_history():
    append_comment("Microsoft Edge History")
    try:
        if os.name == 'nt':  # Windows
            app_data_path = os.getenv('LOCALAPPDATA')
            edge_path = os.path.join(app_data_path, 'Microsoft', 'Edge', 'User Data', 'Default', 'History')
        else:  # macOS
            edge_path = os.path.expanduser('~/Library/Application Support/Microsoft Edge/Default/History')

        connection = sqlite3.connect(edge_path)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM urls')
        rows = cursor.fetchall()

        history = []
        for row in rows:
            history.append({
                "url": row[1],
                "title": row[2],
                "visit_count": row[3],
                "last_visit_time": row[4]
            })
        
        save_to_json({"edge_history": history})
        connection.close()
    except Exception as e:
        save_to_json({"edge_history_error": str(e)})
        add_log_entry({"error": str(e)})

# 41. Get Safari History
def get_safari_history():
    append_comment("Safari History")
    try:
        if os.name != 'nt':  # macOS
            safari_path = os.path.expanduser('~/Library/Safari/History.db')

            connection = sqlite3.connect(safari_path)
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM history_items')
            rows = cursor.fetchall()

            history = []
            for row in rows:
                history.append({
                    "url": row[2],
                    "title": row[3],
                    "visit_count": row[4],
                    "last_visit_time": row[5]
                })

            save_to_json({"safari_history": history})
            connection.close()
    except Exception as e:
        save_to_json({"safari_history_error": str(e)})
        add_log_entry({"error": str(e)})

# 42. Get Opera History
def get_opera_history():
    append_comment("Opera History")
    try:
        if os.name == 'nt':  # Windows
            app_data_path = os.getenv('APPDATA')
            opera_path = os.path.join(app_data_path, 'Opera Software', 'Opera Stable', 'History')
        else:  # macOS
            opera_path = os.path.expanduser('~/Library/Application Support/com.operasoftware.Opera/History')

        connection = sqlite3.connect(opera_path)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM urls')
        rows = cursor.fetchall()

        history = []
        for row in rows:
            history.append({
                "url": row[1],
                "title": row[2],
                "visit_count": row[3],
                "last_visit_time": row[4]
            })

        save_to_json({"opera_history": history})
        connection.close()
    except Exception as e:
        save_to_json({"opera_history_error": str(e)})
        add_log_entry({"error": str(e)})


class MainApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        add_log_entry("Main app started.")
        def center_window(window, width, height):
            # Get the screen width and height
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()

            # Calculate the x and y positions for the window to be centered
            x = (screen_width - width) // 2
            y = (screen_height - height) // 2

            # Set the window geometry
        self.title("Data Finder")
        window_width = 1200
        window_height = 750
        self.geometry(f"{window_width}x{window_height}")
        center_window(self, window_width, window_height)

        font_name = "Calibri"
        def check_and_execute():
            add_log_entry("Execute started.")
            open(OUTPUT_JSON_PATH, 'w').close()
            if self.switch_get_os_info.get():
                get_os_info()
            if self.switch_get_cpu_info.get():
                get_cpu_info()
            if self.switch_get_memory_info.get():
                get_memory_info()
            if self.switch_get_disk_info.get():
                get_disk_info()
            if self.switch_get_gpu_info.get():
                get_gpu_info()
            if self.switch_get_display_info.get():
                get_display_info()
            if self.switch_get_bios_info.get():
                #get_bios_info()
                pass
            if self.switch_get_motherboard_info.get():
                get_motherboard_info()
            if self.switch_get_network_configuration.get():
                get_network_configuration()
            if self.switch_get_installed_software.get():
                get_installed_software()
            if self.switch_get_filesystem_usage.get():
                get_filesystem_usage()
            if self.switch_get_system_events.get():
                get_system_events()
            if self.switch_get_graphics_card_info.get():
                get_graphics_card_info()
            if self.switch_get_storage_devices_info.get():
                get_storage_devices_info()
            if self.switch_get_dns_settings.get():
                get_dns_settings()
            if self.switch_get_gateway_info.get():
                get_gateway_info()
            if self.switch_get_dhcp_lease.get():
                get_dhcp_lease()

            # Process and Usage Information
            if self.get_environment_variables.get():
                get_environment_variables()
            if self.switch_get_system_paths.get():
                get_system_paths()
            if self.get_python_version.get():
                get_python_version()
            if self.get_installed_packages.get():
                get_installed_packages()
            if self.get_running_processes.get():
                get_running_processes()
            if self.get_cpu_usage.get():
                get_cpu_usage()
            if self.get_memory_usage.get():
                get_memory_usage()
            if self.get_disk_usage.get():
                get_disk_usage()
            if self.get_filesystem_type.get():
                get_filesystem_type()
            if self.get_boot_time.get():
                get_boot_time()
            if self.get_users.get():
                get_users()
            if self.get_system_uptime.get():
                get_system_uptime()
            if self.get_battery_info.get():
                get_battery_info()
            if self.get_audio_devices.get():
                get_audio_devices()

            # Network Information
            if self.get_ip_address.get():
                get_ip_address()
            if self.get_mac_address.get():
                get_mac_address()
            if self.get_network_interfaces.get():
                get_network_interfaces()
            if self.get_network_speed.get():
                get_network_speed()
            if self.get_network_usage.get():
                get_network_usage()

            # USB and Other Devices
            if self.get_usb_devices.get():
                get_usb_devices()

            # Web data
            if self.get_chrome_history.get():
                get_chrome_history()
            if self.get_brave_history.get():
                get_brave_history()
            if self.get_edge_history.get():
                get_edge_history()
            if self.get_safari_history.get():
                get_safari_history()
            if self.get_opera_history.get():
                get_opera_history()

        def select_all_switches():
            # Select all switches in the system information frame
            self.switch_get_os_info.select()
            self.switch_get_cpu_info.select()
            self.switch_get_memory_info.select()
            self.switch_get_disk_info.select()
            self.switch_get_gpu_info.select()
            self.switch_get_display_info.select()
            self.switch_get_bios_info.select()
            self.switch_get_motherboard_info.select()
            self.switch_get_network_configuration.select()
            self.switch_get_installed_software.select()
            self.switch_get_filesystem_usage.select()
            self.switch_get_system_events.select()
            self.switch_get_graphics_card_info.select()
            self.switch_get_storage_devices_info.select()
            self.switch_get_dns_settings.select()
            self.switch_get_gateway_info.select()
            self.switch_get_dhcp_lease.select()

            # Select all switches in the process and usage information frame
            self.get_environment_variables.select()
            self.switch_get_system_paths.select()
            self.get_python_version.select()
            self.get_installed_packages.select()
            self.get_running_processes.select()
            self.get_cpu_usage.select()
            self.get_memory_usage.select()
            self.get_disk_usage.select()
            self.get_filesystem_type.select()
            self.get_boot_time.select()
            self.get_users.select()
            self.get_system_uptime.select()
            self.get_battery_info.select()
            self.get_audio_devices.select()

            # Select all switches in the network information frame
            self.get_ip_address.select()
            self.get_mac_address.select()
            self.get_network_interfaces.select()
            self.get_network_speed.select()
            self.get_network_usage.select()

            # Select all switches in the USB and other devices frame
            self.get_usb_devices.select()

            # Select all switches in the web information frame
            self.get_chrome_history.select()
            self.get_brave_history.select()
            self.get_edge_history.select()
            self.get_safari_history.select()
            self.get_opera_history.select()


        def deselect_all_switches():
            # Deselect all switches in the system information frame
            self.switch_get_os_info.deselect()
            self.switch_get_cpu_info.deselect()
            self.switch_get_memory_info.deselect()
            self.switch_get_disk_info.deselect()
            self.switch_get_gpu_info.deselect()
            self.switch_get_display_info.deselect()
            self.switch_get_bios_info.deselect()
            self.switch_get_motherboard_info.deselect()
            self.switch_get_network_configuration.deselect()
            self.switch_get_installed_software.deselect()
            self.switch_get_filesystem_usage.deselect()
            self.switch_get_system_events.deselect()
            self.switch_get_graphics_card_info.deselect()
            self.switch_get_storage_devices_info.deselect()
            self.switch_get_dns_settings.deselect()
            self.switch_get_gateway_info.deselect()
            self.switch_get_dhcp_lease.deselect()

            # Deselect all switches in the process and usage information frame
            self.get_environment_variables.deselect()
            self.switch_get_system_paths.deselect()
            self.get_python_version.deselect()
            self.get_installed_packages.deselect()
            self.get_running_processes.deselect()
            self.get_cpu_usage.deselect()
            self.get_memory_usage.deselect()
            self.get_disk_usage.deselect()
            self.get_filesystem_type.deselect()
            self.get_boot_time.deselect()
            self.get_users.deselect()
            self.get_system_uptime.deselect()
            self.get_battery_info.deselect()
            self.get_audio_devices.deselect()

            # Deselect all switches in the network information frame
            self.get_ip_address.deselect()
            self.get_mac_address.deselect()
            self.get_network_interfaces.deselect()
            self.get_network_speed.deselect()
            self.get_network_usage.deselect()

            # Deselect all switches in the USB and other devices frame
            self.get_usb_devices.deselect()

            # Deselect all switches in the web information frame
            self.get_chrome_history.deselect()
            self.get_brave_history.deselect()
            self.get_edge_history.deselect()
            self.get_safari_history.deselect()
            self.get_opera_history.deselect()


        # Create GUI elements
# Main GUI elements
        self.main_frame = customtkinter.CTkFrame(self, width=1180, height=50)
        self.main_frame.place(x=10, y=10)

        self.main_lable = customtkinter.CTkLabel(master=self.main_frame, text="Data selection", font=(font_name, 35))
        self.main_lable.place(x=485, y=2)

        self.main_execute_button = customtkinter.CTkButton(master=self.main_frame, text="Run", font=(font_name, 25), command=check_and_execute)
        self.main_execute_button.place(x=1030, y=7)

        self.main_select_all_button = customtkinter.CTkButton(master=self.main_frame, text="Select All", font=(font_name, 20), command=select_all_switches)
        self.main_select_all_button.place(x=10, y=10)

        self.main_deselect_all_button = customtkinter.CTkButton(master=self.main_frame, text="Deselect All", font=(font_name, 20), command=deselect_all_switches)
        self.main_deselect_all_button.place(x=200, y=10)

        self.main_show_output_button = customtkinter.CTkButton(master=self.main_frame, text="Show Output", font=(font_name, 20), command=show_output)
        self.main_show_output_button.place(x=850, y=10)

# System Information GUI elements
        self.system_information_frame = customtkinter.CTkFrame(self, width=585, height=400)
        self.system_information_frame.place(x=10, y=70)

        self.system_info_lable = customtkinter.CTkLabel(master=self.system_information_frame, text="System Information", font=(font_name,20))
        self.system_info_lable.place(x=180, y=5)

        self.switch_get_os_info = customtkinter.CTkSwitch(master=self.system_information_frame, text="Get os info", font=(font_name, 13))
        self.switch_get_os_info.place(x=25, y=40)

        self.switch_get_cpu_info = customtkinter.CTkSwitch(master=self.system_information_frame, text="Get cpu info", font=(font_name, 13))
        self.switch_get_cpu_info.place(x=25, y=80)

        self.switch_get_memory_info = customtkinter.CTkSwitch(master=self.system_information_frame, text="Get memory info", font=(font_name, 13))
        self.switch_get_memory_info.place(x=25, y=120)

        self.switch_get_disk_info = customtkinter.CTkSwitch(master=self.system_information_frame, text="Get disk info", font=(font_name, 13))
        self.switch_get_disk_info.place(x=25, y=160)

        self.switch_get_gpu_info = customtkinter.CTkSwitch(master=self.system_information_frame, text="Get gpu info", font=(font_name, 13))
        self.switch_get_gpu_info.place(x=25, y=200)

        self.switch_get_display_info = customtkinter.CTkSwitch(master=self.system_information_frame, text="Get display info", font=(font_name, 13))
        self.switch_get_display_info.place(x=25, y=240)

        self.switch_get_bios_info = customtkinter.CTkSwitch(master=self.system_information_frame, text="Get bios info", font=(font_name, 13))
        self.switch_get_bios_info.place(x=25, y=280)

        self.switch_get_motherboard_info = customtkinter.CTkSwitch(master=self.system_information_frame, text="Get motherboard info", font=(font_name, 13))
        self.switch_get_motherboard_info.place(x=25, y=320)

        self.switch_get_network_configuration = customtkinter.CTkSwitch(master=self.system_information_frame, text="Get network configuration", font=(font_name, 13))
        self.switch_get_network_configuration.place(x=25, y=360)

        self.switch_get_installed_software = customtkinter.CTkSwitch(master=self.system_information_frame, text="Get installed software", font=(font_name, 13))
        self.switch_get_installed_software.place(x=350, y=40)

        self.switch_get_filesystem_usage = customtkinter.CTkSwitch(master=self.system_information_frame, text="Get filesystem usage", font=(font_name, 13))
        self.switch_get_filesystem_usage.place(x=350, y=80)

        self.switch_get_system_events = customtkinter.CTkSwitch(master=self.system_information_frame, text="Get system events", font=(font_name, 13))
        self.switch_get_system_events.place(x=350, y=120)

        self.switch_get_graphics_card_info = customtkinter.CTkSwitch(master=self.system_information_frame, text="Get graphics card info", font=(font_name, 13))
        self.switch_get_graphics_card_info.place(x=350, y=160)

        self.switch_get_storage_devices_info = customtkinter.CTkSwitch(master=self.system_information_frame, text="Get storage devices info", font=(font_name, 13))
        self.switch_get_storage_devices_info.place(x=350, y=200)

        self.switch_get_dns_settings = customtkinter.CTkSwitch(master=self.system_information_frame, text="Get DNS settings", font=(font_name, 13))
        self.switch_get_dns_settings.place(x=350, y=240)

        self.switch_get_gateway_info = customtkinter.CTkSwitch(master=self.system_information_frame, text="Get gateway info", font=(font_name, 13))
        self.switch_get_gateway_info.place(x=350, y=280)

        self.switch_get_dhcp_lease = customtkinter.CTkSwitch(master=self.system_information_frame, text="Get DHCP lease", font=(font_name, 13))
        self.switch_get_dhcp_lease.place(x=350, y=320)


# Process and Usage Information GUI elements
        self.process_and_usage_information_frame = customtkinter.CTkFrame(self, width=580, height=400)
        self.process_and_usage_information_frame.place(x=610, y=70)

        self.system_info_lable = customtkinter.CTkLabel(master=self.process_and_usage_information_frame, text="Process and Usage Information", font=(font_name,20))
        self.system_info_lable.place(x=140, y=5)

        self.get_environment_variables = customtkinter.CTkSwitch(master=self.process_and_usage_information_frame, text="Get Environment variables", font=(font_name, 13))
        self.get_environment_variables.place(x=25, y=40)

        self.switch_get_system_paths = customtkinter.CTkSwitch(master=self.process_and_usage_information_frame, text="Get system paths", font=(font_name, 13))
        self.switch_get_system_paths.place(x=25, y=80)

        self.get_python_version = customtkinter.CTkSwitch(master=self.process_and_usage_information_frame, text="Get Python version", font=(font_name, 13))
        self.get_python_version.place(x=25, y=120)

        self.get_installed_packages = customtkinter.CTkSwitch(master=self.process_and_usage_information_frame, text="Get installed packages", font=(font_name, 13))
        self.get_installed_packages.place(x=25, y=160)

        self.get_running_processes = customtkinter.CTkSwitch(master=self.process_and_usage_information_frame, text="Get running processes", font=(font_name, 13))
        self.get_running_processes.place(x=25, y=200)

        self.get_cpu_usage = customtkinter.CTkSwitch(master=self.process_and_usage_information_frame, text="Get CPU usage", font=(font_name, 13))
        self.get_cpu_usage.place(x=25, y=240)

        self.get_memory_usage = customtkinter.CTkSwitch(master=self.process_and_usage_information_frame, text="Get memory usage", font=(font_name, 13))
        self.get_memory_usage.place(x=25, y=280)

        self.get_disk_usage = customtkinter.CTkSwitch(master=self.process_and_usage_information_frame, text="Get disk usage", font=(font_name, 13))
        self.get_disk_usage.place(x=25, y=320)

        self.get_filesystem_type = customtkinter.CTkSwitch(master=self.process_and_usage_information_frame, text="Get filesystem type", font=(font_name, 13))
        self.get_filesystem_type.place(x=25, y=360)

        self.get_boot_time = customtkinter.CTkSwitch(master=self.process_and_usage_information_frame, text="Get boot time", font=(font_name, 13))
        self.get_boot_time.place(x=350, y=40)

        self.get_users = customtkinter.CTkSwitch(master=self.process_and_usage_information_frame, text="Get users", font=(font_name, 13))
        self.get_users.place(x=350, y=80)

        self.get_system_uptime = customtkinter.CTkSwitch(master=self.process_and_usage_information_frame, text="Get system uptime", font=(font_name, 13))
        self.get_system_uptime.place(x=350, y=120)

        self.get_battery_info = customtkinter.CTkSwitch(master=self.process_and_usage_information_frame, text="Get battery info", font=(font_name, 13))
        self.get_battery_info.place(x=350, y=160)

        self.get_audio_devices = customtkinter.CTkSwitch(master=self.process_and_usage_information_frame, text="Get audio devices", font=(font_name, 13))
        self.get_audio_devices.place(x=350, y=200)


# Network Information GUI elements
        self.network_information_frame = customtkinter.CTkFrame(self, width=585, height=260)
        self.network_information_frame.place(x=10, y=480)

        self.network_information_lable = customtkinter.CTkLabel(master=self.network_information_frame, text="Network Information", font=(font_name,20))
        self.network_information_lable.place(x=200, y=5)

        self.get_ip_address = customtkinter.CTkSwitch(master=self.network_information_frame, text="Get IP address", font=(font_name, 13))
        self.get_ip_address.place(x=25, y=40)

        self.get_mac_address = customtkinter.CTkSwitch(master=self.network_information_frame, text="Get MAC address", font=(font_name, 13))
        self.get_mac_address.place(x=25, y=80)

        self.get_network_interfaces = customtkinter.CTkSwitch(master=self.network_information_frame, text="Get network interfaces", font=(font_name, 13))
        self.get_network_interfaces.place(x=25, y=120)

        self.get_network_speed = customtkinter.CTkSwitch(master=self.network_information_frame, text="Get network speed", font=(font_name, 13))
        self.get_network_speed.place(x=25, y=160)

        self.get_network_usage = customtkinter.CTkSwitch(master=self.network_information_frame, text="Get network usage", font=(font_name, 13))
        self.get_network_usage.place(x=25, y=200)


# USB and other devices Information GUI elements
        self.USB_and_other_devices_frame = customtkinter.CTkFrame(self, width=285, height=260)
        self.USB_and_other_devices_frame.place(x=610, y=480)

        self.USB_and_other_devices_lable = customtkinter.CTkLabel(master=self.USB_and_other_devices_frame, text="USB and other devices", font=(font_name,20))
        self.USB_and_other_devices_lable.place(x=43, y=5)

        self.get_usb_devices = customtkinter.CTkSwitch(master=self.USB_and_other_devices_frame, text="Get USB devices", font=(font_name, 13))
        self.get_usb_devices.place(x=25, y=40)

# Web Information GUI elements
        self.web_information_frame = customtkinter.CTkFrame(self, width=285, height=260)
        self.web_information_frame.place(x=905, y=480)

        self.web_information_lable = customtkinter.CTkLabel(master=self.web_information_frame, text="Web information", font=(font_name,20))
        self.web_information_lable.place(x=65, y=5)

        self.get_chrome_history = customtkinter.CTkSwitch(master=self.web_information_frame, text="Get Chrome history", font=(font_name, 13))
        self.get_chrome_history.place(x=25, y=40)

        self.get_brave_history = customtkinter.CTkSwitch(master=self.web_information_frame, text="Get Brave history", font=(font_name, 13))
        self.get_brave_history.place(x=25, y=80)

        self.get_edge_history = customtkinter.CTkSwitch(master=self.web_information_frame, text="Get Edge history", font=(font_name, 13))
        self.get_edge_history.place(x=25, y=120)

        self.get_safari_history = customtkinter.CTkSwitch(master=self.web_information_frame, text="Get Safari history", font=(font_name, 13))
        self.get_safari_history.place(x=25, y=160)

        self.get_opera_history = customtkinter.CTkSwitch(master=self.web_information_frame, text="Get Opera history", font=(font_name, 13))
        self.get_opera_history.place(x=25, y=200)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()