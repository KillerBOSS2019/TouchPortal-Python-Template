# Version string of this plugin (in Python style).
__version__ = "1.0"

# The unique plugin ID string is used in multiple places.
# It also forms the base for all other ID strings (for states, actions, etc).
PLUGIN_ID = "tp.plugin.example.python"

# Basic plugin metadata
TP_PLUGIN_INFO = {
    "sdk": 6,
    "version": int(float(__version__) * 100),  # TP only recognizes integer version numbers
    "name": "Touch Portal Plugin Example",
    "id": PLUGIN_ID,
    # Startup command, with default logging options read from configuration file (see main() for details)
    "plugin_start_cmd": "%TP_PLUGIN_FOLDER%TPExamplePlugin\\pluginexample.exe @plugin_config.txt",
    "configuration": {
        "colorDark": "#25274c",
        "colorLight": "#707ab5"
    },
    "doc": {
        "repository": "KillerBOSS2019:TouchPortal-API",
        "Install": "example install instruction",
        "description": "example description"
    }
}

# Setting(s) for this plugin. These could be either for users to
# set, or to persist data between plugin runs (as read-only settings).
TP_PLUGIN_SETTINGS = {
    "example": {
        "name": "Example Setting",
        # "text" is the default type and could be omitted here
        "type": "text",
        "default": "Example value",
        "readOnly": False,  # this is also the default
        "doc": "example doc for example setting",
        "value": None  # we can optionally use the settings struct to hold the current value
    },
}

# This example only uses one Category for actions/etc., but multiple categories are supported also.
TP_PLUGIN_CATEGORIES = {
    "main": {
        "id": PLUGIN_ID + ".main",
        "name" : "Python Examples",
        # "imagepath" : "icon-24.png"
    }
}

# Action(s) which this plugin supports.
TP_PLUGIN_ACTIONS = {
    "example": {
        # "category" is optional, if omitted then this action will be added to all, or the only, category(ies)
        "category": "main",
        "id": PLUGIN_ID + ".act.example",
        "name": "Set Example Action",
        "prefix": TP_PLUGIN_CATEGORIES["main"]["name"],
        "type": "communicate",
        "tryInline": True,
        "doc": "Example doc for this action in readme",
        # "format" tokens like $[1] will be replaced in the generated JSON with the corresponding data id wrapped with "{$...$}".
        # Numeric token values correspond to the order in which the data items are listed here, while text tokens correspond
        # to the last part of a dotted data ID (the part after the last period; letters, numbers, and underscore allowed).
        "format": "Set Example State Text to $[text] and Color to $[2]",
        "data": {
            "text": {
                "id": PLUGIN_ID + ".act.example.data.text",
                # "text" is the default type and could be omitted here
                "type": "text",
                "label": "Text",
                "default": "Hello World!"
            },
            "color": {
                "id": PLUGIN_ID + ".act.example.data.color",
                "type": "color",
                "label": "Color",
                "default": "#818181FF"
            },
        }
    },
}

TP_PLUGIN_CONNECTORS = {}

# Plugin static state(s). These are listed in the entry.tp file,
# vs. dynamic states which would be created/removed at runtime.
TP_PLUGIN_STATES = {
    "text": {
        # "category" is optional, if omitted then this state will be added to all, or the only, category(ies)
        "category": "main",
        "id": PLUGIN_ID + ".state.text",
        # "text" is the default type and could be omitted here
        "type": "text",
        "desc": "Example State Text",
        "doc": "example doc",
        # we can conveniently use a value here which we already defined above
        "default": TP_PLUGIN_ACTIONS["example"]["data"]["text"]["default"]
    },
    "color": {
        "id": PLUGIN_ID + ".state.color",
        "desc": "Example State Color",
        "default": TP_PLUGIN_ACTIONS["example"]["data"]["color"]["default"]
    },
}

# Plugin Event(s).
TP_PLUGIN_EVENTS = {}