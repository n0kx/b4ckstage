import machine, time, network, ntptime, utime, math, urequests, json
import splashscreen, places
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY

# Variables
is_connected = False
time_remaining = 15

# Overclock to 200Mhz
machine.freq(200000000)

# Create Galactic Unicorn object and graphics surface for drawing
galactic_unicorn = GalacticUnicorn()
graphics = PicoGraphics(DISPLAY)

# Load splashscreen
splashscreen.galactic_unicorn = galactic_unicorn
splashscreen.graphics = graphics
splashscreen.init()

# Import WiFi SSID and Password
try:
    from secrets import WIFI_SSID, WIFI_PASSWORD
    wifi_available = True
except ImportError:
    print("Create secrets.py with WiFi credentials")
    wifi_available = False

# Connect to WiFi and synchronize the RTC time from NTP
def connect_to_wifi():
    global is_connected
    
    if is_connected or not wifi_available:
        return
    
    timeout_seconds = 20

    # Start connection
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm=0xa11140) # Disable WiFi power-saving mode to improve compatibility with some slow access points
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    
    start_time = utime.time()
    
    print("Connecting to WiFi...")
    while not wlan.isconnected() and (utime.time() - start_time) < timeout_seconds:
        utime.sleep(0.5)
        
    print("Connected to WiFi")
    is_connected = wlan.isconnected()

def set_time():
    try:
        print("Setting time...")
        ntptime.settime()
        print("Time set:", utime.localtime())
    except OSError:
        pass

def get_show_information():
    try:
        from secrets import PRODUCTION_URL
    except ImportError:
        print("Create secrets.py with the production URL")
        return
    
    try:
        print("Fetching production data...")
        response = urequests.get(PRODUCTION_URL)
        
        if response.status_code == 200:
            production = json.loads(response.text)
            print("Show Time:", production["showtime"])
            
            for element in production["structure"]:
                name = element["name"]
                duration = element["duration"]
                
                print("Name:", name)
                print("Duration:", duration, "minutes")
                
                if "scenes" in element:
                    for scene in element["scenes"]:
                        scene_name = scene["name"]
                        scene_duration = scene["duration"]
                        
                        print("Scene:", scene_name)
                        print("Duration:", scene_duration, "minutes")
        elif response.status_code == 404:
            print("Production data not found")
        else:
            print("Failed to fetch data. Status Code:", response.status_code)
    except Exception as e:
        print("Error occurred:", e)
        return
    finally:
        if response:
            response.close()
    
    # Begin "Places"
    places.galactic_unicorn = galactic_unicorn
    places.graphics = graphics
    places.init()

connect_to_wifi()

if is_connected:
    set_time()
    get_show_information()
else:
    # TODO: Or maybe just show the time or do nothing?
    connect_to_wifi()

while True:
    current_time = utime.localtime()
    hour = current_time[3]
    hour_12 = hour % 12 if hour != 0 else 12
    minute = current_time[4]
    second = current_time[5]
    am_pm = "AM" if hour < 12 else "PM"
    
    print("Light:", galactic_unicorn.light())
    print("Current time:", "{:02d}:{:02d}:{:02d} {}".format(hour_12, minute, second, am_pm))
    places.draw(str(time_remaining))
    time_remaining -= 1
    time.sleep(1)