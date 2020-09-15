import json
import os

FILE_PATH = os.path.dirname(os.path.abspath( __file__ ))

class Schedule:
    def __init__(self,user,blocks):
        self.user = user
        self.blocks = blocks
        self.update_ib()

    def update_ib(self):
        if len(self.blocks) == 7:
            self.ib = 1
        else:
            self.ib = 0
    
    def __dict__(self):
        self.update_ib()
        return_dict = {"user": self.user, "ib" : self.ib, "blocks" : []}
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
        if index:
            return self.blocks[index]
        return None

    def change_block(self, num, name, link):
        index = self.get_block_index(num)
        if index:
            self.blocks[index].num = int(num)
            self.blocks[index].name = name
            self.blocks[index].link = link
        else:
            self.blocks.append(Block(num, name, link))
        self.update_ib()

class Block:
    def __init__(self,num, name, link):
        self.num = num
        self.name = name
        self.link = link
    
    def __dict__(self):
        return {"num": self.num, "name": self.name, "link": self.link}

def change_data(changed_list):
    with open(FILE_PATH + "/data.txt", "w+") as data_txt:
        changed_list = [json.dumps(x) + "\n" for x in changed_list]
        data_txt.writelines(changed_list)

def convert_object_to_dict(schedule):
    new_dict = {
        "user": schedule.user,
        "ib": schedule.ib,
        "blocks": [

        ]
    }
    for x in schedule.blocks:
        new_dict['blocks'].append({"num": x.num, "name": x.name, "link": x.link})
    return new_dict

def convert_legacy_dict_to_object(legacy_dict):
    classes = []
    for x in range(1,len(legacy_dict['links'])+1):
        classes.append(Block(x,legacy_dict['names'][str(x)],legacy_dict['links'][str(x)]))
    schedule = Schedule(int(legacy_dict['user']),classes)
    return schedule

def convert_legacy_data():
    with open(FILE_PATH + "/data.txt", "r+") as data_txt:
        data = data_txt.readlines()
    new_data = []
    for x in data:
        x = json.loads(x)
        print(x)
        try:
            x = convert_legacy_dict_to_object(x)
            x = convert_object_to_dict(x)
            new_data.append(x)
        except:
            new_data.append(x)
    change_data(new_data)

convert_legacy_data()
