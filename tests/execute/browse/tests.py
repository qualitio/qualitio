# -*- coding: utf-8 -*-
from selenium import selenium
from config import settings
import unittest, time, base64

class BaseSeleniumTestCase(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 
                                 4444, 
                                 "*%s" % settings['browser'], 
                                 settings['hostname'])
        
        if settings['username']:
            self.selenium.addCustomRequestHeader("Authorization", "Basic %s" % 
                                                 base64.b64encode("%s:%s" % (settings['username'], settings['password'])).strip())
        self.selenium.start()

    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

    def login(self):
        sel = self.selenium
        sel.open("/store/#testcasedirectory/1/details/")
        self.assertEqual("qualitio: login", sel.get_title())
        try: self.failUnless(sel.is_text_present("Qualitio"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("id_password")
        sel.type_keys("id_password", "admin")
        sel.click("logo")
        try: self.failUnless(sel.is_element_present("id_username"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("id_username")
        sel.type_keys("id_username", "admin")
        sel.click("logo")
        try: self.assertEqual("admin", sel.get_value("id_username"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_password"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//input[@value='login']"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//input[@value='login']")
        for i in range(60):
            try:
                if sel.is_text_present("qualitio store"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=store"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=Loading ...")
        for i in range(60):
            try:
                if sel.is_element_present("logo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("id_username")
        sel.type("id_username", "admin")
        sel.click("id_password")
        sel.type("id_password", "admin")
        sel.click("submit-panel")
        sel.click("//input[@value='login']")
        sel.wait_for_page_to_load("30000")


class Test01Loginexecute(BaseSeleniumTestCase):
    
    def test_01_loginexecute(self):
        sel = self.selenium
        sel.open("/execute/")
        self.assertEqual("qualitio: login", sel.get_title())
        for i in range(60):
            try:
                if sel.is_text_present("Qualitio"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Qualitio"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("id_username")
        sel.type("id_username", "admin")
        sel.click("id_password")
        sel.type("id_password", "admin")
        sel.click("submit-panel")
        try: self.failUnless(sel.is_element_present("//input[@value='login']"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//input[@value='login']")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("qualitio: execute", sel.get_title())
        for i in range(60):
            try:
                if sel.is_text_present("qualitio execute"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("qualitio execute"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Welcome, admin"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=Log out"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=Log out")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("qualitio: login", sel.get_title())
        try: self.failUnless(sel.is_text_present("Qualitio"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("id_username")
        sel.type("id_username", "admin")
        sel.click("id_password")
        sel.type("id_password", "admin")
        sel.click("submit-panel")
        sel.click("//input[@value='login']")
        sel.wait_for_page_to_load("30000")


class Test28ExecTestdirectVerify(BaseSeleniumTestCase):
    
    def test_28_exec_testdirect_verify(self):
        self.login()
        sel = self.selenium
#        sel.open("/require/#requirement/1/details/")
        self.assertEqual("qualitio: requirements", sel.get_title())
        for i in range(60):
            try:
                if sel.is_text_present("execute"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=execute"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=execute")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_text_present("qualitio execute"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("qualitio execute"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_text_present("TestRun directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=TestRun directory")
        for i in range(60):
            try:
                if sel.is_text_present("test run directory: TestRun directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("application-view-header"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div#application-view-header h1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("test run directory: TestRun directory"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("application-view-menu"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div#application-view-menu span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=edit"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("details"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("edit"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div#application-view div:nth-child(3)"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=a.button[href=\"#testrundirectory/1/newtestrun/\"]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("full name: /TestRun directory"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("description"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("not set"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=table.display"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("path"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("id"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("modified"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("created"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div.dataTables_scrollBody"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=/TestRun directory/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=TestRun 1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("/TestRun directory/", sel.get_text("link=/TestRun directory/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("TestRun 1", sel.get_text("link=TestRun 1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("TestRun 2", sel.get_text("link=TestRun 2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//div[@id='application-view']/div[3]/div[4]/div[2]/div"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Search:"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//input[@type='text']"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div#application-view-footer div a span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=a.button[href=\"#testrundirectory/1/new/\"]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("create test run"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("create test case directory"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div#application-view-footer div"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_text_present("test run directory : TestRun directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test run directory : TestRun directory"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Name:"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=form#testrundirectory_form div:nth-child(2)"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("name_wrapper"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Parent:"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("parent_wrapper"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_parent"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Description:"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("description_wrapper"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_description"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div#application-view-footer div"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("Executed"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Save", sel.get_value("css=input[name='Executed'][value='Save']"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=input[name='Executed'][value='Save']"))
        except AssertionError, e: self.verificationErrors.append(str(e))



class Test29ExecTestrunVerify(BaseSeleniumTestCase):
    
    def test_29_exec_testrun_verify(self):
        self.login()
        sel = self.selenium
#        sel.open("/require/#requirement/1/details/")
        self.assertEqual("qualitio: requirements", sel.get_title())
        for i in range(60):
            try:
                if sel.is_text_present("execute"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=execute"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=execute")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_text_present("qualitio execute"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("qualitio execute"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_text_present("TestRun directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=TestRun directory")
        for i in range(60):
            try:
                if sel.is_text_present("test run directory: TestRun directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=li#1_testrundirectory ins")
        for i in range(60):
            try:
                if sel.is_element_present("link=TestRun 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=TestRun 1")
        for i in range(60):
            try:
                if sel.is_text_present("test run: TestRun 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test run: TestRun 1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div#application-view-header h1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("application-view-menu"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div#application-view-menu span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=edit"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("edit", sel.get_text("link=edit"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div#application-view-menu a:nth-child(2)"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("execute", sel.get_text("css=a[href=\"#testrun/1/execute/\"]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=notes"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("notes", sel.get_text("link=notes"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div.application-view-content"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("full name: /TestRun directory/TestRun 1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("pass rate: not set"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("status: not set"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("exact:notes:"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("test cases:"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("id"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("path"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("status"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("modified"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("created"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("No data available in table"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div.dataTables_filter"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Search:"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=input[type='text']"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div.dataTables_scrollBody"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_text_present("Name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Name:"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_testrun-name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Parent:"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_testrun-parent"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=form#testrun_form div:nth-child(2)"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//form[@id='testrun_form']/div[3]/div[1]/div"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//form[@id='testrun_form']/div[4]/div[1]/div"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("connected testcase"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("available testcase"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("id"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("status"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("modified"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("No data available in table"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Close navigation"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("exact:Search:"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//form[@id='testrun_form']/div[4]/div[2]/div/div/div[1]/div[1]/div/table/thead/tr/th[2]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//form[@id='testrun_form']/div[4]/div[2]/div/div/div[2]/div/input"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("id", sel.get_text("//form[@id='testrun_form']/div[4]/div[2]/div/div/div[1]/div[1]/div/table/thead/tr/th[2]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("path", sel.get_text("//form[@id='testrun_form']/div[4]/div[2]/div/div/div[1]/div[1]/div/table/thead/tr/th[3]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("name", sel.get_text("//form[@id='testrun_form']/div[4]/div[2]/div/div/div[1]/div[1]/div/table/thead/tr/th[4]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Search:", sel.get_text("//form[@id='testrun_form']/div[4]/div[2]/div/div/div[2]/div"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("Executed"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Save", sel.get_value("Executed"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=a[href=\"#testrun/1/execute/\"]")
        for i in range(60):
            try:
                if sel.is_element_present("testcaserun-list"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("testcaserun-list"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("id"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("path"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("status"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("bugs"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("modified"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("created"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div.dataTables_scrollBody"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div.dataTables_filter"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=select.action-list"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//div[@id='testcaserun-list']/div[2]/select/option[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("-- action on selected --", sel.get_text("//div[@id='testcaserun-list']/div[2]/select/option[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("set status"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("remove bug"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("add bug"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("add"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("-- action on selected -- set status add bug remove bug"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=notes")
        for i in range(60):
            try:
                if sel.is_text_present("notes"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("css=div.application-view-content textarea"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("css=div.application-view-content textarea"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("Executed"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if "Save" == sel.get_value("Executed"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("Save", sel.get_value("Executed"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=history"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=history")
        for i in range(60):
            try:
                if sel.is_element_present("//div[@id='application-view']/div[3]/div/div[1]/div[1]/div/table/thead/tr/th[1]"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("date", sel.get_text("//div[@id='application-view']/div[3]/div/div[1]/div[1]/div/table/thead/tr/th[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("user", sel.get_text("//div[@id='application-view']/div[3]/div/div[1]/div[1]/div/table/thead/tr/th[2]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("comment", sel.get_text("//div[@id='application-view']/div[3]/div/div[1]/div[1]/div/table/thead/tr/th[3]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//div[@id='application-view']/div[3]/div/div[2]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//div[@id='application-view']/div[3]/div/div[2]/div[2]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("exact:Search:"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//input[@type='text']"))
        except AssertionError, e: self.verificationErrors.append(str(e))


class Test30ExecTestdirectCreate(BaseSeleniumTestCase):
    
    def test_30_exec_testdirect_create(self):
        self.login()
        sel = self.selenium
#        sel.open("/require/#requirement/1/details/")
        self.assertEqual("qualitio: requirements", sel.get_title())
        for i in range(60):
            try:
                if sel.is_element_present("link=execute"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "execute" == sel.get_text("link=execute"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=execute")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("qualitio: execute", sel.get_title())
        for i in range(60):
            try:
                if sel.is_element_present("link=TestRun directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=TestRun directory")
        for i in range(60):
            try:
                if sel.is_text_present("test run directory: TestRun directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test run directory: TestRun directory"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=div#application-view-footer div a:nth-child(2)")
        for i in range(60):
            try:
                if sel.is_text_present("test run directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_name", "testrun subdirectory")
        try: self.failUnless(sel.is_text_present("Description"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id_description", "Description\ndescription")
        sel.click("css=input[name='Executed'][value='Save']")
        for i in range(60):
            try:
                if sel.is_text_present("test run directory: testrun subdirectory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test run directory: testrun subdirectory"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("full name: /TestRun directory/testrun subdirectory"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Description\ndescription"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=TestRun directory")
        for i in range(60):
            try:
                if sel.is_text_present("test run directory: TestRun directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("//div[@id='application-view']/div[3]/div[4]/div[1]/div[2]/table/tbody/tr[1]/td[4]/a"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("testrun subdirectory", sel.get_text("//div[@id='application-view']/div[3]/div[4]/div[1]/div[2]/table/tbody/tr[1]/td[4]/a"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("TestRun 1", sel.get_text("//div[@id='application-view']/div[3]/div[4]/div[1]/div[2]/table/tbody/tr[2]/td[4]/a"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("TestRun 2", sel.get_text("//div[@id='application-view']/div[3]/div[4]/div[1]/div[2]/table/tbody/tr[3]/td[4]/a"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//div[@id='application-view']/div[3]/div[4]/div[1]/div[2]/table/tbody/tr[1]/td[4]/a")
        for i in range(60):
            try:
                if sel.is_text_present("test run directory: testrun subdirectory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_element_present("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("testrun subdirectory", sel.get_value("id_name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Description description", sel.get_text("id_description"))
        except AssertionError, e: self.verificationErrors.append(str(e))


class Test31ExecTestrunCreate(BaseSeleniumTestCase):
    
    def test_31_exec_testrun_create(self):
        self.login()
        sel = self.selenium
#        sel.open("/require/#requirement/1/details/")
        self.assertEqual("qualitio: requirements", sel.get_title())
        for i in range(60):
            try:
                if sel.is_element_present("link=execute"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "execute" == sel.get_text("link=execute"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=execute")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("qualitio: execute", sel.get_title())
        for i in range(60):
            try:
                if sel.is_element_present("link=TestRun directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=TestRun directory")
        for i in range(60):
            try:
                if sel.is_text_present("test run directory: TestRun directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test run directory: TestRun directory"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=div#application-view-footer div a span")
        for i in range(60):
            try:
                if sel.is_text_present("test run"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("new"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_name", "Test run testowy")
        sel.click("//input[@value='2']")
        sel.click("//input[@value='3']")
        try: self.failUnless(sel.is_element_present("//a[@id='add-testcases-button']/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//a[@id='add-testcases-button']/span")
        for i in range(60):
            try:
                if sel.is_element_present("link=Open navigation"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=TestCase"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_text_present("test run: Test run testowy"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test run: Test run testowy"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("full name: /TestRun directory/Test run testowy"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("pass rate: not set"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("status: not set"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("notes:"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("notes: not set"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("test cases:"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("/MeeGo Netbook/MeeGo IVI BAT/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=/MeeGo Netbook/MeeGo IVI BAT/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=Open navigation"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Open navigation", sel.get_text("link=Open navigation"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=TestCase"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("TestCase", sel.get_text("link=TestCase"))
        except AssertionError, e: self.verificationErrors.append(str(e))


class Test34ExecSamename(BaseSeleniumTestCase):
    
    def test_34_exec_samename(self):
        self.login()
        sel = self.selenium
#        sel.open("/require/#requirement/1/details/")
        self.assertEqual("qualitio: requirements", sel.get_title())
        for i in range(60):
            try:
                if "MeeGo" == sel.get_text("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=execute")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("qualitio: execute", sel.get_title())
        sel.click("link=TestRun directory")
        for i in range(60):
            try:
                if sel.is_text_present("test run directory: TestRun directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=div#application-view-footer div a:nth-child(2)")
        for i in range(60):
            try:
                if sel.is_text_present("test run directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("new"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_name", "Directory1")
        sel.click("css=input[name='Executed'][value='Save']")
        for i in range(60):
            try:
                if sel.is_text_present("test run directory: Directory1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=TestRun directory")
        for i in range(60):
            try:
                if sel.is_text_present("test run directory: TestRun directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=div#application-view-footer div a:nth-child(2)")
        for i in range(60):
            try:
                if sel.is_text_present("test run directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("new"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_name", "Directory1")
        sel.click("css=input[name='Executed'][value='Save']")
        for i in range(60):
            try:
                if sel.is_text_present("Validation errors: \"parent\" and \"name\" fields need to be always unique together."): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Validation errors: \"parent\" and \"name\" fields need to be always unique together."))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id_name", "Directory2")
        sel.click("css=input[name='Executed'][value='Save']")
        for i in range(60):
            try:
                if sel.is_text_present("test run directory: Directory2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test run directory: Directory2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("full name: /TestRun directory/Directory2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_text_present("test run directory : Directory2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_name", "Directory1")
        sel.click("css=input[name='Executed'][value='Save']")
        for i in range(60):
            try:
                if sel.is_text_present("Validation errors: \"parent\" and \"name\" fields need to be always unique together."): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Validation errors: \"parent\" and \"name\" fields need to be always unique together."))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.select("id_parent", "label=/TestRun directory/Directory1")
        for i in range(60):
            try:
                if sel.is_element_present("id_parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_description"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=input[name='Executed'][value='Save']")
        for i in range(60):
            try:
                if sel.is_element_present("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_description"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("Directory1", sel.get_value("id_name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_text_present("description"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("full name: /TestRun directory/Directory1/Directory1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_text_present("Name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.select("id_parent", "label=/TestRun directory")
        sel.click("css=input[name='Executed'][value='Save']")
        for i in range(60):
            try:
                if sel.is_text_present("Validation errors: \"parent\" and \"name\" fields need to be always unique together."): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Validation errors: \"parent\" and \"name\" fields need to be always unique together."))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id_name", "Directory1 same name")
        sel.click("css=input[name='Executed'][value='Save']")
        for i in range(60):
            try:
                if sel.is_element_present("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_description"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("Directory1 same name", sel.get_value("id_name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_text_present("test run directory: Directory1 same name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test run directory: Directory1 same name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("full name: /TestRun directory/Directory1 same name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.select_window("null")


class Test35ExecTestrunSamename(BaseSeleniumTestCase):
    
    def test_35_exec_testrun_samename(self):
        self.login()
        sel = self.selenium
#        sel.open("/require/#requirement/1/details/")
        self.assertEqual("qualitio: requirements", sel.get_title())
        for i in range(60):
            try:
                if "MeeGo" == sel.get_text("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=execute")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("qualitio: execute", sel.get_title())
        sel.click("link=TestRun directory")
        for i in range(60):
            try:
                if sel.is_text_present("test run directory: TestRun directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=div#application-view-footer div a:nth-child(2)")
        for i in range(60):
            try:
                if sel.is_text_present("test run directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("new"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_name", "Directory3")
        sel.click("css=input[name='Executed'][value='Save']")
        for i in range(60):
            try:
                if sel.is_text_present("test run directory: Directory3"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=div#application-view-footer div a")
        for i in range(60):
            try:
                if sel.is_text_present("test run"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("new"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "" == sel.get_text("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_name", "TestRun 1")
        sel.select("id_parent", "label=/TestRun directory")
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_text_present("Validation errors"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Validation errors"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id_name", "TestRun 3")
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_text_present("test run: TestRun 3"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("pass rate:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("full name: /TestRun directory/TestRun 3"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("test run: TestRun 3"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_text_present("test run : TestRun 3"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("Name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_testrun-name", "TestRun 1")
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_text_present("Validation errors"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Validation errors"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.select("id_testrun-parent", "label=/TestRun directory/Directory3")
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_text_present("qualitio execute"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=TestRun directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("test run: TestRun 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("pass rate:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test run: TestRun 1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("full name: /TestRun directory/Directory3/TestRun 1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=edit")
        for i in range(60):
            try:
                if "" == sel.get_text("id_testrun-name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.select("id_testrun-parent", "label=/TestRun directory")
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_text_present("Validation errors"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Validation errors"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id_testrun-name", "TestRun 1 same name")
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_text_present("test run: TestRun 1 same name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("pass rate:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test run: TestRun 1 same name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("full name: /TestRun directory/TestRun 1 same name"))
        except AssertionError, e: self.verificationErrors.append(str(e))


class Test36ExecTreeVerify(BaseSeleniumTestCase):
    
    def test_36_exec_tree_verify(self):
        self.login()
        sel = self.selenium
#        sel.open("/require/#requirement/1/details/")
        self.assertEqual("qualitio: requirements", sel.get_title())
        for i in range(60):
            try:
                if "MeeGo" == sel.get_text("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=execute")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_text_present("qualitio execute"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=TestRun directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.assertEqual("qualitio: execute", sel.get_title())
        sel.click("link=TestRun directory")
        for i in range(60):
            try:
                if sel.is_text_present("test run directory: TestRun directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test run directory: TestRun directory"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("full name: /TestRun directory"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=li#1_testrundirectory ins")
        for i in range(60):
            try:
                if sel.is_element_present("link=TestRun 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=TestRun 2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=TestRun 1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=TestRun 2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=TestRun 1")
        for i in range(60):
            try:
                if sel.is_text_present("full name: /TestRun directory/TestRun 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test run: TestRun 1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("full name: /TestRun directory/TestRun 1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=TestRun 2")
        for i in range(60):
            try:
                if sel.is_text_present("test run: TestRun 2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test run: TestRun 2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("full name: /TestRun directory/TestRun 2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=TestRun directory")
        for i in range(60):
            try:
                if sel.is_text_present("test run directory: TestRun directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test run directory: TestRun directory"))
        except AssertionError, e: self.verificationErrors.append(str(e))


class Test37ExecConnecttest(BaseSeleniumTestCase):
    
    def test_37_exec_connecttest(self):
        self.login()
        sel = self.selenium
#        sel.open("/require/#requirement/1/details/")
        self.assertEqual("qualitio: requirements", sel.get_title())
        for i in range(60):
            try:
                if "MeeGo" == sel.get_text("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=execute")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("qualitio: execute", sel.get_title())
        sel.click("link=TestRun directory")
        for i in range(60):
            try:
                if sel.is_text_present("test run directory: TestRun directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=li#1_testrundirectory ins")
        for i in range(60):
            try:
                if sel.is_element_present("link=TestRun 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=TestRun 2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=TestRun 2")
        for i in range(60):
            try:
                if sel.is_text_present("test run: TestRun 2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("Name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type_keys("//form[@id='testrun_form']/div[4]/div[2]/div/div/div[2]/div/input", "Open")
        for i in range(60):
            try:
                if sel.is_element_present("link=Open navigation"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=/MeeGo Netbook/MeeGo IVI BAT/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("//input[@value='2']"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("//form[@id='testrun_form']/div[4]/div[2]/div/div/div[1]/div[1]/div/table/thead/tr/th[1]/input")
        try: self.failUnless(sel.is_element_present("//a[@id='add-testcases-button']/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//a[@id='add-testcases-button']/span")
        for i in range(60):
            try:
                if sel.is_element_present("link=Open navigation"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("//form[@id='testrun_form']/div[4]/div[2]/div/div/div[1]/div[2]/table/tbody"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=/MeeGo Netbook/MeeGo IVI BAT/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Open navigation", sel.get_table("//form[@id='testrun_form']/div[4]/div[1]/div/div/div[1]/div[2]/table.1.3"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_text_present("test run: TestRun 2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name: /TestRun directory/TestRun 2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("full name: /TestRun directory/TestRun 2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("test run: TestRun 2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=Open navigation"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Open navigation", sel.get_text("link=Open navigation"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=/MeeGo Netbook/MeeGo IVI BAT/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_text_present("Name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("//input[@value='2']")
        for i in range(60):
            try:
                if sel.is_element_present("//a[@id='remove-testcases-button']/span"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("//a[@id='remove-testcases-button']/span")
        for i in range(60):
            try:
                if sel.is_element_present("link=Open navigation"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_text_present("No data available in table"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("Open navigation", sel.get_table("//form[@id='testrun_form']/div[4]/div[2]/div/div/div[1]/div[2]/table.2.3"))
        except AssertionError, e: self.verificationErrors.append(str(e))


class Test38ExecConnecttestname(BaseSeleniumTestCase):
    
    def test_38_exec_connecttestname(self):
        self.login()
        sel = self.selenium
#        sel.open("/require/#requirement/4/details/")
        self.assertEqual("qualitio: requirements", sel.get_title())
        sel.click("link=store")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("qualitio: store", sel.get_title())
        for i in range(60):
            try:
                if sel.is_text_present("qualitio store"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=MeeGo Netbook"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=MeeGo Handset bat")
        for i in range(60):
            try:
                if sel.is_text_present("test case directory: MeeGo Handset bat"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name: /MeeGo Handset bat"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("full name: /MeeGo Handset bat"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=div#application-view-footer div a span")
        for i in range(60):
            try:
                if sel.is_text_present("test case"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("id_name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id_name", "TestCase1")
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_text_present("test case: TestCase1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=execute")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("qualitio: execute", sel.get_title())
        for i in range(60):
            try:
                if sel.is_element_present("link=TestRun directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("qualitio execute"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=li#1_testrundirectory ins")
        for i in range(60):
            try:
                if sel.is_element_present("link=TestRun 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=TestRun 1")
        for i in range(60):
            try:
                if sel.is_text_present("test run: TestRun 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name: /TestRun directory/TestRun 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test run: TestRun 1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type_keys("//form[@id='testrun_form']/div[4]/div[2]/div/div/div[2]/div/input", "TestCase1")
        for i in range(60):
            try:
                if sel.is_element_present("link=TestCase1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("//input[@value='4']")
        sel.click("//input[@value='18']")
        for i in range(60):
            try:
                if sel.is_element_present("//a[@id='add-testcases-button']/span"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("//a[@id='add-testcases-button']/span")
        for i in range(60):
            try:
                if sel.is_element_present("link=TestCase1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_text_present("full name: /TestRun directory/TestRun 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("test cases:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("TestCase1", sel.get_table("//div[@id='application-view']/div[3]/div/div[6]/div[1]/div[2]/table.1.2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("TestCase1", sel.get_text("//div[@id='application-view']/div[3]/div/div[6]/div[1]/div[2]/table/tbody/tr[2]/td[3]/a"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("TestCase1", sel.get_text("link=TestCase1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("TestCase1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=/MeeGo Netbook/MeeGo IVI BAT/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=/MeeGo Handset bat/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("select-all")
        for i in range(60):
            try:
                if sel.is_element_present("//a[@id='remove-testcases-button']/span"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("//a[@id='remove-testcases-button']/span")
        for i in range(60):
            try:
                if sel.is_element_present("link=TestCase1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_text_present("test cases:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("No data available in table"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("No data available in table"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type_keys("//form[@id='testrun_form']/div[4]/div[2]/div/div/div[2]/div/input", "TestCase1")
        for i in range(60):
            try:
                if sel.is_element_present("link=TestCase1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("//form[@id='testrun_form']/div[4]/div[2]/div/div/div[1]/div[1]/div/table/thead/tr/th[1]/input")
        for i in range(60):
            try:
                if sel.is_element_present("//a[@id='add-testcases-button']/span"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("//a[@id='add-testcases-button']/span")
        for i in range(60):
            try:
                if sel.is_text_present("4"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_text_present("test run: TestRun 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("test cases:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=TestCase1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=TestCase10"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=TestCase11"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=TestCase12"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=TestCase13"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=TestCase14"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//div[@id='application-view']/div[3]/div/div[6]/div[1]/div[2]/table/tbody/tr[7]/td[3]/a"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=/MeeGo Handset bat/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("select-all")
        for i in range(60):
            try:
                if sel.is_element_present("//input[@value='4']"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("//a[@id='remove-testcases-button']/span")
        for i in range(60):
            try:
                if sel.is_text_present("No data available in table"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_text_present("test run: TestRun 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("test cases:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("No data available in table"))
        except AssertionError, e: self.verificationErrors.append(str(e))


class Test39ExecTestcolor(BaseSeleniumTestCase):
    
    def test_39_exec_testcolor(self):
        self.login()
        sel = self.selenium
#        sel.open("/require/#requirement/1/details/")
        self.assertEqual("qualitio: requirements", sel.get_title())
        for i in range(60):
            try:
                if sel.is_text_present("qualitio requirements"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=requirements"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=store"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=execute"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=execute"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=execute")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_text_present("qualitio execute"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.assertEqual("qualitio: execute", sel.get_title())
        for i in range(60):
            try:
                if sel.is_element_present("//li[@id='1_testrundirectory']/ins"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("//li[@id='1_testrundirectory']/ins"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//li[@id='1_testrundirectory']/ins")
        for i in range(60):
            try:
                if sel.is_element_present("link=TestRun 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=TestRun 2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=TestRun 1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=TestRun 1")
        for i in range(60):
            try:
                if sel.is_element_present("//div[@id='application-view-header']/h1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("test run: TestRun 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test run: TestRun 1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("link=edit"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=edit"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type_keys("//form[@id='testrun_form']/div[4]/div[2]/div/div/div[2]/div/input", "Case1")
        for i in range(60):
            try:
                if sel.is_element_present("link=TestCase1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=TestCase10"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("//input[@value='4']"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//input[@value='4']")
        try: self.failUnless(sel.is_element_present("//a[@id='add-testcases-button']/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("//input[@value='4']"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("//a[@id='add-testcases-button']/span")
        try: self.failUnless(sel.is_element_present("Executed"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("//div[@id='application-view-menu']/a[2]")
        for i in range(60):
            try:
                if sel.is_element_present("select-all"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("id"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("path"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("//tr[@id='testcaserun_3']/td[2]"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("//tr[@id='testcaserun_3']/td[2]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//tr[@id='testcaserun_3']/td[2]")
        for i in range(60):
            try:
                if sel.is_text_present("test case: TestCase1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("directory: TestCase1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("origin test case: /MeeGo Netbook/MeeGo IVI BAT/TestCase1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("//form[@id='testcaserun-status-form']/label[1]/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//form[@id='testcaserun-status-form']/label[2]/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//form[@id='testcaserun-status-form']/label[3]/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("IDLE"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("PASSED"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("FAILED"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("FAILED", sel.get_text("//form[@id='testcaserun-status-form']/label[3]/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("PASSED", sel.get_text("//form[@id='testcaserun-status-form']/label[2]/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("IDLE", sel.get_text("//form[@id='testcaserun-status-form']/label[1]/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//form[@id='testcaserun-status-form']/label[2]/span")
        sel.click("id_status_1")
        for i in range(60):
            try:
                if sel.is_element_present("//tr[@style=\"background: none repeat scroll 0% 0% rgb(136, 187, 102);\"]"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("//tr[@style=\"background: none repeat scroll 0% 0% rgb(136, 187, 102);\"]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//form[@id='testcaserun-status-form']/label[3]/span")
        sel.click("id_status_2")
        for i in range(60):
            try:
                if sel.is_element_present("//tr[@style=\"background: none repeat scroll 0% 0% red;\"]"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("//tr[@style=\"background: none repeat scroll 0% 0% red;\"]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//form[@id='testcaserun-status-form']/label[1]/span")
        sel.click("id_status_0")
        for i in range(60):
            try:
                if sel.is_element_present("//tr[@style=\"background: none repeat scroll 0% 0% rgb(204, 238, 238);\"]"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("//tr[@style=\"background: none repeat scroll 0% 0% rgb(204, 238, 238);\"]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("link=edit"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=edit"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("//input[@value='4']")
        for i in range(60):
            try:
                if sel.is_element_present("//a[@id='remove-testcases-button']/span"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("//a[@id='remove-testcases-button']/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//a[@id='remove-testcases-button']/span")
        for i in range(60):
            try:
                if sel.is_element_present("//div[@id='application-view-footer']/div/input"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("//div[@id='application-view-footer']/div/input")



class Test040ExecAddbug(BaseSeleniumTestCase):
    
    def test_040_exec_addbug(self):
        self.login()
        sel = self.selenium
#        sel.open("/require/#requirement/9/details/")
        self.assertEqual("qualitio: requirements", sel.get_title())
        for i in range(60):
            try:
                if sel.is_element_present("link=execute"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=execute")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("qualitio: execute", sel.get_title())
        for i in range(60):
            try:
                if sel.is_text_present("qualitio execute"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=TestRun directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=li#1_testrundirectory ins")
        for i in range(60):
            try:
                if sel.is_element_present("link=TestRun 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=TestRun 1")
        for i in range(60):
            try:
                if sel.is_text_present("test run: TestRun 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=edit"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("css=div#application-view-menu a:nth-child(2)"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=notes"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("//input[@value='1']"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//input[@value='1']")
        try: self.failUnless(sel.is_element_present("//a[@id='add-testcases-button']/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//a[@id='add-testcases-button']/span")
        for i in range(60):
            try:
                if sel.is_element_present("link=Close navigation"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=Close navigation"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//form[@id='testrun_form']/div[4]/div[2]/div/div/div[1]/div[2]/table/tbody"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=div#application-view-menu a:nth-child(3)")
        for i in range(60):
            try:
                if sel.is_element_present("select-all"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("id"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("path"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("css=tr#testcaserun_1 td:nth-child(4)"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("css=tr#testcaserun_1 td:nth-child(4)"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=div#header div")
        sel.click("css=tr#testcaserun_1 td:nth-child(4)")
        for i in range(60):
            try:
                if sel.is_text_present("test case: Close navigation"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("precondition"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test case: Close navigation"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_bugs"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id_bugs", "1234,1235,1236")
        sel.click("css=input[value='add']")
        for i in range(60):
            try:
                if sel.is_element_present("link=1234"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=1235"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=1236"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("VERIFIED"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("id_bugs-0-DELETE"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_bugs-1-DELETE"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_bugs-2-DELETE"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=1234"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=1235"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=1236"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("we need default style for the html 4 style tags", sel.get_text("link=we need default style for the html 4 style tags"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("VERIFIED"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("DUPLICATE"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("FIXED"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("INVALID"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("#1234 #1235 #1236"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("id_bugs-0-DELETE")
        sel.click("id_bugs-1-DELETE")
        sel.click("id_bugs-2-DELETE")
        for i in range(60):
            try:
                if sel.is_element_present("//input[@value='remove']"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("//input[@value='remove']")
        for i in range(60):
            try:
                if sel.is_element_present("//form[@id='testcaserun-remove-bug-form']/div[2]/div/div[2]/table/tbody/tr/td"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("//input[@value='remove']"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("Bugs"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_bugs", "1237 , 1238 , 1239")
        for i in range(60):
            try:
                if sel.is_element_present("//input[@value='add']"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("//input[@value='add']")
        for i in range(60):
            try:
                if sel.is_element_present("link=1237"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=1238"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=1239"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=1237"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=1238"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=1239"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("#1237 #1238 #1239"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("id_bugs-0-DELETE")
        sel.click("id_bugs-1-DELETE")
        sel.click("id_bugs-2-DELETE")
        for i in range(60):
            try:
                if sel.is_element_present("//input[@value='remove']"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("//input[@value='remove']")
        for i in range(60):
            try:
                if sel.is_element_present("//form[@id='testcaserun-remove-bug-form']/div[2]/div/div[2]/table/tbody/tr/td"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("No data available in table"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("//form[@id='testcaserun-remove-bug-form']/div[2]/div/div[2]/table/tbody/tr/td"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("Bugs"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("//input[@value='add']"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_bugs", "1231, 1232, 1233, 1234")
        for i in range(60):
            try:
                if sel.is_element_present("//input[@value='add']"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("//input[@value='add']")
        for i in range(60):
            try:
                if sel.is_element_present("link=1231"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=1232"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=1231"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=1232"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=1233"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=1234"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("#1231 #1232 #1233 #1234"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("//input[@value='1']"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//input[@value='1']")
        try: self.failUnless(sel.is_element_present("//a[@id='remove-testcases-button']/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//a[@id='remove-testcases-button']/span")
        for i in range(60):
            try:
                if sel.is_element_present("link=Close navigation"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("Executed"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=details"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_text_present("test run: TestRun 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name: /TestRun directory/TestRun 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("No data available in table"))
        except AssertionError, e: self.verificationErrors.append(str(e))


class Test039ExecAddbug(BaseSeleniumTestCase):
    
    def test_039_exec_addbug(self):
        self.login()
        sel = self.selenium
#        sel.open("/require/#requirement/1/details/")
        self.assertEqual("qualitio: requirements", sel.get_title())
        for i in range(60):
            try:
                if sel.is_text_present("qualitio requirements"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=execute")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("qualitio: execute", sel.get_title())
        for i in range(60):
            try:
                if sel.is_text_present("qualitio execute"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=TestRun directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=li#1_testrundirectory ins")
        for i in range(60):
            try:
                if sel.is_element_present("link=TestRun 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=TestRun 2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=TestRun 1")
        for i in range(60):
            try:
                if sel.is_text_present("test run: TestRun 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name: /TestRun directory/TestRun 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type_keys("//form[@id='testrun_form']/div[4]/div[2]/div/div/div[2]/div/input", "close navi")
        for i in range(60):
            try:
                if sel.is_element_present("link=Close navigation"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("//input[@value='1']")
        for i in range(60):
            try:
                if sel.is_element_present("//a[@id='add-testcases-button']/span"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("//a[@id='add-testcases-button']/span")
        for i in range(60):
            try:
                if sel.is_element_present("link=Close navigation"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=/MeeGo Netbook/MeeGo IVI BAT/"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=Close navigation"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//form[@id='testrun_form']/div[4]/div[2]/div/div/div[1]/div[2]/table/tbody"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=a[href=\"#testrun/1/execute/\"]")
        for i in range(60):
            try:
                if sel.is_element_present("select-all"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("id"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("path"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("exact:Search:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("/MeeGo Netbook/MeeGo IVI BAT/"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("Close navigation"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("test run: TestRun 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("//tr[@id='testcaserun_1']/td[1]"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("//tr[@id='testcaserun_1']/td[1]")
        for i in range(60):
            try:
                if sel.is_element_present("select-all"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("id"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("test case: Close navigation"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test case: Close navigation"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id_bugs", "1234")
        sel.click("css=input[value='add']")
        for i in range(60):
            try:
                if sel.is_element_present("id_bugs-0-DELETE"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=1234"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=1234"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("we need default style for the html 4 style tags"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("VERIFIED"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("FIXED"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id_bugs", "1235")
        sel.click("css=input[value='add']")
        for i in range(60):
            try:
                if sel.is_text_present("id"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_bugs-1-DELETE"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=1235"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=1235"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link={feature} we don"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("DUPLICATE"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("link=TestRun 2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=TestRun 2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=TestRun 2")
        for i in range(60):
            try:
                if sel.is_text_present("test run: TestRun 2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name: /TestRun directory/TestRun 2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type_keys("//form[@id='testrun_form']/div[4]/div[2]/div/div/div[2]/div/input", "close navigation")
        for i in range(60):
            try:
                if sel.is_element_present("link=/MeeGo Netbook/MeeGo IVI BAT/"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("//form[@id='testrun_form']/div[4]/div[2]/div/div/div[1]/div[1]/div/table/thead/tr/th[1]/input")
        for i in range(60):
            try:
                if sel.is_element_present("//input[@value='1']"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("//a[@id='add-testcases-button']/span")
        for i in range(60):
            try:
                if sel.is_element_present("link=Close navigation"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=Close navigation"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//form[@id='testrun_form']/div[4]/div[2]/div/div/div[1]/div[2]/table/tbody"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("//div[@id='application-view-menu']/a[2]")
        for i in range(60):
            try:
                if sel.is_text_present("test run: TestRun 2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("Close navigation"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("/MeeGo Netbook/MeeGo IVI BAT/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Close navigation"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//tr[@id='testcaserun_2']/td[1]")
        for i in range(60):
            try:
                if sel.is_text_present("test case: Close navigation"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("origin test case:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=1234"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("we need default style for the html 4 style tags", sel.get_text("link=we need default style for the html 4 style tags"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("VERIFIED"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("FIXED"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("1235", sel.get_text("link=1235"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("{feature} we don", sel.get_text("link={feature} we don"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("DUPLICATE"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id_bugs", "1236")
        sel.click("css=input[value='add']")
        for i in range(60):
            try:
                if sel.is_element_present("link=1236"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_bugs-0-DELETE"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("1236", sel.get_text("link=1236"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("id_bugs-0-DELETE")
        for i in range(60):
            try:
                if sel.is_element_present("id_bugs-0-DELETE"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=input[value='remove']")
        for i in range(60):
            try:
                if sel.is_text_present("No data available in table"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("No data available in table"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=TestRun 1")
        for i in range(60):
            try:
                if sel.is_text_present("test run: TestRun 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("//div[@id='application-view-menu']/a[2]")
        for i in range(60):
            try:
                if sel.is_text_present("/MeeGo Netbook/MeeGo IVI BAT/"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("Close navigation"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("//div[@id='testcaserun-list']/div[2]/select"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("#1235"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("#1234"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//tr[@id='testcaserun_1']/td[1]")
        for i in range(60):
            try:
                if sel.is_text_present("test case: Close navigation"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("origin test case:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("//form[@id='testcaserun-remove-bug-form']/div[2]/div/div[1]/div/table/thead/tr/th[1]/input"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("//form[@id='testcaserun-remove-bug-form']/div[2]/div/div[1]/div/table/thead/tr/th[1]/input"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//form[@id='testcaserun-remove-bug-form']/div[2]/div[1]/div[1]/div/table/thead/tr/th[1]/input")
        for i in range(60):
            try:
                if sel.is_element_present("id_bugs-0-DELETE"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_bugs-1-DELETE"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=input[value='remove']")
        for i in range(60):
            try:
                if sel.is_element_present("//form[@id='testcaserun-remove-bug-form']/div[2]/div[1]/div[2]/table/tbody/tr/td"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("No data available in table"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("//form[@id='testcaserun-remove-bug-form']/div[2]/div[1]/div[1]/div/table/thead/tr/th[1]/input"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("//form[@id='testcaserun-remove-bug-form']/div[2]/div[1]/div[2]/table/tbody/tr/td"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("No data available in table", sel.get_text("//form[@id='testcaserun-remove-bug-form']/div[2]/div/div[2]/table/tbody/tr/td"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("No data available in table"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("off", sel.get_value("//input[@value='1']"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//input[@value='1']")
        try: self.failUnless(sel.is_element_present("//a[@id='remove-testcases-button']/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//a[@id='remove-testcases-button']/span")
        for i in range(60):
            try:
                if sel.is_text_present("No data available in table"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("Executed"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=details"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_text_present("test run: TestRun 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("test cases:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=TestRun 2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=TestRun 2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=TestRun 2")
        for i in range(60):
            try:
                if sel.is_element_present("link=edit"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("edit"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=edit"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("select-all"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("select-all")
        for i in range(60):
            try:
                if sel.is_element_present("//input[@value='1']"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("//a[@id='remove-testcases-button']/span")
        for i in range(60):
            try:
                if sel.is_text_present("No data available in table"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("Executed"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_text_present("No data available in table"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("No data available in table"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//li[@id='1_testrundirectory']/ins")


class Test041ExecTestparam(BaseSeleniumTestCase):
    
    def test_041_exec_testparam(self):
        self.login()
        sel = self.selenium
#        sel.open("/require/#requirement/9/details/")
        self.assertEqual("qualitio: requirements", sel.get_title())
        for i in range(60):
            try:
                if sel.is_text_present("qualitio requirements"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("qualitio requirements"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=store"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=store")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("qualitio: store", sel.get_title())
        for i in range(60):
            try:
                if sel.is_text_present("qualitio store"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=MeeGo Netbook"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=li#1_testcasedirectory ins")
        for i in range(60):
            try:
                if sel.is_element_present("link=MeeGo IVI BAT"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=TestCase"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("css=li#4_testcasedirectory ins"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=li#4_testcasedirectory ins")
        for i in range(60):
            try:
                if sel.is_element_present("link=Close navigation"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=Open navigation"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=Open navigation")
        for i in range(60):
            try:
                if sel.is_text_present("test case: Open navigation"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=edit"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=edit"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_element_present("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_description"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_description", "description\ndescription")
        sel.type("id_precondition", "precondition\nprecondition")
        try: self.failUnless(sel.is_element_present("css=a#add-step-0 span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=a#add-step-0 span")
        sel.type("id_steps-0-description", "descriptionstep1\ndescriptionstep1")
        sel.type("id_steps-0-expected", "expectedstep1\nexpectedstep1")
        sel.click("//form[@id='testcase_form']/div[3]/div[2]/div[1]/a/span")
        sel.type("id_steps-1-expected", "expectedstep2\nexpectedstep2")
        sel.type("id_steps-1-description", "descriptionstep2\ndescriptionstep2")
        try: self.failUnless(sel.is_element_present("Executed"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_text_present("test case: Open navigation"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=execute"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=execute")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("qualitio: execute", sel.get_title())
        for i in range(60):
            try:
                if sel.is_text_present("qualitio execute"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("TestRun directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("css=li#1_testrundirectory ins"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=li#1_testrundirectory ins")
        for i in range(60):
            try:
                if sel.is_element_present("link=TestRun 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=TestRun 2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=TestRun 2")
        for i in range(60):
            try:
                if sel.is_text_present("test run: TestRun 2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test cases:"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("link=edit"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=edit"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type_keys("//form[@id='testrun_form']/div[4]/div[2]/div/div/div[2]/div/input", "open")
        for i in range(60):
            try:
                if sel.is_element_present("link=Open navigation"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("//form[@id='testrun_form']/div[4]/div[2]/div/div/div[1]/div[1]/div/table/thead/tr/th[1]/input")
        for i in range(60):
            try:
                if sel.is_element_present("//input[@value='2']"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("//a[@id='add-testcases-button']/span")
        try: self.failUnless(sel.is_element_present("Executed"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("//div[@id='application-view-menu']/a[2]"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("//div[@id='application-view-menu']/a[2]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//div[@id='application-view-menu']/a[2]")
        for i in range(60):
            try:
                if sel.is_element_present("select-all"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("id"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("path"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("css=tr#testcaserun_1 td input"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=tr#testcaserun_1 td")
        for i in range(60):
            try:
                if sel.is_element_present("//div[@id='testcaserun-details']/div[1]/h1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test case: Open navigation"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("origin test case: /MeeGo Netbook/MeeGo IVI BAT/Open navigation"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("precondition"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("step 1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("step 2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("precondition precondition"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("descriptionstep1 descriptionstep1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("expectedstep1 expectedstep1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("descriptionstep2 descriptionstep2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("expectedstep2 expectedstep2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=edit"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("select-all")
        for i in range(60):
            try:
                if sel.is_element_present("//input[@value='2']"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("//a[@id='remove-testcases-button']/span")
        try: self.failUnless(sel.is_element_present("Executed"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_testrun-parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=store"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=store"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=store")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_element_present("link=Open navigation"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("qualitio store"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("test case: Open navigation"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=edit"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_element_present("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_description", "")
        sel.type("id_precondition", "")
        sel.click("id_steps-0-DELETE")
        sel.click("id_steps-1-DELETE")
        sel.click("Executed")


if __name__ == "__main__":
    unittest.main()
