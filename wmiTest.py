import platform
import subprocess
import wmi


def sys_service(server, username, password):
    c = wmi.WMI(computer=server, user=username, password=password)
    for s in c.Win32_Service():
        if s.State == 'Stopped':
            print(s.Caption, s.State)


def sys_version(server, username, password):
    c = wmi.WMI(computer=server, user=username, password=password)
    # 获取操作系统版本
    for sys in c.Win32_OperatingSystem():
        print("Version:%s" % sys.Caption.encode("UTF"), "Vernum:%s" % sys.BuildNumber)
        print(sys.OSArchitecture.encode("UTF"))  # 系统是位还是位的
        print(sys.NumberOfProcesses)  # 当前系统运行的进程总数


def cpu_mem(server, username, password):
    c = wmi.WMI(computer=server, user=username, password=password)
    # CPU类型和内存
    for processor in c.Win32_Processor():
        # print "Processor ID: %s" % processor.DeviceID
        print("Process Name: %s" % processor.Name.strip())
        for Memory in c.Win32_PhysicalMemory():
            print("Memory Capacity: %.fMB" % (int(Memory.Capacity)))


def network(server, username, password):
    c = wmi.WMI(computer=server, user=username, password=password)
    # 获取MAC和IP地址
    for interface in c.Win32_NetworkAdapterConfiguration(IPEnabled=True):
        print("MAC: %s" % interface.MACAddress)
        for ip_address in interface.IPAddress:
            print("ip_add: %s" % ip_address)


def w_disk(server, username, password):
    c = wmi.WMI(computer=server, user=username, password=password)
    i = 0
    # 获取磁盘信息
    for disk in c.Win32_LogicalDisk(DriveType=3):
        print(disk)
        print(disk.size + 'byte')
        # 可用大小G
        a = round(int(disk.FreeSpace) / (1024 * 1024 * 1024), 2)
        print(str(a) + 'G')
        # 可用大小%
        b = int(100.0 * float(disk.FreeSpace) / float(disk.Size))
        print(str(b) + '%')
        if disk.Caption == "C:":
            if (a < 2) or (b < 10):
                i += 1
            else:
                i += 0
        else:
            if (a < 10) or (b < 10):
                i += 1
            else:
                i += 0
    print(i)


def L_disk():
    free = subprocess.getstatusoutput('df -h|grep dev|egrep -v "tmp|var|shm"')
    list = free[1].split('\n')
    i = 0
    for disk in range(len(list)):
        vd = list[disk][6:8]
        a = list[disk].split()[3]
        if a[-1] == 'T':
            a = int(float(a[:-1])) * 1024
        else:
            a = int(float(a[:-1]))
            b = 100 - int(list[disk].split()[4][:-1])
        if vd == "da":
            if (a < 2) or (b < 10):
                i += 1
            else:
                i += 0
        else:
            if (a < 10) or (b < 10):
                i += 1
    else:
        i += 0
    print(i)


def watchFile(server, username, password):
    c = wmi.WMI(computer=server, user=username, password=password)
    filename = r"c:\temp\temp.txt"
    process = c.Win32_Process
    process_id, result = process.Create(CommandLine="notepad.exe " + filename)
    watcher = c.watch_for(
        notification_type="Deletion",
        wmi_class="Win32_Process",
        delay_secs=1,
        ProcessId=process_id
    )

    watcher()
    print("This is what you wrote:")
    print(open(filename).read())


def startNotepad(server, username, password):
    c = wmi.WMI(computer=server, user=username, password=password)
    process = c.Win32_Process
    #process_id, result = process.Create(CommandLine=r"cmd /c ping 10.0.0.1 -n 1 > c:\temp\temp.txt")
    #process_id, result = process.Create(CommandLine=r"cmd /c c:\mk.bat > c:\temp.txt")
    #process_id, result = process.Create(CommandLine=r"cmd /c netstat -aon |findstr 00 > c:\temp.txt")
    result= process.Create(CommandLine=r"cmd /c netstat -aon |findstr 00 > c:\temp.txt")
    print(result)


if __name__ == "__main__":
    os = platform.system()
    if os == "Windows":

        # sys_version('9.110.179.98','administrator','Password123')
        # cpu_mem()
        # network()
        # services()
        # watchFile()
        # cpu_mem('9.110.179.98','administrator','Password123')
        # cpu_mem('','','')
        # w_disk('9.110.179.98','administrator','Password123')
        # w_disk()
        #startNotepad('9.110.179.98', 'administrator', 'Password123')
        startNotepad('', '', '')
    elif os == "Linux":
        L_disk()
