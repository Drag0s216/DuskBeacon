import requests, time, pytz
from astral import LocationInfo
from astral.sun import sun
from datetime import datetime, date
from ping3 import ping



HA_URL = "http://localhost:8123/api/services/light/turn_on"
TOKEN = ""

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "content-type": "application/json"
}

ENTITY = "light.calex_gaming_light_bar"


city = LocationInfo(
    "Timisoara",
    "Romania",
    "Europe/Bucharest",
    45.745239098833615, 
    21.22658163188974
)

tz = pytz.timezone("Europe/Bucharest")



def nightLight(rgb = [255,0,0], brightness = 40, waitingTime = 150):
    payload = {
        "entity_id": ENTITY,
        "rgb_color": rgb,
        "brightness": brightness
    }

    try:
        post = requests.post(HA_URL, headers=HEADERS, json=payload)
    except Exception as e:
        print(f"ERROR: {e}")
    
    for i in range(waitingTime):
        power = None
        try:
            power = requests.get("http://localhost:8123/api/states/light.calex_gaming_light_bar", headers=HEADERS).json()
        except Exception as e:
            print(f"Error: {e}")

        time.sleep(2)

        if power and power.get("state") == 'off':
            raise SystemExit
        time.sleep(2)

    try:
        turnOff = requests.post("http://localhost:8123/api/services/light/turn_off", headers=HEADERS)
    except Exception as e:
        print(f"ERROR: {e}")

    print("Waiting time passed. Exiting...")
    raise SystemExit


running = False


def gps(ipr = '192.168.95.1', ipp = '192.168.95.135'):
    global running
    running = True

    while True:
        try:
            router = ping(ipr)
            phone = ping(ipp)
        
            if router and phone:
                nightLight()

            
            else:
                time.sleep(5)
                timeCheck()
        except Exception as e:
            print(f"ERROR: {e}")


def timeCheck():
    while True:
        now = datetime.now(tz)
        sunToday = sun(city.observer, date=date.today(), tzinfo=tz)

        duskToday = sunToday['dusk']
        dawnToday = sunToday['dawn']


        if (now >= duskToday or now < dawnToday) and not running:
            print("Starting GPS")
            gps()

        elif (now >= duskToday or now < dawnToday) and running:
            return
        

        elif dawnToday <= now < duskToday:
            print("Daytime reached. Exiting...")
            raise SystemExit

print("Running")
        
timeCheck()
