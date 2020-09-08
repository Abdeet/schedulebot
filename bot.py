import discord
import os
import asyncio
import io
import json
import datetime
import calendar
import re
import math

"""
{
    "user" : string,
    "ib" : boolean
    "names" : {
        "1": string,
        "2": string,
        "3": string,
        "4": string,
        *"5": string,
        *"6": string,
        *"7": string,
    }
    "links" : {
        "1": string,
        "2": string,
        "3": string,
        "4": string,
        *"5": string,
        *"6": string,
        *"7": string,
    }
}
"""





FILE_PATH = os.path.dirname(os.path.abspath( __file__ ))

def get_secret():
    with open(FILE_PATH + "/secret.txt", "r+") as secret_txt:
        secret = secret_txt.readlines()[0]
        return secret

def get_data():
    with open(FILE_PATH + "/data.txt", "r+") as data_txt:
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
    with open(FILE_PATH + "/data.txt", "w+") as data_txt:
        changed_list = [json.dumps(x) + "\n" for x in changed_list]
        data_txt.writelines(changed_list)

def create_empty_object(user_mention):
    return {"user" : user_mention,"ib" : False, "names" : {"1" : "nothing", "2" : "nothing", "3" : "nothing", "4" : "nothing"}, "links" : {"1" : "fortnite.com", "2" : "epicgames.com", "3" : "bing.com", "4" : "netscape.com"}}
 
