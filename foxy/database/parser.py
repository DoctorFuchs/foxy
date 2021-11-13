import math
import configparser as cp

config = cp.ConfigParser()
config.read(__file__.replace("parser.py", "database.ini"))

class defaultParser:
    def __init__(self, table_) -> None:
        self.identifier = "="
        self.table_ = table_

    def __beforeHandle__(self, cell_):
        if cell_.getRawValue().startswith(self.identifier):
            self.handle(cell_)

    def handle(self, cell_):
        pass

class mathParser(defaultParser):
    def __init__(self, cell_) -> None:
        super().__init__(cell_)
    
    def handle(self, cell_):
        code = cell_.getRawValue().replace(self.identifier, "", 1)
        try:
            cell_.value = eval(code, {"__builtins__": None})

        except Exception as e:
            cell_.value = "#ERROR "+str(e)

        if cell_.value == None and cell_.raw == None:
            del self.table_.cells[cell_.pos]
            del cell_


class excelParser(defaultParser):
    def __init__(self, cell_) -> None:
        super().__init__(cell_)
    
    def handle(self, cell_):
        code = cell_.getRawValue().replace(self.identifier, "", 1)

        globals_ = {"__builtins__": None}
        for cell in self.table_.cells:
            globals_[self.table_.cells[cell].pos] = self.table_.cells[cell].getValue()

        # mathematic functions 
        globals_["SIN"] = lambda x: math.sin(float(x))
        globals_["TAN"] = lambda x: math.tan(float(x))
        globals_["COS"] = lambda x: math.cos(float(x))
        
        globals_["SINH"] = lambda x: math.sinh(float(x))
        globals_["TANH"] = lambda x: math.tanh(float(x))
        globals_["COSH"] = lambda x: math.cosh(float(x))
        
        globals_["ASIN"] = lambda x: math.asin(float(x))
        globals_["ATAN"] = lambda x: math.atan(float(x))
        globals_["ACOS"] = lambda x: math.acos(float(x))
        globals_["ATAN"] = lambda y, x: math.atan2(float(y), float(x))

        globals_["ASINH"] = lambda x: math.asinh(float(x))
        globals_["ATANH"] = lambda x: math.atanh(float(x))
        globals_["ACOSH"] = lambda x: math.acosh(float(x))

        globals_["LOG"] = lambda x, y=10: math.log(float(x), float(y))
         
        globals_["SUM"] = lambda x, y: x+y
        globals_["QUOTIENT"] = lambda x, y: x/y
        globals_["SUB"] = lambda x, y: x-y
        globals_["PRODUCT"] = lambda x, y: x*y
        
        # mathematic consts
        globals_["PI"] = math.pi
        globals_["EXP"] = lambda x: math.exp(float(x))
        
        # python3 allowed built-in functions
        globals_["MAX"] = max
        globals_["MIN"] = min
        globals_["ABS"] = abs

        try:
            cell_.value = eval(code, globals_)

        except Exception as e:
            cell_.value = "#ERROR "+str(e)

        if cell_.value == None and cell_.raw == None:
            del self.table_.cells[cell_.pos]
            del cell_
