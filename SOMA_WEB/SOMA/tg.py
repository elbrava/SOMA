import datetime
from time import sleep
from functools import partial
import os
import telebot
from kivy.storage.jsonstore import JsonStore
import datetime
import threading
import pytz

"""
notes
unit
record
revise
login 
signup
profile
encode date
$links gen
$reply to

"""

tz = pytz.timezone('Africa/Nairobi')
match_list = []
running = True
api_key = os.environ["API_KEY"]
bot = telebot.TeleBot(api_key)
error_msg = """
Commands
    /all-all lessons,cats,assignments
    /work launches mesenger application
Keywords
    lesson ![description]![time]
    e.g 0900h -h must be included
    assignments![description]![time_due]
        e.g=time_due=[2w]-2 weeks,[2d]-2 days
        
    cat![description]![time_due]
    remove![type]![name]
    type-lesson,cat,assignments
    name-name of lesson,cat or assignments
    !!!!!!!! 
    []is not part of the message and should not be used     
"""


@bot.message_handler(commands=["Greet"])
def start(message):
    bot.reply_to(message, "nice")


def message_handle(message):
    print(message.text)
    if message.text.__contains__("!"):
        if message.text.split("!")[0] == "remove" or message.text.split(
                "!")[0] == "Remove":
            print("remove")
            remove(message)
            return False
        else:
            return True
    else:
        if message.text == "/all" or message.text == "/work":
            pass
        else:
            bot.reply_to(message, error_msg)


@bot.message_handler(func=message_handle)
def add(message):
    try:
        if len(message.text.split("!")) != 3:
            raise ValueError
    except ValueError:
        bot.reply_to(message, error_msg)
    else:

        store = JsonStore("result.json")

        determinant = message.text.split("!")[0]

        if determinant == "Lesson" or determinant == "lesson":
            s = dict(store)["store"]
            lessons = s["Lessons"]
            if lessons.__contains__(message.text):
                bot.reply_to(message, "ELEMENT ALREADY EXISTS")
            else:
                lessons.append(message.text)
                s["Lessons"] = lessons
                print(s)
                store["store"] = s
                bot.send_message(message.chat.id, "Lesson saved successfully")
                bot.reply_to(message, "Which assignment was given")
                get_times(message)

        elif determinant == "Assignment" or determinant == "assignment":
            s = dict(store)["store"]
            lessons = s["Assignments"]
            if lessons.__contains__(message.text):
                bot.reply_to(message, "ELEMENT ALREADY EXISTS")
            else:
                lessons.append(message.text)
                s["Assignments"] = lessons
                print(s)
                store["store"] = s
                bot.send_message(message.chat.id,
                                 "Assignment saved successfully")
                get_times(message)
        elif determinant == "Cat" or determinant == "cat":
            s = dict(store)["store"]
            lessons = s["Cats"]
            if lessons.__contains__(message.text):
                bot.reply_to(message, "ELEMENT ALREADY EXISTS")
            else:
                lessons.append(message.text)
                s["Cats"] = lessons
                print(s)
                store["store"] = s
                bot.send_message(message.chat.id, "Cat saved successfully")