def get_mentioned_roles(message):
    roles = re.findall(r"<@&[0-9]+>",message)
    roles = [role.replace("!","").replace("&","").replace("@","").strip("<").strip(">") for role in roles]
    return roles

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
        mentions = [str(mention.id) for mention in message.mentions]
        mentions = [x.replace("!","").replace("&","").replace("@","").strip("<").strip(">") for x in mentions]
        roles = get_mentioned_roles(message.content)
        if str(self.user.id) not in mentions:
            yes = False
            for role in message.guild.get_member(self.user.id).roles:
                if str(role.id) in roles:
                    messagecapitalization = messagecapitalization.replace(f"<@&{str(role.id)}>","").replace(f"<@{str(role.id)}>","").replace(f"<@!{str(role.id)}>","")
                    themessage = themessage.replace(f"<@&{str(role.id)}>","").replace(f"<@{str(role.id)}>","").replace(f"<@!{str(role.id)}>","")
                    yes = True
                    break
            if not yes:
                return
        userdata = get_user_data(get_data(),str(message.author.id))
        try:
            ib = userdata['ib']
        except:
            ib = 0
        messagecapitalization = [x.strip() for x in messagecapitalization.replace("<@!749979907282436166>","").replace("<@749979907282436166>","").replace("<@&749979907282436166>","").split("-")]
        themessage = [x.strip() for x in themessage.replace("<@!749979907282436166>","").replace("<@749979907282436166>","").replace("<@&749979907282436166>","").split("-")]
        if "create" in themessage[0]:
            messagecapitalization.pop(0)
            for x in messagecapitalization:
                userdata['names'][x[0]] = x[2:].split("@")[0].strip()
                userdata['links'][x[0]] = x[2:].split("@")[1].strip()
            if len(userdata['names']) > 4:
                userdata['ib'] = 1
            else:
                userdata['ib'] = 0
            change_data(change_user_data(get_data(),userdata))
            await message.channel.send(f"Schedule created for {message.author.mention}")    
        if "modify" in themessage[0]:
            messagecapitalization.pop(0)
            for x in messagecapitalization:
                userdata['names'][x[0]] = x[2:].split("@")[0].strip()
                userdata['links'][x[0]] = x[2:].split("@")[1].strip()
            if len(userdata['names']) > 4:
                userdata['ib'] = 1
            else:
                userdata['ib'] = 0
            change_data(change_user_data(get_data(),userdata))
            await message.channel.send(f"Schedule modified for {message.author.mention}")
        if "delete" in themessage[0]:
            delete_user_data(get_data(),userdata)
            await message.channel.send(f"Schedule deleted for {message.author.mention}")
        if "list" in themessage[0]:
            if not int(ib):
                listembed = discord.Embed(title = f"**Schedule for {message.author.name}**", description = f"**Block 1:** [{userdata['names']['1']}]({userdata['links']['1']})\n**Block 2:** [{userdata['names']['2']}]({userdata['links']['2']})\n**Block 3:** [{userdata['names']['3']}]({userdata['links']['3']})\n**Block 4:** [{userdata['names']['4']}]({userdata['links']['4']})")
            elif int(ib):
                listembed = discord.Embed(title = f"**Schedule for {message.author.name}**", description = f"**Block 1:** [{userdata['names']['1']}]({userdata['links']['1']})\n**Block 2:** [{userdata['names']['2']}]({userdata['links']['2']})\n**Block 3:** [{userdata['names']['3']}]({userdata['links']['3']})\n**Block 4:** [{userdata['names']['4']}]({userdata['links']['4']})\n**Block 5:** [{userdata['names']['5']}]({userdata['links']['5']})\n**Block 6:** [{userdata['names']['6']}]({userdata['links']['6']})\n**Block 7:** [{userdata['names']['7']}]({userdata['links']['7']})")
            await message.channel.send(embed=listembed)              
        if "now" in themessage[0]:
            d202098 = datetime.date(2020,9,8)
            time = datetime.datetime.now()
            date = time.date()
            week_diff = math.floor((date - d202098).days / 7) % 2
            a_week = 0
            b_week = 1
            hour = int(time.strftime("%H"))
            minute = int(time.strftime("%M"))
            weekday = time.weekday()
            period = '0'
            if not int(ib):
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
            elif int(ib):
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
                            if week_diff == a_week:
                                period = "1"
                            elif week_diff == b_week:
                                period = "5"
                    elif hour == 12:
                        if minute == 0:
                            if week_diff == a_week:
                                period = "1"
                            elif week_diff == b_week:
                                period = "5"
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
                            if week_diff == a_week:
                                period = "2"
                            elif week_diff == b_week:
                                period = "6"
                    elif hour == 12:
                        if minute == 0:
                            if week_diff == a_week:
                                period = "2"
                            elif week_diff == b_week:
                                period = "6"
                        elif minute > 20:
                            period = "1"
                    elif hour == 13:
                        if minute <= 5:
                            period = "1"
                        elif minute > 5 and minute <= 45:
                            period = "2"
                if weekday == 3:
                    if hour == 8:
                        period = "5"
                    elif hour == 9:
                        if minute <= 50:
                            period = "5"
                        elif minute > 50:
                            period = "6"
                    elif hour == 10:
                        period = "6"
                    elif hour == 11:
                        if minute <= 20:
                            period = "6"
                        elif minute > 20:
                            if week_diff == a_week:
                                period = "3"
                            elif week_diff == b_week:
                                period = "7"
                    elif hour == 12:
                        if minute == 0:
                            if week_diff == a_week:
                                period = "3"
                            elif week_diff == b_week:
                                period = "7"
                        elif minute > 20:
                            period = "7"
                    elif hour == 13:
                        if minute <= 5:
                            period = "7"
                        elif minute > 5 and minute <= 45:
                            period = "4"
                if weekday == 4:
                    if hour == 8:
                        period = "7"
                    elif hour == 9:
                        if minute <= 50:
                            period = "7"
                        elif minute > 50:
                            period = "4"
                    elif hour == 10:
                        period = "4"
                    elif hour == 11:
                        if minute <= 20:
                            period = "4"
                        elif minute > 20:
                            if week_diff == a_week:
                                period = "4"
                            elif week_diff == b_week:
                                period = "4"
                    elif hour == 12:
                        if minute == 0:
                            if week_diff == a_week:
                                period = "4"
                            elif week_diff == b_week:
                                period = "4"
                        elif minute > 20:
                            period = "5"
                    elif hour == 13:
                        if minute <= 5:
                            period = "5"
                        elif minute > 5 and minute <= 45:
                            period = "6"
                if weekday == 2:
                    if week_diff == a_week:
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
                    elif week_diff == b_week:
                        if hour == 9:
                            if minute > 50:
                                period = "5"
                        elif hour == 10:
                            if minute <= 35:
                                period = "5"
                            elif minute > 35:
                                period = "6"
                        elif hour == 11:
                            if minute <= 20:
                                period = "6"
                        elif hour == 12:
                            if minute > 20:
                                period = "7"
                        elif hour == 13:
                            if minute <= 5:
                                period = "7"
                            elif minute > 5 and minute <= 45:
                                period = "4"
            if period == "0":
                await message.channel.send(f"{message.author.mention}, you do not have any classes right now")
            elif period == "8":
                await message.channel.send(f"{message.author.mention}, we do not have IB now functionality yet. For now please use list instead. @abdeet if you have a copy of the schedule so abhi can implement now")
            else:
                nowembed = discord.Embed(title = f"**Class right now for {message.author.name}**", description = f"[{userdata['names'][period]}]({userdata['links'][period]})")
                await message.channel.send(embed = nowembed)
        if themessage[0] == "info":
            await message.channel.send("**Schedulebot by Abdeet**\n\nSchedulebot allows you to keep track of your classes and meeting links by doing all the remembering stuff for you.\n\nTo create a new schedule for yourself, type in `@Schedulebot create -1 [classname]@[link] -2 [classname]@[link] -3 [classname]@[link] -4 [classname]@[link]`\n\nFor exampple:\n`@Schedulebot create -1 Shully@https://www.meet.google.com -2 Miller@https://www.google.com -3 Eisenhower@https://www.fortnite.com -4 JFK@https://www.reddit.com`\n\nIt is VERY important that the links have either http:// or https:// at the start.\n\nTo modify your schedule use `@Schedulebot modify -[blocknumber] [classname]@[link]`\nExample: `@Schedulebot modify -2 test@http://example.com`\n\nTo delete your schedule just type in `@Schedulebot delete`\n\nTo list your schedule type `@Schedulebot list` and to see what class you have now type in `@Schedulebot now`\n\nThat's all there is to it and if you have a question or there is a bug message <@333600742386565120>")
        if "meeting" in themessage[0]:
            custom_rooms = message.guild.get_channel(752942661018845273)
            people = message.mentions
            channel_name = messagecapitalization[1]
            overwrites_object = {
                message.guild.default_role : discord.PermissionOverwrite(read_messages=False, send_messages = False),
                message.guild.get_role(687996857653264393) : discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
            for person in people:
                    overwrites_object[person] = discord.PermissionOverwrite(read_messages=True,send_messages=True, manage_channels=True)
            await message.guild.create_text_channel(channel_name, overwrites = overwrites_object,category = custom_rooms)

client = MyClient()
client.run(get_secret())
