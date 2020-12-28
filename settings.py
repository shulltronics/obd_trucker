from elm327 import Elm327

gPROG_NAME = "OBD Console"
gVERSION = "0.1"
gCURSES_CH_TIMEOUT = 50
gMENU_PADDING = 3
# the main instance of comms with the truck
elm = Elm327()

# key bindings for UI
key_options = {'s' : 'Display this legend'  ,
               'q' : 'Quit'                 ,
               'c' : 'Clear Screen'         ,
               'v' : 'Read Battery Voltage' ,
               'r' : 'Reset ELM327'         ,
               'h' : 'Set OBD Header'       ,
               'l' : 'Display List View'
              }
