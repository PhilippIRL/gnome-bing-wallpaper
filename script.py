#!/usr/bin/env python3
import sys
if sys.version_info[0] < 3: # raise an exception in case of running under python2 environment.
    raise BaseException('Please run under python3 environment.')

import os, requests, json, pathlib

countryCode='en-US' # country code, e.g. en-US or de-DE

current_dir = os.path.dirname(os.path.realpath(__file__))   # get this script current path.
base_url = 'http://www.bing.com'    # bing website base url.
hpimagearchive_url = '/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=%s' % countryCode  # this part makes a request to get image of the day.
target_image = None # target image to set as wallpaper.


def get_image_link():
    """
        Fetches json object received from bing.com and gets target image link.
    """

    GET_DATA = requests.get(base_url + hpimagearchive_url)  # send a get request to bing.com to read json data.
    json_obj = json.loads(GET_DATA.content.decode('utf-8'))
    return json_obj['images'][0]['url']


def download_image(img_link):
    """
        Checks for a valid full-size image file and if valid, downloads the image.
    """

    if img_link is not None:  # ensure that we got a valid full-size jpeg background image.
        img = requests.get(img_link)    # download image.
        img_file = open(os.path.join(current_dir, 'img', img_link.split('/')[-1]), 'wb')  # create file named with last part of the url.
        img_file.write(img.content) # write bytes to file.
        img_file.close()
        return img_file.name
    return None


def set_wallpaper():
    """
        Downloads and sets received image from bing.com as gnome current wallpaper.
    """

    name = download_image(base_url + get_image_link())  # make complete image link and download it.
    path = os.path.join(current_dir, 'img', name)  # get image full path.
    uri = pathlib.Path(path).as_uri() # get image path as uri

    # create command string to change the desktop wallpaper
    cmd_set_last_image = 'gsettings set org.gnome.desktop.background picture-uri {0}'.format(uri)

    # execute generated command above using os module although this can be done using subprocess module.
    os.system(cmd_set_last_image)


set_wallpaper() # call set_wallpaper to download and set background image.
