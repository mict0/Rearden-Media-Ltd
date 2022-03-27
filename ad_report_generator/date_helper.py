from datetime import datetime, timedelta


class DateHelper(object):
    def __init__(self, one_day=False, week=False, month=False, lifetime=False):
        self.one_day = one_day
        self.week = week
        self.month = month
        self.lifetime = lifetime
        self.now = datetime.today()

    def _to_string(self):
        return vars(self)

    def _get_string_date(self, date):
        return date.strftime("%Y-%m-%d")

    def get_end_date(self):
        """Returns current date"""
        return self._get_string_date(self.now)

    def get_start_date(self):
        """
        Returns the starting date,
        date from which the counting starts
        """
        if self.one_day:
            days = 1
        elif self.week:
            days = 7
        elif self.month:
            days = 30
        elif self.lifetime:
            return self._get_string_date(datetime.min)
        days = self.now - timedelta(days=days)
        return self._get_string_date(days)
