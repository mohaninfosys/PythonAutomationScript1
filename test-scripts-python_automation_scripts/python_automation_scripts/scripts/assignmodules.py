from commonMethods.commonUtils import commonUtils
import time

configObj = commonUtils().configObj

class assignmodules:

    def editassignmodules(self):
        self.logixlogin()
        self.modules()
        self.editModules()

    def logixlogin(self):
        commonUtils.logixurl(self)
        adminemail = "//input[@id='txtEmail']"
        next = "//input[@name='btnNext']"
        logixotp = "//input[@id='txtOtp']"

        commonUtils.enterkeys(adminemail, configObj["logix"]["user"])
        commonUtils.click(next)
        otp = input('Enter the OTP:')
        print(otp)
        commonUtils.enterkeys(logixotp, otp)
        commonUtils.click("//input[@name='btnVerify']")

    def modules(self):
        commonUtils.mouseover("//li[@class='dropdown dropdown-user dropdown-light']")
        time.sleep(.2)
        commonUtils.click("(//a[@href='/admin/assignmodules'])[1]")

    def editModules(self):
        companydetails = configObj["CompanyID"]["CompanyName"]
        comname = companydetails.split(">>")
        i = 0
        for i in range(0,930):
            details = comname[i].split("#")
            commonUtils.enterkeys("//input[@type='search']",details[1])
            commonUtils.waitforlocator("//td/a[contains(text(),'Edit')]")
            commonUtils.click("(//tbody/tr/td[text()='" + details[0] + "']//following::td/a[contains(text(),'Edit')])[1]");
            print(details[1])
            if commonUtils.verifyelementispresent("//div/input[@value='12_145'][@checked='checked']"):
                print("present")
                commonUtils.deselectcheckbox("//div/input[@value='12_145']")
                commonUtils.click("//input[@id='submit']")
            else:
                commonUtils.click("//button[@id='cancel']")


        # for i in range(0,882):
        #     details = comname[i].split("#")
        #     print(details[0],details[1])
        #     commonUtils.enterkeys("//input[@type='search']", details[0]);
        #     commonUtils.waitforlocator("//td/a[contains(text(),'Edit')]");
        #     commonUtils.click("(//tbody/tr/td[text()='" + details[0] + "']//following::td/a[contains(text(),'Edit')])[1]");
        #     if commonUtils.verifyelementispresent("//input[@value='11'][@checked='checked']"):
        #         print("present")
        #         commonUtils.selectcheckbox("//input[@value='254']")
        #         commonUtils.selectcheckbox("//input[@value='255']")
        #         commonUtils.click("//input[@id='submit']")
        #     else:
        #         commonUtils.click("//button[@id='cancel']")
