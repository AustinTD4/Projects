##################################################
#    A Simple Tool for Tracking Compute Times    #
#    By Austin Dickerson                         #
##################################################

import time
import pickle

class timer:

    def __init__(self):
        self.netTime = 0
        self.windows = 0
        
    def start(self):
        self.startTime = time.monotonic_ns()

    def stop(self):
        self.netTime += time.monotonic_ns() - self.startTime
        self.windows += 1

class clockManager:

    def __init__(self, fileName):
        self.fileName = fileName
        self.start = time.monotonic_ns()
        self.timers = {}

    def makeTimer(self, name):
        self.timers[name] = timer()
        return self.timers[name]

    def tallyCompare(self):
        duration = time.monotonic_ns() - self.start
        timeTotals = []
        timerNames = []

        for clock in self.timers.keys():
            timerNames.append(clock)
            timeTotals.append(self.timers[f'{clock}'].netTime)
            print(f'{clock} used a total of {timeTotals[-1]} nanoseconds, {round(timeTotals[-1]/self.timers[f"{clock}"].windows,3)} per window')

        netFractions = []
        relativeFractions = []
        for i in range(len(timeTotals)):
            netFraction = timeTotals[i]/duration
            relativeFraction = timeTotals[i]/sum(timeTotals)
            netFractions.append(netFraction)
            relativeFractions.append(relativeFraction)
            print(f'{timerNames[i]} took {round(netFraction,3)} of total time and {round(relativeFraction,3)} of timed processes')

        results = {}
        results['Timer Names'] = timerNames
        results['Time Totals'] = timeTotals
        results['Net Fractions'] = netFractions
        results['Relative Fractions'] = relativeFractions

        with open(f'{self.fileName}_Timers.pkl', 'wb') as file:
            pickle.dump(results, file, protocol=pickle.HIGHEST_PROTOCOL)

