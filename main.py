import machine, time, network, ntptime
import splashscreen, places
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY

# Variables
is_connected = False

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
    print("Create secrets.py with your WiFi credentials to get time from NTP")
    wifi_available = False

# Connect to WiFi and synchronize the RTC time from NTP
def connect_to_wifi():
    if not wifi_available:
        return
    
    global is_connected

    # Start connection
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm=0xa11140)  # Turn WiFi power saving off for some slow APs
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    # Wait for connect success or failure
    max_wait = 100
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print("Waiting for connection...")
        time.sleep(0.2)

    if max_wait > 0:
        is_connected = True
        print("Connected")

        try:
            ntptime.settime()
            print("Time set")
        except OSError:
            pass

    wlan.disconnect()
    wlan.active(False)

connect_to_wifi()

if is_connected:
    places.galactic_unicorn = galactic_unicorn
    places.graphics = graphics
    places.init()
else:
    connect_to_wifi()

while True:
    print("Light:", galactic_unicorn.light());
    time.sleep(1)