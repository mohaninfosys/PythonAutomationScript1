from commonMethods.commonUtils import commonUtils
import time

configObj = commonUtils().configObj

class VPMS:

    def editassignmodules(self):
        self.logixlogin()

    def logixlogin(self):
        commonUtils.get("https://v100.xoxoday.com/experiences")
        adminemail = "//div/input[@id='username']"
        password = "//div/input[@id='password']"
        submit = "//div/button[@type='submit']"

        commonUtils.enterkeys(adminemail, "sheetal@xoxoday.com")
        commonUtils.enterkeys(password, "Test@123")
        commonUtils.click(submit)
        commonUtils.click("//a/span[contains(text(),' dashboard ')]")
        commonUtils.click("//a/span[contains(text(),'experiences')]")

        companydetails = configObj["CompanyID"]["CompanyName"]
        comname = companydetails.split(">>")
        i = 0
        for i in range(0, 930):
            details = comname[i]
            commonUtils.enterkeys("//input[@placeholder='Experience name']", details)
            time.sleep(2)
            commonUtils.click("//a/h5")
            commonUtils.click("//b[contains(text(),'Images')]")
            for x in range(1,50):
                print("#"+details)
                if commonUtils.verifyelementispresent("(//span[@class='ReactTags__tag'])["+str(x)+"]"):
                    print(commonUtils.getinnertext("(//span[@class='ReactTags__tag'])[" +str(x)+"]"))
                else:
                    break
            commonUtils.click("//a/span[contains(text(),' dashboard ')]")
            commonUtils.click("//a/span[contains(text(),'experiences')]")
