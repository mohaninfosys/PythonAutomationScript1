from commonMethods.commonUtils import commonUtils
import config
import time
from commonMethods.jsonLoader import jsonLoader

configObj = commonUtils().configObj

class stores:
    config_file = config.config_path
    config_vouchers = config.voucher_file_path
    configObj = jsonLoader.json_read(config_file)
    global voucherstatus
    voucherstatus = jsonLoader.json_read(config_vouchers)

    vouchers = configObj["stores"]["vouchers"]
    addquantity = "(//button/span[contains(text(),'+')])[1]"
    voucherCode = "//div[@id='voucher-code']/input"
    apply = "//div//button[contains(text(),'Apply')]"
    placeOrder = "//div//button[contains(text(),'Place Order')]"

    def directlogin(self, product, user):
        global pointsPresent
        url = configObj["stores"]["url"]
        userPoints = "//a/span[@class='user_points']"
        logout = "//ul[@id='login-dropdown']/li[3]"
        emailId = configObj["Directlogin"]["useremail"]
        password = configObj["Directlogin"]["password"]
        userLogout = "//li[@class='dropdown account-user-dropdown']/a"

        if(user == "user"):
            self.login(emailId, password)
        else:
            self.login("test@signin.com", "Test@1234")
        points = commonUtils.gettext(userPoints)
        pointsInAccount = points.split(':')
        pointsPresent = (pointsInAccount[1])
        usedXoxoPoints = self.pointsCheckout(product,user)
        commonUtils.get(url)
        pd = commonUtils.gettext(userPoints)
        p = pd.split(':')
        pp = (p[1])
        if(pointsPresent == pp):
            print("Points Not deducted for the Placed Order ID")
        else:
            xoxopoints = usedXoxoPoints.split(' ')
            pointsUsed = xoxopoints[0]
            pointsDeducted = (float(pointsPresent) - float(pointsUsed))
            print(pointsDeducted)
        commonUtils.click(userLogout)
        time.sleep(3)
        commonUtils.waitforlocator(logout)
        commonUtils.mouseoverandclick(logout)
        commonUtils.click(logout)
        time.sleep(3)

    def login(self, emailID, password):
        url = configObj["stores"]["url"]
        login = "//li/a[contains(text(),'Login')]"
        useremail = "//div/input[@name='email'][@placeholder='someone@example.com']"
        verifyEmail = "//div/button[@type='submit'][contains(text(),'Verify Email')]"
        userpassword = "//div/input[@name='password']"
        loginSubmit = "//div/button[@type='submit'][contains(text(),'Login')]"

        commonUtils.get(url)
        commonUtils.click(login)
        commonUtils.enterkeys(useremail, emailID)
        commonUtils.click(verifyEmail)
        commonUtils.enterkeys(userpassword, password)
        commonUtils.click(loginSubmit)
        time.sleep(3)
        commonUtils.get(url)

    def pointsCheckout(self, product, voucher):
        cart = "//i[@class='pe-7s-cart']"
        proceed = "//button/span[contains(text(),'PROCEED TO PAYMENT')]"
        netorderPoints = "(//ul[@class='orderSummery']/li/span)[1]"
        xoxoPointsUsed = "(//ul[@class='orderSummery']/div/li/span)[1]"
        totalPayablePoints = "(//ul[@class='orderSummery']/div/li/span)[2]"
        payableInINR = "(//ul[@class='orderSummery']/li/span)[2]"
        cartValue = "(//div[@class='summary-wrapper total-pay']/table/tbody/tr/td[@class='text-right'])[1]"
        pointsUsed = "(//div[@class='summary-wrapper total-pay']/table/tbody/tr/td[@class='text-right'])[2]"
        totalpayable = "(//div[@class='summary-wrapper total-pay']/table/tbody/tr/td[@class='text-right'])[3]"
        placeOrder = "//div//button[contains(text(),'Place Order')]"
        orderid = "//h4[contains(text(),'Your Order #')]"
        voucher1 = configObj["stores"]["giftvouchers"]
        voucher2 = configObj["stores"]["giftvouchers2"]
        search = "//div/input[@id='search-input']"
        makepayment = "//div/button[@id='make-payment']"
        voucher50 = configObj["vouchers"]["50"]
        voucher300 = configObj["vouchers"]["300"]
        voucher500 = configObj["vouchers"]["500"]

        self.giftvouchers()
        if(product == "Single Product"):
            commonUtils.enterkeys(search, voucher1)
            time.sleep(3)
            self.selectprice()
        if (product == "Foreign Denomination"):
            commonUtils.enterkeys(search, configObj["stores"]["currencyVouchers"])
            time.sleep(3)
            self.selectprice()
        if(product == "Multiple Product"):
            commonUtils.enterkeys(search, voucher1)
            time.sleep(3)
            self.selectprice()
            commonUtils.clearandtype(search, voucher2)
            time.sleep(3)
            commonUtils.waitforlocator("//div[@class='content']/h4[contains(text(),'"+voucher2+"')]")
            self.selectprice()
        if (product == "Multiple Foreign Denomination"):
            commonUtils.enterkeys(search, configObj["stores"]["currencyVouchers"])
            time.sleep(3)
            self.selectprice()
            time.sleep(2)
            commonUtils.clearandtype(search, "Amazon Tango")
            time.sleep(3)
            commonUtils.waitforlocator("//div[@class='content']/h4[contains(text(),'Amazon Tango')]")
            self.selectprice()
        time.sleep(3)
        commonUtils.click(cart)
        netOrder = commonUtils.gettext(netorderPoints)
        pointsUsedXoxo = commonUtils.gettext(xoxoPointsUsed)
        commonUtils.click(proceed)
        cartPrice = commonUtils.gettext(cartValue)
        cartPriceValue = cartPrice.split('.')
        pricevalue = (cartPriceValue[0])
        usedPoints = commonUtils.gettext(pointsUsed)
        payableValue = commonUtils.gettext(totalpayable)
        payPriceValue = payableValue.split(' ')
        payvalue = (payPriceValue[0])
        if(cartPrice == usedPoints):
           commonUtils.click(placeOrder)
        elif(voucher == "voucher"):
            self.voucherRedeemption(voucher500)
        elif (voucher == "Partialvoucher"):
            self.voucherRedeemption(voucher50)
        elif(float(payvalue)>0):
            commonUtils.click(makepayment)
        orderIDdetails = commonUtils.gettext(orderid)
        print(orderIDdetails)
        return usedPoints

    def voucherRedeemption(self,voucher300):
        usedvouchers = []
        usedvouchers.append(voucherstatus['usedVouchers'])
        global vouchersUsed
        vouchersUsed = usedvouchers[0]

        voucherCode = "//div[@id='voucher-code']/input"
        apply = "//div//button[contains(text(),'Apply')]"
        placeOrder = "//div/button[@class='btn btn-block btn-default btn-lg']"
        search = "//div/input[@id='search-input']"
        makepayment = "//div/button[@class='btn btn-block btn-default btn-lg']"

        arr =[]
        data = []
        arr.append(voucher300)
        for x in arr:
            for y in range(0, 100):
                if x[y] in vouchersUsed:
                    print(x[y] + " is used")
                else:
                    commonUtils.enterkeys(voucherCode, x[y])
                    commonUtils.click(apply)
                    vouchersUsed.append(x[y])
                    if(commonUtils.isenabled(voucherCode)):
                        commonUtils.enterkeys(voucherCode, x[y + 1])
                        commonUtils.click(apply)
                        vouchersUsed.append(x[y + 1])
                    if ("Place Order"==commonUtils.gettext(placeOrder)):
                        time.sleep(3)
                        commonUtils.click(placeOrder)
                    else:
                        commonUtils.click(makepayment)        
                    data.append({"usedVouchers": vouchersUsed})
                    jsonLoader.write_vouchers(data[0])
                    commonUtils.write_Json()

    def voucherCheckout(self, voucher1, voucher300):

        usedvouchers = []
        usedvouchers.append(voucherstatus['usedVouchers'])
        global vouchersUsed
        vouchersUsed = usedvouchers[0]
        print(vouchersUsed)

        voucherCode = "//div[@id='voucher-code']/input"
        apply = "//div//button[contains(text(),'Apply')]"
        placeOrder = "//div/button[@class='btn btn-block btn-default btn-lg']"
        search = "//div/input[@id='search-input']"
        makepayment = "//div/button[@class='btn btn-block btn-default btn-lg']"

        self.giftvouchers()
        commonUtils.enterkeys(search, voucher1)
        time.sleep(3)
        self.selectprice()
        self.cartcheckout()
        arr =[]
        data = []
        arr.append(voucher300)
        for x in arr:
            for y in range(0, 100):
                if x[y] in vouchersUsed:
                    print(x[y] + " is used")
                else:
                    commonUtils.enterkeys(voucherCode, x[y])
                    commonUtils.click(apply)
                    vouchersUsed.append(x[y])
                    if("Place Order"==commonUtils.gettext(placeOrder)) :
                        commonUtils.click(placeOrder)
                    else:
                        time.sleep(2)
                        commonUtils.doubleclick(makepayment)
                    data.append({"usedVouchers": vouchersUsed})
                    print(data[0])
                    jsonLoader.write_vouchers(data[0])
                    commonUtils.write_Json()
                    break
        self.otpCheckout()


    def multiplevoucherCheckout(self, voucher1, voucher2, voucher1000):

        usedvouchers = []
        usedvouchers.append(voucherstatus['usedVouchers'])
        global vouchersUsed
        vouchersUsed = usedvouchers[0]
        print(vouchersUsed)

        voucherCode = "//div[@id='voucher-code']/input"
        apply = "//div//button[contains(text(),'Apply')]"
        placeOrder = "//div/button[@class='btn btn-block btn-default btn-lg']"
        search = "//div/input[@id='search-input']"
        makePayment = "//div/button[@class='btn btn-block btn-default btn-lg']"

        self.giftvouchers()
        commonUtils.enterkeys(search, voucher1)
        time.sleep(2)
        self.selectprice()
        commonUtils.clearandtype(search, voucher2)
        time.sleep(3)
        commonUtils.waitforlocator("//div[@class='content']/h4[contains(text(),'"+voucher2+"')]")
        self.selectprice()
        self.cartcheckout()
        arr =[]
        data = []
        arr.append(voucher1000)
        for x in arr:
            for y in range(0,100):
                if x[y] in vouchersUsed:
                    print(x[y]+ " is used")
                else:
                    commonUtils.enterkeys(voucherCode, x[y])
                    commonUtils.click(apply)
                    vouchersUsed.append(x[y])
                    if(commonUtils.isenabled(voucherCode)):
                        commonUtils.enterkeys(voucherCode, x[y + 1])
                        commonUtils.click(apply)
                        time.sleep(2)
                        vouchersUsed.append(x[y + 1])
                        print(commonUtils.getattribute(placeOrder,"innerText"))
                    if (commonUtils.verifyelementispresent(placeOrder)):
                        time.sleep(2)
                        commonUtils.click(placeOrder)
                    elif("Make Payment"==commonUtils.gettext(makePayment)):
                        time.sleep(2)
                        commonUtils.click(makePayment)
                    data.append({"usedVouchers": vouchersUsed})
                    print(data[0])
                    jsonLoader.write_vouchers(data[0])
                    commonUtils.write_Json()
                    break
        self.otpCheckout()

    def selectprice(self):
        selectPrice = "(//div[contains(text(),'Select Price')])[1]"
        addquantity = "(//button/span[contains(text(),'+')])[1]"
        addtocart = "(//button/span[contains(text(),'ADD TO CART')])[1]"

        commonUtils.click(selectPrice)
        commonUtils.click("(//ul[@role='listbox']/li)[2]")
        for i in range(0, 3):
            commonUtils.click(addquantity)
        commonUtils.click(addtocart)

    def giftvouchers(self):
        url = configObj["stores"]["url"]
        giftvouchers = "//ul[@class='secondary-navbar']//li[2]"

        commonUtils.get(url)
        commonUtils.click(giftvouchers)

    def cartcheckout(self):
        cart = "//i[@class='pe-7s-cart']"
        proceed = "//button/span[contains(text(),'PROCEED TO PAYMENT')]"
        email = "//div/input[@type='email']"
        continuebutton = "//button[contains(text(),'Continue')]"
        entername = "//div[@id='email-input']/input[@placeholder='Enter Name']"
        mobileNumber = "//div/input[@type='number']"
        mailid = configObj["stores"]["email"]
        name = configObj["stores"]["name"]
        phonenumber = configObj["stores"]["mobilenumber"]

        commonUtils.click(cart)
        commonUtils.click(proceed)
        commonUtils.enterkeys(email, mailid)
        commonUtils.click(continuebutton)
        commonUtils.enterkeys(entername, name)
        commonUtils.enterkeys(mobileNumber, phonenumber)

    def otpCheckout(self):
        otpsubmit = "//div/input[@placeholder='OTP']"
        submit = "//div//input[@value='Submit']"
        redendotp = "//button[contains(text(),'Resend OTP')]"
        orderid = "//h4[contains(text(),'Your Order #')]"

        time.sleep(3)
        otp = commonUtils.getcustomerotp()
        print(otp)
        commonUtils.enterkeys(otpsubmit, otp)
        commonUtils.click(submit)
        commonUtils.waitforlocator(orderid)
        orderIDdetails = commonUtils.gettext(orderid)
        print(orderIDdetails)