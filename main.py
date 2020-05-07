import requests
from datetime import date
from datetime import datetime


class HolidayTracker:
    all_holidays = None
    current_date = datetime.now().timestamp() * 1000

    def __init__(self, country_code, year):
        self.url = f'https://date.nager.at/api/v2/publicholidays/{year}/{country_code}'

    def ask_for_holidays(self):
        response = requests.get(self.url)

        if response.status_code == 200:

            self.all_holidays = response.json()
            return
        raise Exception('It was unsuccessful.')

    def show_holidays(self, holidays):
        for holiday in holidays:
            date = holiday['date']
            loc_name = holiday['localName']
            inter_name = holiday['name']
            print(f'when: {date}\nname:{loc_name}/{inter_name}\n')

    def convert_str_to_date(self, strDate):
        return datetime.strptime(strDate, '%Y-%m-%d').timestamp() * 1000

    def check_today(self):

        def check(holiday):
            holiday_date = self.convert_str_to_date(holiday['date'])
            return holiday_date == self.current_date

        today_holidays = list(filter(check, self.all_holidays))

        if len(today_holidays):
            self.show_holidays(today_holidays)
            return

        print('Unfortunately today is not a holiday in target country. But...')
        self.find_nearest_next()

    def find_nearest_next(self):

        for holiday in self.all_holidays:
            holiday_date = self.convert_str_to_date(holiday['date'])

            day = holiday['date']
            name = holiday['name']

            if self.current_date < holiday_date:
                print(
                    f'The nearest holiday will be on {day}. {name}.')
                break


holidays = HolidayTracker('UA', 2020)
holidays.ask_for_holidays()
holidays.check_today()
