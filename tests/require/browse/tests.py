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


class HeaderpageVerifytext(BaseSeleniumTestCase):
    
    def test_headerpage_verifytext(self):
        sel = self.selenium
        sel.open("/require/#requirement/1/details/")
        sel.click("link=MeeGo")
        try: self.assertEqual("eQual: requirements", sel.get_title())
        except AssertionError, e: self.verificationErrors.append(str(e))
        self.failUnless(sel.is_element_present("css=#logo"))
        try: self.assertEqual("eQualrequirements", sel.get_text("css=#logo"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        self.failUnless(sel.is_element_present("css=#notification.notify-wrapper-oneattime"))
        try: self.assertEqual("requirments", sel.get_text("link=requirments"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("store", sel.get_text("link=store"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("execute", sel.get_text("link=execute"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("report", sel.get_text("link=report"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("settings", sel.get_text("link=settings"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("admin", sel.get_text("link=admin"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        self.failUnless(sel.is_element_present("css=#application-menu"))
        try: self.assertEqual("browse", sel.get_text("css=#application-menu ul li"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("filter", sel.get_text("css=#application-menu ul li a"))
        except AssertionError, e: self.verificationErrors.append(str(e))

class NewreqSaveSamename(BaseSeleniumTestCase):
    
    def test_newreq_save_samename(self):
	sel = self.selenium
        sel.open("/require/#requirement/1/details/")
        for i in range(60):
            try:
                if "MeeGo" == sel.get_text("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=MeeGo")
        for i in range(60):
            try:
                if "TV" == sel.get_text("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=TV")
        for i in range(60):
            try:
                if "MeeGo Handset test" == sel.get_text("link=MeeGo Handset test"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=MeeGo Handset test")
        sel.click("css=div#application-view-footer div a span")
        for i in range(60):
            try:
                if sel.is_element_present("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
	time.sleep(5)
        sel.type("id_name", "taka sama nazwa")
	time.sleep(5)
        sel.click("id_release_target")
        sel.click("link=8")
        sel.type("id_description", "opis")
        sel.add_selection("id_dependencies", "label=/MeeGo/Legacy/n900/pr 1.1")
        sel.add_selection("id_dependencies", "label=/MeeGo/Legacy/n900/pr 1.2")
        sel.add_selection("id_dependencies", "label=/MeeGo/Legacy/n900/pr 1.3")
        sel.click("Executed")
        for i in range(60):
            try:
                if "MeeGo Handset test" == sel.get_text("link=MeeGo Handset test"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=MeeGo Handset test")
	time.sleep(5)
        sel.click("css=div#application-view-footer div a span")
	time.sleep(5)
        sel.type("id_name", "taka sama nazwa")
        sel.click("link=15")
        sel.type("id_description", "opis2")
        sel.add_selection("id_dependencies", "label=/MeeGo/Notebook")
        # Test of creating requirements with the same name
        sel.click("Executed")
        sel.click("link=taka sama nazwa")
        # Test exist second requirement 
        for i in range(60):
            try:
                if "TV" == sel.get_text("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=TV")
	time.sleep(1)
        sel.click("link=MeeGo Handset test")
	time.sleep(1)
        try: self.failIf(sel.is_element_present("css=li#31 a"))
        except AssertionError, e: self.verificationErrors.append(str(e))

class NewreqSaveLink(BaseSeleniumTestCase):
    
    def test_newreq_save_link(self):
        sel = self.selenium
        sel.open("/require/#requirement/1/details/")
        try: self.assertEqual("eQual: requirements", sel.get_title())
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=MeeGo")
        sel.click("link=TV")
        for i in range(60):
            try:
                if sel.is_text_present("MeeGo Handset test"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=MeeGo Handset test")
        sel.click("css=#application-view-footer div a span")
        for i in range(60):
            try:
                if sel.is_element_present("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_name", "newrequirement")
        sel.click("id_release_target")
        sel.click("link=15")
        sel.type("id_description", "new requirement test tworzenia")
        sel.add_selection("id_dependencies", "label=/MeeGo/TV/MeeGo Handset test")
        sel.add_selection("id_dependencies", "label=/MeeGo/Legacy/n900/pr 1.1")
        sel.click("Executed")
        sel.wait_for_page_to_load("")
        # Test of new requirement link exist
        time.sleep(5)
        sel.click("link=newrequirement")
        try: self.assertEqual("requirement: newrequirement", sel.get_text("css=#application-view-header h1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=newrequirement"))
        except AssertionError, e: self.verificationErrors.append(str(e))
    

class NewreqSaveError(BaseSeleniumTestCase):

    def test_newreq_save_error(self):
        sel = self.selenium
        sel.open("/require/#requirement/1/details/")
        sel.click("link=MeeGo")
        try: self.assertEqual("eQual: requirements", sel.get_title())
        except AssertionError, e: self.verificationErrors.append(str(e))
        
        sel.click("css=#application-view-footer div a span")
        time.sleep(5)
        sel.click("Executed")
        time.sleep(5)
        self.failUnless(sel.is_element_present("css=#name_wrapper.ui-state-error"))
        # Test of message "This field is required"
        try: self.assertEqual("This field is required.", sel.get_text("css=#name_wrapper.ui-state-error span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        self.failUnless(sel.is_element_present("css=#release_target_wrapper.ui-state-error"))
        try: self.assertEqual("This field is required.", sel.get_text("css=#release_target_wrapper.ui-state-error span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("Executed")
        self.failUnless(sel.is_element_present("css=#name_wrapper.ui-state-error"))
        try: self.assertEqual("This field is required.", sel.get_text("css=#name_wrapper.ui-state-error span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        self.failUnless(sel.is_element_present("css=#release_target_wrapper.ui-state-error"))
        try: self.assertEqual("This field is required.", sel.get_text("css=#release_target_wrapper.ui-state-error span"))
        except AssertionError, e: self.verificationErrors.append(str(e))

class ModreqName(BaseSeleniumTestCase):
    
    def test_modreq_name(self):
        sel = self.selenium
        sel.open("/require/#requirement/32/edit/")
        try: self.assertEqual("eQual: requirements", sel.get_title())
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=MeeGo")
        time.sleep(5)
        sel.click("link=TV")
	time.sleep(5)
	sel.click("link=MeeGo Handset test")
	time.sleep(5)
        sel.click("link=newrequirement")
	time.sleep(5)
        sel.type("id_name", "nowe wymaganie po modyfikacji")
        sel.click("css=input.ui-button")
        try: self.failUnless(sel.is_text_present("full name: /MeeGo/TV/MeeGo Handset test/nowe wymaganie po modyfikacji"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        time.sleep(5)
	sel.click("link=edit")
	time.sleep(5)
        sel.type("id_name", "newrequirement")
        sel.click("css=input.ui-button")
        try: self.failUnless(sel.is_text_present("full name: /MeeGo/TV/MeeGo Handset test/newrequirement"))
        except AssertionError, e: self.verificationErrors.append(str(e))

if __name__ == "__main__":
    unittest.main()
