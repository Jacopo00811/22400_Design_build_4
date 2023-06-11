from machine import RTC

class TimeAndDate:
    def __init__(self):
        self.rtc = RTC()
        self.dateAndTime = self.rtc.datetime()

    def date_time(self):
        # Format: yyyy-mm-dd hh:mm:ss
        date = '{:04d}-{:02d}-{:02d}'.format(self.dateAndTime[0], self.dateAndTime[1], self.dateAndTime[2])
        time = '{:02d}:{:02d}:{:02d}'.format(self.dateAndTime[4], self.dateAndTime[5], self.dateAndTime[6])
        # Add the following line if you want to include hundredths of a second:
        # time += ',{:02d}'.format(self.dateAndTime[7] // 10000)
        date_and_time = date + " " + time
        return date_and_time

    def print_date_time(self):
        print(self.date_time(), "-->", end=" ")