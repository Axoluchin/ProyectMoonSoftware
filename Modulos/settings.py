import json
import os

def get_json():
    with open('settings/settings.json', 'r') as myfile:
        data=myfile.read()

    return json.loads(data)

def get_theme():
    data = get_json()
    return str(data['theme'])

def get_moons():
    data = get_json()
    return int(data['moons'])

def get_history():
    data = get_json()
    return int(data['history'])

def get_temple():
    data = get_json()
    return int(data['temple'])

def get_temple_name():
    lista = os.listdir('settings/images/temples')
    return lista[get_temple()-1]


def get_photo():
    data = get_json()
    return int(data['photo'])


def update_json(theme, moons,history,temple,photo):
    data ={
        "theme": str(theme),
        "history": int(history),
        "moons": int(moons),
        "temple": int(temple),
        "photo": int(photo)
    }
    
    json_object = json.dumps(data, indent = 4)
    
    with open('settings/settings.json', "w") as outfile:
        outfile.write(json_object)