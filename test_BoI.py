from unittest import TestCase, main
import unittest
from unittest.mock import Mock, patch
import BoI
import time

skip = True


class test_BoI(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.testboi = BoI.Boi()
        # cls.testboi.connectToRemoteServer('9.110.179.98', 'administrator', 'Password123')
        # cls.testboi.connectToRemoteServer('9.111.221.161', 'Administrator', 'Passw0rd')
        cls.testboi.connectToRemoteServer('9.111.139.201', 'Administrator', 'Passw0rd')
        cls.testboi.startService('LanmanServer')
        cls.testboi.mountDisktoLocal('z')
        time.sleep(10)

    @classmethod
    def tearDownClass(cls):
        time.sleep(3)
        cls.testboi.removeLocalDisk()

    @unittest.skipIf(skip == True,"skiped")
    def test_Sample(self):
        self.testboi.creatScriptInServer(r"ping 10.0.0.1 -n 1 > c:\testlog\log.txt")
        self.testboi.runScriptInServer()
        time.sleep(5)
        self.testboi.getTestLog()
        self.testboi.clearTestlog()

    @unittest.skipIf(skip == True,"skiped")
    def testSysteminfo(self):
        self.testboi.creatScriptInServer(r"systeminfo > c:\testlog\log.txt")
        self.testboi.runScriptInServer()
        time.sleep(15)
        self.testboi.getTestLog()
        self.testboi.clearTestlog()

    @unittest.skipIf(skip == True,"skiped")
    def testPort139(self):
        self.testboi.creatScriptInServer(r"netstat -ano | findstr 139 > c:\testlog\log.txt")
        self.testboi.runScriptInServer()
        time.sleep(5)
        self.testboi.getTestLog()
        self.testboi.clearTestlog()

    # @unittest.skipIf(skip == True,"skiped")
    def testIP(self):
        self.testboi.getIPInfo()

    @unittest.skipIf(skip == True,"skiped")
    def testOSVersion(self):
        self.testboi.getOSVersion()

    @unittest.skipIf(skip == True,"skiped")
    def testCPUAndMEM(self):
        self.testboi.getCPU_MEM()

    @unittest.skipIf(skip == True, "skiped")
    def testrunEXEInBackground(self):
        self.testboi.copyEXE('capturescreen.exe')
        self.testboi.runEXEInBackground('capturescreen.exe')

    # @unittest.skipIf(skip == True, "skiped")
    def testrunEXEInForeground(self):
        self.testboi.copyEXE('capturescreen.exe')
        self.testboi.runEXEInForeground('capturescreen.exe')

if __name__ == '__main__':
    unittest.main()
    # 装载测试用例
    test_cases = unittest.TestLoader().loadTestsFromTestCase(test_BoI)
    # 使用测试套件并打包测试用例
    test_suit = unittest.TestSuite()
    test_suit.addTests(test_cases)
    # 运行测试套件，并返回测试结果
    test_result = unittest.TextTestRunner(verbosity=2).run(test_suit)
    #生成测试报告
    print("testsRun:%s" % test_result.testsRun)
    print("failures:%s" % len(test_result.failures))
    print("errors:%s" % len(test_result.errors))
    print("skipped:%s" % len(test_result.skipped))