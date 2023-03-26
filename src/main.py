"""
Touch Portal Plugin Example
"""

# Load the TP Python API. Note that TouchPortalAPI must be installed (eg. with pip)
# _or_ be in a folder directly below this plugin file.
import TouchPortalAPI
from TouchPortalAPI import TYPES
from TouchPortalAPI.logger import Logger

# Importing our python entry struct so we can get infomations of the plugin without copy and paste
# So you can change a action id and it will update here.
import TPPEntry

# Importing other required modules
import os
from threading import Thread
from sys import exit
import configparser



class ClientInterface(TouchPortalAPI.Client):
    def __init__(self):
        super().__init__(self)
        
        self.pluginId = TPPEntry.PLUGIN_ID
        self.configFile = self.ParseConfig("plugin_config.ini")
        
        # TP connection settings - These can be left at default
        self.TPHOST = self.configFile["TP CONFIG"]["tphost"]
        self.TPPORT = int(self.configFile["TP CONFIG"]["tpport"])
        
        self.RCV_BUFFER_SZ = int(self.configFile["TP CONFIG"]["rcv_buffer_sz"]) # Incoming data buffer size
        self.SND_BUFFER_SZ = int(self.configFile["TP CONFIG"]["snd_buffer_sz"]) # maximum size of send data buffer ( 1MB )
        
        # Log settings
        self.logLevel = self.configFile["LOGGING"]["loglevel"]
        self.setLogFile(self.configFile["LOGGING"]["logname"])
        
        # Register events
        self.add_listener(TYPES.onConnect, self.onConnect)
        self.add_listener(TYPES.onAction, self.onAction)
        self.add_listener(TYPES.onShutdown, self.onShutdown)
        self.add_listener(TYPES.onListChange, self.onListChange)
        
        # State updater thread
        self.stateUpdaterThread = Thread(target=self.stateUpdate)
        
        # Global Class Variable
        self.variableTest1 = 0
        
    
    """
    Custom Method/Functions
    """
    def settingsToDict(self, settings):
        # Converts from [{"setting1": "value"}, {"setting1": "value"}] to {"Setting1": "value", "Setting2": "value"}
        return { list(settings[i])[0] : list(settings[i].values())[0] for i in range(len(settings)) }
    
    def ParseConfig(self, file):
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), file))
        return {s:dict(config.items(s)) for s in config.sections()}


    """
    StateThread
    """
    def stateUpdate(self):
        while (self.isConnected()):
            pass # update stuff


    """
    Events
    """
    def onConnect(self, data):
        self.log.info(f"Connected to TP v{data.get('tpVersionString', '?')}, plugin v{data.get('pluginVersion', '?')}.")
        self.log.info(self.settingsToDict(data["settings"]))
        self.log.debug(f"Connection: {data}")
        print(self.ParseConfig("config.ini"))
        self.stateUpdaterThread.start() # as soon as it connects state update thread 


    def onSettings(self, data):
        self.log.debug(f"Connection: {data}")


    def onAction(self, data):
        self.log.debug(f"Connection: {data}")
        g_log.debug(f"Action: {data}")
        # check that `data` and `actionId` members exist and save them for later use
        if not (action_data := data.get('data')) or not (aid := data.get('actionId')):
            return
        if aid == TPPEntry.TP_PLUGIN_ACTIONS['example']['id']:
            # set our example State text and color values with the data from this action
            text = plugin.getActionDataValue(action_data, TPPEntry.TP_PLUGIN_ACTIONS['example']['data']['text'])
            color = plugin.getActionDataValue(action_data, TPPEntry.TP_PLUGIN_ACTIONS['example']['data']['color'])
            plugin.stateUpdate(TPPEntry.TP_PLUGIN_STATES['text']['id'], text)
            plugin.stateUpdate(TPPEntry.TP_PLUGIN_STATES['color']['id'], color)
        else:
            g_log.warning("Got unknown action ID: " + aid)


    ## When a Choice List is Changed in a Button Action
    def onListChange(self, data):
        self.log.debug(f"Connection: {data}")


    def onShutdown(self, data):
        self.log.info('Received shutdown event from TP Client.')
        if (self.stateUpdaterThread.is_alive):
            self.stateUpdaterThread.join(0)
        self.disconnect()
        


    def onError(self, data):
        self.error(f'Error in TP Client event handler: {repr(data)}')



# Crate the (optional) global logger, an instance of `TouchPortalAPI::Logger` helper class.
# Logging configuration is set up in main().
g_log = Logger(name = TPPEntry.PLUGIN_ID)


plugin = ClientInterface()
ret = 0
try:
    plugin.connect()
except KeyboardInterrupt:
    plugin.log.warning("Caught keyboard interrupt, exiting.")
except Exception:
    from traceback import format_exc
    plugin.log.error(f"Exception in TP Client:\n{format_exc()}")
    ret = -1
finally:
    plugin.disconnect()
    del plugin
    exit(ret)

