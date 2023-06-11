class PID:
    def __init__(self, measuredValue, desiredTemperature):
        self.measuredValue = measuredValue
        self.goal = desiredTemperature
        self.errorArray = [self.measuredValue - self.goal]
        self.lengthErrorArray = 1

    def setProportional(self, value):
        self.P = value

    def setIntegral(self, value):
        self.I = value

    def setDerivative(self, value):
        self.D = value
        
    def update(self, newMeasure):
        if self.lengthErrorArray > 10:
            self.errorArray.pop(0)

        self.errorArray.append(newMeasure - self.goal)
        self.lengthErrorArray += 1
        self.measuredValue = newMeasure

        P = self.P * self.errorArray[-1]
        I = self.I * sum(self.errorArray)
        D = self.D * (self.errorArray[-1] - self.errorArray[-2])

        self.overviewParameters = "\nP -> "+ str(P) + "\nI -> "+ str(I) + "\nD -> "+ str(D)
        output = P + I + D
        return output
    
    
    