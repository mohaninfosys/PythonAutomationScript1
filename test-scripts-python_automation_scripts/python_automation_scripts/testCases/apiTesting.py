from requests import request

import config
from commonMethods.commonUtils import commonUtils
import time
from commonMethods.jsonLoader import jsonLoader
import requests
import json

configObj = commonUtils().configObj

class apitesting:

    config_file = config.config_path
    configObj = jsonLoader.json_read(config_file)

    def getstatus(self):
        result_code = request('POST','http://129.213.96.7:8087/v2/points/addPoints?auth_company_id=43&auth_entity_id=10004300000000210&auth_access_role_id=1', data={"sent_point_type": "AP","point_type":"RP","sent_by":"10004300000000210","received_by":"10004300000000210","points":100,"budget_id":106})
        result_json = result_code.json()
        print(result_json)

    def addBudget(self):
        url = configObj["budgetAPI"]["url"]
        paramater = {"budgetname": configObj["budgetAPI"]["budgetname"],"description": configObj["budgetAPI"]["description"],
                     "is_company_budget": configObj["budgetAPI"]["is_company_budget"],
                     "budget_creator_id": configObj["budgetAPI"]["budget_creator_id"]}
        result = commonUtils.postapi(paramater,url)
        if result == "Pass":
            print("test")

    def addPoints(self):
        url = configObj["addPointsCP"]["url"]
        parameter = {"sent_point_type": configObj["addPointsCP"]["sent_point_type"],
                     "point_type": configObj["addPointsCP"]["point_type"],
                     "sent_by": configObj["addPointsCP"]["sent_by"],
                     "budget_creator_id": configObj["addPointsCP"]["received_by"], "points": configObj["addPointsCP"]["points"]}
        result = commonUtils.postapi(parameter, url)
        print(result)

    def addPointsCPAP(self):
        url = configObj["addPointsCPAP"]["url"]
        paramater = {"sent_point_type": configObj["addPointsCPAP"]["sent_point_type"],
                 "point_type": configObj["addPointsCPAP"]["point_type"],
                 "sent_by": configObj["addPointsCPAP"]["sent_by"],
                 "budget_creator_id": configObj["addPointsCPAP"]["received_by"],
                 "points": configObj["addPointsCPAP"]["points"]}
        result = commonUtils.postapi(paramater, url)
        print(result)

    def addPointsRP(self):
        url = configObj["addPointsRP"]["url"]
        paramater = {"sent_point_type": configObj["addPointsRP"]["sent_point_type"],
                 "point_type": configObj["addPointsRP"]["point_type"],
                 "sent_by": configObj["addPointsRP"]["sent_by"],
                 "budget_creator_id": configObj["addPointsRP"]["received_by"],
                 "points": configObj["addPointsRP"]["points"], "budget_id": configObj["addPointsRP"]["budget_id"]}
        result = commonUtils.postapi(paramater, url)
        print(result)



