class Public:
    def __init__(self, _obj) -> None:
        for item in dir(_obj):
            if item.startswith("_"):
                continue
            else:
                self.__setattr__(item, _obj.__getattribute__(item))
