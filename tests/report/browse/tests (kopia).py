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
        sel.open("/project/meego/store/#testcasedirectory/1/details/")
        self.assertEqual("qualitio: login", sel.get_title())
        try: self.failUnless(sel.is_text_present("test@qualitio"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id=id_username"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("id=id_password")
        sel.type("id=id_password", "admin")
        try: self.failUnless(sel.is_element_present("id=id_username"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("id=id_username")
        sel.type("id=id_username", "qualitio1@gmail.com")
        try: self.assertEqual("qualitio1@gmail.com", sel.get_value("id=id_username"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id=id_password"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//input[@value='login']"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//input[@value='login']")
        for i in range(60):
            try:
                if sel.is_text_present("test@Qualitio"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=store"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        sel.click("link=filter")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_element_present("id=id_username"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        sel.click("id=id_username")
        sel.type("id=id_username", "qualitio1@gmail.com")
        sel.click("id=id_password")
        sel.type("id=id_password", "admin")
        sel.click("//input[@value='login']")
        sel.wait_for_page_to_load("30000")


class Test01Loginreport(BaseSeleniumTestCase):
    
    def test_01_loginreport(self):
        sel = self.selenium
        sel.open("/project/meego/report/")
        self.assertEqual("qualitio: login", sel.get_title())
        for i in range(60):
            try:
                if sel.is_text_present("test@qualitio"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test@qualitio"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("id_username")
        sel.type("id_username", "qualitio1@gmail.com")
        sel.click("id_password")
        sel.type("id_password", "admin")
        try: self.assertEqual("qualitio: login", sel.get_title())
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//input[@value='login']"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//input[@value='login']")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if "test@qualitio :: report" == sel.get_title(): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        self.assertEqual("test@qualitio :: report", sel.get_title())
        for i in range(60):
            try:
                if sel.is_text_present("test@Qualitio"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test@Qualitio"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("account admin"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=logout"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=logout")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("qualitio: login", sel.get_title())
        try: self.failUnless(sel.is_text_present("test@qualitio"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("id_username")
        sel.type("id_username", "qualitio1@gmail.com")
        sel.click("id_password")
        sel.type("id_password", "admin")
        sel.click("//input[@value='login']")
        sel.wait_for_page_to_load("30000")


class Test43ReportRepdirectCreate(BaseSeleniumTestCase):
    
    def test_43_report_repdirect_create(self):
        self.login()
        sel = self.selenium
        sel.open("/project/meego/require/#requirement/1/details/")
        self.assertEqual("test@qualitio :: require", sel.get_title())
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
                if sel.is_text_present("test@Qualitio"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "test@qualitio :: report" == sel.get_title(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.assertEqual("test@qualitio :: report", sel.get_title())
        try: self.failUnless(sel.is_text_present("test@Qualitio"))
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
        try: self.failUnless(sel.is_text_present("id"))
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
        sel.open("/project/meego/require/#requirement/1/details/")
        self.assertEqual("test@qualitio :: require", sel.get_title())
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
                if sel.is_text_present("test@Qualitio"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "test@qualitio :: report" == sel.get_title(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.assertEqual("test@qualitio :: report", sel.get_title())
        try: self.failUnless(sel.is_text_present("test@Qualitio"))
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
        for i in range(60):
            try:
                if sel.is_text_present("full name:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("report directory: BigProject"): break
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
                if sel.is_text_present("report"): break
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
                if sel.is_element_present("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("report"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("new"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id_name", "report testcases")
        sel.type("id_context-0-name", "TESTCASES")
        sel.type("id_context-0-query", "TestCase.all()")
        sel.type("id_template", "<h1>Testcases</h1> <br/> {% for testcase in TESTCASES %} <h2>{{testcase.name}}</h2> <ul>     <li><b>name</b>: {{testcase.name}}</li>     <li><b>path</b>: {{testcase.path}}</li>     <li><b>requirement</b>: {{testcase.requirement.name|default:'empty'}}</li> </ul> <hr/> <br/> {% endfor %}")
        for i in range(60):
            try:
                if sel.is_element_present("//input[@value='Save']"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("//input[@value='Save']"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//input[@value='Save']")
        for i in range(60):
            try:
                if sel.is_element_present("//li[@id='1_reportdirectory']/ins"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
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
        for i in range(60):
            try:
                if sel.is_text_present("name: report testcases"): break
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
        try: self.failUnless(sel.is_text_present("link: http://"))
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



class Test45ReportModPublic(BaseSeleniumTestCase):
    
    def test_45_report_mod_public(self):
        self.login()
        sel = self.selenium
        sel.open("/project/meego/require/#requirement/1/details/")
        self.assertEqual("test@qualitio :: require", sel.get_title())
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
                if sel.is_text_present("test@Qualitio"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "test@qualitio :: report" == sel.get_title(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.assertEqual("test@qualitio :: report", sel.get_title())
        try: self.failUnless(sel.is_text_present("test@Qualitio"))
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
                if sel.is_text_present("report directory: BigProject"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("Report, html", sel.get_table("css=div.dataTables_scrollBody > table.display.1.2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Report, json", sel.get_table("css=div.dataTables_scrollBody > table.display.2.2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("report testcases", sel.get_table("css=div.dataTables_scrollBody > table.display.3.2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=Report, html")
        for i in range(60):
            try:
                if sel.is_text_present("exact:report: Report, html"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("/BigProject/"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("report: Report, html", sel.get_text("css=h1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("public: yes"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=edit"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_text_present("report : Report, html"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("id=id_parent"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Public"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id=id_public"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("id=id_public")
        for i in range(60):
            try:
                if "off" == sel.get_value("id=id_public"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("id=id_public")
        for i in range(60):
            try:
                if "on" == sel.get_value("id=id_public"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("//input[@value='Save']"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//input[@value='Save']")
        for i in range(60):
            try:
                if sel.is_element_present("id=id_mime"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("exact:report : Report, html"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "details" == sel.get_text("link=details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if "test@qualitio :: report" == sel.get_title(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "details" == sel.get_text("link=details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("id=id_parent"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_text_present("exact:report: Report, html"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("exact:link:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "edit" == sel.get_text("link=edit"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "path:" == sel.get_text("css=span.name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("exact:public:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("public: yes"))
        except AssertionError, e: self.verificationErrors.append(str(e))


class Test46ReportCheckPublic(BaseSeleniumTestCase):
    
    def test_46_report_check_public(self):
        sel = self.selenium
        sel.open("/project/meego/report/external/1/bigproject/report-html/2011/04/22")
        for i in range(60):
            try:
                if sel.is_text_present("test@qualitio"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "" == sel.get_text("id=id_username"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "" == sel.get_text("id=id_password"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("", sel.get_text("id=id_username"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("", sel.get_text("id=id_password"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        self.assertEqual("qualitio: login", sel.get_title())
        sel.open("/project/meego/report/external/2/bigproject/report-html/2011/04/22")
        for i in range(60):
            try:
                if sel.is_text_present("Report, html"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "Report, html" == sel.get_title(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.assertEqual("Report, html", sel.get_title())
        try: self.failUnless(sel.is_text_present("Report, html"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Testcases"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Close navigation"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("name: Close navigation"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("path: /MeeGo Netbook/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("requirement: MeeGo"))
        except AssertionError, e: self.verificationErrors.append(str(e))

class Test46ReportCheckPublicNo(BaseSeleniumTestCase):
    
    def test_46_report_check_public_no(self):
        sel = self.selenium
        sel.open("/project/meego/report/external/1/bigproject/report-html/2011/04/22")
        for i in range(60):
            try:
                if sel.is_text_present("test@qualitio"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "" == sel.get_text("id=id_username"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "" == sel.get_text("id=id_password"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("", sel.get_text("id=id_username"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("", sel.get_text("id=id_password"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        self.assertEqual("qualitio: login", sel.get_title())
        sel.open("/project/meego/report/external/1/bigproject/report-json/2011/04/20")
        sel.wait_for_page_to_load("")
        for i in range(60):
            try:
                if sel.is_element_present("link=test@qualitio"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "Login" == sel.get_text("css=h1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("//input[@value='login']"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=test@qualitio"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=h1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id=id_username"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id=id_password"))
        except AssertionError, e: self.verificationErrors.append(str(e))


class Test47ReportModDirect(BaseSeleniumTestCase):
    
    def test_47_report_mod_direct(self):
        self.login()
        sel = self.selenium
        sel.open("/project/meego/report/#reportdirectory/1/details/")
        for i in range(60):
            try:
                if "test@qualitio :: report" == sel.get_title(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "test@qualitio :: report" == sel.get_title(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("test@Qualitio"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.assertEqual("test@qualitio :: report", sel.get_title())
        sel.click("link=BigProject")
        for i in range(60):
            try:
                if sel.is_text_present("test@Qualitio"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "edit" == sel.get_text("link=edit"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=edit"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_text_present("report directory : BigProject"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("id=id_name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id=id_name", "BigProject modify")
        sel.select("id=id_parent", "label=2: /Report directory")
        sel.type("id=id_description", "description\ndescription")
        for i in range(60):
            try:
                if sel.is_element_present("name=Reportd"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("name=Reportd"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("name=Reportd")
        for i in range(60):
            try:
                if sel.is_text_present("report directory saved"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("report directory saved"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_text_present("report directory: BigProject modify"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_element_present("link=details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id=id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=details"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_text_present("report directory: BigProject modify"): break
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
                if sel.is_element_present("css=span.active"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("report directory: BigProject modify"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("full name: /Report directory/BigProject modify"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("description\ndescription"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_text_present("report directory : BigProject modify"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id=id_name", "BigProject")
        sel.select("id=id_parent", "label=---------")
        sel.type("id=id_description", "")
        for i in range(60):
            try:
                if sel.is_element_present("name=Reportd"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("name=Reportd")


if __name__ == "__main__":
    unittest.main()