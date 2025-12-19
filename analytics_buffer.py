from datetime import datetime
from mock_api import MockApi

class AnalyticsBuffer:
    def __init__(self, bufferLimit, timerLimit, api, failureLimit):
        self.buffer = [] #Stores events until they are flushed (removed from the list)
        self.lastCall = datetime.now() #Stores the time of the last successful API call
        self.failureCount = 0 #Stores the number of consecutive unsuccessful API calls

        self.bufferLimit = bufferLimit #Stores the lower limit for the buffer length before events are flushed
        self.timerLimit = timerLimit #Stores how frequently the timer "goes off" and events are subsequently flushed
        self.api = api
        self.failureLimit = failureLimit #Stores the number of consecutive API calls which raises an error

    # ---- bufferLimit ----
    @property
    def bufferLimit(self):
        return self.__bufferLimit

    #Checks that 'bufferLimit' is a positive integer
    @bufferLimit.setter
    def bufferLimit(self, newBufferLimit):
        if not isinstance(newBufferLimit, int):
            raise TypeError("bufferLimit must be an integer")

        if newBufferLimit <= 0:
            raise ValueError("bufferLimit must be a positive integer")

        self.__bufferLimit = newBufferLimit

    # ---- timerLimit ----
    @property
    def timerLimit(self):
        return self.__timerLimit

    #Checks that 'timerLimit' is a positive integer
    @timerLimit.setter
    def timerLimit(self, newTimerLimit):
        if not isinstance(newTimerLimit, int):
            raise TypeError("timerLimit must be an integer")

        if newTimerLimit <= 0:
            raise ValueError("timerLimit must be a positive integer")

        self.__timerLimit = newTimerLimit

    # ---- api ----
    @property
    def api(self):
        return self.__api

    #Checks that `api` is a MockApi object
    @api.setter
    def api(self, newApi):
        if not isinstance(newApi, MockApi):
            raise TypeError("api must be a MockApi object")

        self.__api = newApi

    # ---- failureLimit ----
    @property
    def failureLimit(self):
        return self.__failureLimit

    #checks that 'failureLimit' is a positive integer
    @failureLimit.setter
    def failureLimit(self, newFailureLimit):
        if not isinstance(newFailureLimit, int):
            raise TypeError("failureLimit must be an integer")

        if newFailureLimit <= 0:
            raise ValueError("failureLimit must be a positive integer")

        self.__failureLimit = newFailureLimit

    #If track() or track(None) is called, no event is added to the buffer but the value of timer is checked (potential flush)
    def track(self, event = None):
        if not event is None:
            self.buffer.append(event)

        #Calculate the time since the last successful API call (in seconds)
        time_elapsed = (datetime.now() - self.lastCall).total_seconds()

        #Check for flush conditions
        if len(self.buffer) >= self.bufferLimit or time_elapsed >= self.timerLimit:
            self.flush()

        #If number of unsuccessful API calls exceeds the limit, raise an error
        if self.failureCount >= self.failureLimit:
            raise RuntimeError("API is down")

    def flush(self):
        #Avoid unecessary flushes
        if len(self.buffer) > 0:
            #Successful API call
            if self.api.call():
                #Remove all events from buffer
                self.buffer.clear()
                #Update time stored in 'lastCall'/re-set the timer
                self.lastCall = datetime.now()
                #Re-set value of 'failureCount' to 0
                self.failureCount = 0
            #Unsuccessful API call
            else:
                print("API call failed")
                self.failureCount += 1
