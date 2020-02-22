from testCases.storesTestcases import LoginTest

class testSriptExecution():

    def StoresTestExecution(self):
        test = LoginTest()
        test.setUp()
        test.stores()
        test.tearDownDriver()
