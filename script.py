#!/usr/bin/python3

import time
import os
import urllib3
import urllib.request
import json

# URL to get JSON data to then find the link to the picture
BING_JSON_URL = "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1"

# Get directory to the resource folder
resourceFolder = os.path.dirname(os.path.realpath(__file__)) + "/res/"

if not os.path.exists(resourceFolder):
    os.mkdir(resourceFolder)

# Attempt to get JSON data
ATTEMPTS = 5
counter = 0

http = urllib3.PoolManager()
response = None

while counter < ATTEMPTS:
    try:
        response = http.request("GET", BING_JSON_URL, timeout=2)
        break
    except urllib3.exceptions.MaxRetryError:
        counter += 1
        time.sleep(5)

if response is None:
    raise Exception("Could not get data from Bing. Check your internet connection")

# Parse JSON Data
jsonData = json.loads(response.data.decode("utf-8"))
imageURLExtension = jsonData["images"][0]["url"]
fileName = jsonData["images"][0]["copyright"].replace("/", " ")  # Remove "/" because causes error

# Save image from URL to file
urllib.request.urlretrieve("http://www.bing.com" + imageURLExtension, resourceFolder + fileName)

# Update Gnome background
os.system('gsettings set org.gnome.desktop.background picture-uri' + ' "file://' + resourceFolder + fileName + '"')