def get_times(message):
    store = JsonStore("result.json")
    s = dict(store)["store"]
    s["Times"] = []
    s["matchlist"] = {}
    print(s)
    s["Times"] = []
    for type in list(s.keys()):
        print(type)
        for element in s[type]:
            print(element)
            element_determinant = element.split("!")[0]
            if element_determinant == "Lesson" or element_determinant == "lesson":
                try:
                    time = int(element.split("!")[2].split("h")[0])
                except Exception as e:
                    print(e)
                    sys_remove(message)

                else:
                    print(time)
                    hour = time // 100
                    minutes = time % 100
                    day = datetime.datetime.today().strftime("%A")
                    t = datetime.time(hour, minutes)
                    s = dict(store)["store"]
                    times = s["Times"]
                    times.append([day, str(t)])
                    s["Times"] = times
                    print(t)
                    list_match = s["matchlist"]
                    list_match[element.split("!")[0] + ": " +
                               element.split("!")[1]] = [day, str(t)]
                    print(s)
                    store.clear()
                    store["store"] = s

            elif element_determinant == "Assignment" or element_determinant == "assignment":
                try:
                    period = element.split("!")[2]
                    if period.__contains__("w") or period.__contains__("d"):
                        pass
                    else:
                        raise ValueError
                except ValueError:
                    sys_remove(message)
                else:
                    period = element.split("!")[2]
                    hour = datetime.datetime.now(tz=tz).hour
                    minutes = datetime.datetime.now(tz=tz).minute
                    t = datetime.time(hour, minutes)
                    s = dict(store)["store"]
                    date1 = datetime.date.today()
                    if period.__contains__("w"):
                        days = int(period.split("w")[0]) * 7
                    elif period.__contains__("d"):
                        days = int(period.split("h")[0])
                    date2 = datetime.timedelta(days)
                    times = s["Times"]
                    times.append([str(date2 + date1), str(t)])
                    s["Times"] = times
                    list_match = s["matchlist"]
                    list_match[element.split("!")[0] + " " +
                               element.split("!")[1]] = [
                        str(date2 + date1),
                        str(t)
                    ]
                    print(s)
                    store.clear()
                    store["store"] = s

            elif element_determinant == "Cat" or element_determinant == "cat":
                try:
                    period = element.split("!")[2]
                    if period.__contains__("w") or period.__contains__("d"):
                        pass
                    else:
                        raise ValueError
                except ValueError:
                    sys_remove(message)
                else:
                    period = element.split("!")[2]
                    hour = datetime.datetime.now(tz=tz).hour
                    minutes = datetime.datetime.now(tz=tz).minute
                    t = datetime.time(hour, minutes)
                    s = dict(store)["store"]
                    date1 = datetime.date.today()
                    if period.__contains__("w"):
                        days = int(period.split("w")[0]) * 7
                    elif period.__contains__("d"):
                        days = int(period.split("h")[0])
                    date2 = datetime.timedelta(days)
                    times = s["Times"]
                    times.append([str(date2 + date1), str(t)])
                    s["Times"] = times
                    list_match = s["matchlist"]
                    list_match[element.split("!")[0] + " " +
                               element.split("!")[1]] = [
                        str(date2 + date1),
                        str(t)
                    ]
                    print(s)
                    store.clear()
                    store["store"] = s


@bot.message_handler(commands=["all"])
def list_all(message):
    print(message)
    store = JsonStore("result.json")
    s = dict(store)["store"]
    lessons = s["Lessons"]
    lessons = "\n".join(lessons)
    bot.reply_to(message, f"Lessons:\n{lessons}")
    s = dict(store)["store"]
    assignments = s["Assignments"]
    assignments = "\n".join(assignments)
    bot.reply_to(message, f"Assignments:\n{assignments}")
    s = dict(store)["store"]
    cats = s["Cats"]
    cats = "\n".join(cats)
    bot.reply_to(message, f"Cats:\n{cats}")


def sys_remove(message):
    store = JsonStore("result.json")
    determinant = message.text.split("!")[1]
    # consider the message
    test_text = message.text.split("!")[2]
    s = dict(store)["store"]
    try:
        if determinant == "Lesson" or determinant == "lesson":

            lessons = s["Lessons"]
            for lesson in lessons:
                if lesson.__contains__(test_text) or lesson == test_text:
                    lessons.remove(lesson)
                    s["Lessons"] = lessons
                else:
                    raise ValueError
        elif determinant == "Assignment" or determinant == "assignment":

            lessons = s["Assignments"]
            for lesson in lessons:
                if lesson.__contains__(test_text) or lesson == test_text:
                    lessons.remove(lesson)
                    s["Assignments"] = lessons
                else:
                    raise ValueError
        elif determinant == "Cat" or determinant == "cat":

            lessons = s["Cats"]
            for lesson in lessons:
                if lesson.__contains__(test_text) or lesson == test_text:
                    lessons.remove(lesson)
                    s["Cats"] = lessons
                else:
                    raise ValueError
    finally:
        bot.reply_to(message, "CHECK UR TIME MESSAGE WAS  DELETED")

        bot.send_message(message.chat.id, error_msg)


