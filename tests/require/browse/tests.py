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
                if sel.is_element_present("link=test cases"): break
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


    def loginview(self):
        sel = self.selenium
        sel.open("/project/meego/store/#testcasedirectory/1/details/")
        self.assertEqual("qualitio: login", sel.get_title())
        try: self.failUnless(sel.is_text_present("test@qualitio"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id=id_username"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("id=id_password")
        sel.type("id=id_password", "viewer")
        try: self.failUnless(sel.is_element_present("id=id_username"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("id=id_username")
        sel.type("id=id_username", "odczyt111@gmail.com")
        try: self.assertEqual("odczyt111@gmail.com", sel.get_value("id=id_username"))
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
                if sel.is_element_present("link=test cases"): break
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
        sel.type("id=id_username", "odczyt111@gmail.com")
        sel.click("id=id_password")
        sel.type("id=id_password", "viewer")
        sel.click("//input[@value='login']")
        sel.wait_for_page_to_load("30000")

    def loginedit(self):
        sel = self.selenium
        sel.open("/project/meego/store/#testcasedirectory/1/details/")
        self.assertEqual("qualitio: login", sel.get_title())
        try: self.failUnless(sel.is_text_present("test@qualitio"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id=id_username"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("id=id_password")
        sel.type("id=id_password", "editor")
        try: self.failUnless(sel.is_element_present("id=id_username"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("id=id_username")
        sel.type("id=id_username", "edytor111@gmail.com")
        try: self.assertEqual("edytor111@gmail.com", sel.get_value("id=id_username"))
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
                if sel.is_element_present("link=test cases"): break
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
        sel.type("id=id_username", "edytor111@gmail.com")
        sel.click("id=id_password")
        sel.type("id=id_password", "editor")
        sel.click("//input[@value='login']")
        sel.wait_for_page_to_load("30000")


class Test01Loginrequire(BaseSeleniumTestCase):
    
    def test_01_loginrequire(self):
        sel = self.selenium
        sel.open("/project/meego/require/")
        self.assertEqual("qualitio: login", sel.get_title())
        for i in range(60):
            try:
                if sel.is_text_present("test@qualitio"): break
            except: pass
            time.sleep(3)
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
                if "test@qualitio :: require" == sel.get_title(): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        self.assertEqual("test@qualitio :: require", sel.get_title())
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
        sel.type("id_username", "admin")
        sel.click("id_password")
        sel.type("id_password", "admin")
        sel.click("//input[@value='login']")
        sel.wait_for_page_to_load("30000")



class Test02Authview(BaseSeleniumTestCase):
    
    def test_02_authview(self):
        self.loginview() 
        sel = self.selenium
        sel.open("/project/meego/require/#requirement/1/details/")

        self.assertEqual("test@qualitio :: require", sel.get_title())

        try: self.failUnless(sel.is_text_present("Meego"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        for i in range(60):

            try:

                if sel.is_text_present("test@Qualitio"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.failUnless(sel.is_text_present("test@Qualitio"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        for i in range(60):

            try:

                if sel.is_element_present("link=MeeGo"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.failUnless(sel.is_text_present("viewer"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        sel.click("link=MeeGo")

        for i in range(60):

            try:

                if sel.is_text_present("exact:requirement: MeeGo"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_text_present("full name:"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.failUnless(sel.is_element_present("css=a.disable[href=\"#requirement/1/edit/\"]"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        try: self.failUnless(sel.is_element_present("css=a.disable[href=\"#requirement/1/testcases/\"]"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        try: self.failUnless(sel.is_element_present("link=history"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        sel.click("link=history")

        for i in range(60):

            try:

                if sel.is_text_present("date"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_text_present("user"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.failUnless(sel.is_element_present("link=details"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        sel.click("link=details")

        for i in range(60):

            try:

                if sel.is_text_present("full name:"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_text_present("exact:directory:"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.failUnless(sel.is_element_present("css=a.disable[href=\"#requirement/1/new/\"]"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        try: self.failUnless(sel.is_element_present("link=test cases"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        sel.click("link=test cases")

        sel.wait_for_page_to_load("30000")

        for i in range(60):

            try:

                if "test@qualitio :: store" == sel.get_title(): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        self.assertEqual("test@qualitio :: store", sel.get_title())

        for i in range(60):

            try:

                if sel.is_text_present("test@Qualitio"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        sel.click("link=MeeGo Handset bat")

        for i in range(60):

            try:

                if sel.is_text_present("test case directory: MeeGo Handset bat"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if "test@qualitio :: store" == sel.get_title(): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.failUnless(sel.is_element_present("css=a.disable[href=\"#testcasedirectory/2/edit/\"]"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        try: self.failUnless(sel.is_element_present("link=history"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        sel.click("link=history")

        for i in range(60):

            try:

                if sel.is_text_present("date"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_text_present("user"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.failUnless(sel.is_element_present("link=details"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        sel.click("link=details")

        for i in range(60):

            try:

                if sel.is_text_present("full name:"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_text_present("description"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.failUnless(sel.is_element_present("css=a.disable[href=\"#testcasedirectory/2/newtestcase/\"]"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        try: self.failUnless(sel.is_element_present("css=a.disable[href=\"#testcasedirectory/2/new/\"]"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        try: self.failUnless(sel.is_element_present("css=li#1_testcasedirectory ins"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        sel.click("css=li#1_testcasedirectory ins")

        for i in range(60):

            try:

                if sel.is_element_present("link=MeeGo IVI BAT"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_element_present("link=TestCase"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.failUnless(sel.is_element_present("link=TestCase"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        sel.click("link=TestCase")

        for i in range(60):

            try:

                if sel.is_text_present("test case: TestCase"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_text_present("full name: /MeeGo Netbook/TestCase"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.failUnless(sel.is_element_present("css=a.disable[href=\"#testcase/3/edit/\"]"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        try: self.failUnless(sel.is_element_present("link=history"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        sel.click("link=history")

        for i in range(60):

            try:

                if sel.is_text_present("date"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_text_present("user"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.assertEqual("details", sel.get_text("link=details"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        try: self.failUnless(sel.is_element_present("link=details"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        sel.click("link=details")

        for i in range(60):

            try:

                if sel.is_text_present("full name:"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_text_present("exact:parent:"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.failUnless(sel.is_element_present("link=test runs"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        sel.click("link=test runs")

        sel.wait_for_page_to_load("30000")

        for i in range(60):

            try:

                if sel.is_text_present("test@Qualitio"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if "test@qualitio :: execute" == sel.get_title(): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        self.assertEqual("test@qualitio :: execute", sel.get_title())

        sel.click("link=TestRun directory")

        for i in range(60):

            try:

                if sel.is_text_present("test run directory: TestRun directory"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_text_present("full name:"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.failUnless(sel.is_element_present("css=a.disable[href=\"#testrundirectory/1/edit/\"]"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        try: self.failUnless(sel.is_element_present("css=a.disable[href=\"#testrundirectory/1/newtestrun/\"]"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        try: self.failUnless(sel.is_element_present("css=a.disable[href=\"#testrundirectory/1/new/\"]"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        try: self.failUnless(sel.is_element_present("link=history"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        sel.click("link=history")

        for i in range(60):

            try:

                if sel.is_text_present("date"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_text_present("user"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_element_present("link=details"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.failUnless(sel.is_element_present("link=details"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        sel.click("link=details")

        for i in range(60):

            try:

                if sel.is_text_present("full name:"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_text_present("description"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.failUnless(sel.is_element_present("css=li#1_testrundirectory ins"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        sel.click("css=li#1_testrundirectory ins")

        for i in range(60):

            try:

                if sel.is_element_present("link=TestRun 1"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_element_present("link=TestRun 2"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        sel.click("link=TestRun 1")

        for i in range(60):

            try:

                if sel.is_text_present("test run: TestRun 1"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_text_present("full name: /TestRun directory/TestRun 1"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.failUnless(sel.is_element_present("css=a.disable[href=\"#testrun/1/execute/\"]"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        try: self.failUnless(sel.is_element_present("css=a.disable[href=\"#testrun/1/notes/\"]"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        try: self.failUnless(sel.is_element_present("css=a.disable[href=\"#testrun/1/edit/\"]"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        try: self.failUnless(sel.is_element_present("link=history"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        sel.click("link=history")

        for i in range(60):

            try:

                if sel.is_text_present("date"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_text_present("user"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_element_present("link=details"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.failUnless(sel.is_element_present("link=details"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        sel.click("link=details")

        for i in range(60):

            try:

                if sel.is_text_present("full name:"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_text_present("test cases:"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.failUnless(sel.is_text_present("full name:"))

        except AssertionError, e: self.verificationErrors.append(str(e))




class Test02Authedit(BaseSeleniumTestCase):
    
    def test_02_authedit(self):
        self.loginedit() 
        sel = self.selenium
        sel.open("/project/meego/require/#requirement/1/details/")

        self.assertEqual("test@qualitio :: require", sel.get_title())

        try: self.failUnless(sel.is_text_present("Meego"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        for i in range(60):

            try:

                if sel.is_text_present("test@Qualitio"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.failUnless(sel.is_text_present("test@Qualitio"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        for i in range(60):

            try:

                if sel.is_element_present("link=MeeGo"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.failUnless(sel.is_text_present("editor"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        sel.click("link=MeeGo")

        for i in range(60):

            try:

                if sel.is_text_present("exact:requirement: MeeGo"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_text_present("full name:"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.failUnless(sel.is_element_present("link=edit"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        try: self.failUnless(sel.is_element_present("link=testcases"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        try: self.failUnless(sel.is_element_present("link=history"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        sel.click("link=history")

        for i in range(60):

            try:

                if sel.is_text_present("date"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_text_present("user"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.failUnless(sel.is_element_present("link=details"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        sel.click("link=details")

        for i in range(60):

            try:

                if sel.is_text_present("full name:"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_text_present("exact:directory:"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.failUnless(sel.is_element_present("css=span.ui-button-text"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        try: self.assertEqual("create requirement", sel.get_text("css=span.ui-button-text"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        try: self.failUnless(sel.is_element_present("link=test cases"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        sel.click("link=test cases")

        sel.wait_for_page_to_load("30000")

        for i in range(60):

            try:

                if "test@qualitio :: store" == sel.get_title(): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        self.assertEqual("test@qualitio :: store", sel.get_title())

        for i in range(60):

            try:

                if sel.is_text_present("test@Qualitio"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        sel.click("link=MeeGo Handset bat")

        for i in range(60):

            try:

                if sel.is_text_present("test case directory: MeeGo Handset bat"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if "test@qualitio :: store" == sel.get_title(): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.failUnless(sel.is_element_present("link=edit"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        try: self.failUnless(sel.is_element_present("link=history"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        sel.click("link=history")

        for i in range(60):

            try:

                if sel.is_text_present("date"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_text_present("user"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.failUnless(sel.is_element_present("link=details"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        sel.click("link=details")

        for i in range(60):

            try:

                if sel.is_text_present("full name:"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_text_present("description"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.failUnless(sel.is_element_present("css=span.ui-button-text"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        try: self.failUnless(sel.is_element_present("//div[@id='application-view-footer']/div/a[2]/span"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        try: self.failUnless(sel.is_element_present("css=li#1_testcasedirectory ins"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        sel.click("css=li#1_testcasedirectory ins")

        for i in range(60):

            try:

                if sel.is_element_present("link=MeeGo IVI BAT"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_element_present("link=TestCase"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.failUnless(sel.is_element_present("link=TestCase"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        sel.click("link=TestCase")

        for i in range(60):

            try:

                if sel.is_text_present("test case: TestCase"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_text_present("full name: /MeeGo Netbook/TestCase"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.failUnless(sel.is_element_present("link=edit"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        try: self.failUnless(sel.is_element_present("link=history"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        sel.click("link=history")

        for i in range(60):

            try:

                if sel.is_text_present("date"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_text_present("user"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.assertEqual("details", sel.get_text("link=details"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        try: self.failUnless(sel.is_element_present("link=details"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        sel.click("link=details")

        for i in range(60):

            try:

                if sel.is_text_present("full name:"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_text_present("exact:parent:"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.failUnless(sel.is_element_present("link=test runs"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        sel.click("link=test runs")

        sel.wait_for_page_to_load("30000")

        for i in range(60):

            try:

                if sel.is_text_present("test@Qualitio"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if "test@qualitio :: execute" == sel.get_title(): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        self.assertEqual("test@qualitio :: execute", sel.get_title())

        sel.click("link=TestRun directory")

        for i in range(60):

            try:

                if sel.is_text_present("test run directory: TestRun directory"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_text_present("full name:"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.failUnless(sel.is_element_present("link=edit"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        try: self.failUnless(sel.is_element_present("css=span.ui-button-text"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        try: self.failUnless(sel.is_element_present("//div[@id='application-view-footer']/div/a[2]/span"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        try: self.failUnless(sel.is_element_present("link=history"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        sel.click("link=history")

        for i in range(60):

            try:

                if sel.is_text_present("date"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_text_present("user"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_element_present("link=details"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.failUnless(sel.is_element_present("link=details"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        sel.click("link=details")

        for i in range(60):

            try:

                if sel.is_text_present("full name:"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_text_present("description"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.failUnless(sel.is_element_present("css=li#1_testrundirectory ins"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        sel.click("css=li#1_testrundirectory ins")

        for i in range(60):

            try:

                if sel.is_element_present("link=TestRun 1"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_element_present("link=TestRun 2"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        sel.click("link=TestRun 1")

        for i in range(60):

            try:

                if sel.is_text_present("test run: TestRun 1"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_text_present("full name: /TestRun directory/TestRun 1"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.failUnless(sel.is_element_present("link=edit"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        try: self.failUnless(sel.is_element_present("link=notes"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        try: self.failUnless(sel.is_element_present("//div[@id='application-view-menu']/a[3]"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        try: self.failUnless(sel.is_element_present("link=history"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        sel.click("link=history")

        for i in range(60):

            try:

                if sel.is_text_present("date"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_text_present("user"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_element_present("link=details"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.failUnless(sel.is_element_present("link=details"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        sel.click("link=details")

        for i in range(60):

            try:

                if sel.is_text_present("full name:"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        for i in range(60):

            try:

                if sel.is_text_present("test cases:"): break

            except: pass

            time.sleep(2)

        else: self.fail("time out")

        try: self.failUnless(sel.is_text_present("full name:"))

        except AssertionError, e: self.verificationErrors.append(str(e))
    

class Test03Gmail(BaseSeleniumTestCase):

    
    def test_03_gmail(self):
        sel = self.selenium
        sel.open("/login/?next=/")
        self.assertEqual("qualitio: login", sel.get_title())
        for i in range(60):
            try:
                if sel.is_element_present("link=test@qualitio"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.select_window("null")
        sel.click("css=span.ui-button-text")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if "Konta Google" == sel.get_title(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "Konta Google" == sel.get_title(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.assertEqual("Konta Google", sel.get_title())
        sel.type("Email", "qualitio2")
        sel.type("Passwd", "testqual")
        try: self.failUnless(sel.is_element_present("signIn"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("signIn")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if "test@qualitio" == sel.get_title(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.assertEqual("test@qualitio", sel.get_title())
        for i in range(60):
            try:
                if "qualitio2@gmail.com" == sel.get_text("css=b"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("qualitio2@gmail.com", sel.get_text("css=b"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=logout"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=logout")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_text_present("qualitio"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "qualitio: login" == sel.get_title(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.assertEqual("qualitio: login", sel.get_title())
        try: self.failUnless(sel.is_element_present("css=span.ui-button-text"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=span.ui-button-text")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_text_present("qualitio"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "test@qualitio" == sel.get_title(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.assertEqual("test@qualitio", sel.get_title())
        try: self.assertEqual("qualitio2@gmail.com", sel.get_text("css=b"))
        except AssertionError, e: self.verificationErrors.append(str(e))
    


class Test04Gmail(BaseSeleniumTestCase):

    
    def test_04_gmail(self):
        sel = self.selenium
        sel.open("/login/?next=/")
        self.assertEqual("qualitio: login", sel.get_title())
        sel.open("https://www.google.com/accounts/ServiceLogin?service=mail&passive=true&rm=false&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F%3Fui%3Dhtml%26zy%3Dl&bsv=llya694le36z&ss=1&scc=1&ltmpl=default&ltmplcache=2&hl=pl")
        for i in range(60):
            try:
                if "Gmail: innowacyjna poczta Google" == sel.get_title(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.assertEqual("Gmail: innowacyjna poczta Google", sel.get_title())
        for i in range(60):
            try:
                if sel.is_element_present("Email"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("Email", "qualitio2")
        sel.type("Passwd", "testqual")
        try: self.failUnless(sel.is_element_present("signIn"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("signIn")
        sel.wait_for_page_to_load("30000")
        sel.open("/login/?next=/")
        for i in range(60):
            try:
                if sel.is_text_present("qualitio"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("css=span.ui-button-text"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=span.ui-button-text")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if "Description of organization" == sel.get_text("css=div.application-view-content.panel > div"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "New Project" == sel.get_text("css=span.ui-button-text"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("Description of organization", sel.get_text("css=div.application-view-content.panel > div"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=span.ui-button-text"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if "test@qualitio" == sel.get_title(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("qualitio2@gmail.com"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("account qualitio2@gmail.com"))
        except AssertionError, e: self.verificationErrors.append(str(e))


class Test05Yahoo(BaseSeleniumTestCase):

    
    def test_05_yahoo(self):
        sel = self.selenium
        sel.open("/login/?next=/")
        self.assertEqual("qualitio: login", sel.get_title())
        for i in range(60):
            try:
                if sel.is_element_present("//div[@id='main']/div/div[2]/a[2]/span"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("//div[@id='main']/div/div[2]/a[2]/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//div[@id='main']/div/div[2]/a[2]/span")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if "Sign in to Yahoo!" == sel.get_title(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.assertEqual("Sign in to Yahoo!", sel.get_title())
        for i in range(60):
            try:
                if sel.is_element_present("username"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("passwd"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("username"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id=username", "qualitio1")
        try: self.failUnless(sel.is_element_present("passwd"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("passwd", "testqual")
        try: self.failUnless(sel.is_element_present(".save"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click(".save")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if "test@qualitio" == sel.get_title(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "test@qualitio" == sel.get_title(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.assertEqual("test@qualitio", sel.get_title())
        for i in range(60):
            try:
                if sel.is_text_present("TomPlak"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("TomPlak"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=logout"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=logout")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_text_present("qualitio"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "qualitio: login" == sel.get_title(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.assertEqual("qualitio: login", sel.get_title())
        try: self.failUnless(sel.is_element_present("//div[@id='main']/div/div[2]/a[2]/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//div[@id='main']/div/div[2]/a[2]/span")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_text_present("qualitio"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "test@qualitio" == sel.get_title(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.assertEqual("test@qualitio", sel.get_title())
        try: self.failUnless(sel.is_text_present("Welcome, TomPlak"))
        except AssertionError, e: self.verificationErrors.append(str(e))


class Test06Googleappsdom(BaseSeleniumTestCase):
    
    def test_06_googleappsdom(self):
        self.login() 
        sel = self.selenium
        sel.open("/project/meego/require/#requirement/1/details/")
        try: self.assertEqual("test@qualitio :: require", sel.get_title())
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "MeeGo" == sel.get_text("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=MeeGo"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("link=settings"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=settings"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=settings")
        sel.wait_for_page_to_load("30000")
        time.sleep(2)
        for i in range(60):
            try:
                if sel.is_text_present("Googleapps domain"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Googleapps domain"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id=id_googleapps_domain"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id=id_googleapps_domain", "binop.com")
        try: self.failUnless(sel.is_element_present("//input[@value='Save']"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//input[@value='Save']")
        time.sleep(2)
        for i in range(60):
            try:
                if sel.is_text_present("Organization profile successfully updated."): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Organization profile successfully updated."))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("binop.com", sel.get_value("id=id_googleapps_domain"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=logout"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=logout")
        sel.wait_for_page_to_load("30000")
        time.sleep(2)
        for i in range(60):
            try:
                if "qualitio: login" == sel.get_title(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("qualitio: login", sel.get_title())
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=span.ui-button-text"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("This domain is also connected with google apps domain binop.com. If you have account in this organization you can login straight in using Googgle Apps OpenID mechanism. No further activation or verification process is needed."))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failIf(sel.is_element_present("//div[@id='main']/div/div[2]/a[2]/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=span.ui-button-text")
        sel.wait_for_page_to_load("30000")
        time.sleep(2)
        for i in range(60):
            try:
                if sel.is_text_present("@binop.com"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("@binop.com"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.open("/login/?next=/")
        time.sleep(2)
        for i in range(60):
            try:
                if sel.is_element_present("id=id_username"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("id=id_username"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("id=id_username")
        sel.type("id=id_username", "qualitio1@gmail.com")
        sel.click("id=id_password")
        try: self.failUnless(sel.is_element_present("//div[@id='main']/div/div/form/fieldset/label[2]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("id=id_password")
        sel.type("id=id_password", "admin")
        sel.click("css=div.right")
        try: self.failUnless(sel.is_element_present("//input[@value='login']"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//input[@value='login']")
        sel.wait_for_page_to_load("30000")
        time.sleep(2)
        try: self.failUnless(sel.is_element_present("link=settings"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("link=settings"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=settings")
        sel.wait_for_page_to_load("30000")
        time.sleep(2)
        sel.type("id=id_googleapps_domain", "")
        sel.click("//input[@value='Save']")
        time.sleep(2)
        sel.click("link=logout")
        sel.wait_for_page_to_load("30000")
        time.sleep(2)
        try: self.failUnless(sel.is_element_present("css=span.ui-button-text"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//div[@id='main']/div/div[2]/a[2]/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("You have also an option to log in with use of regular OpenID, but in this case you have to wait till one of the users with administration privileges will accept your membership."))
        except AssertionError, e: self.verificationErrors.append(str(e))

        # <tr>
        # 	<td>verifyTextPresent</td>
        # 	<td>Create your own organization</td>
        # 	<td></td>
        # </tr>
        # <tr>
        # 	<td>verifyElementPresent</td>
        # 	<td>link=qualitio@qualitio.com</td>
        # 	<td></td>
        # </tr>
        # <tr>
        # 	<td>verifyTextPresent</td>
        # 	<td>If you need an new organization please feel free to contact with us qualitio@qualitio.com.</td>
        # 	<td></td>
        # </tr>


class Test1HeaderpageVerifytext(BaseSeleniumTestCase):
    
    def test_1_headerpage_verifytext(self):
        self.login() 
        sel = self.selenium
        sel.open("/project/meego/require/#requirement/1/details/")
        try: self.assertEqual("test@qualitio :: require", sel.get_title())
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if "MeeGo" == sel.get_text("link=MeeGo"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        sel.click("link=MeeGo")
        try: self.assertEqual("test@qualitio :: require", sel.get_title())
        except AssertionError, e: self.verificationErrors.append(str(e))
        self.failUnless(sel.is_element_present("css=div.logo"))
        try: self.assertEqual("test@Qualitio", sel.get_text("css=div.logo"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        self.failUnless(sel.is_element_present("css=#notification.notify-wrapper-oneattime"))
        try: self.assertEqual("requirements", sel.get_text("link=requirements"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("test cases", sel.get_text("link=test cases"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("test runs", sel.get_text("link=test runs"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("admin", sel.get_text("link=admin"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("reports", sel.get_text("link=reports"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("admin", sel.get_text("link=admin"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        self.failUnless(sel.is_element_present("css=#application-menu"))
        try: self.assertEqual("browse", sel.get_text("css=#application-menu ul li"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("filter", sel.get_text("link=filter"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("test :: Meego"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=logout"))
        except AssertionError, e: self.verificationErrors.append(str(e))



class Test2TreeVerifyelements(BaseSeleniumTestCase):
    
    def test_2_tree_verifyelements(self):
        self.login() 
        sel = self.selenium
        sel.open("/project/meego/require/#requirement/1/details/")
        self.assertEqual("test@qualitio :: require", sel.get_title())
        for i in range(60):
            try:
                if sel.is_text_present("MeeGo"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        sel.click("link=MeeGo")
        sel.click("css=li#1_requirement ins")
        for i in range(60):
            try:
                if "Notebook" == sel.get_text("link=Notebook"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("css=li#2_requirement a ins"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=Notebook"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=li#2_requirement a ins"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=li#1_requirement ins"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=li#1_requirement ins")
        sel.click("css=li#1_requirement ins")
        for i in range(60):
            try:
                if "TV" == sel.get_text("link=TV"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=TV"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=li#2_requirement ins"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=li#4_requirement a ins"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=li#4_requirement ins"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=li#4_requirement ins")
        sel.click("css=li#4_requirement ins")
        for i in range(60):
            try:
                if sel.is_element_present("link=Bootscreen"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("css=li#8_requirement ins"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=Notebook")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: Notebook"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("exact:requirement: Notebook"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("full name: /MeeGo/Notebook"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("exact:directory: /MeeGo/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=TV")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: TV"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("exact:requirement: TV"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("full name: /MeeGo/TV"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("exact:directory: /MeeGo/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=MeeGo Media Phone")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: MeeGo Media Phone"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("exact:requirement: MeeGo Media Phone"))
        except AssertionError, e: self.verificationErrors.append(str(e))


class Test3Newreq(BaseSeleniumTestCase):
    
    def test_3_newreq(self):
        self.login() 
        sel = self.selenium
        sel.open("/project/meego/require/#requirement/1/details/")
        try: self.assertEqual("test@qualitio :: require", sel.get_title())
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if "MeeGo" == sel.get_text("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=MeeGo"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=li#1_requirement ins")
        for i in range(60):
            try:
                if "" == sel.get_text("css=#4_requirement > ins.jstree-icon"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "TV" == sel.get_text("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("css=#4_requirement > ins.jstree-icon"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("css=#4_requirement > ins.jstree-icon"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=TV"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=TV")
        for i in range(60):
            try:
                if "full name:" == sel.get_text("css=span.name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "create requirement" == sel.get_text("css=span.ui-button-text"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("css=span.ui-button-text"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=div#application-view-footer div a span")
        for i in range(60):
            try:
                if "requirement" == sel.get_text("css=div#application-view-header h1"): break
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
                if sel.is_element_present("id=id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("id=id_name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id_name", "new requirement 1")
        sel.click("id_release_target")
        for i in range(60):
            try:
                if sel.is_element_present("css=div#ui-datepicker-div div div"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=1")
        sel.click("release_target_wrapper")
        for i in range(60):
            try:
                if sel.is_text_present("requirement"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("Executed")
        sel.wait_for_page_to_load("")
        for i in range(60):
            try:
                if "details" == sel.get_text("link=details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "MeeGo" == sel.get_text("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=MeeGo")
        for i in range(60):
            try:
                if "full name:" == sel.get_text("css=span.name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=li#1_requirement ins")
        for i in range(60):
            try:
                if sel.is_element_present("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "TV" == sel.get_text("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=TV")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=li#4_requirement ins")
        for i in range(60):
            try:
                if "" == sel.get_text("css=img"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("css=tr.even > td..sorting_1 > img"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=new requirement 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=new requirement 1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//div[@id='application-view']/div[4]/div/div[1]/div[1]/div/table/thead/tr/th[3]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//div[@id='application-view']/div[4]/div/div[1]/div[1]/div/table/thead/tr/th[3]")
        for i in range(60):
            try:
                if sel.is_element_present("//div[@id='application-view']/div[4]/div/div[1]/div[2]/table/tbody/tr[3]/td[3]/a"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("//div[@id='application-view']/div[4]/div/div[1]/div[2]/table/tbody/tr[3]/td[3]/a")
        for i in range(60):
            try:
                if sel.is_text_present("full name:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("exact:directory:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("exact:description:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: new requirement 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("/MeeGo/TV/new requirement 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("/MeeGo/TV/new requirement 1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("exact:requirement: new requirement 1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=history"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=history")
        for i in range(60):
            try:
                if sel.is_element_present("css=div#application-view-menu span"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
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
        try: self.failUnless(sel.is_text_present("Object created."))
        except AssertionError, e: self.verificationErrors.append(str(e))
	time.sleep(2)
        sel.open("/admin/require/requirement/")
        for i in range(60):
            try:
                if sel.is_text_present("new requirement 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "Select requirement to change | Django site admin" == sel.get_title(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("xpath=(//input[@name='_selected_action'])[8]")
        try: self.assertEqual("on", sel.get_value("css=tr.row2.selected > td > input[name=\"_selected_action\"]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("name=action"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.select("name=action", "label=Delete selected requirements")
        sel.click("name=index")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_text_present("exact:28: /MeeGo/TV/new requirement 1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.failUnless(sel.is_text_present("exact:28: /MeeGo/TV/new requirement 1"))
        sel.click("css=input[type=\"submit\"]")
        sel.wait_for_page_to_load("30000")


class Test4Modreq(BaseSeleniumTestCase):
    
    def test_4_modreq(self):
        self.login() 
        sel = self.selenium
        sel.open("/project/meego/require/#requirement/1/details/")
        self.assertEqual("test@qualitio :: require", sel.get_title())
        for i in range(60):
            try:
                if "MeeGo" == sel.get_text("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=MeeGo"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//li[@id='1_requirement']/ins")
        for i in range(60):
            try:
                if "TV" == sel.get_text("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=TV"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=TV")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=div#application-view-footer div a span")
        for i in range(60):
            try:
                if "requirement" == sel.get_text("css=div#application-view-header h1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_name", "new requirement 2")
        sel.click("id_release_target")
        for i in range(60):
            try:
                if sel.is_element_present("css=div#ui-datepicker-div div div"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=1")
        sel.click("release_target_wrapper")
        for i in range(60):
            try:
                if sel.is_text_present("requirement"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("Executed")
        sel.wait_for_page_to_load("")
        for i in range(60):
            try:
                if "MeeGo" == sel.get_text("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if "TV" == sel.get_text("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=MeeGo"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=TV"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=#4_requirement > ins.jstree-icon"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=#4_requirement > ins.jstree-icon")
        for i in range(60):
            try:
                if sel.is_element_present("link=new requirement 2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=new requirement 2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=new requirement 2")
        for i in range(60):
            try:
                if "requirement: new requirement 2" == sel.get_text("css=div#application-view-header h1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.failUnless(sel.is_element_present("css=div#application-view-header h1"))
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
        sel.type("id_name", "mod requirement 3")
        sel.click("css=input.ui-button")
        for i in range(60):
            try:
                if sel.is_element_present("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "Notebook" == sel.get_text("link=Notebook"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "TV" == sel.get_text("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=mod requirement 3"): break
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
                if sel.is_element_present("id_release_target"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=details")
        for i in range(60):
            try:
                if "requirement: mod requirement 3" == sel.get_text("css=div#application-view-header h1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("exact:requirement: mod requirement 3"))
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
        try: self.failUnless(sel.is_text_present("Changed name."))
        except AssertionError, e: self.verificationErrors.append(str(e))
	time.sleep(2)
        sel.open("/admin/require/requirement/")
        for i in range(60):
            try:
                if sel.is_text_present("mod requirement 3"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "Select requirement to change | Django site admin" == sel.get_title(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("xpath=(//input[@name='_selected_action'])[8]")
        try: self.assertEqual("on", sel.get_value("css=tr.row2.selected > td > input[name=\"_selected_action\"]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("name=action"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.select("name=action", "label=Delete selected requirements")
        sel.click("name=index")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_text_present("exact:28: /MeeGo/TV/mod requirement 3"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.failUnless(sel.is_text_present("exact:28: /MeeGo/TV/mod requirement 3"))
        sel.click("css=input[type=\"submit\"]")
        sel.wait_for_page_to_load("30000")


class Test5TestcasesDel(BaseSeleniumTestCase):
    
    def test_5_testcases_del(self):
        self.login() 
        sel = self.selenium
        sel.open("/project/meego/require/#requirement/1/details/")
        for i in range(60):
            try:
                if sel.is_text_present("test@Qualitio"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "MeeGo" == sel.get_text("link=MeeGo"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=MeeGo"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=li#1_requirement ins")
        for i in range(60):
            try:
                if sel.is_element_present("link=TV"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "TV" == sel.get_text("link=TV"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=TV"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if "" == sel.get_text("css=#4_requirement > ins.jstree-icon"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("css=#4_requirement > ins.jstree-icon"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=li#4_requirement ins")
        for i in range(60):
            try:
                if sel.is_element_present("link=MeeGo Handset test"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "MeeGo Handset test" == sel.get_text("link=MeeGo Handset test"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=MeeGo Handset test"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=MeeGo Handset test")
        for i in range(60):
            try:
                if "requirement: MeeGo Handset test" == sel.get_text("css=div#application-view-header h1"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.assertEqual("requirement: MeeGo Handset test", sel.get_text("css=div#application-view-header h1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if "testcases" == sel.get_text("link=testcases"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=testcases"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=testcases")
        for i in range(60):
            try:
                if sel.is_element_present("id=testcase-3"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("id=testcase-3"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=a#remove-testcases-button span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("id=testcase-3")
        sel.click("css=a#remove-testcases-button span")
        for i in range(60):
            try:
                if "No data available in table" == sel.get_text("css=td.dataTables_empty"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("No data available in table"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("css=input[type='text']"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("css=input[type='text']"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("link=details"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: MeeGo Handset test"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name: /MeeGo/TV/MeeGo Handset test"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("full name: /MeeGo/TV/MeeGo Handset test"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("exact:requirement: MeeGo Handset test"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("//div[@id='application-view']/div[5]/div/div[1]/div[2]/table/tbody/tr/td"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.assertEqual("No data available in table", sel.get_text("//div[@id='application-view']/div[5]/div/div[1]/div[2]/table/tbody/tr/td"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Showing 0 to 0 of 0 entries", sel.get_text("//div[@id='application-view']/div[5]/div/div[2]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=history"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=history")
        for i in range(60):
            try:
                if sel.is_text_present("date"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("user"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Deleted test case \"3: /meego netbook/testcase\"."))
        except AssertionError, e: self.verificationErrors.append(str(e))


class Test6TestcasesAdd(BaseSeleniumTestCase):
    
    def test_6_testcases_add(self):
        self.login() 
        sel = self.selenium
        sel.open("/project/meego/require/#requirement/1/details/")
        try: self.failUnless(sel.is_text_present("test@Qualitio"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        self.assertEqual("test@qualitio :: require", sel.get_title())
        for i in range(60):
            try:
                if "MeeGo" == sel.get_text("link=MeeGo"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=MeeGo"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=li#1_requirement ins")
        for i in range(60):
            try:
                if sel.is_element_present("link=TV"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "TV" == sel.get_text("link=TV"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "" == sel.get_text("css=#4_requirement > ins.jstree-icon"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=TV"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=#4_requirement > ins.jstree-icon"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=li#4_requirement ins")
        for i in range(60):
            try:
                if sel.is_element_present("link=MeeGo Handset test"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "MeeGo Handset test" == sel.get_text("link=MeeGo Handset test"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=MeeGo Handset test"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=MeeGo Handset test")
        for i in range(60):
            try:
                if "requirement: MeeGo Handset test" == sel.get_text("css=div#application-view-header h1"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.assertEqual("requirement: MeeGo Handset test", sel.get_text("css=div#application-view-header h1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if "testcases" == sel.get_text("link=testcases"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=testcases"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=testcases")
        for i in range(60):
            try:
                if sel.is_element_present("css=input[type='text']"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("css=#application-view-footer > div.dataTables_wrapper > div.bottom.clearfix > div.dataTables_filter > input[type=\"text\"]"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("css=#application-view-footer > div.dataTables_wrapper > div.bottom.clearfix > div.dataTables_filter > input[type=\"text\"]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("css=#application-view-footer > div.dataTables_wrapper > div.bottom.clearfix > div.dataTables_filter > input[type=\"text\"]", "TestCase")
        sel.type_keys("css=#application-view-footer > div.dataTables_wrapper > div.bottom.clearfix > div.dataTables_filter > input[type=\"text\"]", "TestCase")
        for i in range(60):
            try:
                if "TestCase" == sel.get_value("css=#application-view-footer > div.dataTables_wrapper > div.bottom.clearfix > div.dataTables_filter > input[type=\"text\"]"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id=testcase-3"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "off" == sel.get_value("id=testcase-3"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("id=testcase-3"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("off", sel.get_value("id=testcase-3"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("id=testcase-3")
        for i in range(60):
            try:
                if "on" == sel.get_value("id=testcase-3"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.assertEqual("on", sel.get_value("id=testcase-3"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("css=a#add-testcases-button span"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "add" == sel.get_text("css=#add-testcases-button > span.ui-button-text"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("css=a#add-testcases-button span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=a#add-testcases-button span")
        for i in range(60):
            try:
                if "TestCase" == sel.get_text("//form[@id='testcases_connect_form']/div[2]/div/div/div[4]/div[2]/table/tbody/tr/td[4]"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "TestCase" == sel.get_table("css=div.dataTables_scrollBody > table.display.1.3"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("//form[@id='testcases_connect_form']/div[2]/div/div/div[4]/div[2]/table/tbody/tr/td[4]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("TestCase", sel.get_text("//form[@id='testcases_connect_form']/div[2]/div/div/div[4]/div[2]/table/tbody/tr/td[4]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_text_present("TestCase"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("3"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("TestCase"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("3"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("/MeeGo Netbook/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id=testcase-3"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("link=details"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=details"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: MeeGo Handset test"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("details"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("testcases"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("css=span.ui-icon.ui-icon-document"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("css=span.ui-icon.ui-icon-document"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//div[@id='application-view']/div[5]/div/div[1]/div[2]/table/tbody/tr/td[1]/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=3"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=TestCase"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=history"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=history")
        for i in range(60):
            try:
                if sel.is_text_present("date"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("user"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("//div[@id='application-view']/div[3]/div/div/div[2]/table/tbody/tr/td[3]"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Added test case \"3: /meego netbook/testcase\"."))
        except AssertionError, e: self.verificationErrors.append(str(e))


class Test7ModreqParent(BaseSeleniumTestCase):
    
    def test_7_modreq_parent(self):
        self.login() 
        sel = self.selenium
        sel.open("/project/meego/require/#requirement/1/details/")
        try: self.assertEqual("test@qualitio :: require", sel.get_title())
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if "MeeGo" == sel.get_text("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=MeeGo"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=li#1_requirement ins")
        time.sleep(2)
        for i in range(60):
            try:
                if "TV" == sel.get_text("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=TV"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("css=#4_requirement > ins.jstree-icon"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("css=#4_requirement > ins.jstree-icon"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=TV")
        time.sleep(2)
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("css=span.ui-button-text"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("css=span.ui-button-text"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=div#application-view-footer div a span")
        for i in range(60):
            try:
                if "requirement" == sel.get_text("css=div#application-view-header h1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_name", "new requirement 4")
        sel.click("id_release_target")
        time.sleep(2)
        for i in range(60):
            try:
                if sel.is_element_present("css=div#ui-datepicker-div div div"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=1")
        sel.click("release_target_wrapper")
        for i in range(60):
            try:
                if sel.is_text_present("requirement"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("Executed")
        time.sleep(2)
        for i in range(60):
            try:
                if "MeeGo" == sel.get_text("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=MeeGo"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "TV" == sel.get_text("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=TV"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("link=new requirement 4"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=new requirement 4"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=new requirement 4")
        sel.click("link=new requirement 4")
        for i in range(60):
            try:
                if sel.is_element_present("css=span.active"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "details" == sel.get_text("css=span.active"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "requirement: new requirement 4" == sel.get_text("css=div#application-view-header h1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.failUnless(sel.is_element_present("css=div#application-view-header h1"))
        try: self.failUnless(sel.is_text_present("full name: /MeeGo/TV/new requirement 4"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("exact:directory: /MeeGo/TV/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=edit")
        time.sleep(1)
        for i in range(60):
            try:
                if sel.is_element_present("id_parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.select("id_parent", "label=13: /MeeGo/TV/MeeGo Handset test")
        sel.click("css=input.ui-button")
        time.sleep(2)
        for i in range(60):
            try:
                if sel.is_element_present("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "MeeGo" == sel.get_text("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=MeeGo"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if "Notebook" == sel.get_text("link=Notebook"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "TV" == sel.get_text("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=TV"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("link=MeeGo Handset test"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "MeeGo Handset test" == sel.get_text("link=MeeGo Handset test"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=MeeGo Handset test"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=MeeGo Handset test")
        time.sleep(2)
        for i in range(60):
            try:
                if sel.is_element_present("link=new requirement 4"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=new requirement 4")
        for i in range(60):
            try:
                if "requirement: new requirement 4" == sel.get_text("css=div#application-view-header h1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name: /MeeGo/TV/MeeGo Handset test/new requirement 4"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("exact:requirement: new requirement 4"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("full name: /MeeGo/TV/MeeGo Handset test/new requirement 4"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("exact:directory: /MeeGo/TV/MeeGo Handset test/"))
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
        try: self.failUnless(sel.is_text_present("Changed parent."))
        except AssertionError, e: self.verificationErrors.append(str(e))
	time.sleep(2)
        sel.open("/admin/require/requirement/")
        for i in range(60):
            try:
                if sel.is_text_present("new requirement 4"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "Select requirement to change | Django site admin" == sel.get_title(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("xpath=(//input[@name='_selected_action'])[8]")
        try: self.assertEqual("on", sel.get_value("css=tr.row2.selected > td > input[name=\"_selected_action\"]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("name=action"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.select("name=action", "label=Delete selected requirements")
        sel.click("name=index")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_text_present("exact:28: /MeeGo/TV/MeeGo Handset test/new requirement 4"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.failUnless(sel.is_text_present("exact:28: /MeeGo/TV/MeeGo Handset test/new requirement 4"))
        sel.click("css=input[type=\"submit\"]")
        sel.wait_for_page_to_load("30000")


class Test8ModreqReltarg(BaseSeleniumTestCase):
    
    def test_8_modreq_reltarg(self):
        self.login() 
        sel = self.selenium
        sel.open("/project/meego/require/#requirement/1/details/")
        try: self.assertEqual("test@qualitio :: require", sel.get_title())
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if "MeeGo" == sel.get_text("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=MeeGo"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//li[@id='1_requirement']/ins")
        for i in range(60):
            try:
                if "TV" == sel.get_text("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=TV"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("css=#4_requirement > ins.jstree-icon"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("css=#4_requirement > ins.jstree-icon"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=TV"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=TV")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: TV"): break
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
                if sel.is_element_present("css=span.ui-button-text"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("css=span.ui-button-text"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=div#application-view-footer div a span")
        for i in range(60):
            try:
                if "requirement" == sel.get_text("css=div#application-view-header h1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_name", "new requirement 5")
        sel.click("id_release_target")
        for i in range(60):
            try:
                if sel.is_element_present("css=div#ui-datepicker-div div div"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=1")
        sel.click("release_target_wrapper")
        for i in range(60):
            try:
                if sel.is_text_present("requirement"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("name=Executed"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("Executed")
        for i in range(60):
            try:
                if "MeeGo" == sel.get_text("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=MeeGo"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "TV" == sel.get_text("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_element_present("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("css=#4_requirement > ins.jstree-icon"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=#4_requirement > ins.jstree-icon")
        time.sleep(2)
        for i in range(60):
            try:
                if sel.is_element_present("link=new requirement 5"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=new requirement 5"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=new requirement 5")
        time.sleep(2)
        for i in range(60):
            try:
                if "requirement: new requirement 5" == sel.get_text("css=div#application-view-header h1"): break
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
                if sel.is_element_present("link=edit"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=edit"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_element_present("id_release_target"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("id_release_target"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("id_release_target")
        sel.click("link=15")
        sel.click("id_description")
        for i in range(60):
            try:
                if sel.is_element_present("Executed"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=input.ui-button")
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
        sel.click("link=details")
        time.sleep(2)
        for i in range(60):
            try:
                if sel.is_element_present("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "Notebook" == sel.get_text("link=Notebook"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "TV" == sel.get_text("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=TV"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("link=new requirement 5"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=new requirement 5"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=new requirement 5")
        for i in range(60):
            try:
                if "requirement: new requirement 5" == sel.get_text("css=h1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "requirement: new requirement 5" == sel.get_text("css=div#application-view-header h1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name: /MeeGo/TV/new requirement 5"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("exact:requirement: new requirement 5"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("edit"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=edit")
        for i in range(60):
            try:
                if "" == sel.get_text("id_release_target"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("id_release_target"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("id_release_target")
        for i in range(60):
            try:
                if sel.is_element_present("link=15"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=15"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("15", sel.get_text("link=15"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("15", sel.get_text("css= .ui-state-active"))
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
        try: self.failUnless(sel.is_text_present("Changed release_target."))
        except AssertionError, e: self.verificationErrors.append(str(e))
	time.sleep(2)
        sel.open("/admin/require/requirement/")
        for i in range(60):
            try:
                if sel.is_text_present("new requirement 5"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "Select requirement to change | Django site admin" == sel.get_title(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("xpath=(//input[@name='_selected_action'])[8]")
        try: self.assertEqual("on", sel.get_value("css=tr.row2.selected > td > input[name=\"_selected_action\"]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("name=action"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.select("name=action", "label=Delete selected requirements")
        sel.click("name=index")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_text_present("exact:28: /MeeGo/TV/new requirement 5"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.failUnless(sel.is_text_present("exact:28: /MeeGo/TV/new requirement 5"))
        sel.click("css=input[type=\"submit\"]")
        sel.wait_for_page_to_load("30000")


class Test9ModreqDesript(BaseSeleniumTestCase):
    
    def test_9_modreq_desript(self):
        self.login() 
        sel = self.selenium
        sel.open("/project/meego/require/#requirement/1/details/")
        try: self.assertEqual("test@qualitio :: require", sel.get_title())
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if "MeeGo" == sel.get_text("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=MeeGo"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//li[@id='1_requirement']/ins")
        for i in range(60):
            try:
                if "TV" == sel.get_text("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=TV"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=TV")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=div#application-view-footer div a span")
        for i in range(60):
            try:
                if "requirement" == sel.get_text("css=div#application-view-header h1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_name", "new requirement 6")
        sel.click("id_release_target")
        for i in range(60):
            try:
                if sel.is_element_present("css=div#ui-datepicker-div div div"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=1")
        sel.click("link=4")
        sel.click("description_wrapper")
        sel.click("release_target_wrapper")
        for i in range(60):
            try:
                if sel.is_text_present("requirement"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("Executed")
        for i in range(60):
            try:
                if "MeeGo" == sel.get_text("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=MeeGo"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "TV" == sel.get_text("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=TV"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("link=new requirement 6"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=new requirement 6"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=new requirement 6")
        for i in range(60):
            try:
                if "requirement: new requirement 6" == sel.get_text("css=div#application-view-header h1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.failUnless(sel.is_element_present("css=div#application-view-header h1"))
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
                if sel.is_element_present("id_description"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("id_description"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id_description", "Desription of test")
        sel.click("css=input.ui-button")
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
                if sel.is_element_present("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "Notebook" == sel.get_text("link=Notebook"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "TV" == sel.get_text("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("Desription of test"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Desription of test"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=TV"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("link=new requirement 6"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "requirement: new requirement 6" == sel.get_text("css=div#application-view-header h1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name: /MeeGo/TV/new requirement 6"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("exact:requirement: new requirement 6"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("edit"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_element_present("id_description"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("id_description"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present(""))
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
                if sel.is_text_present("Changed description."): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Changed description."))
        except AssertionError, e: self.verificationErrors.append(str(e))
	time.sleep(2)
        sel.open("/admin/require/requirement/")
        for i in range(60):
            try:
                if sel.is_text_present("new requirement 6"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "Select requirement to change | Django site admin" == sel.get_title(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("xpath=(//input[@name='_selected_action'])[8]")
        try: self.assertEqual("on", sel.get_value("css=tr.row2.selected > td > input[name=\"_selected_action\"]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("name=action"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.select("name=action", "label=Delete selected requirements")
        sel.click("name=index")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_text_present("exact:28: /MeeGo/TV/new requirement 6"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.failUnless(sel.is_text_present("exact:28: /MeeGo/TV/new requirement 6"))
        sel.click("css=input[type=\"submit\"]")
        sel.wait_for_page_to_load("30000")


class Test10ModreqDepend(BaseSeleniumTestCase):
    
    def test_10_modreq_depend(self):
        self.login() 
        sel = self.selenium
        sel.open("/project/meego/require/#requirement/1/details/")
        try: self.assertEqual("test@qualitio :: require", sel.get_title())
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "MeeGo" == sel.get_text("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=MeeGo"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=MeeGo")
        time.sleep(2)
        for i in range(60):
            try:
                if "full name:" == sel.get_text("css=span.name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=li#1_requirement ins")
        time.sleep(2)
        for i in range(60):
            try:
                if "" == sel.get_text("css=#4_requirement > ins.jstree-icon"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("css=ins.jstree-icon"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "TV" == sel.get_text("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=TV"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=TV")
        time.sleep(2)
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: TV"): break
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
                if "create requirement" == sel.get_text("css=span.ui-button-text"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("css=#4_requirement > ins.jstree-icon"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("css=#4_requirement > ins.jstree-icon"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=#4_requirement > ins.jstree-icon")
        time.sleep(2)
        for i in range(60):
            try:
                if "" == sel.get_text("css=#13_requirement > ins.jstree-icon"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=MeeGo Handset test"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("css=span.ui-button-text"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=div#application-view-footer div a span")
        time.sleep(2)
        for i in range(60):
            try:
                if "requirement" == sel.get_text("css=div#application-view-header h1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "new" == sel.get_text("css=span.active"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_name", "new requirement 7")
        try: self.assertEqual("", sel.get_value("id=id_release_target"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("id_release_target")
        time.sleep(2)
        for i in range(60):
            try:
                if sel.is_element_present("css=div#ui-datepicker-div div div"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=1")
        time.sleep(2)
        sel.click("release_target_wrapper")
        time.sleep(1)
        for i in range(60):
            try:
                if sel.is_text_present("requirement"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("name=Executed"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("name=Executed"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("Executed")
        time.sleep(2)
        sel.wait_for_page_to_load("")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: new requirement 7"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "MeeGo" == sel.get_text("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "MeeGo" == sel.get_text("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=new requirement 7"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=MeeGo"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=new requirement 7"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("id_dependencies"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("id_dependencies"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.add_selection("id_dependencies", "label=3: /MeeGo/IVI")
        sel.click("Executed")
        time.sleep(2)
        sel.wait_for_page_to_load("")
        for i in range(60):
            try:
                if sel.is_element_present("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_release_target"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        time.sleep(2)
        try: self.assertEqual("test@qualitio :: require", sel.get_title())
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("Executed"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=new requirement 7"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=new requirement 7")
        time.sleep(2)
        for i in range(60):
            try:
                if "requirement: new requirement 7" == sel.get_text("css=div#application-view-header h1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name: /MeeGo/TV/new requirement 7"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("exact:requirement: new requirement 7"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_text_present("depends"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        time.sleep(2)
        for i in range(60):
            try:
                if sel.is_element_present("link=history"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("xpath=(//a[contains(text(),'IVI')])[2]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=3"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=IVI"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("IVI", sel.get_text("link=IVI"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("3", sel.get_text("link=3"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//div[@id='application-view']/div[6]/div/div/div/div/div[2]/table/tbody/tr/td[3]/a"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("IVI", sel.get_text("//div[@id='application-view']/div[6]/div/div/div/div/div[2]/table/tbody/tr/td[3]/a"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=history"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=history")
        time.sleep(2)
        for i in range(60):
            try:
                if sel.is_element_present("css=div#application-view-menu span"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
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
        time.sleep(2)
        try: self.failUnless(sel.is_text_present("Changed dependencies."))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Object created."))
        except AssertionError, e: self.verificationErrors.append(str(e))
        time.sleep(3)
        sel.open("/admin/require/requirement/")
        for i in range(60):
            try:
                if sel.is_text_present("new requirement 7"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "Select requirement to change | Django site admin" == sel.get_title(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("xpath=(//input[@name='_selected_action'])[8]")
        try: self.assertEqual("on", sel.get_value("css=tr.row2.selected > td > input[name=\"_selected_action\"]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("name=action"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.select("name=action", "label=Delete selected requirements")
        sel.click("name=index")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_text_present("exact:28: /MeeGo/TV/new requirement 7"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.failUnless(sel.is_text_present("exact:28: /MeeGo/TV/new requirement 7"))
        sel.click("css=input[type=\"submit\"]")
        sel.wait_for_page_to_load("30000")


class Test11Subrequir(BaseSeleniumTestCase):
    
    def test_11_subrequir(self):
        self.login() 
        sel = self.selenium
        sel.open("/project/meego/require/#requirement/1/details/")
        try: self.assertEqual("test@qualitio :: require", sel.get_title())
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if "MeeGo" == sel.get_text("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=MeeGo"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=ins.jstree-icon"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//li[@id='1_requirement']/ins")
        time.sleep(2)
        for i in range(60):
            try:
                if "" == sel.get_text("css=#10_requirement > ins.jstree-icon"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "" == sel.get_text("css=#4_requirement > ins.jstree-icon"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("css=#4_requirement > ins.jstree-icon"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "TV" == sel.get_text("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=TV"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=TV")
        time.sleep(1)
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("exact:requirement: TV"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=span.ui-button-text"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=div#application-view-footer div a span")
        time.sleep(1)
        for i in range(60):
            try:
                if "requirement" == sel.get_text("css=div#application-view-header h1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_name", "new requirement 8")
        for i in range(60):
            try:
                if "" == sel.get_text("id=id_release_target"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("id_release_target")
        time.sleep(1)
        for i in range(60):
            try:
                if sel.is_element_present("css=div#ui-datepicker-div div div"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=1")
        time.sleep(1)
        sel.click("release_target_wrapper")
        time.sleep(1)
        for i in range(60):
            try:
                if sel.is_text_present("requirement"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("Executed"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("Executed"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("Executed")
        time.sleep(1)
        for i in range(60):
            try:
                if "new requirement 8" == sel.get_text("link=new requirement 8"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "MeeGo" == sel.get_text("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=new requirement 8"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=new requirement 8"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("new requirement 8", sel.get_text("link=new requirement 8"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=new requirement 8"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=new requirement 8")
        time.sleep(1)
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: new requirement 8"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("exact:directory:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name: /MeeGo/TV/new requirement 8"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=div#application-view-footer div a span")
        time.sleep(1)
        for i in range(60):
            try:
                if "requirement" == sel.get_text("css=div#application-view-header h1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("id=id_name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id_name", "new subrequirement 8")
        for i in range(60):
            try:
                if "" == sel.get_text("id=id_release_target"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("id_release_target")
        for i in range(60):
            try:
                if sel.is_element_present("css=div#ui-datepicker-div div div"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=1")
        time.sleep(1)
        sel.click("release_target_wrapper")
        for i in range(60):
            try:
                if sel.is_text_present("requirement"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("exact:requirement"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("Executed")
        time.sleep(2)
        sel.wait_for_page_to_load("")
        for i in range(60):
            try:
                if "new requirement 8" == sel.get_text("link=new requirement 8"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "" == sel.get_text("css=#29_requirement > ins.jstree-icon"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "MeeGo" == sel.get_text("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=new requirement 8"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("new requirement 8"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if "new requirement 8" == sel.get_text("link=new requirement 8"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=new requirement 8")
        time.sleep(1)
        for i in range(60):
            try:
                if "new subrequirement 8" == sel.get_text("link=new subrequirement 8"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("", sel.get_text("css=#29_requirement > ins.jstree-icon"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=new subrequirement 8"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=new subrequirement 8")
        time.sleep(1)
        for i in range(60):
            try:
                if "requirement: new subrequirement 8" == sel.get_text("css=h1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name: /MeeGo/TV/new requirement 8/new subrequirement 8"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("directory: /MeeGo/TV/new requirement 8/"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=MeeGo"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=new requirement 8"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("exact:requirement: new subrequirement 8"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("full name: /MeeGo/TV/new requirement 8/new subrequirement 8"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("directory: /MeeGo/TV/new requirement 8/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if "create requirement" == sel.get_text("css=span.ui-button-text"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("css=span.ui-button-text"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//div[@id='application-view-footer']/div/a/span")
        time.sleep(1)
        for i in range(60):
            try:
                if "requirement" == sel.get_text("css=div#application-view-header h1"): break
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
        for i in range(60):
            try:
                if sel.is_element_present("id_release_target"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("id_name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id_name", "new sub2requirement 8")
        sel.select("id_parent", "label=28: /MeeGo/TV/new requirement 8")
        sel.click("id_release_target")
        for i in range(60):
            try:
                if sel.is_element_present("css=div#ui-datepicker-div div div"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=1")
        sel.click("release_target_wrapper")
        for i in range(60):
            try:
                if sel.is_text_present("new requirement"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("Executed"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("Executed"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("Executed")
        time.sleep(2)
        for i in range(60):
            try:
                if "MeeGo" == sel.get_text("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: new sub2requirement 8"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "TV" == sel.get_text("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=new requirement 8"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("exact:requirement: new sub2requirement 8"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if "MeeGo" == sel.get_text("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=MeeGo"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=TV"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=new requirement 8"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=details")
        time.sleep(1)
        for i in range(60):
            try:
                if sel.is_text_present("exact:directory:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("directory: /MeeGo/TV/new requirement 8/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("No data available in table"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Showing 0 to 0 of 0 entries"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("full name: /MeeGo/TV/new requirement 8/new sub2requirement 8"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("directory: /MeeGo/TV/new requirement 8/"))
        except AssertionError, e: self.verificationErrors.append(str(e))

        # <tr>
        # 	<td>click</td>
        # 	<td>//div[@id='application-view-footer']/div/a/span</td>
        # 	<td></td>
        # </tr>
        # <tr>
        # 	<td>click</td>
        # 	<td>//li[@id='28_requirement']/ins</td>
        # 	<td></td>
        # </tr>
        # <tr>
        # 	<td>clic</td>
        # 	<td>link=new requirement 8</td>
        # 	<td></td>
        # </tr>
        # <tr>
        # 	<td>waitForTextPresent</td>
        # 	<td>exact:requirement: new requirement 8</td>
        # 	<td></td>
        # </tr>
        # <tr>
        # 	<td>waitForTextPresent</td>
        # 	<td>exact:requirements:</td>
        # 	<td></td>
        # </tr>
        # <tr>
        # 	<td>waitForTextPresent</td>
        # 	<td>testcases</td>
        # 	<td></td>
        # </tr>
        # <tr>
        # 	<td>verifyTextPresent</td>
        # 	<td>full name: /MeeGo/TV/new requirement 8</td>
        # 	<td></td>
        # </tr>
        # <tr>
        # 	<td>verifyTextPresent</td>
        # 	<td>new subrequirement 8</td>
        # 	<td></td>
        # </tr>
        # <tr>
        # 	<td>verifyTextPresent</td>
        # 	<td>new sub2requirement 8</td>
        # 	<td></td>
        # </tr>
        # <tr>
        # 	<td>verifyElementPresent</td>
        # 	<td>//div[@id='application-view']/div[4]/div/div[1]/div[2]/table/tbody/tr[1]/td[3]/a</td>
        # 	<td></td>
        # </tr>
        # <tr>
        # 	<td>verifyElementPresent</td>
        # 	<td>//div[@id='application-view']/div[4]/div/div[1]/div[2]/table/tbody/tr[2]/td[3]/a</td>
        # 	<td></td>
        # </tr>


        try: self.failUnless(sel.is_element_present("link=new requirement 8"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        try: self.failUnless(sel.is_element_present("link=new sub2requirement 8"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        try: self.failUnless(sel.is_element_present("link=new subrequirement 8"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        time.sleep(3)

        sel.open("/admin/require/requirement/")

        for i in range(60):

            try:

                if sel.is_text_present("new requirement 8"): break

            except: pass

            time.sleep(1)

        else: self.fail("time out")

        for i in range(60):

            try:

                if "Select requirement to change | Django site admin" == sel.get_title(): break

            except: pass

            time.sleep(1)

        else: self.fail("time out")

        sel.click("xpath=(//input[@name='_selected_action'])[8]")

        try: self.assertEqual("on", sel.get_value("css=tr.row2.selected > td > input[name=\"_selected_action\"]"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        try: self.failUnless(sel.is_element_present("name=action"))

        except AssertionError, e: self.verificationErrors.append(str(e))

        sel.select("name=action", "label=Delete selected requirements")

        sel.click("name=index")

        sel.wait_for_page_to_load("30000")

        for i in range(60):

            try:

                if sel.is_text_present("exact:28: /MeeGo/TV/new requirement 8"): break

            except: pass

            time.sleep(1)

        else: self.fail("time out")

        self.failUnless(sel.is_text_present("exact:28: /MeeGo/TV/new requirement 8"))

        sel.click("css=input[type=\"submit\"]")

        sel.wait_for_page_to_load("30000")


class Test12DetailsVerify(BaseSeleniumTestCase):

    def test_12_details_verify(self):
        self.login() 
        sel = self.selenium
        sel.open("/project/meego/require/#requirement/1/details/")
        for i in range(60):
            try:
                if sel.is_text_present("MeeGo"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        sel.click("link=MeeGo")
        try: self.assertEqual("test@qualitio :: require", sel.get_title())
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_text_present("details"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("css=div#application-view-header"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div#application-view-header h1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("requirement: MeeGo", sel.get_text("css=div#application-view-header h1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("details", sel.get_text("css=div#application-view-menu span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("application-view-menu"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=edit"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=testcases"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=history"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div.application-view-content"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("full name: /MeeGo"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div#application-view div.application-view-content div:first-child"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div.application-view-content div span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("full name:", sel.get_text("css=div.application-view-content div span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("full name: /MeeGo", sel.get_text("css=div#application-view div.application-view-content div:first-child"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div#application-view div.application-view-content div:nth-child(2)"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("exact:directory:"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("directory: /"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div#application-view div.application-view-content div:nth-child(3)"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div#application-view div.application-view-content h2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div#application-view div.application-view-content div:nth-child(3)"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div#application-view div.application-view-content h2:nth-child(1)"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("connected testcases", sel.get_text("css=div#application-view div.application-view-content h2:contains(\"testcases\")"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div#application-view-footer div a span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("application-view-footer"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div#application-view-footer div"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("create requirement", sel.get_text("css=div#application-view-footer div a span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("depends"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("blocks"))
        except AssertionError, e: self.verificationErrors.append(str(e))


class Test13EditVerify(BaseSeleniumTestCase):
    
    def test_13_edit_verify(self):
        self.login() 
        sel = self.selenium
        sel.open("/project/meego/require/#requirement/1/details/")
        self.assertEqual("test@qualitio :: require", sel.get_title())
        for i in range(60):
            try:
                if sel.is_text_present("test@Qualitio"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "MeeGo" == sel.get_text("link=MeeGo"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=MeeGo"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=MeeGo")
        for i in range(60):
            try:
                if "requirement: MeeGo" == sel.get_text("css=div#application-view-header h1"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=edit"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        self.failUnless(sel.is_element_present("css=div#application-view-header h1"))
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_text_present("Parent"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("application-view-header"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("application-view-menu"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div.application-view-content"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("id_release_target")
        try: self.failUnless(sel.is_element_present("parent_wrapper"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_parent"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("name_wrapper"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("release_target_wrapper"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_release_target"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div#ui-datepicker-div"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("description_wrapper"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_description"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("dependencies_wrapper"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_dependencies"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("application-view-footer"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("Executed"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=input.ui-button[value='Save']"))
        except AssertionError, e: self.verificationErrors.append(str(e))


class Test14TestcasesVerify(BaseSeleniumTestCase):
    
    def test_14_testcases_verify(self):
        self.login() 
        sel = self.selenium
        sel.open("/project/meego/require/#requirement/1/details/")
        try: self.assertEqual("test@qualitio :: require", sel.get_title())
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if "MeeGo" == sel.get_text("link=MeeGo"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=MeeGo"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=MeeGo")
        for i in range(60):
            try:
                if "requirement: MeeGo" == sel.get_text("css=div#application-view-header h1"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=testcases"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        self.failUnless(sel.is_element_present("css=div#application-view-header h1"))
        sel.click("link=testcases")
        for i in range(60):
            try:
                if sel.is_element_present("//form[@id='testcases_connect_form']/div[2]/div/div/div/div/div/table/thead/tr/th/div"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("//form[@id='testcases_connect_form']/div[3]/div"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("css=th.sorting"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//form[@id='testcases_connect_form']/div[2]/div/div/div/div/div/table/thead/tr/th[3]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//form[@id='testcases_connect_form']/div[2]/div/div/div/div/div/table/thead/tr/th[4]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//form[@id='testcases_connect_form']/div[2]/div/div/div/div/div/table/thead/tr/th[5]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//form[@id='testcases_connect_form']/div[2]/div/div/div/div/div/table/thead/tr/th[6]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("id", sel.get_text("css=th.sorting"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("path", sel.get_text("//form[@id='testcases_connect_form']/div[2]/div/div/div/div/div/table/thead/tr/th[3]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("name", sel.get_text("//form[@id='testcases_connect_form']/div[2]/div/div/div/div/div/table/thead/tr/th[4]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("modified", sel.get_text("//form[@id='testcases_connect_form']/div[2]/div/div/div/div/div/table/thead/tr/th[5]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("created", sel.get_text("//form[@id='testcases_connect_form']/div[2]/div/div/div/div/div/table/thead/tr/th[6]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=span.ui-button-text"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=#add-testcases-button > span.ui-button-text"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//form[@id='testcases_connect_form']/div[4]/div"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("connected testcases"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("available testcases"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//form[@id='testcases_connect_form']/div[4]/div/div/div/div/div/table/thead/tr/th/div/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//form[@id='testcases_connect_form']/div[4]/div/div/div/div/div/table/thead/tr/th/div/span")
        for i in range(60):
            try:
                if sel.is_element_present("//form[@id='testcases_connect_form']/div[4]/div/div/div/div/div/table/thead/tr/th/div[2]/div"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("//form[@id='testcases_connect_form']/div[4]/div/div/div/div/div/table/thead/tr/th/div[2]/div"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//form[@id='testcases_connect_form']/div[4]/div/div/div/div/div/table/thead/tr/th/div[2]/div[2]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//form[@id='testcases_connect_form']/div[4]/div/div/div/div/div/table/thead/tr/th/div[2]/div[3]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//form[@id='testcases_connect_form']/div[4]/div/div/div/div/div/table/thead/tr/th/div/span")
        try: self.assertEqual("id", sel.get_text("//form[@id='testcases_connect_form']/div[4]/div/div/div/div/div/table/thead/tr/th[2]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("path", sel.get_text("//form[@id='testcases_connect_form']/div[4]/div/div/div/div/div/table/thead/tr/th[3]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("name", sel.get_text("//form[@id='testcases_connect_form']/div[4]/div/div/div/div/div/table/thead/tr/th[4]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("requirement", sel.get_text("//form[@id='testcases_connect_form']/div[4]/div/div/div/div/div/table/thead/tr/th[5]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("modified", sel.get_text("//form[@id='testcases_connect_form']/div[4]/div/div/div/div/div/table/thead/tr/th[6]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("created", sel.get_text("//form[@id='testcases_connect_form']/div[4]/div/div/div/div/div/table/thead/tr/th[7]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//form[@id='testcases_connect_form']/div[4]/div/div/div/div/div/table/thead/tr/th[6]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Search:"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=input[type=text]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id=testcase-3"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("css=div.select-btn.ui-state-default"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("css=div.select-btn.ui-state-default"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=span.ui-icon.ui-icon-triangle-1-s")
        for i in range(60):
            try:
                if sel.is_element_present("//div[@name='all']"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("//div[@name='all']"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//div[@name='none']"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//div[@name='invert']"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//form[@id='testcases_connect_form']/div[4]/div/div/div/div/div/table/thead/tr/th/div/span")
        for i in range(60):
            try:
                if "All" == sel.get_text("//form[@id='testcases_connect_form']/div[4]/div/div/div/div/div/table/thead/tr/th/div[2]/div"): break
            except: pass
            time.sleep(2)
        else: self.fail("time out")
        try: self.assertEqual("All", sel.get_text("//form[@id='testcases_connect_form']/div[4]/div/div/div/div/div/table/thead/tr/th/div[2]/div"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("None", sel.get_text("//form[@id='testcases_connect_form']/div[4]/div/div/div/div/div/table/thead/tr/th/div[2]/div[2]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Invert", sel.get_text("//form[@id='testcases_connect_form']/div[4]/div/div/div/div/div/table/thead/tr/th/div[2]/div[3]"))
        except AssertionError, e: self.verificationErrors.append(str(e))



class Test20SetTree(BaseSeleniumTestCase):
    
    def test_20_set_tree(self):
        self.login() 
        sel = self.selenium
        sel.open("/project/meego/require/#requirement/1/details/")
        for i in range(60):
            try:
                if sel.is_text_present("test@Qualitio"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=MeeGo")
        for i in range(60):
            try:
                if sel.is_element_present("css=li#1_requirement ins"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.assertEqual("test@qualitio :: require", sel.get_title())
        try: self.failUnless(sel.is_element_present("css=li#1_requirement ins"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=li#1_requirement ins")
        for i in range(60):
            try:
                if sel.is_text_present("TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=TV")
        for i in range(60):
            try:
                if sel.is_element_present("css=li#4_requirement ins"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=li#4_requirement ins")
        for i in range(60):
            try:
                if sel.is_element_present("link=MeeGo Handset test"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("MeeGo Handset test"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=MeeGo Handset test")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: MeeGo Handset test"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("exact:requirement: MeeGo Handset test"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=test cases")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_text_present("test@Qualitio"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.assertEqual("test@qualitio :: store", sel.get_title())
        sel.click("link=MeeGo Netbook")
        sel.click("css=li#1_testcasedirectory ins")
        for i in range(60):
            try:
                if sel.is_text_present("TestCase"): break
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
        try: self.failUnless(sel.is_text_present("test case: TestCase"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=requirements")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_text_present("test@Qualitio"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=ins.jstree-icon")
        time.sleep(2)
        for i in range(60):
            try:
                if sel.is_text_present("MeeGo Handset test"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=MeeGo Handset test"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=MeeGo Handset test")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: MeeGo Handset test"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("exact:requirement: MeeGo Handset test"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=test cases")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_text_present("test@Qualitio"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("MeeGo Netbook"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=#1_testcasedirectory > ins.jstree-icon")
        for i in range(60):
            try:
                if sel.is_text_present("TestCase"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=TestCase"))
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
        try: self.failUnless(sel.is_text_present("test case: TestCase"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("css=div#application-view-header h1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("test case: TestCase", sel.get_text("css=div#application-view-header h1"))
        except AssertionError, e: self.verificationErrors.append(str(e))



class Test23TreeNewreq(BaseSeleniumTestCase):
    
    def test_23_tree_newreq(self):
        self.login() 
        sel = self.selenium
        sel.open("/project/meego/require/#requirement/1/details/")
        for i in range(60):
            try:
                if sel.is_text_present("test@Qualitio"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.assertEqual("test@qualitio :: require", sel.get_title())
        try: self.failUnless(sel.is_element_present("css=ins.jstree-icon"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=ins.jstree-icon")
        for i in range(60):
            try:
                if sel.is_text_present("Notebook"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("css=li#4_requirement ins"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=TV")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("//div[@id='application-view-footer']/div/a/span"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("//div[@id='application-view-footer']/div/a/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if "create requirement" == sel.get_text("css=span.ui-button-text"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=div#application-view-footer div a span")
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
        sel.type("id_name", "new requirement 9")
        sel.click("id_release_target")
        sel.click("link=16")
        sel.type("id_description", "description\nnew\nrequirement\n9")
        for i in range(60):
            try:
                if sel.is_element_present("Executed"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("Executed"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=input[name='Executed'][value='Save']")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: new requirement 9"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "details" == sel.get_text("link=details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "testcases" == sel.get_text("link=testcases"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("exact:requirement: new requirement 9"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=new requirement 9"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("new requirement 9", sel.get_text("link=new requirement 9"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=details"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_element_present("//div[@id='application-view-footer']/div/a/span"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("//div[@id='application-view-footer']/div/a/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=div#application-view-footer div a span")
        for i in range(60):
            try:
                if sel.is_text_present("requirement"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("requirement"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_text_present("Parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_name", "new subrequirement9")
        sel.click("css=input[name='Executed'][value='Save']")
        for i in range(60):
            try:
                if "requirement: new subrequirement9" == sel.get_text("css=h1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if "" == sel.get_text("css=#28_requirement > ins.jstree-icon"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: new subrequirement9"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("exact:requirement: new subrequirement9"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=new subrequirement9"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("new subrequirement9", sel.get_text("link=new subrequirement9"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_text_present("Parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=div > b")
        sel.click("id=id_parent_chzn_o_2")
        try: self.failUnless(sel.is_text_present("exact:3: /MeeGo/IVI"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: new subrequirement9"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_element_present("id_release_target"): break
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
                if sel.is_element_present("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=details"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=details")
        time.sleep(2)
        for i in range(60):
            try:
                if sel.is_text_present("/MeeGo/IVI/new subrequirement9"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("test@Qualitio"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=new subrequirement9"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("/MeeGo/IVI/new subrequirement9"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("full name: /MeeGo/IVI/new subrequirement9"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=new subrequirement9"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("new subrequirement9", sel.get_text("link=new subrequirement9"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=new subrequirement9")
        time.sleep(2)
        sel.click("link=edit")
        time.sleep(3)
        for i in range(60):
            try:
                if sel.is_text_present("Parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=div > b")
        sel.click("id=id_parent_chzn_o_11")
        try: self.failUnless(sel.is_text_present("exact:28: /MeeGo/TV/new requirement 9"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//input[@name='Executed' and @value='Save']")
        for i in range(60):
            try:
                if sel.is_element_present("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_release_target"): break
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
                if sel.is_element_present("link=testcases"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=details"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=details")
        time.sleep(2)
        for i in range(60):
            try:
                if sel.is_text_present("full name: /MeeGo/TV/new requirement 9/new subrequirement9"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("test@Qualitio"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("directory:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("full name: /MeeGo/TV/new requirement 9/new subrequirement9"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("exact:directory: /MeeGo/TV/new requirement 9/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("exact:requirement: new subrequirement9"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=history"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=history")
        for i in range(60):
            try:
                if sel.is_element_present("link=details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("css=div#application-view-menu span"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
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
        try: self.assertEqual("Changed parent.", sel.get_text("//div[@id='application-view']/div[3]/div/div[1]/div[2]/table/tbody/tr[1]/td[3]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Changed parent.", sel.get_text("//div[@id='application-view']/div[3]/div/div[1]/div[2]/table/tbody/tr[2]/td[3]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
	time.sleep(2)
        sel.open("/admin/require/requirement/")
        for i in range(60):
            try:
                if sel.is_text_present("new requirement 9"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "Select requirement to change | Django site admin" == sel.get_title(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("xpath=(//input[@name='_selected_action'])[8]")
        try: self.assertEqual("on", sel.get_value("css=tr.row2.selected > td > input[name=\"_selected_action\"]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("name=action"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.select("name=action", "label=Delete selected requirements")
        sel.click("name=index")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_text_present("exact:28: /MeeGo/TV/new requirement 9"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.failUnless(sel.is_text_present("exact:28: /MeeGo/TV/new requirement 9"))
        self.failUnless(sel.is_text_present("exact:29: /MeeGo/TV/new requirement 9/new subrequirement9"))
        sel.click("css=input[type=\"submit\"]")
        sel.wait_for_page_to_load("30000")


class Test24Dependblock(BaseSeleniumTestCase):

    def test_24_dependblock(self):
        self.login() 
        sel = self.selenium
        sel.open("/project/meego/require/#requirement/1/details/")
        self.assertEqual("test@qualitio :: require", sel.get_title())
        for i in range(60):
            try:
                if sel.is_element_present("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=li#1_requirement ins")
        for i in range(60):
            try:
                if sel.is_element_present("link=Notebook"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=TV")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: TV"): break
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
        sel.add_selection("id_dependencies", "label=3: /MeeGo/IVI")
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
                if sel.is_text_present("full name: /MeeGo/TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("exact:directory: /MeeGo/"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=3"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("link=IVI"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=IVI")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: IVI"): break
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
        for i in range(60):
            try:
                if sel.is_element_present("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.add_selection("id_dependencies", "label=2: /MeeGo/Notebook")
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
                if sel.is_element_present("link=testcases"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=details"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_text_present("full name: /MeeGo/IVI"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=4"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=4"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=Notebook")
        for i in range(60):
            try:
                if sel.is_text_present("full name: /MeeGo/Notebook"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("exact:directory: /MeeGo/"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=3"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=3"))
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
                if sel.is_element_present("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.add_selection("id_dependencies", "label=4: /MeeGo/TV")
        sel.click("css=input[name='Executed'][value='Save']")
        for i in range(60):
            try:
                if sel.is_text_present("Validation errors"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Validation errors"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_text_present("You cannot set TV(id=4) as dependency because it produces cycle."): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("You cannot set TV(id=4) as dependency because it produces cycle."))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=input[name='Executed'][value='Save']")
        for i in range(60):
            try:
                if sel.is_element_present("id_description"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Parent"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_description"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=IVI")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: IVI"): break
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
                if sel.is_text_present("Parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "IVI" == sel.get_value("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("IVI", sel.get_value("id_name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.remove_selection("id_dependencies", "label=2: /MeeGo/Notebook")
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
                if sel.is_element_present("link=testcases"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_text_present("full name: /MeeGo/IVI"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("exact:directory: /MeeGo/"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=TV"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=TV")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: TV"): break
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
                if sel.is_text_present("Parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "TV" == sel.get_value("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.remove_selection("id_dependencies", "label=3: /MeeGo/IVI")
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


class Test25Verifylinks(BaseSeleniumTestCase):
    
    def test_25_verifylinks(self):
        self.login() 
        sel = self.selenium
        sel.open("/project/meego/require/#requirement/1/details/")
        self.assertEqual("test@qualitio :: require", sel.get_title())
        for i in range(60):
            try:
                if sel.is_element_present("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=MeeGo")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: MeeGo"): break
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
                if sel.is_text_present("Parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("Name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.add_selection("id_dependencies", "label=3: /MeeGo/IVI")
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_element_present("id_name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id_release_target"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if "history" == sel.get_text("link=history"): break
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
                if sel.is_text_present("full name:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("exact:directory:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("//li[@id='1_requirement']/ins")
        for i in range(60):
            try:
                if sel.is_element_present("link=Notebook"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=TV"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=TV")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: TV"): break
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
                if sel.is_text_present("Parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("Name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.add_selection("id_dependencies", "label=1: /MeeGo")
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
                if sel.is_element_present("link=testcases"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_text_present("full name:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("exact:directory:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=Notebook"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=Notebook")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: Notebook"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("exact:requirement: Notebook"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("full name: /MeeGo/Notebook"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("directory: /MeeGo/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("description: test1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=MeeGo")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name: /MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=Close navigation")
        sel.wait_for_page_to_load("30000")
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
        for i in range(60):
            try:
                if sel.is_element_present("link=exact:1: /MeeGo"): break
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
        try: self.failUnless(sel.is_text_present("full name: /MeeGo Netbook/MeeGo IVI BAT/Close navigation"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("parent: /MeeGo Netbook/MeeGo IVI BAT/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=exact:1: /MeeGo"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("requirement: 1: /MeeGo"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=exact:1: /MeeGo")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("edit"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("exact:description:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=3")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: IVI"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("exact:requirement: IVI"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("full name: /MeeGo/IVI"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("directory: /MeeGo/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=MeeGo")
        for i in range(60):
            try:
                if sel.is_element_present("link=edit"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("exact:description:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("//div[@id='application-view']/div[6]/div/div[2]/div/div/div[2]/table/tbody/tr/td[3]/a")
        for i in range(60):
            try:
                if "full name:" == sel.get_text("css=span.name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("exact:requirement: TV"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("full name: /MeeGo/TV"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("directory: /MeeGo/"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=MeeGo")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: MeeGo"): break
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
                if sel.is_text_present("exact:directory:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("//div[@id='application-view']/div[6]/div/div/div/div/div[2]/table/tbody/tr/td[3]/a")
        for i in range(60):
            try:
                if "edit" == sel.get_text("link=edit"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: IVI"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name:"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("exact:requirement: IVI"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("full name: /MeeGo/IVI"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("xpath=(//a[contains(text(),'MeeGo')])[4]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("xpath=(//a[contains(text(),'MeeGo')])[4]")
        for i in range(60):
            try:
                if sel.is_element_present("link=MeeGo"): break
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
                if sel.is_text_present("exact:requirement: MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name:"): break
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
        for i in range(60):
            try:
                if sel.is_text_present("Name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.remove_selection("id_dependencies", "label=3: /MeeGo/IVI")
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_element_present("link=details"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: MeeGo"): break
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
                if sel.is_element_present("link=TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "" == sel.get_text("css=#4_requirement > ins.jstree-icon"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=TV"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=TV")
        sel.click("link=TV")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("full name:"): break
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
        for i in range(60):
            try:
                if sel.is_text_present("Name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.remove_selection("id_dependencies", "label=1: /MeeGo")
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: TV"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("css=li#1_requirement ins"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("css=li#1_requirement ins")


class Test32Samename(BaseSeleniumTestCase):
    
    def test_32_samename(self):
        self.login() 
        sel = self.selenium
        sel.open("/project/meego/require/#requirement/1/details/")
        self.assertEqual("test@qualitio :: require", sel.get_title())
        for i in range(60):
            try:
                if "MeeGo" == sel.get_text("link=MeeGo"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=MeeGo")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: MeeGo"): break
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
                if sel.is_element_present("//div[@id='application-view-footer']/div/a/span"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("//div[@id='application-view-footer']/div/a/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//div[@id='application-view-footer']/div/a/span")
        for i in range(60):
            try:
                if sel.is_text_present("requirement"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_text_present("new"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_name", "IVI")
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_text_present("Validation errors: \"parent\", \"name\" and \"project\" fields need to be always unique together."): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Validation errors: \"parent\", \"name\" and \"project\" fields need to be always unique together."))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id_name", "IVI2")
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: IVI2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("link=IVI2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("exact:requirement: IVI2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=IVI2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_text_present("Parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("id_name", "IVI")
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_text_present("Validation errors: \"parent\", \"name\" and \"project\" fields need to be always unique together."): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Validation errors: \"parent\", \"name\" and \"project\" fields need to be always unique together."))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.select("id_parent", "label=10: /MeeGo/Legacy")
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
                if sel.is_element_present("link=testcases"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=details")
        for i in range(60):
            try:
                if sel.is_text_present("full name: /MeeGo/Legacy/IVI"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("full name: /MeeGo/Legacy/IVI"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=edit")
        for i in range(60):
            try:
                if sel.is_text_present("Parent"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.select("id_parent", "label=1: /MeeGo")
        sel.click("Executed")
        for i in range(60):
            try:
                if sel.is_text_present("Validation errors: \"parent\", \"name\" and \"project\" fields need to be always unique together."): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("Validation errors: \"parent\", \"name\" and \"project\" fields need to be always unique together."))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id_name", "requirement")
        sel.type("id_name", "requirement same name")
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
        try: self.failUnless(sel.is_element_present("link=details"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=details")
        time.sleep(2)
        for i in range(60):
            try:
                if sel.is_text_present("exact:requirement: requirement same name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_text_present("exact:requirement: requirement same name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=requirement same name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
	time.sleep(2)
        sel.open("/admin/require/requirement/")
        for i in range(60):
            try:
                if sel.is_text_present("requirement same name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "Select requirement to change | Django site admin" == sel.get_title(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("xpath=(//input[@name='_selected_action'])[16]")
        try: self.assertEqual("on", sel.get_value("css=tr.row2.selected > td > input[name=\"_selected_action\"]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("name=action"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.select("name=action", "label=Delete selected requirements")
        sel.click("name=index")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_text_present("exact:28: /MeeGo/requirement same name"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.failUnless(sel.is_text_present("exact:28: /MeeGo/requirement same name"))
        sel.click("css=input[type=\"submit\"]")
        sel.wait_for_page_to_load("30000")


class Test45FilterVerify(BaseSeleniumTestCase):

    
    def test_45_filter_verify(self):
        self.login() 
        sel = self.selenium
        sel.open("/project/meego/require/#requirement/1/details/")
        self.assertEqual("test@qualitio :: require", sel.get_title())
        for i in range(60):
            try:
                if sel.is_element_present("link=filter"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=filter"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=filter")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_element_present("link=browse"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("link=browse"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_control-new-group-add_group"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Select one group to start the search"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("link=2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("15 on page 30 on page 50 on page 100 on page"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_onpage"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Id"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Modified time"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Created time"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Path"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Name"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Release target"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.select("id_control-new-group-add_group", "label=Name")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_element_present("//div[@id='application-view']/form/div/div[1]"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("//input[@value='Filter']"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("//input[@value='Filter']"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("", sel.get_text("//input[@value='Filter']"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Reset query", sel.get_text("//div[@id='application-view']/form/div/div/a/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//div[@id='application-view']/form/div/div/a/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if sel.is_element_present("id_1-1-1-lookup"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("Name", sel.get_text("//div[@id='application-view']/form/div/div[1]/div[1]/div[1]/label"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Name", sel.get_text("//div[@id='application-view']/form/div/div[1]/div[1]/div[1]/label"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_1-1-1-lookup"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("contains"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("id_1-1-1-q"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//div[@id='application-view']/form/div/div[1]/div[1]/div[4]/div/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Remove"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("control-remove-filter-1-1-1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.select("id=id_1-control-new-criteria-add_field_filter", "label=Requirement (parent)")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_text_present("Requirement (parent)"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if sel.is_element_present("id=id_1-7-1-q"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("id=id_1-7-1-q"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Requirement (parent)"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//div[@id='application-view']/form/div/div[2]/a/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//div[@id='application-view']/form/div/div[2]/a/span")
        sel.wait_for_page_to_load("30000")
        time.sleep(2)
        for i in range(60):
            try:
                if sel.is_element_present("//div[@id='application-view']/form/div/div[1]/div[1]"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.failUnless(sel.is_element_present("//input[@value='Filter']"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failIf(sel.is_element_present("id=id_1-1-1-lookup"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=browse")
        sel.wait_for_page_to_load("30000")
        for i in range(60):
            try:
                if sel.is_text_present("test@Qualitio"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if "test@qualitio :: require" == sel.get_title(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.assertEqual("test@qualitio :: require", sel.get_title())
    

if __name__ == "__main__":
    unittest.main()
