# Sub Vizualizer GUI using PySimpleGUI

import PySimpleGUI as sg      
import rospy
import sys

#Adjust this line to match the location of your gbl.py
sys.path.append('../sub-utilities/submodules/subdriver/StateMachine')

import gbl

def updateGbl():
    for i in gblCommands:
        exec(i)    
        
#Get all variables in gbl, remove the ones we don't care about
gblVars = dir(gbl)
gblVars = [gblVars for gblVars in gblVars if not gblVars.startswith('__')]

#Colelct active topics from ROS
topics = rospy.get_published_topics()

#Separate topics and msg types into their own lists
msgTypes = list(list(zip(*topics))[1])
topics = list(list(zip(*topics))[0])

#Remove backslash in rostopic names. It breaks stuff
for i in range(len(topics)):
    topics[i] = topics[i].replace('/', '')

topicBoxes = []
topicText = []
gblCommands = []

#TODO: Dynamically subscribe to n rostopics and get messages.
for i in topics:
    gblCommands.append('global {}; {} = "TODO" '.format(i,i))

topics.extend(gblVars)

for i in gblVars:
    gblCommands.append('global {}; {} = gbl.{}'.format(i,i,i))

#Create GUI objects based on the topics that were collected
for i in topics:
    topicBoxes.append([sg.Checkbox('{}'.format(i), enable_events=True, default=False)])
    topicText.append(sg.Text('', visible=False, size=(30,1), key='{}'.format(i)))

layout = [
    [sg.Frame(layout=[      
        *topicBoxes
        ], title='Select topics to listen to:', relief=sg.RELIEF_SUNKEN),
        *topicText],
    [sg.Exit()]
]

#Displays the Window
window = sg.Window('Sub_Viz', layout)

#GUI Event Loop
#Loop occurrs every time a window.read() happens (either a button is pressed or timeout)
while True:
    #timeout=250 -> ms until window updates. Increase to make GUI 
    #readout more responsive at the cost of CPU time, and vise versa
    event, values = window.read(timeout=250, timeout_key='Timeout') 
    
    #Importing gbl again updates its values? Need to verify...
    import gbl
    updateGbl()

    if event == 'Timeout':
        for i in range(len(values)):
            if values[i] == True:
                try:
                    window[topics[i]].update('{}: {}'.format(topics[i], eval(topics[i])),visible=True)
                except:
                    window[topics[i]].update('{}: ERROR'.format(topics[i]))
            else:
                window[topics[i]].update(visible=False)
    if event in (None, 'Exit'):
        break
window.close()




