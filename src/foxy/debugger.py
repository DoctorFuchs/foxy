from foxy.listener.database import *

class EventLogger(Event):
    def trigger(self):
        print(dir(self))
        print(f"[DEBUGGER][{self.get_eventname()}][object: {str(self.item_information())}]")

