#!/usr/bin/env python3
import requests
import socket
import json
import sys
import time
import argparse
import os
from zeroconf import ServiceBrowser, Zeroconf

# Credit to https://github.com/adamesch/elgato-key-light-api for work done in documenting the REST-style API.

data_dir = os.environ.get('SNAP_USER_DATA') or "."

SETTINGS_FILE = os.path.join(data_dir,"keylight_settings.json")
SETTINGS_SET = (
    "default"  # support multiple settings to enable saved profiles in a future version
)


def get_all_saved_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            all_settings_sets = json.load(f)
            return all_settings_sets
    else:
        return None


def get_saved_settings():
    all_settings_sets = get_all_saved_settings()
    if all_settings_sets:
        saved_settings = all_settings_sets.get(SETTINGS_SET)
    else:
        saved_settings = None

    return saved_settings or {"bright": 50, "temp": 4000, "ip": "auto"}


def save_settings(settings):
    all_settings_saved = get_all_saved_settings() or {}
    all_settings_saved[SETTINGS_SET] = settings
    with open(SETTINGS_FILE, "w") as f:
        json.dump(all_settings_saved, f)


def get_light_data(ip):
    response = requests.get(f"http://{ip}:9123/elgato/lights")
    if response.status_code == 200:
        return response.json()
    else:
        return None


def send_light_data(ip, brightness, temperature):
    data = {
        "numberOfLights": 1,
        "lights": [
            {
                "on": 1 if brightness > 0 else 0,
                "brightness": brightness,
                "temperature": temperature,
            }
        ],
    }

    data_json = json.dumps(data)

    # Execute the PUT request
    response = requests.put(
        f"http://{ip}:9123/elgato/lights",
        headers={"Accept": "application/json"},
        data=data_json,
    )


class MyListener:
    def __init__(self, target_name):
        self.target_name = target_name
        self.target_address = None

    def remove_service(self, zeroconf, type, name):
        pass

    def update_service(self, zeroconf, type, name):
        pass

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        if info and self.target_name.lower() in info.name.lower():
            self.target_address = socket.inet_ntoa(info.addresses[0])


def find_avahi_ip(service_name, timeout):
    zeroconf = Zeroconf()
    listener = MyListener(service_name)
    browser = ServiceBrowser(zeroconf, "_elg._tcp.local.", listener)

    start_time = time.time()
    while time.time() - start_time < timeout:
        if listener.target_address is not None:
            break
        time.sleep(0.1)

    zeroconf.close()
    return listener.target_address


def main():
    parser = argparse.ArgumentParser(
        description="Sets brightness and color temperature of an Elgato keylight. It assumes there is only one such light. ip of auto will attempt to find the IP address of the lamp. " +
        "Avoiding ip=auto after you have used it once is faster because the saved IP address is used."
    )
    parser.add_argument(
        "--bright", type=int, help="set brightness, 0 to 100. O will turn lamp off"
    )
    parser.add_argument("--temp", type=int, help="set color K. Range is 2900K to 7000K")
    parser.add_argument(
        "--ip", type=str, help="Use auto to find it with avahi aka zeroconf, otherwise provide an IPV4 address."
    )

    args = parser.parse_args()

    last_settings = get_saved_settings()

    elgato_ip = args.ip if args.ip else last_settings["ip"]
    if elgato_ip == "auto":
        elgato_ip = find_avahi_ip(service_name="elgato", timeout=5)
        if not elgato_ip:
            raise RuntimeError(
                "Could not find the IP address of the elgato light. You could try to pass the IP address e.g. --ip=192.168.1.55"
            )

    brightness = args.bright if args.bright is not None else last_settings["bright"]
    temperature_kelvin = args.temp if args.temp else last_settings["temp"]

    if not temperature_kelvin:
        existing_values = get_light_data(elgato_ip)
        temperature = existing_values["lights"][0]["temperature"]
    else:
        temperature = int(temperature_kelvin / 20.34)

    send_light_data(elgato_ip, brightness, temperature)

    new_settings = {"bright": brightness, "temp": temperature_kelvin, "ip": elgato_ip}
    save_settings(new_settings)

if __name__ == "__main__":
    main()    
