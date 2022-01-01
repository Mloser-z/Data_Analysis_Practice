import json
import re


def get_time(time, time_today):
    if re.match(re.compile(r'\d\d:\d\d'), time) is not None:
        return time_today + '-' + time
    else:
        return time.string


if __name__ == "__main__":
    time = "20:22"
    time_today = "2222"
    print(get_time(time, time_today))
