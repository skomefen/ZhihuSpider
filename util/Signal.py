class signal:

    def __init__(self,signal_num):
        self.signal_num = signal_num

    def signal_num_change(self,num):
        self.signal_num += num

    def get_signal_num(self):
        return self.signal_num