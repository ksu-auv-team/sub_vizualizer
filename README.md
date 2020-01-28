# sub_vizualizer
GUI that displays sub status!

Uses PySimpleGUI. 
To install:

<code>
pip install pysimplegui
</code>

or

<code>
pip3 install pysimplegui
  
</code>

This script accesses gbl.py to get variables. Currently, where this will live in the greater folder structure is TBD. It currenlty expects to be in a folder under the sub_utilities root. You can place it anywhere else if you want, but you must edit  the sys.path command at the top of viz.py to the location of gbl.py.

Broken:

~~-Value of a variable doesn't print in GUI~~

TODO:

-Create ROS subscriber and callback that dynamically subs to n topics. Currently using dummy values

-Create whitelist that ignores gbl variables that we'll never care about

-Verify script's ability to get accurate gbl values. gbl.py variables likely aren't accessible by GUI unless gbl.py and GUI are   launched by the same console or something. Currently using dummy values

~-GUI values output should be to the right of the checkboxes~

~-GUI checkboxes should have a scrollbar~
