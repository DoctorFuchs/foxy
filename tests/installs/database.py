from os import name


def check():
    try:
        import foxy.database.database # check database
        import foxy.database.parser # check parser

    except:
        return False
    
    finally:
        return True
    
if __name__ == "__main__":
    check()