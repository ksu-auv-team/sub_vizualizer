"""
Sub Vizualizer GUI using PySimpleGUI

"""

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


topics = rospy.get_published_topics()

#Separate topics and msg types into their own lists
msgTypes = list(list(zip(*topics))[1])
topics = list(list(zip(*topics))[0])

for i in range(len(topics)):
    topics[i] = topics[i].replace('/', '')



topicBoxes = []
topicText = []
gblCommands = []

#TODO: Dynamically subscribe to n rostopics and get messages. For now, just set each to 0
for i in topics:
    gblCommands.append('global {}; {} = str(1)'.format(i,i))
    
topics.extend(gblVars)

for i in gblVars:
    gblCommands.append('global {}; {} = gbl.{}'.format(i,i,i))

#Create objects for PySimpleGUi
for i in topics:
    topicBoxes.append([sg.Checkbox('{}'.format(i), enable_events=True, default=False)])
    topicText.append([sg.Text('{}:'.format(i), visible=False, key='{}'.format(i))])

layout = [                 
    [sg.Frame(layout=[      
    *topicBoxes,
    ], title='Select topics to listen to:',title_color='red', relief=sg.RELIEF_SUNKEN, tooltip='Use these to set flags')],
        *topicText,
    [sg.Exit()]
]

window = sg.Window('Sub_Viz', layout)

#GUI Event Loop
while True:
    event, values = window.read() 
    print(event)
    import gbl
    updateGbl()
    
    if type(event) == int:
        if values[event] == True:
            try:
                window[topics[event]].Update('{}: {}'.format(topics[event], eval(topics[event])), visible=True)
            except:
                window[topics[event]].Update('{}: ERROR'.format(topics[event]))
        if values[event] == False:
            window.FindElement(topics[event]).Update(visible=False)
    
    if event in (None, 'Exit'):      
        break      

window.close()




