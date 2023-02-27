import requests
import matplotlib.pyplot as plt
import datetime
from collections import OrderedDict

url = 'https://raw.githubusercontent.com/joincounter/code-test-python/master/event_data.csv'
get = requests.get(url)
text = get.text
print(text.find(')'))
textLines = text.split('\n')
textLinesWithState = ''
dictionarState = {}
x_axis = []
y_axis = []

for i, line in enumerate(textLines):
    if i > 0:
        point = line.split(',')[7]
        point = point[point.find('(')+1:point.find(')')]
        lon, lat = point.split()
        response = requests.get(f'https://us-state-api.herokuapp.com/?lat={lat}&lon={lon}').json()
        response = response['state']['name']
        if response in dictionarState.keys():
            dictionarState[response] += 1
        else:
            dictionarState[response] = 1
        line = line.replace('\r', ',' + response + '\r')
    textLinesWithState += line

dictionarState = sorted(dictionarState.items(), key=lambda x: x[1], reverse=True)
for entry in dictionarState:
    x_axis.append(entry[0])
    y_axis.append(entry[1])

plt.bar(x_axis, y_axis)
plt.title('Event Frequency by State Chart')
plt.xlabel('State')
plt.ylabel('No. of Events')
plt.show()

dateDict = {}

for i, line in enumerate(textLines):
    if i > 0:
        myDateTime = (line.split(',')[1]).split()[0][5:]
        if myDateTime in dateDict.keys():
            dateDict[myDateTime] += 1
        else:
            dateDict[myDateTime] = 1

x_axis, y_axis = [], []
eventFrequencyList = sorted(dateDict.items())
for event in eventFrequencyList:
    x_axis.append(event[0])
    y_axis.append(event[1])

plt.bar(x_axis, y_axis, align='edge', width=0.3)
plt.ylabel('No. of Events')
plt.xlabel('Month and Day')
plt.xticks(rotation=30)
plt.show()




