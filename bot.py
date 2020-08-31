import discord
import os
import asyncio
import io
import json
import datetime
import calendar

"""
{
    "user" : string,
    "names" : {
        "1": string,
        "2": string,
        "3": string,
        "4": string
    }
    "links" : {
        "1" : string,
        "2" : string,
        "3" : string,
        "4" : string
    }
}
"""





FILE_PATH = os.path.dirname(os.path.abspath( __file__ ))

def get_secret():
    with open(FILE_PATH + "\secret.txt", "r+") as secret_txt:
        secret = secret_txt.readlines()[0]
        return secret

def get_data():
    with open(FILE_PATH + "\data.txt", "r+") as data_txt:
        data = data_txt.readlines()
        return [json.loads(x) for x in data]

def get_user_data(datalist, user):
    for x in datalist:
        if x['user'] == user:
            return x
    return create_empty_object(user)

def change_user_data(datalist, user_data):
    for x in datalist:
        if x['user'] == user_data['user']:
            datalist[datalist.index(x)] = user_data
            return datalist
    datalist.append(user_data)
    return datalist

def delete_user_data(datalist, user_data):
    for x in datalist:
        if x['user'] == user_data['user']:
            datalist.pop(datalist.index(x))
    change_data(datalist)

def change_data(changed_list):
    with open(FILE_PATH + "\data.txt", "w+") as data_txt:
        changed_list = [json.dumps(x) for x in changed_list]
        data_txt.writelines(changed_list)

def create_empty_object(user_mention):
    return {"user" : user_mention, "names" : {"1" : "nothing", "2" : "nothing", "3" : "nothing", "4" : "nothing"}, "links" : {"1" : "fortnite.com", "2" : "epicgames.com", "3" : "bing.com", "4" : "netscape.com"}}
 
class MyClient(discord.Client): 
    async def on_ready(self):
        print('Schedulebot Up')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        messagecapitalization = message.content
        themessage = message.content.lower()
        if message.author.id == self.user.id:
            return
        if self.user not in message.mentions:
            return
        userdata = get_user_data(get_data(),str(message.author.mention))
        messagecapitalization = [x.strip() for x in messagecapitalization.replace("<@!749979907282436166>","").split("-")]
        themessage = [x.strip() for x in themessage.replace("<@!749979907282436166>","").split("-")]
        if themessage[0] == "create":
            messagecapitalization.pop(0)
            for x in messagecapitalization:
                userdata['names'][x[0]] = x[2:].split("@")[0].strip()
                userdata['links'][x[0]] = x[2:].split("@")[1].strip()
            change_data(change_user_data(get_data(),userdata))
            await message.channel.send(f"Schedule created for {userdata['user']}")    
        if themessage[0] == "modify":
            messagecapitalization.pop(0)
            for x in messagecapitalization:
                print(x)
                userdata['names'][x[0]] = x[2:].split("@")[0].strip()
                userdata['links'][x[0]] = x[2:].split("@")[1].strip()
            change_data(change_user_data(get_data(),userdata))
            await message.channel.send(f"Schedule modified for {userdata['user']}")
        if themessage[0] == "delete":
            delete_user_data(get_data(),userdata)
            await message.channel.send(f"Schedule deleted for {userdata['user']}")
        if themessage[0] == "list":
            listembed = discord.Embed(title = f"**Schedule for {message.author.name}**", description = f"**Block 1:** [{userdata['names']['1']}]({userdata['links']['1']})\n**Block 2:** [{userdata['names']['2']}]({userdata['links']['2']})\n**Block 3:** [{userdata['names']['3']}]({userdata['links']['3']})\n**Block 4:** [{userdata['names']['4']}]({userdata['links']['4']})")
            await message.channel.send(embed=listembed)              
        if themessage[0] == "now":
            time = datetime.datetime.now()
            hour = int(time.strftime("%H"))
            minute = int(time.strftime("%M"))
            weekday = time.weekday()
            period = '0'
            if weekday == 0:
                if hour == 8:
                    period = "1"
                elif hour == 9:
                    if minute <= 50:
                        period = "1"
                    elif minute > 50:
                        period = "2"
                elif hour == 10:
                    period = "2"
                elif hour == 11:
                    if minute <= 20:
                        period = "2"
                    elif minute > 20:
                        period = "1"
                elif hour == 12:
                    if minute == 0:
                        period = "1"
                    elif minute > 20:
                        period = "3"
                elif hour == 13:
                    if minute <= 5:
                        period = "3"
                    elif minute > 5 and minute <= 45:
                        period = "4"
            if weekday == 1:
                if hour == 8:
                    period = "3"
                elif hour == 9:
                    if minute <= 50:
                        period = "3"
                    elif minute > 50:
                        period = "4"
                elif hour == 10:
                    period = "4"
                elif hour == 11:
                    if minute <= 20:
                         period = "4"
                    elif minute > 20:
                        period = "2"
                elif hour == 12:
                    if minute == 0:
                        period = "2"
                    elif minute > 20:
                        period = "1"
                elif hour == 13:
                    if minute <= 5:
                        period = "1"
                    elif minute > 5 and minute <= 45:
                        period = "2"
            if weekday == 3:
                if hour == 8:
                    period = "1"
                elif hour == 9:
                    if minute <= 50:
                        period = "1"
                    elif minute > 50:
                        period = "2"
                elif hour == 10:
                    period = "2"
                elif hour == 11:
                    if minute <= 20:
                         period = "2"
                    elif minute > 20:
                        period = "3"
                elif hour == 12:
                    if minute == 0:
                        period = "3"
                    elif minute > 20:
                        period = "3"
                elif hour == 13:
                    if minute <= 5:
                        period = "3"
                    elif minute > 5 and minute <= 45:
                        period = "4"
            if weekday == 4:
                if hour == 8:
                    period = "3"
                elif hour == 9:
                    if minute <= 50:
                        period = "3"
                    elif minute > 50:
                        period = "4"
                elif hour == 10:
                    period = "4"
                elif hour == 11:
                    if minute <= 20:
                         period = "4"
                    elif minute > 20:
                        period = "4"
                elif hour == 12:
                    if minute == 0:
                        period = "4"
                    elif minute > 20:
                        period = "1"
                elif hour == 13:
                    if minute <= 5:
                        period = "1"
                    elif minute > 5 and minute <= 45:
                        period = "2"
            if weekday == 2:
                if hour == 9:
                    if minute > 50:
                        period = "1"
                elif hour == 10:
                    if minute <= 35:
                        period = "1"
                    elif minute > 35:
                        period = "2"
                elif hour == 11:
                    if minute <= 20:
                         period = "2"
                elif hour == 12:
                    if minute > 20:
                        period = "3"
                elif hour == 13:
                    if minute <= 5:
                        period = "3"
                    elif minute > 5 and minute <= 45:
                        period = "4"
            if period == "0":
                await message.channel.send(f"{userdata['user']}, you do not have any classes right now")
            else:
                nowembed = discord.Embed(title = f"**Class right now for {message.author.name}**", description = f"[{userdata['names'][period]}]({userdata['links'][period]})", url=userdata['links'][period])
                await message.channel.send(embed = nowembed)
        
client = MyClient()
client.run(get_secret())
