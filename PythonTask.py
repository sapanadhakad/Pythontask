import subprocess
import platform
import psutil
import requests
import win32api
import getmac
import socket
import speedtest
from screeninfo import get_monitors
import wmi
import math

def execute_system_command(command):
    return subprocess.run(command, stdout=subprocess.PIPE, text=True, shell=True).stdout.strip()

def retrieve_network_information():
    mac_address = getmac.get_mac_address()
    public_ip = socket.gethostbyname(socket.gethostname())
    return f'MAC Address: {mac_address}, Public IP: {public_ip}'

def fetch_installed_programs():
    software_info = execute_system_command('wmic product get name,version') or "No installed software found."
    return software_info

def measure_internet_speed():
    st = speedtest.Speedtest()
    download_speed = st.download() / 10**6
    upload_speed = st.upload() / 10**6
    return f'Download Speed: {download_speed:.2f} Mbps, Upload Speed: {upload_speed:.2f} Mbps'

def determine_screen_dimensions():
    return win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)

def inspect_cpu():
    return platform.processor(), psutil.cpu_count(logical=False), psutil.cpu_count(logical=True)

def identify_graphics_card():
    try:
        gpu_info = wmi.WMI().Win32_VideoController()[0].name
        return gpu_info
    except Exception as e:
        return None

def get_memory_size():
    return round(psutil.virtual_memory().total / (1024**3), 2)

def retrieve_screen_sizes():
    monitors = get_monitors()
    sizes = set((monitor.width, monitor.height) for monitor in monitors)
    return ', '.join(f"{width}x{height}" for width, height in sizes)

def obtain_mac_address():
    return getmac.get_mac_address()

def fetch_public_ip():
    return requests.get("https://api.ipify.org").text

def determine_windows_version():
    return platform.platform()

def main():
    system_info = {
        "Installed Programs": fetch_installed_programs(),
        "Internet Speed": measure_internet_speed(),
        "Screen Dimensions": determine_screen_dimensions(),
        "CPU Model": inspect_cpu()[0],
        "CPU Cores": inspect_cpu()[1],
        "CPU Threads": inspect_cpu()[2],
        "Graphics Card Model": identify_graphics_card(),
        "RAM Size": get_memory_size(),
        "Screen Sizes": retrieve_screen_sizes(),
        "MAC Address": obtain_mac_address(),
        "Public IP Address": fetch_public_ip(),
        "Windows Version": determine_windows_version()
    }

    for key, value in system_info.items():
        print(f"{key}:\n{value}\n")

if __name__ == "__main__":
    main()
