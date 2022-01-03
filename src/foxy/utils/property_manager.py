from foxy.listener.event import Event
from foxy.utils.exceptions import EventCanceledByListener
from foxy.utils.publisher import Public

def get_default_fget(obj_name):
    def f(self):
        return self.__getattribute__(obj_name)
    
    return f

def get_default_fset(obj_name):
    def f(self, value):
        self.__setattr__(obj_name, value)

    return f

def get_default_fdel(obj_name):
    def f(self):
        self.__setattr__(obj_name, None)
    
    return f

def get_cancelable_checker(obj_name, event: Event):
    """returns a function, that checks an event for cancelable"""
    def f(self):
        if event.is_cancelable():
            if event(Public(self)).canceled:
                raise EventCanceledByListener
    
    return f

def generate_property_with_events(obj_name, on_get_event: Event, on_change_event: Event, on_delete_event: Event):
    def fget(self):
        get_cancelable_checker(obj_name, on_get_event)
        get_default_fget(obj_name)

    def fset(self, value):
        get_cancelable_checker(obj_name, on_change_event)
        get_default_fset(obj_name)

    def fdel(self):
        get_cancelable_checker(obj_name, on_delete_event)
        get_default_fdel(obj_name)

    return property(fget=fget, fset=fset, fdel=fdel)
