from trello import TrelloClient
import markdown
import json
from trello import TrelloClient
import markdown
import json
import re
import matplotlib
import matplotlib.dates
import matplotlib.pyplot
import numpy as np
import datetime
import pytz

local_tz = pytz.timezone('US/Eastern')

client = TrelloClient(
    api_key = 'abdcf64bc3a4843d1d21ffe6bb1d4859',
    api_secret = 'fbdd4beb9918f1b6832ce97b716adf5f5cad124f8ebe37bc89847a4e7e3f015c',
    token = 'bd58a05d838be1764b283ac14631b553b01d8b2936a4bf5e8b7fc91abb07df71',
    token_secret = '4ed5c91a0b7e777559a512207e047041')

def pretty_print_board(board_id):
    board = client.get_board(board_id)
    lists = board.open_lists()
    with open(board_id + ".html", "w") as f:
        f.write("<body>\n")
        for lst in lists:
            f.write(f"{lst.name}:\n<ul>\n")
            for card in lst.list_cards():
                desc = markdown.markdown(card.desc)
                desc = f"<ul><li>{desc}\n</li></ul>" if desc != "" else ""
                members = ", ".join([m['fullName'] for m in client.fetch_json("cards/" + card.id + "/members")])
                members = f" [{members}]" if members != "" else ""
                f.write(f"<li>{card.name}{members}\n{desc}</li>\n")
            f.write("</ul>\n")
        f.write("</body>")

def graph_board(board_id):
    days = {}
    board = client.get_board(board_id)
    #lists = board.open_lists()
    lists = [board.get_list("58962dc4febccd3c67734ee9")] #done
    for lst in lists:
        for card in lst.list_cards():
            movements = card.list_movements()
            date = ""
            if len(movements) > 0:
                date = movements[0]['datetime'].astimezone(local_tz).date()
            else:
                date = card.created_date.astimezone(local_tz).date()
            match = re.match(r".*\(([.\d]+)\)", card.name)
            days[date] = days.get(date, 0) + float(match.group(1)) if match is not None else 0
            if match is None:
                print("Missing number:", card.name)

    graph(days)
    return days

def plot(label, data, color):
    matplotlib.pyplot.plot_date(*zip(*sorted(data.items())), fmt='-', label=label, color=color)

def plot_fill(label, data, color):
    matplotlib.pyplot.fill_between(*zip(*sorted(data.items())), 0, color=color)

w = {}
def graph(days):
    startDay = datetime.date(2017, 2, 2)
    endDay = datetime.date(2017, 2, 9)
    total = sum(days.values())

    ideal = {}
    actual = {}
    done = {}

    runningTotal = 0
    for day in sorted(days.keys()):
        runningTotal += days[day]
        done[day] = runningTotal

    day = startDay
    while day <= endDay:
        ideal[day] = total - ((day - startDay).days * (total/(endDay - startDay).days))
        done[day] = done.get(day, 0)
        actual[day] = total - done.get(day, 0)
        day += datetime.timedelta(1)

    matplotlib.pyplot.clf()
    matplotlib.pyplot.ylabel("Hours")
    matplotlib.pyplot.xlabel("Days")
    matplotlib.pyplot.title("Burndown Chart")
    matplotlib.pyplot.xlim([startDay, endDay])

    plot_fill("Ideal", ideal, (1,0,0, 0.2))
    plot_fill("Actual", actual, (0,1,0, 0.5))
    plot_fill("Done", done, (0,0,1, 0.5))
    plot("Ideal", ideal, (1,0,0))
    plot("Actual", actual, (0,1,0))
    plot("Done", done, (0,0,1))

    matplotlib.pyplot.gcf().autofmt_xdate()
    matplotlib.pyplot.gcf().set_size_inches(18.5, 10.5)
    matplotlib.pyplot.legend(loc='upper center')
    matplotlib.pyplot.savefig("test.png", dpi=100)
    matplotlib.pyplot.show()

# pretty_print_board("5IktL1TM") #pre implementation board
# pretty_print_board("XxLTzb0K") #Tasks board
#graph_board("XxLTzb0K")
#graph(dates, vals)
