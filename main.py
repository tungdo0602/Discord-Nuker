import requests
import threading
import os
import colorama
from colorama import *
import random
import json
import base64
import time

isIdling = False
isIdling2 = False

config = {"threads": 10,"proxy_timeout": 6000,"guildId": "", "channelId": "", "channelName": "", "channelType": 0, "Message": "", "webhookName": "ABC", "adminToken": ""}
webhookURL = []
try:
    if os.stat("config.json").st_size == 0:
        with open("config.json", "w") as f:
            json.dump(config, f, indent=2)
        print("Successfully Write the config!")
except:
    with open("config.json", "a+") as f:
        json.dump(config, f, indent=2)
    print("Successfully Write the config!")


with open("config.json", "r") as config_file:
    data = json.load(config_file)

proxies = set()
with open("proxies.txt", "r") as f1:
    fl1 = f1.readlines()
    for line in fl1:
        proxies.add(line.strip())

if os.stat("tokens.txt").st_size == 0:
    print("You need to fill tokens.txt with token dumb!")
    exit()

tokens = set()
with open("tokens.txt", "r") as f2:
    fl2 = f2.readlines()
    for line in fl2:
        tokens.add(line.strip())

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def createChannel(token, guildId, channelName="new-channel", type=0, message=None):
    global proxies
    proxy = random.choice(list(proxies))
    proxy_form = {'http': f"socks4://{proxy}", 'https': f"socks4://{proxy}"}
    try:
        cc = requests.post(f"https://discord.com/api/v9/guilds/{guildId}/channels", headers={"authorization": token}, json={"type":type,"name":channelName,"permission_overwrites":[]}, proxies=proxy_form, timeout=data["proxy_timeout"])
        channelId = cc.json().get("id")
        if cc.status_code == 201:
            if message != None:
                try:
                    requests.post(f"https://discord.com/api/v9/channels/{channelId}/messages", headers={"authorization": token}, json={"content": message,"tts": False}, proxies=proxy_form, timeout=data["proxy_timeout"])
                except:
                    pass
            print(Fore.GREEN + "Created!", end="\n")
        else:
            print(Fore.RED + f"Failed to Create channel! | {cc.status_code}", end="\n")
    except:
        pass

def sendMessage(token, channelid, content):
    global isIdling
    global proxies
    proxy = random.choice(list(proxies))
    proxy_form = {'http': f"socks4://{proxy}", 'https': f"socks4://{proxy}"}
    try:
        sm = requests.post(f"https://discord.com/api/v9/channels/{channelid}/messages", headers={"authorization": token}, json={"content": content,"tts": False}, proxies=proxy_form, timeout=data["proxy_timeout"])
        if sm.status_code == 200:
            print(Fore.GREEN + "Sent!", end="\n")
        elif sm.status_code == 429:
            if isIdling == False:
                print(Fore.RED + "Rate limit! retry after: {}".format(sm.json().get("retry_after")))
                isIdling = True
                time.sleep(int(sm.json().get("retry_after")))
                isIdling = False
        else:
            print(Fore.RED + f"Failed to send! | {sm.status_code}", end="\n")
    except:
        pass

def joinGuild(token, inviteCode):
    inviteData = requests.get(f'https://discord.com/api/v9/invites/{inviteCode}')
    if inviteData.status_code == 200:
        inviteGuild = inviteData.json().get("guild").get("id")
        inviteChannel = inviteData.json().get("channel").get("id")
        inviteChannelType = inviteData.json().get("channel").get("type")
        magicStuff = str(base64.b64encode((f'{{"location":"Join Guild","location_guild_id":{inviteGuild},"location_channel_id":{inviteChannel},"location_channel_type":{inviteChannelType}}}').encode('ascii'))).split("'")[1]
    else:
        print(Fore.RED + "Invaild Invite Code!")
        exit()
    headers = {
    "accept": "*/*",
    "accept-language": "en,vi;q=0.9,vi-VN;q=0.8,en-US;q=0.7",
    "authorization": token,
    "content-type": "application/json",
    "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"98\", \"Google Chrome\";v=\"98\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "x-debug-options": "bugReporterEnabled",
    "x-context-properties": magicStuff,
    "x-discord-locale": "en-US",
    "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzk4LjAuNDc1OC4xMDIgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6Ijk4LjAuNDc1OC4xMDIiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTE2MjE2LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=="
    }
    try:
        joiner = requests.post(f"https://discord.com/api/v9/invites/{inviteCode}", headers=headers, json={})
        if joiner.status_code == 200:
            print(Fore.GREEN + "Sent!", end="\n")
        else:
            print(Fore.RED + f"Failed to Join server! | {joiner.status_code} {joiner.json()}", end="\n")
    except:
        pass 

