from decimal import Decimal
import datetime
from datetime import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as md

class StateResult:
    name: str
    timeStamp: datetime.datetime
    stateDifference: float

    def __init__(self, n, ts, sd):
        self.name = n
        self.timeStamp = ts
        self.stateDifference = sd

stateNames = ['state.q1', 'state.q2', 'state.q3', 'state.q4', 'state.q5', 'state.q6']
targetNames = ['target.q1', 'target.q2', 'target.q3', 'target.q4', 'target.q5', 'target.q6']
jointsResults = {
    'A1': [],
    'A2': [],
    'A3': [],
    'A4': [],
    'A5': [],
    'A6': []
}

# Holds the difference and the timestamp at which it happens for each joint
greatestDiffs = {
    'A1': [0, None],
    'A2': [0, None],
    'A3': [0, None],
    'A4': [0, None],
    'A5': [0, None],
    'A6': [0, None]
}
def sanitizeResultItem(item: str):
    return item.split('=', 1)[1].strip()

def calculateDiff(state: str, target: str):
    return float(Decimal(state) - Decimal(target))
    
def ingestData():
    lines = open('kuka_robot.log', 'r').read().splitlines()
    for line in lines:
        # Check if line contains relevant info
        if (stateNames[0] in line and targetNames[0] in line):
            lineItems = line.split(';')
            timeStamp = lineItems[0]
            # Array of joint states at time
            stateResults = lineItems[6:12]
            # Array of targets for those states at time
            targetResults = lineItems[12:18]
            # Sanitize input states and targets
            for i, result in enumerate(stateResults):
                stateResults[i] = sanitizeResultItem(result)
            for i, result in enumerate(targetResults):
                targetResults[i] = sanitizeResultItem(result)
            # Store the time stamp and differences into jointResults dict
            for i, (key, value) in enumerate(jointsResults.items()):
                stateDiff = calculateDiff(stateResults[i], targetResults[i])
                jointsResults[key].append(StateResult(key, timeStamp, stateDiff))
                # Check if the state/target difference is the biggest so far, store if so
                if (abs(stateDiff) > abs(greatestDiffs[key][0])):
                    greatestDiffs[key] = [stateDiff, timeStamp]
    print(greatestDiffs)

def plotData():
    for i, (key, results) in enumerate(jointsResults.items()):
        plt.figure(i)
        ax = plt.axes()
        ax.xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
        plt.title('Joint ' + key)
        plt.xlabel('Time')
        plt.ylabel('Difference (State - Target)')
        xRange = []
        yRange = []
        for result in results:
            xRange.append(result.timeStamp)
            yRange.append(result.stateDifference)
        xRange = md.datestr2num(xRange)
        plt.plot_date(xRange, yRange, markersize=1)
        plt.annotate(
            'Max Difference ({0})'.format(greatestDiffs[key][0]), xy=(md.datestr2num(greatestDiffs[key][1], dt.strptime('2020-01-31',"%Y-%m-%d")), greatestDiffs[key][0]),
            xytext=(8 if greatestDiffs[key][0] > 0 else -15, 8 if greatestDiffs[key][0] > 0 else -15),
            textcoords=('offset points'),
            fontsize='8',
            arrowprops=dict(arrowstyle='->')
        )
    plt.show()


if __name__ == "__main__":
    ingestData()
    plotData()