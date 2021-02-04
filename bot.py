#Template
#Schedule
#Block
import discord
import os
import asyncio
import io
import json
import datetime
import calendar
import re
import math
import time
import copy
FILE_PATH = os.path.dirname(os.path.abspath( __file__ ))

""" default_schedule = {
    "name": "Urbana High School Default Schedule",
    "id": 0,
    "weeks": 1,
    "start_week": "20200907",
    "blocks": [1,2,3,4,99],
    "schedule": {
        0: {
            0: [
                {
                    "start": 730,
                    "end": 825,
                    "period": 1,
                    "special": None,
                    "block": ""
                },
                {
                    "start": 830,
                    "end": 925,
                    "period": 2,
                    "special": None,
                    "block": ""
                },
                {
                    "start": 930,
                    "end": 955,
                    "period": 1,
                    "special": "Hawktime",
                    "block": ""
                },
                {
                    "start": 1000,
                    "end": 1030,
                    "period": 0,
                    "special": "Lunch",
                    "block": ""
                },
                {
                    "start": 1035,
                    "end": 1130,
                    "period": 3,
                    "special": None,
                    "block": ""
                },
                {
                    "start": 1135,
                    "end": 1230,
                    "period": 4,
                    "special": None,
                    "block": ""
                }
            ],
            1: [
                {
                    "start": 730,
                    "end": 825,
                    "period": 1,
                    "special": None,
                    "block": ""
                },
                {
                    "start": 830,
                    "end": 925,
                    "period": 2,
                    "special": None,
                    "block": ""
                },
                {
                    "start": 930,
                    "end": 955,
                    "period": 2,
                    "special": "Hawktime",
                    "block": ""
                },
                {
                    "start": 1000,
                    "end": 1030,
                    "period": 0,
                    "special": "Lunch",
                    "block": ""
                },
                {
                    "start": 1035,
                    "end": 1130,
                    "period": 3,
                    "special": None,
                    "block": ""
                },
                {
                    "start": 1135,
                    "end": 1230,
                    "period": 4,
                    "special": None,
                    "block": ""
                }
            ],
            2: [
                {
                    "start": 830,
                    "end": 905,
                    "period": 1,
                    "special": None,
                    "block": ""
                },
                {
                    "start": 910,
                    "end": 945,
                    "period": 2,
                    "special": None,
                    "block": ""
                },
                {
                    "start": 950,
                    "end": 1020,
                    "period": 99,
                    "special": "Hawktime",
                    "block": ""
                },
                {
                    "start": 1020,
                    "end": 1050,
                    "period": 0,
                    "special": "Lunch",
                    "block": ""
                },
                {
                    "start": 1055,
                    "end": 1130,
                    "period": 3,
                    "special": None,
                    "block": ""
                },
                {
                    "start": 1135,
                    "end": 1210,
                    "period": 4,
                    "special": None,
                    "block": ""
                }
            ],
            3: [
                {
                    "start": 730,
                    "end": 825,
                    "period": 1,
                    "special": None,
                    "block": ""
                },
                {
                    "start": 830,
                    "end": 925,
                    "period": 2,
                    "special": None,
                    "block": ""
                },
                {
                    "start": 930,
                    "end": 955,
                    "period": 3,
                    "special": "Hawktime",
                    "block": ""
                },
                {
                    "start": 1000,
                    "end": 1030,
                    "period": 0,
                    "special": "Lunch",
                    "block": ""
                },
                {
                    "start": 1035,
                    "end": 1130,
                    "period": 3,
                    "special": None,
                    "block": ""
                },
                {
                    "start": 1135,
                    "end": 1230,
                    "period": 4,
                    "special": None,
                    "block": ""
                }
            ],
            4: [
                {
                    "start": 730,
                    "end": 825,
                    "period": 1,
                    "special": None,
                    "block": ""
                },
                {
                    "start": 830,
                    "end": 925,
                    "period": 2,
                    "special": None,
                    "block": ""
                },
                {
                    "start": 930,
                    "end": 955,
                    "period": 4,
                    "special": "Hawktime",
                    "block": ""
                },
                {
                    "start": 1000,
                    "end": 1030,
                    "period": 0,
                    "special": "Lunch",
                    "block": ""
                },
                {
                    "start": 1035,
                    "end": 1130,
                    "period": 3,
                    "special": None,
                    "block": ""
                },
                {
                    "start": 1135,
                    "end": 1230,
                    "period": 4,
                    "special": None,
                    "block": ""
                }
            ]
        }
    }
} """

