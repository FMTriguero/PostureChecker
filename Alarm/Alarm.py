import winsound


class Alarm:
    def __init__(self):
        self.frequency = 2500
        self.duration = 1000

    def ring(self):
        winsound.Beep(self.frequency, self.duration)
