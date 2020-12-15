import time

class LEDDisplay:
    def __init__(self) -> None:
        super().__init__()
        self.shown_text = None

    def tasks_change_text(self, new_text):
        self.shown_text = new_text
        
    def threaded_rest(self,):
        print('a')
        print('b')
        while True:
            print(self.shown_text)
            time.sleep(1)