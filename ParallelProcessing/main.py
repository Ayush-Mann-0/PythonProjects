from time import time, sleep
from threading import Thread

def test():
    print("test pass")

class Instance:
    """Class to manage a process"""
    def __init__(self, name, id_):
        """Constructor"""
        self.name = name
        self.id_ = id_
        self._start_time = None
        self._end_time = None
        self.time_taken = None

    def start(self, func):
        """Start a process"""
        if not callable(func):
            raise ValueError("func must be a callable")

        self._start_time = time()
        Thread(target=func).start()

    def stop(self):
        """Stop a process"""
        self._end_time = time()
        self.time_taken = int(self._end_time - self._start_time)

def exampleUsage():
    process_1 = Instance("Process 1", 1)
    process_2 = Instance("Process 2", 2)

    process_1.start(test)
    sleep(2)
    process_2.start(test)

    process_1.stop()
    sleep(3)
    process_2.stop()
    
def main():
    exampleUsage()

if __name__ == "__main__":
    main()
