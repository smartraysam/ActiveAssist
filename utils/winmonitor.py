import wmi
import platform
import subprocess
import psutil
import locale

# Get the account name of the current user
def get_account_name():
    return psutil.users()[0].name

# Get the BIOS caption
def get_bios_caption():
    c = wmi.WMI()
    bios = c.Win32_BIOS()[0]
    return bios.Caption

# Get the BIOS manufacturer
def get_bios_maker():
    c = wmi.WMI()
    bios = c.Win32_BIOS()[0]
    return bios.Manufacturer

# Get the BIOS serial number
def get_bios_serial_number():
    c = wmi.WMI()
    bios = c.Win32_BIOS()[0]
    return bios.SerialNumber

# Get the board product ID
def get_board_product_id():
    c = wmi.WMI()
    board = c.Win32_BaseBoard()[0]
    return board.Product

# Get the board manufacturer
def get_board_maker():
    c = wmi.WMI()
    board = c.Win32_BaseBoard()[0]
    return board.Manufacturer

# Get the CD/DVD-ROM drive information
def get_cdrom_drive():
    c = wmi.WMI()
    for drive in c.Win32_CDROMDrive():
        return drive.Name

# Get the computer name
def get_computer_name():
    return platform.node()

# Get the current CPU clock speed
def get_cpu_current_clock_speed():
    c = wmi.WMI()
    cpu = c.Win32_Processor()[0]
    return cpu.CurrentClockSpeed

# Get the CPU manufacturer
def get_cpu_manufacturer():
    c = wmi.WMI()
    cpu = c.Win32_Processor()[0]
    return cpu.Manufacturer

# Get the CPU speed in GHz
def get_cpu_speed_in_ghz():
    c = wmi.WMI()
    cpu = c.Win32_Processor()[0]
    return cpu.MaxClockSpeed / 1000.0

# Get the HDD serial number
def get_hdd_serial_number():
    result = subprocess.check_output(['wmic', 'diskdrive', 'get', 'serialnumber'])
    serial_numbers = result.decode().strip().split('\n')[1:]
    return serial_numbers[0].strip()

# Get the MAC address
def get_mac_address():
    for interface in psutil.net_if_addrs().values():
        for addr in interface:
            if addr.family == psutil.AF_LINK:
                return addr.address

# Get the OS information
def get_os_information():
    return platform.platform()

# Get the physical memory (RAM) in bytes
def get_physical_memory():
    return str(psutil.virtual_memory().total/(1024 * 1024))

# Get the processor ID
def get_processor_id():
    c = wmi.WMI()
    processor = c.Win32_Processor()[0]
    return processor.ProcessorId

# Get the processor information
def get_processor_information():
    c = wmi.WMI()
    processor = c.Win32_Processor()[0]
    return processor.Name

# Get the number of RAM slots
def get_no_ram_slots():
    c = wmi.WMI()
    memory = c.Win32_PhysicalMemory()
    return len(memory)

# Get the current language
def get_current_language():
    return locale.getlocale()[0]



def get_available_ram():
    remain_ram = ""
    try:
        virtual_memory = psutil.virtual_memory()
        free_ram = virtual_memory.available / (1024 * 1024)  # Convert to MB
        remain_ram = str(free_ram)
    except Exception as exception:
        pass
    return remain_ram


def get_cpu_usage():
    value_use = ""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        value_use = str(cpu_percent)
    except Exception as exception:
        pass
    return value_use

def get_pc_space():
    drive_info = psutil.disk_usage('/')
    total_free_space = drive_info.free / (1024 * 1024 * 1024)  # Convert to GB
    return str(total_free_space) + "GB"
