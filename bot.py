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

class Schedule:
    def __init__(self,user,blocks, clubs = None):
        self.user = int(user)
        self.blocks = blocks
        if clubs == None:
            self.clubs = [Block(1, "Nothing", "None"),Block(2, "Nothing", "None"),Block(3, "Nothing", "None"),Block(4, "Nothing", "None")]
        else: self.clubs = clubs
        self.update_ib()

    def update_ib(self):
        if len(self.blocks) == 7:
            self.ib = 1
        else:
            self.ib = 0
    
    def __dict__(self):
        self.update_ib()
        return_dict = {"user": self.user, "ib" : self.ib, "blocks" : [], "clubs": []}
        for block in self.blocks:
            return_dict["blocks"].append(block.__dict__())
        for club in self.clubs:
            return_dict["blocks"].append(block.__dict__())
        return return_dict

    def get_block_index(self, num, club = False):
        if club:
            for club in self.clubs:
                if int(club.num) == int(num):
                    return self.clubs.index(club)
        else:
            for block in self.blocks:
                if int(block.num) == int(num):
                    return self.blocks.index(block)
        return None

    def get_block(self, num, club = False):
        index = self.get_block_index(int(num), club)
        if index is not None:
            if club:
                return self.clubs[index]
            else:
                return self.blocks[index]
        return None

    def change_block(self, num, name, link, club = False):
        index = self.get_block_index(num, club)
        if index is not None:
            if club:
                self.clubs[index].num = int(num)
                self.clubs[index].name = name
                self.clubs[index].link = link
                return self.clubs[index].__dict__()
            else:
                self.blocks[index].num = int(num)
                self.blocks[index].name = name
                self.blocks[index].link = link
                return self.blocks[index].__dict__()
        else:
            if club:
                self.clubs.append(Block(num,name,link))
                return self.clubs[-1].__dict__()
            else:
                self.blocks.append(Block(num, name, link))
                return self.clubs[-1].__dict__()
        self.update_ib()

class Block:
    def __init__(self,num, name, link):
        self.num = num
        self.name = name
        self.link = link
    
    def __dict__(self):
        return {"num": self.num, "name": self.name, "link": self.link}

FILE_PATH = os.path.dirname(os.path.abspath( __file__ ))

def get_secret():
    with open(FILE_PATH + "/secret.txt", "r+") as secret_txt:
        secret = secret_txt.readlines()[0]
        return secret

def get_data(return_data = False):
    with open(FILE_PATH + "/data.txt", "r+") as data_txt:
        data = data_txt.readlines()
        if return_data:
            return data
        else:
            return [json.loads(x) for x in data]

def get_user_data(datalist, user):
    for x in datalist:
        if x['user'] == user:
            return convert_dict_to_object(x)
    return create_empty_object(user)

def change_user_data(datalist, user_data):
    for x in datalist:
        if x['user'] == user_data.user:
            datalist[datalist.index(x)] = convert_object_to_dict(user_data)
            return datalist
    datalist.append(convert_object_to_dict(user_data))
    return datalist

def delete_user_data(datalist, user_data):
    for x in datalist:
        if x['user'] == user_data.user:
            datalist.pop(datalist.index(x))
    change_data(datalist)

def change_data(changed_list):
    with open(FILE_PATH + "/data.txt", "w+") as data_txt:
        changed_list = [json.dumps(x) + "\n" for x in changed_list]
        data_txt.writelines(changed_list)

def create_empty_object(user_mention, ib = False):
    if not ib:
        return Schedule(user_mention,[Block(1, 'nothing', 'http://example.com'),Block(2, 'nothing', 'http://example.com'),Block(3, 'nothing', 'http://example.com'),Block(4, 'nothing', 'http://example.com')])
    else:
        return Schedule(user_mention,[Block(1, 'nothing', 'http://example.com'),Block(2, 'nothing', 'http://example.com'),Block(3, 'nothing', 'http://example.com'),Block(4, 'nothing', 'http://example.com'),Block(5, 'nothing', 'http://example.com'),Block(6, 'nothing', 'http://example.com'),Block(7, 'nothing', 'http://example.com')])


