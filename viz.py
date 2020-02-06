#!/usr/bin/env python3
# Sub Vizualizer GUI using PySimpleGUI

import PySimpleGUI as sg      
import rospy
import sys

#Adjust this line to match the location of your gbl.py
sys.path.append('../subdriver/StateMachine')


def main():
    import gbl
    
    #Get all variables in gbl, remove the ones we don't care about
    gbl_vars = dir(gbl)
    gbl_vars = [gbl_vars for gbl_vars in gbl_vars if not gbl_vars.startswith('__')]
    
    #Colelct active topics from ROS
    topics = rospy.get_published_topics()
    
    #Separate topics and msg types into their own lists.
    #TODO: get real data from ROS, create a big ol switch to handle many msg formats
    msg_Types = list(list(zip(*topics))[1])
    topics = list(list(zip(*topics))[0])
    
    #Remove backslash in rostopic names. It breaks stuff
    for i in range(len(topics)):
        topics[i] = topics[i].replace('/', '')
    
    topic_boxes = []
    topic_text = []
    gbl_commands = []
    
    #TODO: Dynamically subscribe to n rostopics and get messages.
    for i in topics:
        gbl_commands.append('global {}; {} = "TODO" '.format(i,i))
    
    topics.extend(gbl_vars)
    
    for i in gbl_vars:
        gbl_commands.append('global {}; {} = gbl.{}'.format(i,i,i))
    
    #Create GUI objects based on the topics that were collected
    for i in topics:
        topic_boxes.append([sg.Checkbox('{}'.format(i), enable_events=True, default=False)])
        topic_text.append(sg.Text('', visible=False, size=(30,1), key='{}'.format(i)))
    
    layout = [
        [sg.Column(layout=[      
            *topic_boxes
            ], scrollable=True, vertical_scroll_only=True),
            *topic_text],
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
        for i in gbl_commands:
            exec(i)
    
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
    


if __name__ == '__main__':
    main()