#ib_schedule = default_schedule

class Schedule:
    def __init__(self, user, template, blocks,):
        self.user = user
        self.template = copy.deepcopy(template)
        self.blocks = blocks
        self.schedule = copy.deepcopy(template)
        self.update_schedule()
    
    def __dict__(self):
        return_dict = {"user": self.user, "template": self.template, "blocks" : []}
        for block in self.blocks:
            return_dict["blocks"].append(block.__dict__())
        return return_dict

    def get_block_index(self, num):
        for block in self.blocks:
            if int(block.num) == int(num):
                return self.blocks.index(block)
        return None

    def get_block(self, num):
        index = self.get_block_index(int(num))
        if index is not None:
            return self.blocks[index]
        return None

    def change_block(self, num, name, link):
        index = self.get_block_index(num)
        if index is not None:
            self.blocks[index].num = int(num)
            self.blocks[index].name = name
            self.blocks[index].link = link
            return self.blocks[index].__dict__()
        else:
            self.blocks.append(Block(num, name, link))
            return self.blocks[-1].__dict__()
        self.update_schedule()
        
    def update_schedule(self):
        self.schedule['start_week'] = datetime.date(int(self.schedule['start_week'][:4]),int(self.schedule['start_week'][4:6]),int(self.schedule['start_week'][6:]))
        for x in self.schedule['schedule']:
            for y in self.schedule['schedule'][x]:
                for period in self.schedule['schedule'][x][y]:
                    period['block'] = self.get_block(period['period'])
        return self.schedule

    def change_template(self, template):
        self.template = template
        self.schedule = template
        self.update_schedule()
        return template
    
    def get_week(self, custom = False):
        if not custom:
            time = datetime.datetime.now()
            week_diff = math.floor((time.date() - self.schedule["start_week"]).days / 7) % self.schedule["weeks"]
        else:
            week_diff = math.floor((custom.date() - self.schedule["start_week"]).days / 7) % self.schedule["weeks"]
        return week_diff
    
    def get_ddhhmm(self, custom = False):
        if not custom:
            time = datetime.datetime.now()
        else:
            time = custom
        ddhhmm = str(time.weekday()).zfill(2) + str(time.strftime("%H")).zfill(2) + str(time.strftime("%M")).zfill(2)
        return ddhhmm

    def current_block(self, custom = False):
        try:
            ddhhmm = self.get_ddhhmm(custom)
            week = self.get_week(custom)
            day = self.schedule['schedule'][str(week)][str(int(ddhhmm[:2]))]
            time = int(ddhhmm[2:])
            for x in day:
                if time >= x['start'] - 5 and time <= x['end']:
                    return x
        except:
            return None
    
    def daily_schedule(self, custom = False):
        try:
            ddhhmm = self.get_ddhhmm(custom)
            week = self.get_week(custom)
            day = self.schedule['schedule'][str(week)][str(int(ddhhmm[:2]))]
            return day 
        except:
           return None

class Block:
    def __init__(self,num, name, link):
        self.num = num
        self.name = name
        self.link = link
    
    def __dict__(self):
        return {"num": self.num, "name": self.name, "link": self.link}

def get_current_block(userdata, custom = None):
    if not custom:
        ddhhmm = False
    else:
        ddhhmm = custom
    data = userdata.current_block(ddhhmm)
    if data is not None:
        return_embed = discord.Embed(title = f"{data['special'] if data['special'] is not None else 'Block ' + str(data['period'])} [{data['start']} - {data['end']}]", description = f"[{data['block'].name}]({data['block'].link})")
    else:
        return_embed = discord.Embed(title = "Nothing")
    return return_embed

