import re
from uuid import uuid4
from wsgiref.simple_server import make_server

import falcon, json
import sqlite3
from datetime import datetime, timedelta

import urllib.request

import sched,time

scheduler = sched.scheduler(time.time, time.sleep)



dbconn = sqlite3.connect(":memory:")
dbcurs = dbconn.cursor()
try:
    pass  # SQL commands go here
except Exception as e:
    print(e)
# finally:
#     if dbcurs:
#         dbcurs.close()
#     if dbconn:
#         dbconn.close()

# TODO check existence of table
dbcurs.execute(
    "CREATE TABLE registrations (uuid char(40), lat float, lon float, path int, row int, hit date, notifications date[], emails varchar(4096), phones varchar(4096))"
)

# These are the most recent datetimes (UTC) when they passed 001-001. Calibrated 2024-10-05
LANDSAT8_OFFSET = datetime(2024, 9, 24, 14, 6, 52, 0)
LANDSAT9_OFFSET = datetime(2024, 10, 2, 14, 6, 58, 0)
LANDSATS_PATH_SEQUENCE = [1, 17, 33, 49, 65, 81, 97, 113, 129, 145, 161, 177, 193, 209, 225, 8, 24, 40, 56, 72, 88, 104, 120, 136, 152, 168, 184, 200, 216, 232, 15, 31, 47, 63, 79, 95, 111, 127, 143, 159, 175, 191, 207, 223, 6, 22, 38, 54, 70, 86, 102, 118, 134, 150, 166, 182, 198, 214, 230, 13, 29, 45, 61, 77, 93, 109, 125, 141, 157, 173, 189, 205, 221, 4, 20, 36, 52, 68, 84, 100, 116, 132, 148, 164, 180, 196, 212, 228, 11, 27, 43, 59, 75, 91, 107, 123, 139, 155, 171, 187, 203, 219, 2, 18, 34, 50, 66, 82, 98, 114, 130, 146, 162, 178, 194, 210, 226, 9, 25, 41, 57, 73, 89, 105, 121, 137, 153, 169, 185, 201, 217, 233, 16, 32, 48, 64, 80, 96, 112, 128, 144, 160, 176, 192, 208, 224, 7, 23, 39, 55, 71, 87, 103, 119, 135, 151, 167, 183, 199, 215, 231, 14, 30, 46, 62, 78, 94, 110, 126, 142, 158, 174, 190, 206, 222, 5, 21, 37, 53, 69, 85, 101, 117, 133, 149, 165, 181, 197, 213, 229, 12, 28, 44, 60, 76, 92, 108, 124, 140, 156, 172, 188, 204, 220, 3, 19, 35, 51, 67, 83, 99, 115, 131, 147, 163, 179, 195, 211, 227, 10, 26, 42, 58, 74, 90, 106, 122, 138, 154, 170, 186, 202, 218]

LANDSATS_SCHEDULE = [
    {"path": 1, "row": 60, "datetime": datetime.now(), "satellite_name": "8", "authority": "hacker"}
]

LANDSAT_DELTA_CYCLE = timedelta(days=16)
LANDSAT_DELTA_PATH = timedelta(seconds=(16 * 86400.0 / 233.0))
LANDSAT_DELTA_ROW = timedelta(seconds=(16 * 86400.0 / 233.0 / 248.0))

landsat_schedule = []

def populate_schedule_generated(schedule):
    for cycle in range(10):  # Predict 160 days into future
        path = 1
        for idxpath in range(233):
            for idxrow in range(248):
                row = idxrow + 1
                schedule.append(
                    {
                        "path": path,
                        "row": row,
                        "datetime": (
                              LANDSAT8_OFFSET
                            + cycle * LANDSAT_DELTA_CYCLE
                            + idxpath * LANDSAT_DELTA_PATH
                            + idxrow * LANDSAT_DELTA_ROW
                        ),
                        "satellite_name": "8",
                        "authority": "hacker"
                    }
                )
                schedule.append(
                    {
                        "path": path,
                        "row": row,
                        "datetime": (
                              LANDSAT9_OFFSET
                            + cycle * LANDSAT_DELTA_CYCLE
                            + idxpath * LANDSAT_DELTA_PATH
                            + idxrow * LANDSAT_DELTA_ROW
                        ),
                        "satellite_name": "9",
                        "authority": "hacker"
                    }
                )
            path = (path + 16) % 233


def populate_schedule_authoritative(schedule):
    now = datetime.now()
    for d in range(6):
        query_date = now + timedelta(days=d)
        query_date_string = query_date.strftime('y%Y/%b/%b-%d-%Y')
        print(query_date_string)
        try:
            content = urllib.request.urlopen("https://landsat.usgs.gov/landsat/all_in_one_pending_acquisition/L9/Pend_Acq/{}.txt".format(query_date_string)).read()
        except:
            break
        content_str = str(content)
        lines = content_str.split("\\n")
        for line in lines:
            result = re.search(r"\A *([0-9]+) +([0-9]+) +([0-9]+)-([:0-9]+) +([A-Z]+)\Z", line)
            if result:
                path = result.groups()[0]
                row = result.groups()[1]
                day_of_year = result.groups()[2]
                time_of_day = result.groups()[3]
                (h, m, s) = (int(time_of_day.split(":")[0]), int(time_of_day.split(":")[1]), int(time_of_day.split(":")[2]))
                station = result.groups()[4]
                schedule.append(
                    {
                        "path": path,
                        "row": row,
                        "datetime": (datetime(year=2024,month=1,day=1) + timedelta(days=(int(day_of_year)-1)) + timedelta(hours=h, minutes=m, seconds=s)),
                        "satellite_name": "9",
                        "authority": "landsat.usgs.gov/landsat/all_in_one_pending_acquisition"
                    }
                )
        print(lines[0])
        print(len(lines))

