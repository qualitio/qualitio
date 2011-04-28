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
        try: self.failUnless(sel.is_element_present("//input[@value='Login']"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//input[@value='Login']")
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
        sel.click("//input[@value='Login']")
        sel.wait_for_page_to_load("30000")


class Test01Loginreport(BaseSeleniumTestCase):
    
    def test_01_loginreport(self):
        sel = self.selenium
        sel.open("/report/")
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
        try: self.failUnless(sel.is_element_present("//input[@value='Login']"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//input[@value='Login']")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("qualitio: report", sel.get_title())
        for i in range(60):
            try:
                if sel.is_text_present("qualitio report"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("qualitio report"))
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
        sel.click("//input[@value='Login']")
        sel.wait_for_page_to_load("30000")


class Test43ReportRepdirectCreate(BaseSeleniumTestCase):
    
    def test_43_report_repdirect_create(self):
        self.login()
        sel = self.selenium
        sel.open("/require/")
        self.assertEqual("qualitio: requirements", sel.get_title())
        for i in range(60):
            try:
                if sel.is_element_present("link=report"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=report"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=report")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_text_present("qualitio report"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "qualitio: report" == sel.get_title(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.assertEqual("qualitio: report", sel.get_title())
        try: self.failUnless(sel.is_text_present("qualitio report"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("link=BigProject"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=BigProject"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=BigProject")
        for i in range(60):
            try:
                if sel.is_element_present("//div[@id='application-view-footer']/div/a[2]/span"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("//div[@id='application-view-footer']/div/a[2]/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//div[@id='application-view-footer']/div/a[2]/span")
        for i in range(60):
            try:
                if sel.is_text_present("report directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("new"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("report directory"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("new"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id_name", "Report directory")
        sel.select("id_parent", "label=---------")
        sel.type("id_description", "Description\nDescription")
        for i in range(60):
            try:
                if sel.is_element_present("Reportd"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("Reportd"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("Reportd")
        for i in range(60):
            try:
                if sel.is_element_present("link=Report directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=Report directory"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=Report directory")
        for i in range(60):
            try:
                if sel.is_text_present("report directory: Report directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("report directory: Report directory"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("full name: /Report directory"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("description"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Description\nDescription"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("children:"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("id"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("path"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("modified"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("created"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("No data available in table"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("exact:Search:"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//input[@type='text']"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//div[@id='application-view-footer']/div/a[1]/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))


class Test44ReportReportCreate(BaseSeleniumTestCase):
    
    def test_44_report_report_create(self):
        self.login()
        sel = self.selenium
        sel.open("/require/")
        self.assertEqual("qualitio: requirements", sel.get_title())
        for i in range(60):
            try:
                if sel.is_element_present("link=report"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=report"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=report")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_text_present("qualitio report"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "qualitio: report" == sel.get_title(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.assertEqual("qualitio: report", sel.get_title())
        try: self.failUnless(sel.is_text_present("qualitio report"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("link=BigProject"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=BigProject"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=BigProject")
        for i in range(60):
            try:
                if sel.is_element_present("//div[@id='application-view-footer']/div/a[2]/span"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("//div[@id='application-view-footer']/div/a[2]/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//div[@id='application-view-footer']/div/a[1]/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//div[@id='application-view-footer']/div/a[1]/span")
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
        try: self.failUnless(sel.is_text_present("test run"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("new"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id_name", "report testcases")
        sel.type("id_context-0-name", "TESTCASES")
        sel.type("id_context-0-query", "TestCase.all()")
        sel.type("id_template", "<h1>Testcases</h1> <br/> {% for testcase in TESTCASES %} <h2>{{testcase.name}}</h2> <ul>     <li><b>name</b>: {{testcase.name}}</li>     <li><b>path</b>: {{testcase.path}}</li>     <li><b>requirement</b>: {{testcase.requirement.name|default:'empty'}}</li> </ul> <hr/> <br/> {% endfor %}")
        sel.click("//input[@value='Save']")
        for i in range(60):
            try:
                if sel.is_element_present("link=report testcases"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("report testcases"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=report testcases")
        for i in range(60):
            try:
                if sel.is_text_present("exact:report: report testcases"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("path: /BigProject/"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("exact:report: report testcases"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("path: /BigProject/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("name: report testcases"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("format: text/html"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("link: http://127.0.0.1:8000/report/external/3/bigproject/report-testcases"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("public: no"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Testcases"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Close navigation"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Open navigation"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("TestCase"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("TestCase1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("TestCase10"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("TestCase11"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("TestCase12"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("TestCase13"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("TestCase14"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("TestCase2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("TestCase3"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("TestCase4"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("TestCase5"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("TestCase6"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("TestCase7"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("TestCase8"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("TestCase9"))
        except AssertionError, e: self.verificationErrors.append(str(e))


if __name__ == "__main__":
    unittest.main()