def get_daily_schedule(userdata, custom = None):
    if not custom:
        ddhhmm = False
    else:
        ddhhmm = custom
    data2 = userdata.daily_schedule(ddhhmm)
    total_string = ""
    if data2 is not None:
        for data in data2:
            total_string += f"{data['special'] if data['special'] is not None else 'Block ' + str(data['period'])} [{data['start']} - {data['end']}]: [{data['block'].name}]({data['block'].link})\n"
        nowembed = discord.Embed(title = f"**Schedule**", description = total_string)
    else:
        nowembed = discord.Embed(title = "**Schedule**", description = "None")
    return nowembed



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

def get_mentioned_roles(message):
    roles = re.findall(r"<@&[0-9]+>",message)
    roles = [role.replace("!","").replace("&","").replace("@","").strip("<").strip(">") for role in roles]
    return roles

def convert_dict_to_object(dict):
    blocks = []
    for x in dict['blocks']:
        blocks.append(Block(x['num'],x['name'],x['link']))
    schedule = Schedule(dict['user'],dict['template'],blocks)
    return schedule

def convert_object_to_dict(schedule):
    new_dict = schedule.__dict__()
    return new_dict

def load_prefix_data():
    with open(FILE_PATH + "/prefix.txt", "r+") as prefixfile:
        prefixes = prefixfile.readlines()
    return [json.loads(x) for x in prefixes]

prefixes = load_prefix_data()

def dump_prefix_data(data):
    prefixes = [json.dumps(x) for x in data]
    with open(FILE_PATH + "/prefix.txt", "w+") as prefixfile:
        prefixfile.writelines("\n".join(prefixes))

def get_prefix(data, server_id):
    for x in data:
        if x['server_id'] == server_id:
            return x['prefix']
    return None

def change_prefix(data, server_id, prefix, prefix_var = prefixes):
    appended = False
    for x in data:
        if x['server_id'] == server_id:
            data[data.index(x)]['prefix'] = prefix
            appended = True
    if appended == False:
        data.append({'server_id': server_id, 'prefix': prefix})
    dump_prefix_data(data)
    prefix_var = data
    return prefix

def load_schedule_data():
    with open(FILE_PATH + "/schedules.txt", "r+") as schedulefile:
        schedules = schedulefile.readlines()
    return [json.loads(x) for x in schedules]

schedules = load_schedule_data()

def dump_schedule_data(data):
    schedules = [json.dumps(x) for x in data]
    with open(FILE_PATH + "/schedules.txt", "w+") as schedulefile:
        schedulefile.writelines("\n".join(schedules))

def get_schedule(data, schedule_id):
    for x in data:
        if int(x['id']) == int(schedule_id):
            return x
    return None

def change_schedule(data, schedule, schedule_var = schedules):
    appended = False
    for x in data:
        if x['id'] == schedule['id']:
            data[data.index(x)] = schedule
            appended = True
    if appended == False:
        data.append(schedule)
    dump_schedule_data(data)
    schedule_var = data
    return schedule

def get_schedule_list(schedules):
    return_string = ""
    for x in schedules:
        return_string += f"**{x['id']}**: *{x['name']}*\n"
    return return_string

def create_empty_object(user_mention, schedule_num = 0, schedule_var = schedules):
        return Schedule(user_mention,get_schedule(schedule_var, schedule_num),[Block(0, '', 'nothing'),Block(99, 'Advisement', 'nothing'),Block(1, 'nothing', 'http://example.com'),Block(2, 'nothing', 'http://example.com'),Block(3, 'nothing', 'http://example.com'),Block(4, 'nothing', 'http://example.com'),Block(5, 'nothing', 'http://example.com'),Block(6, 'nothing', 'http://example.com'),Block(7, 'nothing', 'http://example.com')])

