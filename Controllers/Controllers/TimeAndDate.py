from machine import RTC

class TimeAndDate:
    def __init__(self, year, month, day, dayOfWeek, hour, minutes):
        self.rtc = RTC()
        self.rtc.datetime((year, month, day, dayOfWeek, hour, minutes, 0, 0))

    def date_time(self):
        dateAndTime = self.rtc.datetime()
        # Format: yyyy-mm-dd hh:mm:ss
        date = '{:04d}-{:02d}-{:02d}'.format(dateAndTime[0], dateAndTime[1], dateAndTime[2])
        time = '{:02d}:{:02d}:{:02d}'.format(dateAndTime[4], dateAndTime[5], dateAndTime[6])
        # Add the following line if you want to include hundredths of a second:
        # time += ',{:02d}'.format(self.dateAndTime[7] // 10000)
        date_and_time = date + " " + time
        return date_and_time

    def print_date_time(self):
        print(self.date_time(), "-->", end=" ")