from unittest import TestCase, main
from unittest.mock import Mock, patch
import BoI_util
import time


class test_BoI(TestCase):
    @classmethod
    def setUpClass(cls):
        BoI_util.mountDisktoLocal('p', '9.110.179.98', 'administrator', 'Password123')
        BoI_util.connectToRemoteServer('9.110.179.98', 'administrator', 'Password123')

    @classmethod
    def tearDownClass(cls):
        BoI_util.removeLocalDisk('p')

    #
    def test_Sample(self):
        BoI_util.creatScriptInServer('p', r"ping 10.0.0.1 -n 1 > c:\testlog\log.txt")
        BoI_util.runScriptInServer()
        time.sleep(5)
        BoI_util.getTestLog('p')
        BoI_util.clear('p')

    # def testSysteminfo(self):
    #     BoI_util.creatScriptInServer('p', '9.110.179.98', 'administrator', 'Password123',
    #                                  r"systeminfo > c:\testlog\log.txt")
    #     BoI_util.runScriptInServer('9.110.179.98', 'administrator', 'Password123')
    #     time.sleep(15)
    #     BoI_util.getTestLog('p')
    #     BoI_util.clear('p')
    #
    # def testPort139(self):
    #     BoI_util.creatScriptInServer('p', '9.110.179.98', 'administrator', 'Password123',
    #                                  r"netstat -ano | findstr 139 > c:\testlog\log.txt")
    #     BoI_util.runScriptInServer('9.110.179.98', 'administrator', 'Password123')
    #     time.sleep(5)
    #     BoI_util.getTestLog('p')
    #     BoI_util.clear('p')

    def testIP(self):
        BoI_util.getIPInfo()

    def testOSVersion(self):
        BoI_util.getOSVersion()

    def testCPUAndMEM(self):
        BoI_util.getCPU_MEM()
