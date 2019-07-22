from stat_tracking import main
import datetime
import calendar
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt


def total_map_hours_per_day(matches):
    time_total = 0
    time_per_day = list()
    current_time = {}
    current_date = ""
    earliest_date = matches[0].info["date"]
    latest_date = matches[len(matches)-1].info["date"]
    for match in matches:
        if match.info["date"] == current_date:
            # current_time += match.info["map_playtime"]/60/60
            if match.info["map"] in current_time:
                current_time[match.info["map"]] += match.info["map_playtime"]/60/60
            else:
                current_time[match.info["map"]] = match.info["map_playtime"] / 60 / 60
        else:
            if current_time:
                time_per_day.append([current_date,current_time])
            current_date = match.info["date"]
            current_time = {}
        time_total += match.info["map_playtime"]
    time_per_day.append([current_date, current_time])
    print(time_per_day)
    # for time in time_per_day:
    #     print(f"Day: {time[0]}, Time: {time[1]}")

    dates = list()
    times = list()
    if not int(earliest_date.split("/")[0]) == int(latest_date.split("/")[0]):
        for year in range(int(earliest_date.split("/")[0]), int(latest_date.split("/")[0])):
            for month in range(int(earliest_date.split("/")[1]), int(latest_date.split("/")[1])):
                print(calendar.monthrange(year, month))
                print("hi")

    elif not int(earliest_date.split("/")[1]) == int(latest_date.split("/")[1]):
        for month in range(int(earliest_date.split("/")[1]), int(latest_date.split("/")[1])):
            print(calendar.monthrange(earliest_date.split("/")[0], month))
            print("hi")
    else:
        mrange = calendar.monthrange(int(earliest_date.split("/")[0]), int(earliest_date.split("/")[1]))
        for i in range(mrange[0]+1, mrange[1]+1):
            # print(i)
            this_date = earliest_date.split("/")[0]+"/"+earliest_date.split("/")[1]+"/"+f"{i:02d}"
            # print(this_date)
            if this_date not in [time[0] for time in time_per_day] and int(f"{i:02d}") >= int(earliest_date.split("/")[2])\
                    and int(f"{i:02d}") < int(latest_date.split("/")[2]):

                times.append(0)
                dates.append(int(earliest_date.split("/")[0]) * 10000 + 100 * int(earliest_date.split("/")[1]) + int(f"{i:02d}"))

            else:
                for idx, p in enumerate(time_per_day):
                    # print(p[0], this_date)
                    if p[0] == this_date:
                        times.append(p[1])
                        dates.append(int(earliest_date.split("/")[0]) * 10000 + 100 * int(earliest_date.split("/")[1]) + int(f"{i:02d}"))

                        break
    print(len(times), len(dates))
    # for time in time_per_day:
    #     print(time[0])
    print(times)
    print(dates)
    print(latest_date)
    # objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
    objects = dates
    y_pos = np.arange(len(objects))
    performance = times

    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects, rotation='vertical')
    plt.ylabel('Hours played')
    plt.title('Hours played per day')

    plt.show()

    return time_total


def plot_hours_per_day(matches):
    time_total = 0
    time_per_day = list()
    current_time = 0
    current_date = ""
    earliest_date = matches[0].info["date"]
    latest_date = matches[len(matches)-1].info["date"]
    for match in matches:
        for player in match.players:
            if match.info["date"] == current_date:
                current_time += player["time_on_team"]/60/60
            else:
                time_per_day.append([current_date,current_time])
                current_date = match.info["date"]
                current_time = 0
            time_total += player["time_on_team"]
    time_per_day.append([current_date, current_time])
    # for time in time_per_day:
    #     print(f"Day: {time[0]}, Time: {time[1]}")

    dates = list()
    times = list()
    if not int(earliest_date.split("/")[0]) == int(latest_date.split("/")[0]):
        for year in range(int(earliest_date.split("/")[0]), int(latest_date.split("/")[0])):
            for month in range(int(earliest_date.split("/")[1]), int(latest_date.split("/")[1])):
                print(calendar.monthrange(year, month))
                print("hi")

    elif not int(earliest_date.split("/")[1]) == int(latest_date.split("/")[1]):
        for month in range(int(earliest_date.split("/")[1]), int(latest_date.split("/")[1])):
            print(calendar.monthrange(earliest_date.split("/")[0], month))
            print("hi")
    else:
        mrange = calendar.monthrange(int(earliest_date.split("/")[0]), int(earliest_date.split("/")[1]))
        for i in range(mrange[0]+1, mrange[1]+1):
            print(i)
            this_date = earliest_date.split("/")[0]+"/"+earliest_date.split("/")[1]+"/"+f"{i:02d}"
            # print(this_date)
            if this_date not in [time[0] for time in time_per_day] and int(f"{i:02d}") >= int(earliest_date.split("/")[2])\
                    and int(f"{i:02d}") < int(latest_date.split("/")[2]):

                times.append(0)
                dates.append(int(earliest_date.split("/")[0]) * 10000 + 100 * int(earliest_date.split("/")[1]) + int(f"{i:02d}"))

            else:
                for idx, p in enumerate(time_per_day):
                    print(p[0], this_date)
                    if p[0] == this_date:
                        times.append(p[1])
                        dates.append(int(earliest_date.split("/")[0]) * 10000 + 100 * int(earliest_date.split("/")[1]) + int(f"{i:02d}"))

                        break
    print(len(times), len(dates))
    # for time in time_per_day:
    #     print(time[0])
    print(times)
    print(dates)
    print(latest_date)
    # objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
    objects = dates
    y_pos = np.arange(len(objects))
    performance = times

    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects, rotation='vertical')
    plt.ylabel('Hours played')
    plt.title('Hours played per day')

    plt.show()

    return time_total
