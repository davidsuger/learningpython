import wmi
import os
import time
import shutil


class Boi():
    def __init__(self):
        self.c = None
        self.driver = None
        self.server = None
        self.username = None
        self.password = None

    def connectToRemoteServer(self, server, username, password):
        self.c = wmi.WMI(computer=server, user=username, password=password)
        self.server = server
        self.username = username
        self.password = password

    # mount server disk to local
    def mountDisktoLocal(self, driver):
        c = wmi.WMI()
        self.driver = driver

        process = c.Win32_Process

        f = open('script.bat', 'w')
        f.write(r"cmd /c net use {0}: \\{1}\c$ {3} /user:{2}".format(driver, self.server, self.username, self.password))
        f.close()
        result = process.Create(
            CommandLine=r"cmd /c " + os.path.abspath(os.curdir) + r"\script.bat")
        if self.checkMountDiskAvailable(driver) == True:
            print('Server disk mount complete.')
        else:
            print('Server disk mount timeout.')

    def checkMountDiskAvailable(self, driver):
        c = wmi.WMI()
        diskAvailable = False
        for i in range(1, 30):
            for sys in c.Win32_MappedLogicalDisk():
                if sys:
                    diskAvailable = True
                    return diskAvailable
            time.sleep(2)
        return diskAvailable

    # remove server disk to local
    def removeLocalDisk(self):
        c = wmi.WMI()
        process = c.Win32_Process
        f = open('script.bat', 'w')
        f.write(r"net use " + self.driver + ": /delete /y")
        f.close()
        result = process.Create(
            CommandLine=r"cmd /c " + os.path.abspath(os.curdir) + r"\script.bat")
        print('Server disk remove complete.')

    def enableService(self, servicename):
        for service in self.c.Win32_Service(Name=servicename):
            if(service.StartMode =='Disabled'):
                return
            else:
                result, = service.ChangeStartMode('Manual')
                if result == 0:
                    print("Service", service.Name, "enabled")
                else:
                    print("Some problem")
                break
        else:
            print("Service not found")

    def startService(self, servicename):
        self.enableService(servicename)
        time.sleep(3)
        for service in self.c.Win32_Service(Name=servicename):
            if service.State =='Running':
                print("Service already running")
                return
            else:
                result, = service.StartService()
                if result == 0:
                    print("Service", service.Name, "started")
                else:
                    print("Some problem")
                break
        else:
            print("Service not found")

    def stopService(self, servicename):
        self.enableService(servicename)
        time.sleep(3)
        for service in self.c.Win32_Service(Name=servicename):
            if service.State =='Stopped':
                print("Service already Stopped")
                return
            else:
                result, = service.StopService()
                if result == 0:
                    print("Service", service.Name, "stopped")
                else:
                    print("Some problem")
                break
        else:
            print("Service not found")

    def creatScriptInServer(self, script):
        if os.path.exists(self.driver + ':/testlog/'):
            pass
        else:
            os.makedirs(self.driver + ':/testlog/')
        f = open(self.driver + ':/testlog/script.bat', 'w')
        f.write(script)
        f.close()
        print('Command: ' + script)
        print('bat file created in server disk complete.')

    def runScriptInServer(self):
        process = self.c.Win32_Process
        result = process.Create(CommandLine=r"cmd /c c:\testlog\script.bat")
        print('bat file run in server complete.')

    def getTestLog(self):
        testlog = open(self.driver + r':\testlog\log.txt')
        print('This is test log:==================')
        print(testlog.read())
        print('Testlog end.=======================')
        testlog.close()

    def clearTestlog(self):
        shutil.rmtree(self.driver + r':\testlog')
        print('Testlog removed.')

    def getIPInfo(self):
        # 获取MAC和IP地址
        print('This is test log:==================')
        for interface in self.c.Win32_NetworkAdapterConfiguration(IPEnabled=True):
            # print(interface)
            print("MAC: %s" % interface.MACAddress)
            for ip_address in interface.IPAddress:
                print("ip_add: %s" % ip_address)
        print('Testlog end.=======================')

    def getOSVersion(self):
        print('This is test log:==================')
        # 获取操作系统版本
        for sys in self.c.Win32_OperatingSystem():
            print("Version:%s" % sys.Caption.encode("UTF"), "Vernum:%s" % sys.BuildNumber)
            print(sys.OSArchitecture.encode("UTF"))
        print('Testlog end.=======================')

    def getCPU_MEM(self):
        print('This is test log:==================')
        # CPU类型和内存
        for processor in self.c.Win32_Processor():
            # print(processor)
            print("Process Name: %s" % processor.Name.strip())
            print("NumberOfCores: %s" % processor.NumberOfCores)
            print("NumberOfLogicalProcessors: %s" % processor.NumberOfLogicalProcessors)
        for Memory in self.c.Win32_PhysicalMemory():
            print("Memory Capacity: %.fMB" % (int(Memory.Capacity)))
        print('Testlog end.=======================')

    def copyEXE(self, exeFilename):
        print('start copy .exe file to server...')
        if os.path.exists(self.driver + ':/testlog/'):
            pass
        else:
            os.makedirs(self.driver + ':/testlog/')
        shutil.copy(exeFilename, self.driver + r':\testlog')
        print('.exe file copy to server complete.')

    def runEXEInBackground(self, exeFilename):
        process = self.c.Win32_Process
        result = process.Create(CommandLine=r"cmd /c c:\testlog\"" + exeFilename)
        print('exe file run in server complete.')

    def runEXEInForeground(self, exeFilename):
        # Method 1
        # self.c = wmi.WMI()
        # process = self.c.Win32_Process
        # result = process.Create(
        #     CommandLine=r"cmd /c schtasks /run /s 9.110.179.98 /u administrator /p Password123 /TN quantest1")
        # Method 2
        # os.system(r"schtasks /run /s 9.110.179.98 /u administrator /p Password123 /TN quantest1")
        # Method 3
        process = self.c.Win32_Process
        # create a schedule task
        result = process.Create(
            CommandLine=r"cmd /c SCHTASKS /Create /TN testtask1 /SC ONCE /ST 00:00 /TR C:\testlog\capturescreen.exe")
        time.sleep(3)
        # run schedule task
        result = process.Create(CommandLine=r"cmd /c schtasks /Run /TN testtask1")
        time.sleep(3)
        # delete schedule task
        # result = process.Create(CommandLine=r"cmd /c schtasks /Delete /TN testtask1 /F")
        # print('exe file start run in server...')


if __name__ == '__main__':
    pass