def get_mentioned_roles(message):
    roles = re.findall(r"<@&[0-9]+>",message)
    roles = [role.replace("!","").replace("&","").replace("@","").strip("<").strip(">") for role in roles]
    return roles

def convert_dict_to_object(dict):
    blocks = []
    clubs = []
    for x in dict['blocks']:
        blocks.append(Block(x['num'],x['name'],x['link']))
    try:
        for x in dict['clubs']:
                clubs.append(Block(x['num'],x['name'],x['link']))
    except:
        clubs = None
    schedule = Schedule(dict['user'],blocks, clubs)
    return schedule

def convert_object_to_dict(schedule):
    new_dict = {
        "user": schedule.user,
        "ib": schedule.ib,
        "blocks": [

        ],
        "clubs": [
            
        ]
    }
    for x in schedule.blocks:
        new_dict['blocks'].append(x.__dict__())
    for x in schedule.clubs:
        new_dict['clubs'].append(x.__dict__())
    return new_dict

def convert_legacy_dict_to_object(legacy_dict):
    classes = []
    for x in range(1,len(legacy_dict['names'])+1):
        classes.append(Block(x,legacy_dict['names'][str(x)],legacy_dict['links'][str(x)]))
    schedule = Schedule(legacy_dict['user'],classes)
    return schedule

prefix_data = []

def load_prefix_data():
    with open(FILE_PATH + "/prefix.txt", "r+") as prefixfile:
        prefixes = prefixfile.readlines()

    return [json.loads(x) for x in prefixes]

def dump_prefix_data(data):
    prefixes = [json.dumps(x) for x in data]
    with open(FILE_PATH + "/prefix.txt", "w+") as prefixfile:
        prefixfile.writelines(prefixes)

def get_prefix(data, server_id):
    for x in data:
        if x['server_id'] == server_id:
            return x['prefix']
    return None

def change_prefix(data, server_id, prefix):
    appended = False
    for x in data:
        if x['server_id'] == server_id:
            x['prefix'] = prefix
            appended = True
    if appended == False:
        data.append({'server_id': server_id, 'prefix': prefix})
    dump_prefix_data(data)
    prefix_data = load_prefix_data()
    return prefix

def is_club_day(day, month, which = False):
    club_days = {9: [24,25], 10: [22,23], 11: [19,20], 12: [17,18], 2: [26], 3: [26], 4: [23]}
    club_day = day in club_days[month]
    if which is False:
        return (club_day, 0)
    else:
        if day == club_days[month][0]:
            return (club_day, 3)
        elif day == club_days[month][1]:
            return (club_day, 4)
        else: return (club_day, 0)

def nowfunction(ib):
    d202098 = datetime.date(2020,9,7)
    time = datetime.datetime.now()
    date = time.date()
    week_diff = math.floor((date - d202098).days / 7) % 2
    a_week = 0
    b_week = 1
    hour = int(time.strftime("%H"))
    minute = int(time.strftime("%M"))
    weekday = time.weekday()
    day = time.day
    month = time.month
    club_day = is_club_day(day, month)
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
    if int(ib):
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
    if club_day[0]:
        if weekday == 3:
            if hour == 13:
                if minute > 35:
                    period = "9"
            elif hour == 14:
                if minute <= 30:
                    period = "9"
                elif minute > 30:
                    period = "10"
            elif hour == 15:
                if minute <= 30:
                    period = "10"
        elif weekday == 4:
            if hour == 13:
                if minute > 35:
                    period = "11"
            elif hour == 14:
                if minute <= 30:
                    period = "11"
                elif minute > 30:
                    period = "12"
            elif hour == 15:
                if minute <= 30:
                    period = "12"
    return period

