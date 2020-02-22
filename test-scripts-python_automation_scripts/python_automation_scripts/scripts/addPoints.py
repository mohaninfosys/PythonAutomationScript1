from commonMethods.commonUtils import commonUtils
import time

configObj = commonUtils().configObj

class addPoints:

    def logixurl(self):
        commonUtils.get(configObj["logix"]["url"])

    def logixlogin(self):
        adminemail = "//input[@id='txtEmail']"
        next = "//input[@name='btnNext']"

        commonUtils.enterkeys(adminemail, configObj["logix"]["user"])
        commonUtils.click(next)
        self.logindb()
        self.points()
        self.creditcompanypoints()


    def logindb(self):
        otp = "//input[@name='txtOtp']"
        commonUtils.opennewtab(configObj["phpmyadmin"]["url"])
        commonUtils.enterkeys("//input[@id='input_username']", configObj["phpmyadmin"]["user"]);
        commonUtils.enterkeys("//input[@id='input_password']", configObj["phpmyadmin"]["password"]);
        commonUtils.click("//input[@value='Go']");
        userid = commonUtils.gettext("(//table[@id='table_results']/tbody/tr/td[7])[1]")
        if userid == "25":
            loginotp = commonUtils.gettext("(//table[@id='table_results']/tbody/tr/td[6])[1]")
        else:
            for i in range(2, 20):
                userid = commonUtils.gettext("(//table[@id='table_results']/tbody/tr/td[7])[" + i + "]")
                if userid is 25:
                    loginotp = commonUtils.gettext("(//table[@id='table_results']/tbody/tr/td[7])[" + i + "]")
                    break
        commonUtils.closenewtab(self)
        commonUtils.enterkeys(otp, loginotp)
        commonUtils.click("//input[@name='btnVerify']")

    def points(self):
        commonUtils.mouseover("//li[@class='dropdown dropdown-user dropdown-light']")
        time.sleep(.2)
        commonUtils.click("(//a[@href='/admin/companypoints'])[1]")
        commonUtils.click("//a[@href='/admin/companypoints/add']")

    def creditcompanypoints(self):
        commonUtils.click("//a//span[text()='Search by Company Name']")
        commonUtils.enterkeys("//ul//li[text()='Please enter 1 or more character']//preceding::input[@id='s2id_autogen1_search']", configObj["companypoints"]["name"])
        time.sleep(.2)
        commonUtils.click("//div[@class='select2-result-label']")
        commonUtils.click("//select[@id='country_id']")
        commonUtils.click("//select[@id='country_id']//option[contains(text(),'India')]")
        commonUtils.enterkeys("//input[@id='points_allocated']", configObj["companypoints"]["points"])
        po_number = commonUtils.randomnumber()
        commonUtils.enterkeys("//input[@id='invoice_number']", "99"+po_number)
        commonUtils.selectbyvalue("//select[@id='payment_term']", configObj["companypoints"]["term"])
        commonUtils.enterkeys("//input[@id='emails']", configObj["companypoints"]["emails"])
        commonUtils.enterkeys("//textarea[@id='details']", configObj["companypoints"]["description"])
        commonUtils.enterkeys("//input[@id='company_invoice']", configObj["companypoints"]["path"])
        commonUtils.click("//input[@id='submit']")
        time.sleep(.10)