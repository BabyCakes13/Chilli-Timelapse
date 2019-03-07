from astral import Astral
from picamera import PiCamera
from time import sleep
import datetime
import sys

# hackit later
city_name = 'Bucharest'
latitude = 0
longitude = 0


def get_sun():
    """
    Calculates the dawn and dusk times for some given coordinates.
    :return: dawn and dusk time
    """

    a = Astral()
    a.solar_depression = 'civil'

    city = a[city_name]
    city.latitude = latitude
    city.longitude = longitude

    today = datetime.datetime.now()

    sun = city.sun(date=datetime.date(today.year, today.month, today.day), local=True)
    dusk = sun['dusk']
    dawn = sun['dawn']

    return dusk, dawn


resolution_x = 1920
resolution_y = 1080
path = "/net/al-media/mnt/raid/chillicam/"
# path = "/home/pi/"
format = ".jpg"
interval = 60


def capture_chillies():
    """
    Method which captures the chillies between dawn and dusk.
    """

    camera = PiCamera()
    camera.resolution = (resolution_x, resolution_y)

    while True:
        now = datetime.datetime.now()
        pretty_now = now.isoformat()
        dusk, dawn = get_sun()

        if dawn.time() < now.time() < dusk.time():
            camera.capture(path + pretty_now + format)
            print(now.time())
        else:
            print("No print at " + str(now.time()), file=sys.stderr)

        sleep(interval)


capture_chillies()
