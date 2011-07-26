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
        try: self.failUnless(sel.is_text_present("qualitio"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_username"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("id_password")
        sel.type_keys("id_password", "admin")
        try: self.failUnless(sel.is_element_present("id_username"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("id_username")
        sel.type_keys("id_username", "admin")
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
        sel.click("link=filter")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_element_present("id_username"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("id_username")
        sel.type("id_username", "admin")
        sel.click("id_password")
        sel.type("id_password", "admin")
        sel.click("//input[@value='login']")
        sel.wait_for_page_to_load("30000")


class Test01Loginstore(BaseSeleniumTestCase):
    
    def test_01_loginstore(self):
        sel = self.selenium
        sel.open("/store/")
        self.assertEqual("qualitio: login", sel.get_title())
        for i in range(60):
            try:
                if sel.is_text_present("qualitio"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("qualitio"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("id_username")
        sel.type("id_username", "admin")
        sel.click("id_password")
        sel.type("id_password", "admin")
        sel.click("css=div.right")
        try: self.failUnless(sel.is_element_present("//input[@value='login']"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//input[@value='login']")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("qualitio: store", sel.get_title())
        for i in range(60):
            try:
                if sel.is_text_present("qualitio store"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("qualitio store"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Welcome, admin"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=Log out"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=Log out")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("qualitio: login", sel.get_title())
        try: self.failUnless(sel.is_text_present("qualitio"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("id_username")
        sel.type("id_username", "admin")
        sel.click("id_password")
        sel.type("id_password", "admin")
        sel.click("css=div.right")
        sel.click("//input[@value='login']")
        sel.wait_for_page_to_load("30000")


class Test01StoreGlossary(BaseSeleniumTestCase):
    
    def test_01_store_glossary(self):
        self.login()
        sel = self.selenium
        sel.open("/account/")
        for i in range(60):
            try:
                if sel.is_text_present("qualitio"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.assertEqual("qualitio:", sel.get_title())
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
                if "qualitio store" == sel.get_text("css=div.logo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.assertEqual("qualitio: store", sel.get_title())
        for i in range(60):
            try:
                if sel.is_text_present("qualitio store"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=MeeGo Netbook"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=glossary"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("glossary", sel.get_text("link=glossary"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=glossary")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_element_present("css=input"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("css=span.ui-button-text"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("//div[@id='project-content']/div[2]/div/a/span"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("css=input"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//div[@id='project-content']/div[2]/div/a/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//div[@id='project-content']/div[2]/div/a"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//div[@id='project-content']/div[2]/div/a/span")
        for i in range(60):
            try:
                if sel.is_element_present("css=h1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "word" == sel.get_text("css=h1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("word"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Name", sel.get_text("css=label"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("default", sel.get_text("//form[@id='word_form']/div[3]/div/label"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("", sel.get_text("id_default-representation"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("Executed"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Save", sel.get_value("Executed"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id_name", "kolor")
        sel.type("id_default-representation", "kolor")
        sel.type("id_english-representation", "color")
        sel.type("id_german-representation", "farbe")
        try: self.failUnless(sel.is_element_present("Executed"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_element_present("id_word_1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("id_word_1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("kolor", sel.get_text("id_word_1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//div[@id='project-content']/div[2]/div/a/span")
        for i in range(60):
            try:
                if sel.is_element_present("css=h1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "word" == sel.get_text("css=h1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id=id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_name", "ekran")
        sel.type("id_default-representation", "ekran")
        sel.type("id_english-representation", "screen")
        sel.type("id_german-representation", "Bildschirm")
        try: self.failUnless(sel.is_element_present("name=Executed"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_text_present("word"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("css=input"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_word_2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("id_word_2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_word_2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if "ekran" == sel.get_text("id=id_word_2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("default"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_default-representation"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("english", sel.get_text("//form[@id='word_form']/div[3]/div[2]/label"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_english-representation"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("german", sel.get_text("//form[@id='word_form']/div[3]/div[3]/label"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_german-representation"))
        except AssertionError, e: self.verificationErrors.append(str(e))


class Test15StoreTestdirectVerify(BaseSeleniumTestCase):
    
    def test_15_store_testdirect_verify(self):
        self.login()
        sel = self.selenium
        sel.open("/require/#requirement/1/details/")
        try: self.assertEqual("qualitio: require", sel.get_title())
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_text_present("store"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("store", sel.get_text("link=store"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=store")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_text_present("qualitio store"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("qualitio store"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_text_present("MeeGo Netbook"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=MeeGo Netbook")
        for i in range(60):
            try:
                if sel.is_element_present("css=div#application-view-header h1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("application-view-header"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div#application-view-header h1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("test case directory: MeeGo Netbook"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("application-view-menu"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("details", sel.get_text("css=div#application-view-menu span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=edit"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div#application-view div:nth-child(3)"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("full name: /MeeGo Netbook"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("description"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=table"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div#application-view-footer div"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div#application-view-footer div a span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=a.button[href=\"#testcasedirectory/1/new/\"]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("create test case"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("create test case directory"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_text_present("Parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("css=form#testcasedirectory_form"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Parent"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_parent"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Description"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_description"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div#application-view-footer div"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("Executed"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Save", sel.get_value("Executed"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=history"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=history")
        for i in range(60):
            try:
                if sel.is_text_present("date"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("user"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("//div[@id='application-view']/div[3]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("date"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("user"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("comment"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("No data available in table"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Show 102550100 entries"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div.paginate_disabled_previous"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div.paginate_disabled_next"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("exact:Search:"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("css=input[type='text']"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")


class Test16StoreTestcaseVerify(BaseSeleniumTestCase):
    
    def test_16_store_testcase_verify(self):
        self.login()
        sel = self.selenium
        sel.open("/require/#requirement/1/details/")
        try: self.assertEqual("qualitio: require", sel.get_title())
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_text_present("store"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("store", sel.get_text("link=store"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=store")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_text_present("qualitio store"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("qualitio store"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_text_present("MeeGo Netbook"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=MeeGo Netbook")
        sel.click("css=li#1_testcasedirectory ins")
        for i in range(60):
            try:
                if sel.is_element_present("link=TestCase"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=TestCase")
        for i in range(60):
            try:
                if sel.is_text_present("test case: TestCase"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("application-view-header"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div#application-view-header h1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("test case: TestCase"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("application-view-menu"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("details", sel.get_text("css=div#application-view-menu span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=edit"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div#application-view div:nth-child(3)"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("full name:"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("exact:parent:"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("exact:status:"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("requirement"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_text_present("description"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_text_present("Parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Parent"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_parent"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Requirement"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_requirement"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Status"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_status"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Description"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_description"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Precondition"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_precondition"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=a#add-step-0 span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("add step", sel.get_text("css=a#add-step-0 span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div#application-view-footer div"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("Executed"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=input[value=\"Save\"]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Save", sel.get_value("css=input[value=\"Save\"]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=history"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=history")
        for i in range(60):
            try:
                if sel.is_text_present("date"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("user"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("date"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("user"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("comment"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("No data available in table"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Show 102550100 entries"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("exact:Search:"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=input[type='text']"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div.paginate_disabled_previous"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div.paginate_disabled_next"))
        except AssertionError, e: self.verificationErrors.append(str(e))


class Test17StoreTestdirectCreate(BaseSeleniumTestCase):
    
    def test_17_store_testdirect_create(self):
        self.login()
        sel = self.selenium
        sel.open("/require/#requirement/1/details/")
        try: self.assertEqual("qualitio: require", sel.get_title())
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if "store" == sel.get_text("link=store"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=store")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_text_present("MeeGo Netbook"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=MeeGo Netbook")
        for i in range(60):
            try:
                if sel.is_text_present("create test case directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("create test case directory"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=div#application-view-footer div a:nth-child(2)")
        for i in range(60):
            try:
                if sel.is_text_present("test case directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_name", "testcase directory")
        try: self.failUnless(sel.is_text_present("Description"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id_description", "Description of testcase directory")
        try: self.failUnless(sel.is_element_present("Executed"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("qualitio: store", sel.get_title())
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_text_present("test case directory: testcase directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("MeeGo Netbook"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=MeeGo Netbook")
        for i in range(60):
            try:
                if sel.is_text_present("test case directory: MeeGo Netbook"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("css=li#1_testcasedirectory ins"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=li#1_testcasedirectory ins")
        for i in range(60):
            try:
                if sel.is_element_present("link=testcase directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("testcase directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=testcase directory"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("testcase directory"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("testcase directory"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=testcase directory")
        for i in range(60):
            try:
                if sel.is_text_present("test case directory: testcase directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test case directory: testcase directory"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("exact:full name: /MeeGo Netbook/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("description Description of testcase directory"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_text_present("Description"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("Description of testcase directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Description of testcase directory"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=history"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=history")
        for i in range(60):
            try:
                if sel.is_text_present("date"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("user"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("comment"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Object created."))
        except AssertionError, e: self.verificationErrors.append(str(e))


class Test18StoreTestcaseCreate(BaseSeleniumTestCase):
    
    def test_18_store_testcase_create(self):
        self.login()
        sel = self.selenium
        sel.open("/require/#requirement/1/details/")
        try: self.assertEqual("qualitio: require", sel.get_title())
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if "store" == sel.get_text("link=store"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=store")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_text_present("MeeGo Netbook"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("qualitio: store", sel.get_title())
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=MeeGo Netbook")
        for i in range(60):
            try:
                if sel.is_text_present("create test case"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("create test case"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=div#application-view-footer div a")
        for i in range(60):
            try:
                if sel.is_text_present("test case"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("new"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test case"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div#application-view-menu span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("new", sel.get_text("css=div#application-view-menu span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Parent"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_parent"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.select("id_parent", "label=2: /MeeGo Handset bat")
        try: self.failUnless(sel.is_element_present("id_name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id_name", "test case 1")
        try: self.failUnless(sel.is_element_present("id_requirement"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.select("id_requirement", "label=1: /MeeGo")
        try: self.failUnless(sel.is_element_present("id_status"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.select("id_status", "label=Proposed")
        for i in range(60):
            try:
                if sel.is_element_present("id_description"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_description", "desription\ndesription")
        try: self.failUnless(sel.is_element_present("id_precondition"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id_precondition", "precondition\nprecondition")
        try: self.failUnless(sel.is_element_present("css=a#add-step-0 span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("add step", sel.get_text("css=a#add-step-0 span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=a#add-step-0 span")
        for i in range(60):
            try:
                if sel.is_text_present("Step 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("id_steps-0-description"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_steps-0-expected"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id_steps-0-description", "Description 1\nDescription 1")
        sel.type("id_steps-0-expected", "Expected 1\nExpected 1")
        try: self.failUnless(sel.is_element_present("//form[@id='testcase_form']/div[3]/div[2]/div[1]/a/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//form[@id='testcase_form']/div[3]/div[2]/div[1]/a/span")
        for i in range(60):
            try:
                if sel.is_text_present("Step 2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("id_steps-1-description"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_steps-1-expected"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id_steps-1-description", "Description 2\nDescription 2")
        sel.type("id_steps-1-expected", "Expected 2\nExpected 2")
        try: self.failUnless(sel.is_element_present("css=input.ui-button[value=\"Save\"]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=input.ui-button[value=\"Save\"]")
        for i in range(60):
            try:
                if sel.is_element_present("link=MeeGo Netbook"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "MeeGo Netbook" == sel.get_text("link=MeeGo Netbook"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=MeeGo Netbook"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("MeeGo Netbook"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("css=div#application-view-header h1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=test case 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=test case 1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if "test case 1" == sel.get_text("link=test case 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("test case 1", sel.get_text("link=test case 1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=test case 1")
        for i in range(60):
            try:
                if sel.is_text_present("test case: test case 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("/MeeGo Handset bat/test case 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("/MeeGo Handset bat/"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("full name: /MeeGo Handset bat/test case 1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("parent: /MeeGo Handset bat/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("status: Proposed"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=exact:1: /MeeGo"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("1: /MeeGo", sel.get_text("link=exact:1: /MeeGo"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("desription\ndesription"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("precondition"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("precondition\nprecondition"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=div#application-view div:nth-child(3)")
        try: self.failUnless(sel.is_text_present("step 1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("step 2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Description 1\nDescription 1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Expected 1\nExpected 1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Description 2\nDescription 2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Expected 2\nExpected 2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=history"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=history")
        for i in range(60):
            try:
                if sel.is_text_present("date"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("user"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("comment"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Object created. Added step \"1\" and added step \"2\"."))
        except AssertionError, e: self.verificationErrors.append(str(e))


class Test19StoreTestcaseDisplay(BaseSeleniumTestCase):
    
    def test_19_store_testcase_display(self):
        self.login()
        sel = self.selenium
        sel.open("/require/#requirement/1/details/")
        try: self.assertEqual("qualitio: require", sel.get_title())
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if "store" == sel.get_text("link=store"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=store")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_text_present("MeeGo Netbook"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("qualitio: store", sel.get_title())
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=MeeGo Netbook")
        sel.click("css=li#1_testcasedirectory ins")
        for i in range(60):
            try:
                if sel.is_text_present("MeeGo IVI BAT"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=MeeGo IVI BAT"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("MeeGo IVI BAT", sel.get_text("link=MeeGo IVI BAT"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("TestCase"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=TestCase")
        for i in range(60):
            try:
                if sel.is_text_present("test case: TestCase"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test case: TestCase"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_text_present("Parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Parent"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id_description", "test\n\ntest")
        sel.type("id_precondition", "test\n\ntest")
        sel.click("css=input.ui-button[value=\"Save\"]")
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
                if sel.is_element_present("link=history"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=details"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_text_present("test case: TestCase"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("full name: /MeeGo Netbook/TestCase"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("link=13: /MeeGo/TV/MeeGo Handset test"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=13: /MeeGo/TV/MeeGo Handset test"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("parent: /MeeGo Netbook/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("requirement: 13: /MeeGo/TV/MeeGo Handset test"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("description test\n\ntest"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("precondition test\n\ntest"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_text_present("Parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("Description"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_description", "")
        sel.type("id_precondition", "")
        sel.click("css=input.ui-button[value=\"Save\"]")
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
                if sel.is_element_present("link=history"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_text_present("test case: TestCase"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name: /MeeGo Netbook/TestCase"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test case: TestCase"))
        except AssertionError, e: self.verificationErrors.append(str(e))


class Test21StoreTreeVerify(BaseSeleniumTestCase):
    
    def test_21_store_tree_verify(self):
        self.login()
        sel = self.selenium
        sel.open("/require/#requirement/1/details/")
        for i in range(60):
            try:
                if sel.is_text_present("qualitio require"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.assertEqual("qualitio: require", sel.get_title())
        for i in range(60):
            try:
                if sel.is_text_present("MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=store")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_element_present("id=header"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "qualitio: store" == sel.get_title(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("qualitio store"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.assertEqual("qualitio: store", sel.get_title())
        for i in range(60):
            try:
                if sel.is_text_present("MeeGo Netbook"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=MeeGo Netbook")
        for i in range(60):
            try:
                if sel.is_text_present("test case directory: MeeGo Netbook"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test case directory: MeeGo Netbook"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=MeeGo Handset bat")
        for i in range(60):
            try:
                if sel.is_text_present("test case directory: MeeGo Handset bat"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test case directory: MeeGo Handset bat"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=li#1_testcasedirectory ins")
        for i in range(60):
            try:
                if "MeeGo IVI BAT" == sel.get_text("link=MeeGo IVI BAT"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=MeeGo IVI BAT")
        for i in range(60):
            try:
                if sel.is_text_present("test case directory: MeeGo IVI BAT"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test case directory: MeeGo IVI BAT"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("full name: /MeeGo Netbook/MeeGo IVI BAT"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("description"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=li#4_testcasedirectory ins")
        for i in range(60):
            try:
                if sel.is_text_present("Close navigation"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=Close navigation")
        for i in range(60):
            try:
                if sel.is_text_present("test case: Close navigation"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test case: Close navigation"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("/MeeGo Netbook/MeeGo IVI BAT/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=Open navigation")
        for i in range(60):
            try:
                if sel.is_text_present("test case: Open navigation"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test case: Open navigation"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("/MeeGo IVI BAT/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=TestCase")
        for i in range(60):
            try:
                if sel.is_text_present("test case: TestCase"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test case: TestCase"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("/MeeGo Netbook/"))
        except AssertionError, e: self.verificationErrors.append(str(e))


class Test22StoreTreeVerifyEdit(BaseSeleniumTestCase):
    
    def test_22_store_tree_verify_edit(self):
        self.login()
        sel = self.selenium
        sel.open("/require/#requirement/1/details/")
        for i in range(60):
            try:
                if sel.is_text_present("qualitio require"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.assertEqual("qualitio: require", sel.get_title())
        for i in range(60):
            try:
                if sel.is_text_present("MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=store")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_text_present("qualitio store"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.assertEqual("qualitio: store", sel.get_title())
        for i in range(60):
            try:
                if sel.is_text_present("MeeGo Netbook"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=MeeGo Netbook")
        for i in range(60):
            try:
                if sel.is_text_present("test case directory: MeeGo Netbook"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test case directory: MeeGo Netbook"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_element_present("id_name"): break
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
        sel.click("css=li#4_testcasedirectory ins")
        for i in range(60):
            try:
                if sel.is_element_present("link=Close navigation"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("MeeGo Netbook", sel.get_value("id_name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=MeeGo IVI BAT")
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
                if "MeeGo IVI BAT" == sel.get_value("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("MeeGo IVI BAT", sel.get_value("id_name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
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
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_element_present("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("MeeGo Handset bat", sel.get_value("id_name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=Close navigation")
        for i in range(60):
            try:
                if sel.is_text_present("test case: Close navigation"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test case: Close navigation"))
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
                if sel.is_element_present("id_description"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("Close navigation", sel.get_value("id_name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=TestCase")
        for i in range(60):
            try:
                if sel.is_text_present("test case: TestCase"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test case: TestCase"))
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
                if "TestCase" == sel.get_value("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("TestCase", sel.get_value("id_name"))
        except AssertionError, e: self.verificationErrors.append(str(e))


class Test26StoreTestdirectModify(BaseSeleniumTestCase):
    
    def test_26_store_testdirect_modify(self):
        self.login()
        sel = self.selenium
        sel.open("/require/#requirement/1/details/")
        self.assertEqual("qualitio: require", sel.get_title())
        for i in range(60):
            try:
                if "store" == sel.get_text("link=store"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=store")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_text_present("MeeGo Netbook"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.assertEqual("qualitio: store", sel.get_title())
        sel.click("link=MeeGo Handset bat")
        for i in range(60):
            try:
                if sel.is_text_present("create test case directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("create test case directory"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=div#application-view-footer div a:nth-child(2)")
        for i in range(60):
            try:
                if sel.is_text_present("test case directory"): break
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
                if "" == sel.get_text("id=id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_name", "test case directory 2")
        try: self.failUnless(sel.is_element_present("id=id_description"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id_description", "direcory2\ndirectory2")
        try: self.failUnless(sel.is_element_present("name=Executed"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("Executed")
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
        for i in range(60):
            try:
                if sel.is_text_present("test case directory: test case directory 2"): break
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
                if sel.is_text_present("details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_text_present("test case directory: test case directory 2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name: /MeeGo Handset bat/test case directory 2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("full name: /MeeGo Handset bat/test case directory 2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("description"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("direcory2\ndirectory2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=div#application-view-footer div a")
        for i in range(60):
            try:
                if sel.is_text_present("test case"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("new"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_name", "test case1")
        sel.select("id_requirement", "label=5: /MeeGo/MeeGo Handset")
        sel.select("id_status", "label=Proposed")
        sel.type("id_description", "description\ndescription")
        sel.type("id_precondition", "descriptprec\ndescriptprec")
        sel.click("css=input[name='Executed'][value='Save']")
        for i in range(60):
            try:
                if sel.is_text_present("test case: test case1"): break
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
                if sel.is_element_present("link=details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_text_present("test case: test case1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name: /MeeGo Handset bat/test case directory 2/test case1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("description\ndescription"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("descriptprec\ndescriptprec"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=test case directory 2")
        for i in range(60):
            try:
                if sel.is_text_present("test case directory: test case directory 2"): break
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
                if sel.is_text_present("test case directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("new"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_name", "testcasesubdirectory")
        sel.type("id_description", "descr1\ndesr1")
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_text_present("test case directory: testcasesubdirectory"): break
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
                if sel.is_element_present("link=details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_text_present("test case directory: testcasesubdirectory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("descr1\ndesr1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=test case directory 2")
        for i in range(60):
            try:
                if sel.is_text_present("test case directory: test case directory 2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=li#6_testcasedirectory ins")
        try: self.failUnless(sel.is_element_present("//div[@id='application-view']/div[3]/div[3]/div[1]/div[2]/table/tbody/tr[1]/td[1]/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=/MeeGo Handset bat/test case directory 2/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//div[@id='application-view']/div[3]/div[3]/div[1]/div[2]/table/tbody/tr[1]/td[4]/a"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("testcasesubdirectory"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//div[@id='application-view']/div[3]/div[3]/div[1]/div[2]/table/tbody/tr[2]/td[1]/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//div[@id='application-view']/div[3]/div[3]/div[1]/div[2]/table/tbody/tr[2]/td[4]/a"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("test case1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=MeeGo Handset"))
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
                if sel.is_text_present("Parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.select("id_parent", "label=1: /MeeGo Netbook")
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_text_present("test case directory: test case directory 2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_name"): break
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
        try: self.failUnless(sel.is_element_present("link=details"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_text_present("full name: /MeeGo Netbook/test case directory 2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("full name: /MeeGo Netbook/test case directory 2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=/MeeGo Netbook/test case directory 2/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("/MeeGo Netbook/test case directory 2/", sel.get_text("link=/MeeGo Netbook/test case directory 2/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_text_present("qualitio store"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=test case directory 2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=test case directory 2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=test case directory 2")
        for i in range(60):
            try:
                if sel.is_text_present("full name: /MeeGo Netbook/test case directory 2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("full name: /MeeGo Netbook/test case directory 2"))
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
        sel.type("id_name", "modified test case directory 2")
        sel.type("id_description", "modifieddirectory2\nmodifieddirectory2")
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_element_present("link=details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_name"): break
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
        try: self.failUnless(sel.is_element_present("link=details"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_text_present("test case directory: modified test case directory 2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test case directory: modified test case directory 2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("modifieddirectory2\nmodifieddirectory2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=/MeeGo Netbook/modified test case directory 2/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("/MeeGo Netbook/modified test case directory 2/", sel.get_text("link=/MeeGo Netbook/modified test case directory 2/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("full name: /MeeGo Netbook/modified test case directory 2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("full name: /MeeGo Netbook/modified test case directory 2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//div[@id='application-view']/div[3]/div[3]/div[1]/div[2]/table/tbody/tr[1]/td[1]/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//div[@id='application-view']/div[3]/div[3]/div[1]/div[2]/table/tbody/tr[2]/td[1]/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=history"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=history")
        for i in range(60):
            try:
                if sel.is_text_present("date"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("user"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("comment"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Changed parent."))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Changed name and changed description."))
        except AssertionError, e: self.verificationErrors.append(str(e))



class Test27StoreTestcaseModify(BaseSeleniumTestCase):
    
    def test_27_store_testcase_modify(self):
        self.login()
        sel = self.selenium
        sel.open("/require/#requirement/1/details/")
        self.assertEqual("qualitio: require", sel.get_title())
        for i in range(60):
            try:
                if "store" == sel.get_text("link=store"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=store")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_text_present("MeeGo Netbook"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.assertEqual("qualitio: store", sel.get_title())
        sel.click("link=MeeGo Handset bat")
        for i in range(60):
            try:
                if sel.is_text_present("create test case directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("create test case"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("create test case directory"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("create test case"))
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
                if sel.is_text_present("new"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_name", "test case modification")
        sel.select("id_requirement", "label=5: /MeeGo/MeeGo Handset")
        sel.select("id_status", "label=Proposed")
        sel.type("id_description", "testcase description")
        sel.type("id_precondition", "test case precondition")
        sel.click("css=a#add-step-0 span")
        for i in range(60):
            try:
                if sel.is_text_present("Step 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_steps-0-description", "step1 description")
        sel.type("id_steps-0-expected", "step 1 expected")
        sel.click("css=input[name='Executed'][value='Save']")
        for i in range(60):
            try:
                if sel.is_text_present("test case: test case modification"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=details"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_text_present("full name: /MeeGo Handset bat/test case modification"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("exact:parent:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test case: test case modification"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("full name: /MeeGo Handset bat/test case modification"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("parent: /MeeGo Handset bat/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=exact:5: /MeeGo/MeeGo Handset"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("5: /MeeGo/MeeGo Handset", sel.get_text("link=exact:5: /MeeGo/MeeGo Handset"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("description testcase description"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("test case precondition"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("step1 description"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("step 1 expected"))
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
        sel.type("id_name", "modify test case modification")
        sel.select("id_parent", "label=1: /MeeGo Netbook")
        sel.select("id_requirement", "label=2: /MeeGo/Notebook")
        sel.type("id_description", "modify testcase description")
        sel.type("id_precondition", "modify test case precondition")
        sel.type("id_steps-0-description", "modify step1 description")
        sel.type("id_steps-0-expected", "modify step 1 expected")
        sel.click("//form[@id='testcase_form']/div[3]/div[2]/div[1]/a/span")
        for i in range(60):
            try:
                if sel.is_text_present("Step 2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_steps-1-description", "step 2 description")
        sel.type("id_steps-1-expected", "step 2 expected")
        sel.click("//form[@id='testcase_form']/div[3]/div[3]/div[1]/a/span")
        for i in range(60):
            try:
                if sel.is_text_present("Step 3"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_steps-2-description", "step 3 decription")
        sel.type("id_steps-2-expected", "step 3 expected")
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
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_element_present("link=details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=details"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_text_present("test case: modify test case modification"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name: /MeeGo Netbook/modify test case modification"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test case: modify test case modification"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("full name: /MeeGo Netbook/modify test case modification"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("parent: /MeeGo Netbook/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=exact:2: /MeeGo/Notebook"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("2: /MeeGo/Notebook", sel.get_text("link=exact:2: /MeeGo/Notebook"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("modify testcase description"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("modify test case precondition"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("modify step1 description"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("modify step 1 expected"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("step 2 description"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("step 2 expected"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("step 3 decription"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("step 3 expected"))
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
        sel.click("//form[@id='testcase_form']/div[3]/div[4]/div[1]/a/span")
        for i in range(60):
            try:
                if sel.is_text_present("Step 4"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Step 4"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id_steps-3-description", "step 4 description")
        sel.type("id_steps-3-expected", "step 4 expected")
        sel.click("id_steps-1-DELETE")
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
                if sel.is_element_present("link=history"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_text_present("test case: modify test case modification"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name: /MeeGo Netbook/modify test case modification"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("parent: /MeeGo Netbook/"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("step 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("step 1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("modify step1 description", sel.get_text("css=div.description"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("step 3 decription", sel.get_text("//div[@id='application-view']/div[4]/div[3]/div/div"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("step 4 description", sel.get_text("//div[@id='application-view']/div[4]/div[4]/div/div"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=history"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=history")
        for i in range(60):
            try:
                if sel.is_text_present("date"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("user"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("comment"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Changed name, changed requirement, changed description, changed precondition and changed parent. Added step \"2\", added step \"3\" and changed description and expected for step \"1\"."))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Added step \"4\" and deleted step \"2\"."))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Object created. Added step \"1\"."))
        except AssertionError, e: self.verificationErrors.append(str(e))


class Test33StoreSamename(BaseSeleniumTestCase):
    
 
   def test_33_store_samename(self):
        self.login()
        sel = self.selenium
        sel.open("/require/#requirement/1/details/")
        self.assertEqual("qualitio: require", sel.get_title())
        for i in range(60):
            try:
                if "MeeGo" == sel.get_text("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=store")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("qualitio: store", sel.get_title())
        for i in range(60):
            try:
                if "MeeGo Handset bat" == sel.get_text("link=MeeGo Handset bat"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=MeeGo Netbook")
        for i in range(60):
            try:
                if sel.is_text_present("test case directory: MeeGo Netbook"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test case directory: MeeGo Netbook"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=div#application-view-footer div a:nth-child(2)")
        for i in range(60):
            try:
                if sel.is_text_present("test case directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("new"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_name", "MeeGo IVI BAT")
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_text_present("Validation errors: \"parent\" and \"name\" fields need to be always unique together."): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Validation errors: \"parent\" and \"name\" fields need to be always unique together."))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id_name", "MeeGo IVI BAT2")
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_element_present("link=details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("test case directory: MeeGo IVI BAT2"): break
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
                if sel.is_element_present("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_text_present("test case directory: MeeGo IVI BAT2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test case directory: MeeGo IVI BAT2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("full name: /MeeGo Netbook/MeeGo IVI BAT2"))
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
        sel.type("id_name", "MeeGo IVI BAT")
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_text_present("Validation errors: \"parent\" and \"name\" fields need to be always unique together."): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Validation errors: \"parent\" and \"name\" fields need to be always unique together."))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.select("id_parent", "label=2: /MeeGo Handset bat")
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_element_present("id_description"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_name"): break
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
                if sel.is_element_present("link=history"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_text_present("test case directory: MeeGo IVI BAT"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name: /MeeGo Handset bat/MeeGo IVI BAT"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("full name: /MeeGo Handset bat/MeeGo IVI BAT"))
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
                if sel.is_element_present("id_parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.select("id_parent", "label=1: /MeeGo Netbook")
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_text_present("Validation errors: \"parent\" and \"name\" fields need to be always unique together."): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Validation errors: \"parent\" and \"name\" fields need to be always unique together."))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id_name", "testcase directory same name")
        sel.click("Executed")
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
                if sel.is_element_present("link=history"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_text_present("test case directory: testcase directory same name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name: /MeeGo Netbook/testcase directory same name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test case directory: testcase directory same name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("full name: /MeeGo Netbook/testcase directory same name"))
        except AssertionError, e: self.verificationErrors.append(str(e))



class Test34StoreSamename(BaseSeleniumTestCase):
    
   def test_34_store_samename(self):
        self.login()
        sel = self.selenium
        sel.open("/require/#requirement/1/details/")
        self.assertEqual("qualitio: require", sel.get_title())
        for i in range(60):
            try:
                if "MeeGo" == sel.get_text("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=store")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("qualitio: store", sel.get_title())
        for i in range(60):
            try:
                if "MeeGo Handset bat" == sel.get_text("link=MeeGo Handset bat"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=MeeGo Netbook")
        for i in range(60):
            try:
                if sel.is_text_present("test case directory: MeeGo Netbook"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test case directory: MeeGo Netbook"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=div#application-view-footer div a")
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
        for i in range(60):
            try:
                if sel.is_element_present("id_parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_name", "TestCase")
        sel.select("id_status", "label=Proposed")
        sel.click("css=input[name='Executed'][value='Save']")
        for i in range(60):
            try:
                if sel.is_text_present("Validation errors: \"parent\" and \"name\" fields need to be always unique together."): break
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
                if sel.is_element_present("id_requirement"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Validation errors: \"parent\" and \"name\" fields need to be always unique together."))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_name", "TestCase2")
        for i in range(60):
            try:
                if sel.is_element_present("id_description"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_precondition"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("Executed"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.wait_for_page_to_load("")
        try: self.failUnless(sel.is_element_present("Executed"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("Executed")
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
        for i in range(60):
            try:
                if sel.is_element_present("id_precondition"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.refresh()
        sel.wait_for_page_to_load("30000")
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
        for i in range(60):
            try:
                if sel.is_element_present("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=MeeGo Netbook")
        for i in range(60):
            try:
                if sel.is_element_present("link=edit"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=TestCase2")
        for i in range(60):
            try:
                if sel.is_text_present("test case: TestCase2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("full name: /MeeGo Netbook/TestCase2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("test case: TestCase2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("full name: /MeeGo Netbook/TestCase2"))
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
        sel.type("id_name", "TestCase")
        sel.click("css=input[name='Executed'][value='Save']")
        for i in range(60):
            try:
                if sel.is_text_present("Validation errors: \"parent\" and \"name\" fields need to be always unique together."): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Validation errors: \"parent\" and \"name\" fields need to be always unique together."))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.select("id_parent", "label=4: /MeeGo Netbook/MeeGo IVI BAT")
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
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_element_present("link=details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_text_present("test case: TestCase"): break
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
                if sel.is_text_present("full name: /MeeGo Netbook/MeeGo IVI BAT/TestCase"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("full name: /MeeGo Netbook/MeeGo IVI BAT/TestCase"))
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
                if sel.is_element_present("id_parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.select("id_parent", "label=1: /MeeGo Netbook")
        sel.click("css=input[name='Executed'][value='Save']")
        for i in range(60):
            try:
                if sel.is_text_present("Validation errors: \"parent\" and \"name\" fields need to be always unique together."): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Validation errors: \"parent\" and \"name\" fields need to be always unique together."))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id_name", "TestCase same name")
        for i in range(60):
            try:
                if sel.is_element_present("Executed"): break
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
                if sel.is_element_present("link=history"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=details"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_text_present("test case: TestCase same name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name: /MeeGo Netbook/TestCase same name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test case: TestCase same name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("full name: /MeeGo Netbook/TestCase same name"))
        except AssertionError, e: self.verificationErrors.append(str(e))



class Test35StoreTestcaseStatus(BaseSeleniumTestCase):

    
    def test_35_store_testcase_status(self):
        self.login()
        sel = self.selenium
        sel.open("/require/#requirement/1/details/")
        self.assertEqual("qualitio: require", sel.get_title())
        for i in range(60):
            try:
                if "store" == sel.get_text("link=store"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=store")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_text_present("MeeGo Netbook"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.assertEqual("qualitio: store", sel.get_title())
        sel.click("link=MeeGo Handset bat")
        for i in range(60):
            try:
                if sel.is_text_present("create test case directory"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("create test case"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("create test case directory"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("create test case"))
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
                if sel.is_text_present("new"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("Executed"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_text_present("Validation errors:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("This field is required."): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Validation errors:"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("This field is required.", sel.get_text("css=div#name_wrapper div"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id_name", "test case 2")
        sel.select("id_status", "label=Proposed")
        sel.type("id_description", "testcase description")
        sel.type("id_precondition", "test case precondition")
        sel.click("css=a#add-step-0 span")
        for i in range(60):
            try:
                if sel.is_text_present("Step 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_steps-0-description", "step1 description")
        sel.type("id_steps-0-expected", "step 1 expected")
        sel.click("css=input[name='Executed'][value='Save']")
        for i in range(60):
            try:
                if sel.is_text_present("test case: test case 2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=details"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_text_present("full name: /MeeGo Handset bat/test case 2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("exact:parent:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("test case: test case 2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("full name: /MeeGo Handset bat/test case 2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("parent: /MeeGo Handset bat/"))
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
        sel.select("id_status", "label=Done")
        for i in range(60):
            try:
                if sel.is_element_present("Executed"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("Executed"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_element_present("link=details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=history"): break
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
                if sel.is_element_present("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_text_present("test case: test case 2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("status: Done"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=history"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=history")
        for i in range(60):
            try:
                if sel.is_text_present("date"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("user"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Changed status."))
        except AssertionError, e: self.verificationErrors.append(str(e))


class Test36StoreLanguage(BaseSeleniumTestCase):

    
    def test_36_store_language(self):
        self.login()
        sel = self.selenium
        sel.open("/account/")
        for i in range(60):
            try:
                if sel.is_text_present("qualitio"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.assertEqual("qualitio:", sel.get_title())
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
                if "qualitio store" == sel.get_text("css=div.logo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.assertEqual("qualitio: store", sel.get_title())
        for i in range(60):
            try:
                if sel.is_text_present("qualitio store"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=MeeGo Netbook"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=#1_testcasedirectory > ins.jstree-icon"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=#1_testcasedirectory > ins.jstree-icon")
        for i in range(60):
            try:
                if sel.is_element_present("link=MeeGo IVI BAT"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("css=#4_testcasedirectory > ins.jstree-icon"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=#4_testcasedirectory > ins.jstree-icon")
        for i in range(60):
            try:
                if "Close navigation" == sel.get_text("link=Close navigation"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("Close navigation"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=Close navigation"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=Close navigation")
        for i in range(60):
            try:
                if sel.is_element_present("link=edit"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("test case: Close navigation"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=edit"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_element_present("id=id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id=id_parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id=id_description", "$kolor$  \n$ekran$")
        for i in range(60):
            try:
                if sel.is_element_present("name=Executed"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("name=Executed"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("name=Executed")
        for i in range(60):
            try:
                if "test case: Close navigation" == sel.get_text("css=h1"): break
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
                if "details" == sel.get_text("link=details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "history" == sel.get_text("link=history"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_element_present("css=span.name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("//div[@id='application-view']/div[3]/div[2]/span"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=exact:1: /MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("kolor"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("ekran"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=label"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Language:", sel.get_text("css=label"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id=id_language"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.select("id=id_language", "label=english")
        for i in range(60):
            try:
                if "Current glossary language: english" == sel.get_text("//div[@id='notification']/div/div/span[2]"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Current glossary language: english"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_text_present("description"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("color"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("screen"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("description"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("color"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("screen"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=option[value=3]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("german", sel.get_text("css=option[value=3]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.select("id=id_language", "label=german")
        for i in range(60):
            try:
                if "Current glossary language: german" == sel.get_text("//div[@id='notification']/div/div/span[2]"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Current glossary language: german"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("description"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if "farbe" == sel.get_text("css=span.glosarry-word.translation"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Bildschirm"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("farbe"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("id=id_language"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.select("id=id_language", "label=default")
        for i in range(60):
            try:
                if "Current glossary language: default" == sel.get_text("//div[@id='notification']/div/div/span[2]"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Current glossary language: default"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if "edit" == sel.get_text("link=edit"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("edit", sel.get_text("link=edit"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=edit")
        for i in range(60):
            try:
                if "" == sel.get_text("id=id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id=id_parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id=id_description", "")
        for i in range(60):
            try:
                if sel.is_element_present("name=Executed"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("name=Executed"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("name=Executed")
    


if __name__ == "__main__":
    unittest.main()