populate_schedule_authoritative(landsat_schedule)
populate_schedule_generated(landsat_schedule)

landsat_schedule.sort(key=lambda x: x["datetime"])
print(landsat_schedule[0:100])

def sanitize_schedule(schedule):
    pass

def query_schedule(schedule, path, row):
    for i in schedule:
        if i["path"] == path and i["row"] == row:
            return i
    return None

# def landsat8_nextmany(path, row, count):
#     addition = LANDSATS_PATH_SEQUENCE.index(path) * (16 * 86400.0 / 233.0) + (row - 60) * (16 * 86400.0 / 233.0 / 248.0)
#     result0 = LANDSAT8_OFFSET + timedelta(seconds=addition)
#     while result0 < datetime.now():
#         result0 += timedelta(days=16)
#     result = [result0]
#     for i in range(1, count):
#         result.append(result0 + i * timedelta(days=16))
#     print(result)


# def landsat9_nextmany(path, row, count):
#     addition = LANDSATS_PATH_SEQUENCE.index(path) * (16 * 86400.0 / 233.0) + (row - 60) * (16 * 86400.0 / 233.0 / 248.0)
#     result0 = LANDSAT9_OFFSET + timedelta(seconds=addition)
#     while result0 < datetime.now():
#         result0 += timedelta(days=16)
#     result = [result0]
#     for i in range(1, count):
#         result.append(result0 + i * timedelta(days=16))
#     return result


# def landsat8_next(path, row):
#     return landsat8_nextmany(path, row, 1)[0]


# def landsat9_next(path, row):
#     return landsat9_nextmany(path, row, 1)[0]


# def landsats_nextmany(path, row, count):
#     return (
#         landsat8_nextmany(path, row, count) + landsat9_nextmany(path, row, count)
#     ).sort()


# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class ThingsResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.content_type = falcon.MEDIA_TEXT  # Default is JSON, so override
        resp.text = (
            "\nTwo things awe me most, the starry sky "
            "above me and the moral law within me.\n"
            "\n"
            "    ~ Immanuel Kant\n\n"
        )

def parse_date(datestring):
    result = re.search(r"\A([0-9]+)-([0-9]+)-([0-9]+)T([0-9]+):([0-9]+)\Z", datestring)
    if result:
        year = int(result.group()[0])
        month = int(result.group()[1])
        day = int(result.group()[2])
        hour = int(result.group()[3])
        minute = int(result.group()[4])
        return datetime(year=year,month=month,day=day,hour=hour,minute=minute)
    return None


class RegistrationAPI:
    def on_post(self, req, resp):
        requestbody = req.get_media()
        print(requestbody)
        uuid = uuid4()
        uuidstr = str(uuid)
        (lat, lon) = (requestbody["lat"], requestbody["lon"])
        # TODO lat, lon to WRS-2 and calc time
        coverage_threshold_result = json.dumps(requestbody["coverage_threshold_result"])
        coverage_threshold_forecast = json.dumps(
            requestbody["coverage_threshold_forecast"]
        )
        hit = json.dumps(requestbody["hit"]).replace('"', "")
        try:
            requestbody[notifications][0]
        except:
            requestbody[notifications] = []
            requestbody[notifications][0] = query_schedule(landsat_schedule, path, row)
            
        notifications = json.dumps(requestbody["notifications"]).replace('"', "")
        for d in notifications:
            date = parse_date(d)
            scheduler.enterabs(time.mktime(d.timetuple()), 0, send_email, (uuid))
        emails = json.dumps(requestbody["emails"])
        phones = json.dumps(requestbody["phones"])
        dbcurs.execute(
            "INSERT INTO registrations(uuid, lat, lon, hit, notifications, emails, phones) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                uuidstr, lat, lon, hit, notifications, emails, phones
            )
        )
        dbcurs.execute("SELECT * FROM registrations")
        print(dbcurs.fetchall())
        dbconn.commit()
        resp.status = falcon.HTTP_200
        # resp.content_type = falcon.MEDIA_TEXT # default is json
        resp.text = json.dumps({"uuid": uuidstr})
        # Send email async

    def on_delete(self, req, resp):
        resp.status = falcon.HTTP_200
        # resp.content_type = falcon.MEDIA_TEXT
        resp.text = "id\n"


# falcon.App instances are callable WSGI apps
# in larger applications the app is created in a separate file
app = falcon.App()

# Resources are represented by long-lived class instances
things = ThingsResource()
registration = RegistrationAPI()

# things will handle all requests to the '/things' URL path
app.add_route("/things", things)
app.add_route("/calibrate", things)
app.add_route("/acquisition", things)
app.add_route("/registration", registration)
app.add_route("/things", things)

# if __name__ == '__main__':
#     with make_server('', 8000, app) as httpd:
#         print('Serving on port 8000...')

#         # Serve until process is killed
#         httpd.serve_forever()
