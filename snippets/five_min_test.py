import datetime


def get_next_friday(some_date: datetime.datetime, if_friday_same=True):
    if if_friday_same:  # if a Friday, then same day
        return some_date + datetime.timedelta((4 - some_date.weekday()) % 7)
    else:               # if a Friday, then next one
        return some_date + datetime.timedelta((3 - some_date.weekday()) % 7 + 1)


if __name__ == "__main__":
    today = datetime.date.today()
    print(get_next_friday(today))

    another_day = datetime.datetime(2022, 7, 28)  # Thursday
    print(get_next_friday(another_day))

    a_friday = datetime.datetime(2022, 7, 29)  # Friday
    print(get_next_friday(a_friday))

    a_friday = datetime.datetime(2022, 7, 29)  # Friday
    print(get_next_friday(a_friday, False))