# command remove
def remove(message):
    store = JsonStore("result.json")
    determinant = message.text.split("!")[1]
    # consider the message
    test_text = message.text.split("!")[2]
    s = dict(store)["store"]
    try:
        if determinant == "Lesson" or determinant == "lesson":

            lessons = s["Lessons"]
            for lesson in lessons:
                if lesson.__contains__(test_text) or lesson == test_text:
                    lessons.remove(lesson)
                    s["Lessons"] = lessons
                else:
                    raise ValueError
        elif determinant == "Assignment" or determinant == "assignment":

            lessons = s["Assignments"]
            for lesson in lessons:
                if lesson.__contains__(test_text) or lesson == test_text:
                    lessons.remove(lesson)
                    s["Assignments"] = lessons
                else:
                    raise ValueError
        elif determinant == "Cat" or determinant == "cat":

            lessons = s["Cats"]
            for lesson in lessons:
                if lesson.__contains__(test_text) or lesson == test_text:
                    lessons.remove(lesson)
                    s["Cats"] = lessons
                else:
                    raise ValueError

    except ValueError:
        bot.reply_to(message, "VALUE NOT FIND CHECK WITH /all")
    else:
        store.clear()
        store["store"] = s

        get_times(message)


def match(date_time):
    print(date_time)
    store = JsonStore("result.json")
    s = dict(store)["store"]

    match_dict = dict(s["matchlist"])
    print(match_dict.keys)
    for key in match_dict.keys():
        if match_dict[key] == date_time:
            return key


@bot.message_handler(commands=["work"])
def go(message):
    threading.Thread(target=partial(run, message)).start()


def run(message):
    store = JsonStore("result.json")
    s = dict(store)["store"]
    times = s["Times"]
    while running:
        sleep(0.7)
        print("AMAI")
        for date, time in times:
            time_diff_list = [(2700 // (3 ** (i + 1))) * -100 for i in range(7)]
            print(time_diff_list)
            now = int(str(datetime.datetime.now(tz=tz).strftime("%H%M00")))

            print(now)
            split_time = time.split(":")
            print(split_time)
            time_to_be_used = int(
                str(
                    datetime.time(int(split_time[0]), int(split_time[1]),
                                  int(split_time[2])).strftime("%H%M00")))
            diff_time = time_to_be_used - now

            print(diff_time)
            if time_diff_list.__contains__(diff_time):
                print(time, datetime.datetime.now(tz))
                # lesson
                try:
                    date = date.split("-")
                    date = datetime.date(int(date[0]), int(date[1]),
                                         int(date[2]))
                except:
                    # the same day
                    if date == datetime.datetime.today().strftime("%A"):
                        print(date, datetime.datetime.today().strftime("%A"))
                        bot.send_message(
                            message.chat.id,
                            f"REMEMBER : {match([str(date), time])} by {str(date)} {time}"
                        )
                        sleep(40)
                else:
                    date1 = int(str(date.strftime("%Y%m%d")))
                    print(date1)
                    date2 = int(str(datetime.date.today().strftime("%Y%m%d")))
                    print(date2)
                    if date1 >= date2:
                        bot.send_message(
                            message.chat.id,
                            f"REMEMBER : {match([str(date), time])} by {str(date)} {time}"
                        )
                        sleep(40)


class messages():
    def __init__(self, payload):
        unique_id = payload
        chat_id = 111


def reply(message):
    pass


bot.polling()
"""
param;
    description
    time
before bed
3 hour to lesson
1 hour
45 min
30min
10min
duration lesson are assumed to be three hours
save to memory
 day of the week
"""
"""

assignments
param:
    description 
due time
    w-weeks
    d-days
    everyday assume to be collected at the same time
"""
"""
cat 
param:description 
      similar to assignment
"""
# consider use of threads
# errors
# reminders