class MyClient(discord.Client): 
    async def on_ready(self):
        print('Schedulebot Up')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        message_content = message.content
        if message.author.id == self.user.id:
            return
        try:
            server_id = message.guild.id
            server_prefix = get_prefix(prefixes, server_id)
            mentions = [str(mention.id).replace("!","").replace("&","").replace("@","").strip("<").strip(">") for mention in message.mentions]
            roles = get_mentioned_roles(message.content)
            if str(self.user.id) not in mentions:
                yes = False
                for role in message.guild.get_member(self.user.id).roles:
                    if str(role.id) in roles:
                        message_content = message_content.replace(f"<@&{str(role.id)}>","").replace(f"<@{str(role.id)}>","").replace(f"<@!{str(role.id)}>","")
                        yes = True
                        break
                if not yes:
                    if server_prefix is not None or "":
                        if server_prefix in message.content:
                            pass
                        else: 
                            return
                    else:
                        return
        except:
            pass
        userdata = get_user_data(get_data(),message.author.id)
        message_content = [x.strip() for x in message_content.replace("<@!749979907282436166>","").replace("<@749979907282436166>","").replace("<@&749979907282436166>","").split("-")]
        if "setup" in message_content[0].lower():
            userdata = create_empty_object(userdata.user)
            await message.channel.send("Check your private messages for a message from me to continue setup. If you don't see one, make sure you have messages from strangers turned on in settings.")
            def checkreply(m):
                return m.author == message.author and m.channel.id == message.author.dm_channel.id
            await message.author.send("Welcome to the guided schedule creator. Just follow the steps and you will be done in no time.")
            await message.author.send("What schedule do you want to use? Reply with the id of the schedule you want to use. Reply with \"list\" to see a list of schedules and their associated ids.")
            schedule_choice = await client.wait_for('message', check = checkreply, timeout = 120.0)
            if schedule_choice.content.lower() == "list":
                await message.author.send(get_schedule_list(schedules))
                await message.author.send("Which schedule do you want to use?")
                schedule_choice = await client.wait_for('message', check = checkreply, timeout = 120.0)
            try: 
                schedule_choice  = int(schedule_choice.content)
                userdata = create_empty_object(userdata.user, schedule_choice)
            except:
                await message.author.send("Something went wrong. Please try again.")
                return
            for x in userdata.schedule["blocks"]:
                if x is 99:
                    await message.author.send(f"Who do you have for advisement? You have two minutes to reply.")
                    msg = await client.wait_for('message', check = checkreply, timeout=120.0)
                    name = msg.content
                    await message.author.send(f"What is your Google Meet link for advisement? Make sure this has the `https://` at the start. You have two minutes to reply.")
                    msg = await client.wait_for('message', check = checkreply, timeout=120.0)
                    link = msg.content
                    userdata.change_block(x,name,link)
                else:
                    await message.author.send(f"What do you have for block {x}? You can name this something descriptive, like `World History with Hontz`. You have two minutes to reply.")
                    msg = await client.wait_for('message', check = checkreply, timeout=120.0)
                    name = msg.content
                    await message.author.send(f"What is your Google Meet link for block {x}? Make sure this has the `https://` at the start. You have two minutes to reply.")
                    msg = await client.wait_for('message', check = checkreply, timeout=120.0)
                    link = msg.content
                    userdata.change_block(x,name,link)
            change_data(change_user_data(get_data(),userdata))
            await message.author.send("The setup is done! Check if it worked properly with @schedulebot schedule and @schedulebot now.")
            return
        
        if "now" in message_content[0].lower():
            await message.channel.send(embed = get_current_block(userdata))
            #await message.channel.send(embed = get_current_block(userdata, custom = datetime.datetime(2021,1,29,10,50)))
            return
        
        if "schedule" in message_content[0].lower():
            await message.channel.send(embed = get_daily_schedule(userdata))
            #await message.channel.send(embed = get_daily_schedule(userdata, custom = datetime.datetime(2021,1,29)))
            return

        if "prefix" in message_content[0].lower():
            await message.channel.send(f"This server's command prefix is `{server_prefix if server_prefix is not None else 'none set'}`. You can also use <@749979907282436166>")
            if message.author.guild_permissions.administrator:
                def checkreply(m):
                    return m.author == message.author and m.channel.id == message.channel.id
                await message.channel.send("Would you like to change the prefix? (y/n)")
                msg = await client.wait_for('message', check = checkreply, timeout = 60.0)
                if msg.content.lower() == "y":
                    await message.channel.send("What do you want to change the prefix to?")
                    msg = await client.wait_for('message', check = checkreply, timeout = 60.0)
                    server_prefix = change_prefix(prefix_data, msg.guild.id, msg.content)
                    await message.channel.send(f"Server prefix changed to {server_prefix}")
                    return
                else:
                    return
                    
        if "change" in message_content[0].lower():
            await message.channel.send("Check your private messages for a message from me to change your block. If you don't see one, make sure you have messages from strangers turned on in settings.")
            def checkreply(m):
                return m.author == message.author and m.channel.id == message.author.dm_channel.id
            await message.author.send("What block do you want to change? (99 for advisement)")
            msg = await client.wait_for('message', check = checkreply, timeout = 120.0)
            try:
                block = userdata.get_block(msg.content)
                if block is not None:
                    await message.channel.send(f"Currently for block **{block.num}** you have **{block.name}@{block.link}** set")
                    await message.channel.send(f"Would you like to change this block? (y/n)")
                    confirm = await client.wait_for('message', check = checkreply, timeout = 120.0)
                    if confirm.content.lower() == "y":
                        await message.channel.send(f"Who do you want to change your block {block.num} teacher to?")
                        name = await client.wait_for('message', check = checkreply, timeout = 120.0)
                        await message.channel.send(f"What is your block {block.num} link?")
                        link = await client.wait_for('message', check = checkreply, timeout = 120.0)
                        userdata.change_block(block.num, name.content, link.content)
                        change_data(change_user_data(get_data(),userdata))
                        new_block = userdata.get_block(block.num)
                        await message.channel.send(f"Changed block **{new_block.num}** to **{new_block.name}@{new_block.link}**")
                        return
                else:
                    await message.channel.send(f"You currently do not have any teacher or link set for block {msg}. Would you like to set one? (y/n)")
                    confirm = await client.wait_for('message', check = checkreply, timeout = 120.0)
                    if confirm.content.lower() == "y":
                        await message.channel.send(f"Who do you want to change your block {msg} teacher to?")
                        name = await client.wait_for('message', check = checkreply, timeout = 120.0)
                        await message.channel.send(f"What is your block {msg} link?")
                        link = await client.wait_for('message', check = checkreply, timeout = 120.0)
                        userdata.change_block(int(msg.content), name.content, link.content)
                        change_data(change_user_data(get_data(),userdata))
                        new_block = userdata.get_block(int(msg.content))
                        await message.channel.send(f"Changed block **{new_block.num}** to **{new_block.name}@{new_block.link}**")
                        return
            except:
                return

        if "help" in message_content[0].lower() or "info" in message_content[0].lower():
            await message.channel.send(f"**Schedulebot** was created by **Abdeet**\n\nCurrent command prefix is `{server_prefix}`\n\nCurrent commands are:\n`setup`: Set up your schedule\n`change`: Change a block\n`schedule`: View your daily schedule\n`now`: View your current class\n`info` or `help`: Does this\n`github`: View Github repo\n`invite`: Get Discord invite link\n\n**Command Structure**: `@Schedulebot [command]` or `[prefix] [command]`\n\nTo report bugs or complain or give encouragement or propose improvements contact **Abdeet**.")
            return

        if "github" in message_content[0].lower():
            await message.channel.send("Schedulebot has a GitHub repository!\nhttps://github.com/Abdeet/schedulebot")
            return

        if "invite" in message_content[0].lower():
            await message.channel.send("To invite Schedulebot to your channel use this link: https://discord.com/api/oauth2/authorize?client_id=749979907282436166&permissions=256000&scope=bot")
            return

        if "love" in message_content[0].lower():
            await message.channel.send("Schedulebot is in a dedicated relationship with No U Bot, who has been in a coma for over a year.")
            return

client = MyClient()
client.run(get_secret())    