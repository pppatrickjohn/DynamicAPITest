from utils import excelUtils

class helperFunctions():

    def getExecutionDetails(self,filepath):
        rows = excelUtils.getRowCount(str(filepath), 'Test_Case_Execution_Summary')
        testToExecute = {}
        for i in range(2, rows+1):
            testCaseID = excelUtils.readData(str(filepath), 'Test_Case_Execution_Summary', i, 1)
            testCaseType = excelUtils.readData(str(filepath), 'Test_Case_Execution_Summary', i, 2)
            executeTestCase = excelUtils.readData(str(filepath), 'Test_Case_Execution_Summary', i, 5)
            if executeTestCase == "YES":
                testToExecute[testCaseID] = str(testCaseType)
        return testToExecute

    def getEnvVariables(self,filepath):
        rows = excelUtils.getRowCount(str(filepath), 'Env_Var')
        envVars = {}
        for j in range(2, rows+1):
            varName = excelUtils.readData(str(filepath), 'Env_Var', j, 1)
            varValue = excelUtils.readData(str(filepath),'Env_Var', j, 2)
            envVars[varName] = varValue
            break
        return envVars