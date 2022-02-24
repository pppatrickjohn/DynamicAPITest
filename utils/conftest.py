import pytest

@pytest.fixture()
def dataPath():
    dataRepoPath = ".//testData/DynamicAPITestData.xlsx"
    return dataRepoPath