def display_schedule(user, userdata):
    schedules = {
        "day_template" : {
            0 : ["8:30 - 9:50", "10:00 - 11:20", "11:30 - 12:00 (check in)", "12:00 - 12:30", "12:30 - 1:05 (support)", "1:10 - 1:45 (support)"],
            1 : ["8:30 - 9:50", "10:00 - 11:20", "11:30 - 12:00 (check in)", "12:00 - 12:30", "12:30 - 1:05 (support)", "1:10 - 1:45 (support)"],
            2 : ["10:00 - 10:35", "10:40 - 11:15", "12:00 - 12:30", "12:30 - 1:05", "1:10 - 1:45"],
            3 : ["8:30 - 9:50", "10:00 - 11:20", "11:30 - 12:00 (check in)", "12:00 - 12:30", "12:30 - 1:05 (support)", "1:10 - 1:45 (support)"],
            4 : ["8:30 - 9:50", "10:00 - 11:20", "11:30 - 12:00 (check in)", "12:00 - 12:30", "12:30 - 1:05 (support)", "1:10 - 1:45 (support)"],
            "club_day" : ["1:45 - 2:30 (club)", "2:45 - 3:30 (club)"]
        },
        "regular": {
            0 : [1,2,1,0,3,4],
            1 : [3,4,2,0,1,2],
            2 : [1,2,0,3,4],
            3 : [1,2,3,0,4,3],
            4 : [3,4,4,0,1,2]
        },
        "ib": {
            0 : {
                0 : [1,2,1,0,3,4],
                1 : [3,4,2,0,1,2],
                2 : [1,2,0,3,4],
                3 : [5,6,3,0,7,4],
                4 : [7,4,4,0,5,6]
            },
            1 : {
                0 : [1,2,5,0,3,4],
                1 : [3,4,6,0,1,2],
                2 : [5,6,0,7,4],
                3 : [5,6,7,0,7,4],
                4 : [7,4,4,0,5,6]
            }
        },
        "club" : {
            3: [3,4],
            4: [1,2]
        }
    }
    userdata.change_block(0, "Lunch", "none")
    d202098 = datetime.date(2020,9,7)
    time = datetime.datetime.now()
    date = time.date()
    week_diff = math.floor((date - d202098).days / 7) % 2
    weekday = time.weekday()
    a_week = 0
    b_week = 1
    week_type = a_week if week_diff == 0 else b_week
    day = time.day
    month = time.month
    club_day = is_club_day(day, month, True)
    if userdata.ib:
        schedule_template = schedules["ib"][week_type][weekday]
    else:
        schedule_template = schedules["regular"][weekday]
    schedule = f""
    for x in range(len(schedule_template)):
        schedule += f"**{schedules['day_template'][weekday][x]}**: {'Block' if schedule_template[x] > 0 else ''} {schedule_template[x] if schedule_template[x] > 0 else ''}{' - ' if schedule_template[x] > 0 else ''}**[{userdata.get_block(schedule_template[x]).name}]({userdata.get_block(schedule_template[x]).link})**\n"
    if club_day[0] > 0:
        club_template = schedules["club"][club_day[1]]
        for x in range(len(club_template)):
            schedule += f"**{schedules['day_template']['club_day'][x]}**: Block {club_template[x]} Club - **[{userdata.get_block(club_template[x], True).name}]({userdata.get_block(club_template[x], True).link})**\n"
    return schedule


