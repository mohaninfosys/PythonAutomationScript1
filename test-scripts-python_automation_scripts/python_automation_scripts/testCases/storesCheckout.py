from requests import request

from commonMethods.commonUtils import commonUtils
import config
from commonMethods.jsonLoader import jsonLoader
from scripts.stores import stores

configObj = commonUtils().configObj
storesRedemption = stores()

class storesScenario:
    config_file = config.config_path
    config_vouchers = config.voucher_file_path
    configObj = jsonLoader.json_read(config_file)

    def storesCheckout(self):
        voucher1 = configObj["stores"]["giftvouchers"]
        voucher2 = configObj["stores"]["giftvouchers2"]
        foreigncurrencyvouchers = configObj["stores"]["currencyVouchers"]
        foreigncurrencyvouchers2 = "Amazon Tango"
        vouchers = configObj["stores"]["vouchers"]
        voucher50 = configObj["vouchers"]["50"]
        voucher100 = configObj["vouchers"]["100"]
        voucher300 = configObj["vouchers"]["300"]
        voucher500 = configObj["vouchers"]["500"]
        voucher1000 = configObj["vouchers"]["1000"]
        voucher2000 = configObj["vouchers"]["2000"]

        #Stores - Non-Registered User Flow

        #Vouchers - 100% Redemption

        storesRedemption.voucherCheckout(voucher1, voucher300)
        storesRedemption.multiplevoucherCheckout(voucher1, voucher2, voucher1000)
        storesRedemption.voucherCheckout(foreigncurrencyvouchers, voucher500)
        storesRedemption.multiplevoucherCheckout(foreigncurrencyvouchers, foreigncurrencyvouchers2, voucher2000)

        # Vouchers + payment

        storesRedemption.voucherCheckout(voucher1, voucher100)
        storesRedemption.multiplevoucherCheckout(voucher1, voucher2, voucher100)
        storesRedemption.voucherCheckout(foreigncurrencyvouchers, voucher100)
        storesRedemption.multiplevoucherCheckout(foreigncurrencyvouchers, foreigncurrencyvouchers2, voucher500)

        # Stores - Enterprise Users

        # Points

        storesRedemption.directlogin("Single Product", "user")
        storesRedemption.directlogin("Multiple Product", "user")

        #Payment

        storesRedemption.directlogin("Single Product", "user1")
        storesRedemption.directlogin("Multiple Product", "user1")

        # Vouchers

        storesRedemption.directlogin("Single Product", "voucher")
        storesRedemption.directlogin("Multiple Product", "voucher")

        # Vouchers + Payment

        storesRedemption.directlogin("Single Product", "Partialvoucher")
        storesRedemption.directlogin("Multiple Product", "Partialvoucher")

        #Points + Payment

        self.addPointsAPI()
        storesRedemption.directlogin("Single Product", "user1")
        self.addPointsAPI()
        storesRedemption.directlogin("Multiple Product", "user1")

        #Points + Vouchers

        self.addPointsAPI()
        storesRedemption.directlogin("Single Product", "voucher")
        self.addPointsAPI()
        storesRedemption.directlogin("Multiple Product", "voucher")

        # Points + Vouchers + Payment
        self.addPointsAPI()
        storesRedemption.directlogin("Single Product", "Partialvoucher")
        self.addPointsAPI()
        storesRedemption.directlogin("Multiple Product", "Partialvoucher")

        #Stores - Foreign denominations Scenarios
        #Points

        storesRedemption.directlogin("Foreign Denomination", "user")
        storesRedemption.directlogin("Multiple Foreign Denomination", "user")

        #Payment

        storesRedemption.directlogin("Foreign Denomination", "user1")
        storesRedemption.directlogin("Multiple Foreign Denomination", "user1")

        # Vouchers

        storesRedemption.directlogin("Foreign Denomination", "voucher")
        storesRedemption.directlogin("Multiple Foreign Denomination", "voucher")

        # Vouchers + Payment

        storesRedemption.directlogin("Foreign Denomination", "Partialvoucher")
        storesRedemption.directlogin("Multiple Foreign Denomination", "Partialvoucher")

        # Points + Payment

        self.addPointsAPI()
        storesRedemption.directlogin("Foreign Denomination", "user1")
        self.addPointsAPI()
        storesRedemption.directlogin("Multiple Foreign Denomination", "user1")

        # Points + Vouchers

        self.addPointsAPI()
        storesRedemption.directlogin("Foreign Denomination", "voucher")
        self.addPointsAPI()
        storesRedemption.directlogin("Multiple Foreign Denomination", "voucher")

        # Points + Vouchers + Payment
        self.addPointsAPI()
        storesRedemption.directlogin("Foreign Denomination", "Partialvoucher")
        self.addPointsAPI()
        storesRedemption.directlogin("Multiple Foreign Denomination", "Partialvoucher")



    def addPointsAPI(self):
        result_code = request('POST',
                              'http://129.213.96.7:8087/v2/points/addPoints?auth_company_id=43&auth_entity_id=10004300000000210&auth_access_role_id=1',
                              data={"sent_point_type": "AP", "point_type": "RP", "sent_by": "10004300000000210",
                                    "received_by": "10004300000000210", "points": 50, "budget_id": 106})
        result_json = result_code.json()
        print(result_json)