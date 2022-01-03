from foxy.utils.publisher import Public


class Event:
    def __init__(self, cancelable=True) -> None:
        def get_eventname():
            return self.__class__.__name__

        def is_cancelable():
            return cancelable
        
        self.is_cancelable = is_cancelable
        self.get_eventname = get_eventname
        if cancelable: 
            self.canceled = False
            def set_cancel(self, mode):
                self.canceled = mode

        else:
            def set_cancel(self, mode):
                pass
        
        self.set_cancel = set_cancel

    def trigger(self):
        pass

    def __call__(self, obj):
        try:
            if self.executed:
                return self

        except AttributeError as ignore:
            pass

        self.target = obj
        for cls in self.__class__.__mro__:
            if isinstance(Event, cls):
                break
            for event in cls.__subclasses__():
                event.trigger(Public(self))
        
        self.executed = False
        return self 
        
    
    def _get_new(self):
        return self.__init__(
            cancelable=self.is_cancelable()
        )
    
    def item_information(self) -> str:
        return str({
            "eventname": self.get_eventname,
            "is_cancelable": str(self.is_cancelable()),
            "listeners_amount": str(len(self.__class__.__subclasses__()))
        })
    