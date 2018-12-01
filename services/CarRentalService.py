import datetime


class CarRentalService(object):
    def validate_datetime(self, date_time_str_list):
        date_str, time_str = date_time_str_list
        try:
            time_format = "%Y-%m-%dT%H:%M"
            datetime_str = date_str + "T" + time_str
            return datetime.datetime.strptime(datetime_str, time_format)
        except ValueError:
            pass
        try:
            year_str, month_str, day_str = date_str.split("-")
        except ValueError:
            try:
                year_str, month_str, day_str = date_str.split("/")
            except ValueError:
                return None
        try:
            hour_str, minute_str = time_str.split(":")
        except ValueError:
            try:
                hour_str, minute_str = time_str.split("-")
            except ValueError:
                return None
        try:
            year = int(year_str)
            month = int(month_str)
            day = int(day_str)
            hour = int(hour_str)
            minute = int(minute_str)
            return datetime.datetime(year, month, day, hour, minute)
        except ValueError:
            return None