cls()
def spam():
    global data
    while True:
        for token in tokens:
            sendMessage(token, data["channelId"], data["Message"])

def spamChannel():
    global data
    while True:
        for token in tokens:
            createChannel(token, data["guildId"], data["channelName"], data["channelType"], data["Message"])

def Inviter():
    inviteCode = input("Invite Code: ")
    for token in tokens:
        joinGuild(token, inviteCode)

def createWebhook(token, channelId, webhookName):
    a = requests.post(f"https://discord.com/api/v9/channels/{channelId}/webhooks", headers={"authorization": token}, json={"name": webhookName})
    if a.status_code == 200:
        return {"token": a.json().get("token"), "id": a.json().get("id")}
    else:
        print(Fore.RED + "Couldn't create webhook!")

def sendWebhookMessage(whURL, message, username="Bot"):
    global proxies
    global isIdling2
    proxy = random.choice(list(proxies))
    proxy_form = {'http': f"socks4://{proxy}", 'https': f"socks4://{proxy}"}
    try:
        a = requests.post(whURL, json={"content": message, "username": username}, proxies=proxy_form, timeout=data["proxy_timeout"])
        if a.status_code == 200:
            print(Fore.GREEN + "Successfully Send the message!")
        elif a.status_code == 429:
            if isIdling2 == False:
                print(Fore.RED + "Rate limit! retry after: {}".format(a.json().get("retry_after")))
                isIdling2 = True
                time.sleep(int(a.json().get("retry_after")))
                isIdling2 = False
        else:
            print(Fore.RED + "Failed to send the message!")
    except:
        pass

def whSpammer():
    global webhookURL
    while True:
        for i in webhookURL:
            sendWebhookMessage(i, data['Message'])

def main():
    global webhookId
    global webhookToken
    print(f"""
{Fore.LIGHTBLUE_EX}
██████╗░██╗░██████╗░█████╗░░█████╗░██████╗░██████╗░  ███╗░░██╗██╗░░░██╗██╗░░██╗███████╗██████╗░
██╔══██╗██║██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗  ████╗░██║██║░░░██║██║░██╔╝██╔════╝██╔══██╗
██║░░██║██║╚█████╗░██║░░╚═╝██║░░██║██████╔╝██║░░██║  ██╔██╗██║██║░░░██║█████═╝░█████╗░░██████╔╝
██║░░██║██║░╚═══██╗██║░░██╗██║░░██║██╔══██╗██║░░██║  ██║╚████║██║░░░██║██╔═██╗░██╔══╝░░██╔══██╗
██████╔╝██║██████╔╝╚█████╔╝╚█████╔╝██║░░██║██████╔╝  ██║░╚███║╚██████╔╝██║░╚██╗███████╗██║░░██║
╚═════╝░╚═╝╚═════╝░░╚════╝░░╚════╝░╚═╝░░╚═╝╚═════╝░  ╚═╝░░╚══╝░╚═════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝
{Fore.RESET}
[1] Spam message
[2] Mass Channel Creator
[3] Mass Token Joiner (WIP)
[4] Webhook Creator
[5] Webhook Spammer
""")
    mode = input("Mode: ")
    cls()
    if mode == "1":
        for i in range(data["threads"]):
            threading.Thread(target=spam).start()
    elif mode == "2":
        for i in range(data["threads"]):
            threading.Thread(target=spamChannel).start()
    elif mode == "3":
        Inviter()
    elif mode == "4":
        whc = int(input("How Many Webhook: "))
        cid = input("Channel Id: ")
        for i in range(whc):
            try:
                webhookGen = createWebhook(data['adminToken'], cid, data["webhookName"])
                whTk = webhookGen.get("token")
                whId = webhookGen.get("id")
                webhookURL.append(f"https://discord.com/api/webhooks/{whId}/{whTk}")
            except:
                pass
        return main()
    elif mode == "5":
        for i in range(data["threads"]):
            threading.Thread(target=whSpammer).start()
    
if __name__ == '__main__':
    main()
