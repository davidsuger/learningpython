import wmi
import os
import time
import shutil

c = None


# mount server disk to local
def mountDisktoLocal(driver, server, username, password):
    c = wmi.WMI()
    process = c.Win32_Process
    # process_id, result = process.Create(CommandLine=r"cmd /c ping 10.0.0.1 -n 1 > c:\temp\temp.txt")
    # process_id, result = process.Create(CommandLine=r"cmd /c c:\mk.bat > c:\temp.txt")
    # process_id, result = process.Create(CommandLine=r"cmd /c netstat -aon |findstr 00 > c:\temp.txt")
    # print(r"net use " + driver + r": \\" + server + r"\c$ " + password + r" /user:" + username + r' > c:\temp.txt')
    # result = process.Create(CommandLine=r"net use p: \\9.110.179.98\c$ Password123 /user:administrator > c:\temp.txt")
    f = open('script.bat', 'w')
    f.write(r"cmd /c net use {0}: \\{1}\c$ {3} /user:{2}".format(driver, server, username, password))
    f.close()
    if os.path.exists('c:/testlog/'):
        pass
    else:
        os.makedirs('c:/testlog/')
    result = process.Create(
        CommandLine=r"cmd /c " + os.path.abspath(os.curdir) + r"\script.bat > c:\testlog\mountDisktoLocal.txt")
    if checkMountDiskAvailable(driver) == True:
        print('Server disk mount complete.')
    else:
        print('Server disk mount timeout.')



def checkMountDiskAvailable(driver):
    c = wmi.WMI()
    diskAvailable = False
    for i in range(1, 10):
        for sys in c.Win32_MappedLogicalDisk():
            if sys:
                diskAvailable = True
                return diskAvailable
        time.sleep(2)
    return diskAvailable


# remove server disk to local
def removeLocalDisk(driver):
    c = wmi.WMI()
    process = c.Win32_Process
    f = open('script.bat', 'w')
    f.write(r"net use p: /delete /y")
    f.close()
    if os.path.exists('c:/testlog/'):
        pass
    else:
        os.makedirs('c:/testlog/')
    result = process.Create(
        CommandLine=r"cmd /c " + os.path.abspath(os.curdir) + r"\script.bat > c:\testlog\removeLocalDiskt.txt")
    print('Server disk remove complete.')


def creatScriptInServer(driver, script):
    global c
    # Create bat in remote server
    if os.path.exists(driver + ':/testlog/'):
        pass
    else:
        os.makedirs(driver + ':/testlog/')
    f = open(driver + ':/testlog/script.bat', 'w')
    f.write(script)
    f.close()
    print('Command: ' + script)
    print('bat file created in server disk complete.')


def connectToRemoteServer(server, username, password):
    global c
    c = wmi.WMI(computer=server, user=username, password=password)
    return c


def runScriptInServer():
    global c
    process = c.Win32_Process
    result = process.Create(CommandLine=r"cmd /c c:\testlog\script.bat")
    print('bat file run in server complete.')


def getTestLog(driver):
    testlog = open(driver + r':\testlog\log.txt')
    print('This is test log:==================')
    print(testlog.read())
    print('Testlog end.=======================')
    testlog.close()


def clear(driver):
    shutil.rmtree(driver + r':\testlog')
    print('Testlog removed.')


# def copyEXEFile(driver):
#     shutil.copy('capturescreen.exe', driver + r':\testlog')


# def runEXE(server, username, password):
#     c = wmi.WMI(computer=server, user=username, password=password)
#     process = c.Win32_Process
#     result = process.Create(CommandLine=r"cmd /c c:\testlog\capturescreen.exe")
#     print('bat file run in server complete.')

def getIPInfo():
    global c
    # 获取MAC和IP地址
    print('This is test log:==================')
    for interface in c.Win32_NetworkAdapterConfiguration(IPEnabled=True):
        # print(interface)
        print("MAC: %s" % interface.MACAddress)
        for ip_address in interface.IPAddress:
            print("ip_add: %s" % ip_address)
    print('Testlog end.=======================')


def getOSVersion():
    global c
    print('This is test log:==================')
    # 获取操作系统版本
    for sys in c.Win32_OperatingSystem():
        print("Version:%s" % sys.Caption.encode("UTF"), "Vernum:%s" % sys.BuildNumber)
        print(sys.OSArchitecture.encode("UTF"))
    print('Testlog end.=======================')


def getCPU_MEM():
    global c
    print('This is test log:==================')
    # CPU类型和内存
    for processor in c.Win32_Processor():
        # print(processor)
        print("Process Name: %s" % processor.Name.strip())
        print("NumberOfCores: %s" % processor.NumberOfCores)
        print("NumberOfLogicalProcessors: %s" % processor.NumberOfLogicalProcessors)
    for Memory in c.Win32_PhysicalMemory():
        print("Memory Capacity: %.fMB" % (int(Memory.Capacity)))
    print('Testlog end.=======================')


# def testCaptureScreen():
#     mountDisktoLocal('p', '9.110.179.98', 'administrator', 'Password123')
#     copyEXEFile('p')
#     runEXE('9.110.179.98', 'administrator', 'Password123')
#     time.sleep(3)
#     removeLocalDisk('p')


if __name__ == '__main__':
    # mountDisktoLocal('p', '9.110.179.98', 'administrator', 'Password123')
    # # time.sleep(15)
    # # removeLocalDisk('p')
    # # time.sleep(3)
    # creatScriptInServer('9.110.179.98', 'administrator', 'Password123', 'script')
    # runScriptInServer('9.110.179.98', 'administrator', 'Password123')
    # removeLocalDisk('p')
    # checkMountDiskAvailable('p')
    # runEXE('', '', '')
    # testCaptureScreen()
    # testSample()
    # testSysteminfo()
    # testPort139()
    # testIP('9.110.179.98', 'administrator', 'Password123')
    # tesyOSVersion('9.110.179.98', 'administrator', 'Password123')
    TestCpu_Mem('9.110.179.98', 'administrator', 'Password123')
    TestCpu_Mem('', '', '')
