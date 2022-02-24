import pytest
import requests
import json
from utils import excelUtils
from utils.helpers import helperFunctions
from utils.customLogger import logGeneration

class Test_dynamicAPI():
    tdFilePath = ".//testData/DynamicAPITestData.xlsx"
    logger = logGeneration.logGenerate()

    def test_DynamicAPI(self):
        self.exeDetails = helperFunctions()
        executionDetails = self.exeDetails.getExecutionDetails(self.tdFilePath)
        envVariables = self.exeDetails.getEnvVariables(self.tdFilePath)

        for i, j in executionDetails.items():
            tcIDtoExe = i
            testType = j

        rows = excelUtils.getRowCount(self.tdFilePath, testType)

        # Get API Details to execute
        for k in range(2, rows+1):
            tcIDtoExeDtls = excelUtils.readData(self.tdFilePath,testType, k, 1)
            tcAPIURL = excelUtils.readData(self.tdFilePath,testType, k, 3)
            tcAPIMethod = excelUtils.readData(self.tdFilePath, testType, k, 4)
            tcAPIHeaders = excelUtils.readData(self.tdFilePath, testType, k, 5)

            if excelUtils.readData(self.tdFilePath, testType, k, 6) != None:
                tcAPIReqBody = excelUtils.readData(self.tdFilePath, testType, k, 6)
            else:
                tcAPIReqBody = "NoVal"

            tcAPIERBV = excelUtils.readData(self.tdFilePath, testType, k, 7)

            if excelUtils.readData(self.tdFilePath, testType, k, 8) != None:
                tcAPIParamToPass = excelUtils.readData(self.tdFilePath, testType, k, 8)
            else:
                tcAPIParamToPass = "NoVal"

            if tcIDtoExe == tcIDtoExeDtls:
                APITestCaseID = tcIDtoExeDtls + "--" + str(k - 1)
                paramsToPass = "NoVal"
                testStatus = "Not Started"
                APIResponseCode = "NoVal"
                APIResponseBody = "NoVal"

                if k == 2:
                    tcAPIDetails = {APITestCaseID : {'API_URL' : tcAPIURL, 'API_Method' : tcAPIMethod, 'API_Headers' : "{" + tcAPIHeaders + "}", 'API_RequestBody' : tcAPIReqBody, 'API_ExpectedResponseBody' : tcAPIERBV, 'API_ParamsToPassKey' : tcAPIParamToPass, 'API_ParamsValToPass' : paramsToPass, 'API_RespStatusCode' : APIResponseCode, 'API_RespBody' : APIResponseBody, 'API_TestResult' : testStatus}}
                else:
                    tcAPIDetails.update({APITestCaseID : {'API_URL' : tcAPIURL, 'API_Method' : tcAPIMethod, 'API_Headers' : "{" + tcAPIHeaders + "}", 'API_RequestBody' : tcAPIReqBody, 'API_ExpectedResponseBody' : tcAPIERBV, 'API_ParamsToPassKey' : tcAPIParamToPass, 'API_ParamsValToPass' : paramsToPass, 'API_RespStatusCode' : APIResponseCode, 'API_RespBody' : APIResponseBody, 'API_TestResult' : testStatus}})

                for tc_id, tc_details in tcAPIDetails.items():
                    for api_keys, api_details in tc_details.items():

                        for envVars_keys, envVars_Val in envVariables.items():
                            if envVars_keys in api_details:
                                tc_details[api_keys] = ((api_details.replace(envVars_keys, envVars_Val)).replace("[","")).replace("]","")
                            else:
                                break

                        if k != 2:
                            paramsKeyToCheck = tcAPIDetails['Test_Uploan_Brwr_API_002--' + str(k-2)]['API_ParamsToPassKey']
                            paramsValToCheck = tcAPIDetails['Test_Uploan_Brwr_API_002--' + str(k-2)]['API_ParamsValToPass']
                            if paramsKeyToCheck != 'NoVal' and paramsValToCheck != 'NoVal':
                                newParamsKeyToCheck = "[" + str(paramsKeyToCheck) + "]"
                                if newParamsKeyToCheck in api_details:
                                    tc_details[api_keys] = api_details.replace(newParamsKeyToCheck, paramsValToCheck)

                # Trigger API Call
                if (tc_details.get('API_Method').strip()).upper() == "GET":
                     response = requests.get(tc_details.get('API_URL'),headers=json.loads(tc_details.get('API_Headers')),data=tc_details.get('API_RequestBody'))
                if (tc_details.get('API_Method').strip()).upper() == "POST":
                     response = requests.post(tc_details.get('API_URL'),headers=json.loads(tc_details.get('API_Headers')),data=tc_details.get('API_RequestBody'))
                if (tc_details.get('API_Method').strip()).upper() == "PUT":
                     response = requests.put(tc_details.get('API_URL'),headers=json.loads(tc_details.get('API_Headers')),data=tc_details.get('API_RequestBody'))

                # Verify Response
                if response.status_code != 200:
                     #print("Test Case ID : " + tc_id + " FAILED - Response Status Code : " + str(response.status_code) + " Response Content : " + str(response.content))
                     tcAPIDetails[APITestCaseID]['API_RespStatusCode'] = str(response.status_code)
                     tcAPIDetails[APITestCaseID]['API_RespBody'] = response.text
                     self.logger.info("FAILED - Response Status Code : " + str(response.status_code) + " Response Content : " + str(response.content))
                     pytest.fail()
                else:
                    #print("Test Case ID : " + tc_id + " PASSED - Response Status Code : " + str(response.status_code) + " Response Content : " + str(response.content))
                    tcAPIDetails[APITestCaseID]['API_RespStatusCode'] = str(response.status_code)
                    if "," in tc_details['API_ExpectedResponseBody'] or "->" in tc_details['API_ExpectedResponseBody']:
                        tcValToVerify = tc_details['API_ExpectedResponseBody'].split(",")
                        # print(response.text)

                        tcAPIDetails[APITestCaseID]['API_RespBody'] = response.text
                        verifyResp = json.loads(response.text)

                        for n in range(len(tcValToVerify)):
                            if tcValToVerify[n] != "":
                                if "->" in tcValToVerify[n]:
                                    getExpecVal = (tcValToVerify[n]).split("->")
                                    keytoVerify = str(getExpecVal[0]).strip()
                                    expectVal = getExpecVal[1].strip()
                                else:
                                    keytoVerify = str(tcValToVerify[n]).strip()
                                    expectVal = ""

                                respDictItems = response.text.split(keytoVerify)

                                # Verify the Response Body Expected Value
                                if respDictItems != "":
                                    if expectVal != "":
                                        if expectVal.isdigit() == True:
                                            getKeyValResp = keytoVerify + "': " + expectVal + ","
                                        else:
                                            getKeyValResp = keytoVerify + "': '" + expectVal + "'"

                                        if getKeyValResp in str(verifyResp):
                                            print(APITestCaseID + " -- PASSED - Response Body Value of Key : " + keytoVerify + " was " + expectVal)
                                            tcAPIDetails[APITestCaseID]['API_TestResult'] = "Passed"
                                        else:
                                            print(APITestCaseID + " -- FAILED - Key Value : " + expectVal + " doesn't match with value in the Response Body.")
                                            tcAPIDetails[APITestCaseID]['API_TestResult'] = "Failed"
                                    else:
                                        print(APITestCaseID + " -- PASSED - Response Body Key : " + keytoVerify + " was found.")
                                else:
                                    pytest.fail("Actual Key and Value in Response Body does not match with Expected.")

                    if tc_details.get('API_ParamsToPassKey') in str(verifyResp):
                        paramToPassKey = tc_details.get('API_ParamsToPassKey')
                        getParamToPass = response.text.split(paramToPassKey)
                        getParamtoPassVal = getParamToPass[1].split(",")
                        tcAPIDetails[APITestCaseID]['API_ParamsValToPass'] = (getParamtoPassVal[0].replace('"', "")).replace(":", "")

                    # print(tcAPIDetails)