import numpy as np

class MockApi:
    def __init__(self, successRate):
        self.successRate = successRate #Stores the probability that the API call is successful

    # ---- successRate ----
    @property
    def successRate(self):
        return self.__successRate

    #Checks that `successRate` is a valid probability
    @successRate.setter
    def successRate(self, newSuccessRate):
        if not isinstance(newSuccessRate, (int, float)):
            raise TypeError("successRate must be a number between 0 and 1")

        if not 0 <= newSuccessRate <= 1:
            raise ValueError("successRate must be between 0 and 1")

        self.__successRate = newSuccessRate

    #API call function
        #Return 0 ~ API call failed
        #Return 1 ~ API call successful
    def call(self):
        return np.random.choice([0, 1],p = [1 - self.__successRate, self.__successRate])