class MyClient(discord.Client): 
    async def on_ready(self):
        print('Schedulebot Up')
        print(self.user.name)
        print(self.user.id)
        print('------')
        prefix_data = load_prefix_data()

    async def on_message(self, message):
        server_id = message.guild.id
        server_prefix = get_prefix(prefix_data, server_id)
        messagecapitalization = message.content
        themessage = message.content.lower()
        if message.author.id == self.user.id:
            return
        mentions = [str(mention.id) for mention in message.mentions]
        mentions = [x.replace("!","").replace("&","").replace("@","").strip("<").strip(">") for x in mentions]
        roles = get_mentioned_roles(message.content)
        #if "testschedulebot" not in themessage:
            #return
        #if message.author.id != 333600742386565120:
            #return
        if str(self.user.id) not in mentions:
            yes = False
            for role in message.guild.get_member(self.user.id).roles:
                if str(role.id) in roles:
                    messagecapitalization = messagecapitalization.replace(f"<@&{str(role.id)}>","").replace(f"<@{str(role.id)}>","").replace(f"<@!{str(role.id)}>","")
                    themessage = themessage.replace(f"<@&{str(role.id)}>","").replace(f"<@{str(role.id)}>","").replace(f"<@!{str(role.id)}>","")
                    yes = True
                    break
            if not yes:
                if server_prefix is not None:
                    if server_prefix in message.content:
                        pass
                    else: 
                        return
                else:
                    return
        userdata = get_user_data(get_data(),message.author.id)
        ib = userdata.ib
        messagecapitalization = [x.strip() for x in messagecapitalization.replace("<@!749979907282436166>","").replace("<@749979907282436166>","").replace("<@&749979907282436166>","").split("-")]
        themessage = [x.strip() for x in themessage.replace("<@!749979907282436166>","").replace("<@749979907282436166>","").replace("<@&749979907282436166>","").split("-")]
        if themessage[0] == "create":
            messagecapitalization.pop(0)
            for x in messagecapitalization:
                userdata.change_block(x[0], x[2:].split("@")[0].strip(), x[2:].split("@")[1].strip())
            change_data(change_user_data(get_data(),userdata))
            await message.channel.send(f"Schedule created for {message.author.mention}")    
        if themessage[0] == "modify":
            messagecapitalization.pop(0)
            for x in messagecapitalization:
                userdata.change_block(x[0], x[2:].split("@")[0].strip(), x[2:].split("@")[1].strip())
            change_data(change_user_data(get_data(),userdata))
            await message.channel.send(f"Schedule modified for {message.author.mention}")
        if themessage[0] == "delete":
            delete_user_data(get_data(),userdata)
            await message.channel.send(f"Schedule deleted for {message.author.mention}")
        if "list" in themessage[0]:
            description = f""
            clubs = "club" in themessage[0]
            if clubs:
                for x in range(1,5):
                    club = userdata.get_block(x, True)
                    description = description + f"**Club {club.num}:** [{club.name}]({club.link})\n"
            else:
                for x in range(1, 8 if ib else 5):
                    block = userdata.get_block(x)
                    description = description + f"**Block {block.num}:** [{block.name}]({block.link})\n"
            try:
                listembed = discord.Embed(title = f"**Schedule for {message.author.nick if message.author.nick is not None else message.author.name}**", description = description)
            except AttributeError:
                listembed = discord.Embed(title = f"**Schedule for {message.author.name}**", description = description)
            await message.channel.send(embed=listembed)
        if "schedule" in themessage[0]:
            schedule = display_schedule(message.author, userdata)
            listembed = discord.Embed(title = f"**Schedule for {message.author.nick if message.author.nick is not None else message.author.name}**", description = schedule)
            await message.channel.send(embed=listembed)
        if "now" in themessage[0]:
            period = nowfunction(ib)
            if period == "0":
                await message.channel.send(f"{message.author.mention if message.author.mention is not None else message.author.name}, you do not have any classes right now")
            elif period == "8":
                await message.channel.send(f"{message.author.mention if message.author.mention is not None else message.author.name}, we do not have IB now functionality yet. For now please use list instead. @abdeet if you have a copy of the schedule so abhi can implement now")
            else:
                if int(period) > 8:
                    period = str(int(period) - 8)
                    club = userdata.get_block(period, True)
                    try:
                        nowembed = discord.Embed(title = f"**Club right now for {message.author.nick if message.author.nick is not None else message.author.name}**", description = f"[{club.name}]({club.link})")
                    except AttributeError:
                        nowembed = discord.Embed(title = f"**Club right now for {message.author.name}**", description = f"[{club.name}]({club.link})")                        
                else:
                    block = userdata.get_block(period)
                    try:
                        nowembed = discord.Embed(title = f"**Class right now for {message.author.nick if message.author.nick is not None else message.author.name}**", description = f"[{block.name}]({block.link})")
                    except AttributeError:
                        nowembed = discord.Embed(title = f"**Class right now for {message.author.name}**", description = f"[{block.name}]({block.link})")
                await message.channel.send(embed = nowembed)
        if "setup" in themessage[0]:
            await message.channel.send("Check your private messages for a message from me to continue setup. If you don't see one, make sure you have messages from strangers turned on in settings.")
            def checkreply(m):
                return m.author == message.author ##and lowermessage == 'yes'
            club = "club" in themessage[0]
            if club:
                await message.author.send("Welcome to the club schedule creator. Answer these questions to setup your club links.")
                for x in range(1,5):
                    await message.author.send(f"Do you have a club during block {x}? If you do, what is the name? If you do not, reply with `no`. You have two minutes to reply.")
                    msg = await client.wait_for('message', check = checkreply, timeout = 120.0)
                    if msg.content.lower() == "no":
                        name = "Nothing"
                        link = "None"
                    else:
                        name = msg.content
                        await message.author.send(f"What is the Google Meet link for your club during block {x}? Make sure this has the `https://` at the start. You have two minutes to reply.")
                        msg = await client.wait_for('message', check = checkreply, timeout = 120.0)
                        link = msg.content
                        userdata.change_block(x, name, link, club)
                change_data(change_user_data(get_data(),userdata))
                await message.author.send("The setup is done! Check if it worked properly with @schedulebot list clubs and @schedulebot now club.")
            else:
                ib = "ib" in themessage[0]
                if ib:
                    userdata = create_empty_object(userdata.user,True)
                else:
                    userdata = create_empty_object(userdata.user)

                await message.author.send("Welcome to the guided schedule creator. Just follow the steps and you will be done in no time.")
                for x in range(1,8 if ib else 5):
                    await message.author.send(f"What do you have for block {x}? You can name this something descriptive, like `World History with Hontz`. You have two minutes to reply.")
                    msg = await client.wait_for('message', check = checkreply, timeout=120.0)
                    name = msg.content
                    await message.author.send(f"What is your Google Meet link for block {x}? Make sure this has the `https://` at the start. You have two minutes to reply.")
                    msg = await client.wait_for('message', check = checkreply, timeout=120.0)
                    link = msg.content
                    userdata.change_block(x,name,link)
                change_data(change_user_data(get_data(),userdata))
                await message.author.send("The setup is done! Check if it worked properly with @schedulebot list and @schedulebot now.")
        if "change" in themessage[0]:
            await message.channel.send("Check your private messages for a message from me to continue setup. If you don't see one, make sure you have messages from strangers turned on in settings.")
            def checkreply(m):
                return m.author == message.author ##and lowermessage == 'yes'
            while True:
                await message.author.send("What block do you want to change? Example: `4`. If it is a club, write club in front. Example: `club 2`. You have two minutes to reply.")
                msg = await client.wait_for('message', check = checkreply, timeout=120.0)
                club = "club" in msg.content
                int_msg = msg.content.replace("club", "").strip()
                try:
                    num = int(int_msg)
                except:
                    num = None
                if num is not None:
                    block = userdata.get_block(num, club)
                    if block:
                        await message.author.send(f"What do you want to change the name of {'club' if club else 'block'} {num} to? You have two minutes to reply.")
                        msg = await client.wait_for('message', check = checkreply, timeout=120.0)
                        name = msg.content
                        await message.author.send(f"What do you want to change the Google Meet link for {'club' if club else 'block'} {num} to? Make sure this has the `https://` at the start. You have two minutes to reply.")
                        msg = await client.wait_for('message', check = checkreply, timeout=120.0)
                        link = msg.content
                        userdata.change_block(num, name, link, club)
                        await message.author.send(f"Changed {'club' if club else 'block'} {num}!")
                        await message.author.send(f"Do you want to change any more blocks/clubs? Reply with `yes` if you do, and with anything else if you don't. You have two minutes to reply.")
                        msg = await client.wait_for('message', check = checkreply, timeout=120.0)
                        affirmative = True if msg.content.lower() == "yes" else False
                        if not affirmative:
                            break
            change_data(change_user_data(get_data(),userdata))
            await message.author.send("Your schedule has been changed! Check if it worked properly with @schedulebot list clubs and @schedulebot now club.")
        if "authorized data" in themessage[0]:
            if message.author.id == 333600742386565120:
                await message.channel.send("Sending data to authorized user, check your PMs.")
                for x in get_data(True):
                    await message.author.send(f"```{json.dumps(x)}```")        
        if "info" in themessage[0] or "help" in themessage[0]:
            await message.channel.send("**Schedulebot by Abdeet**\n\nSchedulebot allows you to keep track of your classes and meeting links by doing all the remembering stuff for you.\n\nCommands:\n**`setup`** - Recommended for new users\n**`setup ib`** - Recommended for new ib users\n**`setup clubs`** - Setup your clubs\n**`change`** - Change parts of your schedule\n`create [-block name@link]` - Create a new schedule [discouraged, but still supported]\n`modify [-block name@link]` - Modify your schedule [discouraged, but still supported]\n**`delete`** - Delete your schedule\n**`list [clubs]`** - List your classes/clubs\n**`schedule`** - See your schedule for today\n**`now`** - Check what class you have now\n**`info`** or **`help`** - See all of the Schedulebot commands and how to use them\n`prefix` - View the server prefix [administrators can change the prefix]\n`github` - Get the Github link for the code\n`invite` - Invite the bot to your server\nThe syntax to use these commands is `@schedulebot {command} [parameters if necessary]`\n\nThat's all there is to it and if you have a question or there is a bug message <@333600742386565120>")
        if "github" in themessage[0]:
            await message.channel.send("Schedulebot has a GitHub repository!\nhttps://github.com/Abdeet/schedulebot")
        if "invite" in themessage[0]:
            await message.channel.send("To invite Schedulebot to your channel use this link: https://discord.com/api/oauth2/authorize?client_id=749979907282436166&permissions=256000&scope=bot")
        if "prefix" in themessage[0]:
            await message.channel.send(f"This server's command prefix is {server_prefix if server_prefix is not None else '[none set]'}. You can also use <@749979907282436166>")
            if message.author.guild_permissions.administrator:
                def checkreply(m):
                    return m.author == message.author
                await message.channel.send("Would you like to change the prefix? (y/n)")
                msg = await client.wait_for('message', check = checkreply, timeout = 60.0)
                if msg.content == "y":
                    await message.channel.send("What do you want to change the prefix to?")
                    msg = await client.wait_for('message', check = checkreply, timeout = 60.0)
                    server_prefix = change_prefix(prefix_data, msg.guild.id, msg.content)
                    await message.channel.send(f"Server prefix changed to {server_prefix}")
        """ if "meeting" in themessage[0]:
            custom_rooms = message.guild.get_channel(752942661018845273)
            people = message.mentions
            other_people = [person for role in roles for person in message.guild.get_role(int(role)).members]
            people = people + list(set(other_people) - set(people))
            channel_name = messagecapitalization[1]
            overwrites_object = {
                message.guild.default_role : discord.PermissionOverwrite(read_messages=False, send_messages = False),
                message.guild.get_role(687996857653264393) : discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
            for person in people:
                    overwrites_object[person] = discord.PermissionOverwrite(read_messages=True,send_messages=True, manage_channels=True)
            await message.guild.create_text_channel(channel_name, overwrites = overwrites_object,category = custom_rooms)
            await message.channel.send(f"Meeting room {channel_name} created") """

client = MyClient()
client.run(get_secret())