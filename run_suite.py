import unittest
import app,time
from tools.HTMLTestRunner_PY3 import HTMLTestRunner
from script.Login import Login
from script.approve import approve
from script.trust import trust
from script.tender import tender
from script.tender_process import test_tender_process

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(Login))
suite.addTest(unittest.makeSuite(approve))
suite.addTest(unittest.makeSuite(trust))
suite.addTest(unittest.makeSuite(tender))
suite.addTest(unittest.makeSuite(test_tender_process))

#report_file = app.BASE_DIR + "/report/report{}.html".format(time.strftime("%Y%m%d-%H%M%S"))
report_file = app.BASE_DIR + "/report/report.html"  #放在jenkinsli里面报告的路口经得这么写
with open(report_file,'wb') as f:
    runner = HTMLTestRunner(f,title="P2P金融项目接口测试报告",description="test")
    runner.run(suite)
