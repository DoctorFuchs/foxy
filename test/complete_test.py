import os
import sys
from benchmarks import save

def testBenchmarks():
    saveCheck = save.check()
    print("SAVECHECK "+"SUCCESS" if saveCheck == [True, True] else "FAILED")

if __name__ == "__main__":
    sys.stderr = open(os.devnull, "wt")
    try: testBenchmarks() 
    except Exception as e: print(e)