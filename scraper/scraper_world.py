from bs4 import BeautifulSoup
from psycopg2 import IntegrityError
from requests import get
import requests

from market.models import Server



def tibia_worlds():
    '''sekcja ponizej zapisuje do slownika/jasona dane na temat serwerow (nazwe, ich lokacje oraz typ servera)'''

    world_url = "https://www.tibia.com/community/?subtopic=worlds"
    r = requests.get(world_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    basic_data = soup.findAll('table', class_='TableContent')
    world_all_list = basic_data[2]
    html_all_data_worlds_1 = world_all_list.findAll('tr', class_='Odd')
    html_all_data_worlds_2 = world_all_list.findAll('tr', class_='Even')

    data_world = {}

    for all_data_worlds in html_all_data_worlds_1:
        data_worlds = all_data_worlds.findAll('td')
        battleye_data = all_data_worlds.find('img')['src']
        if 'battleyeinitial' in battleye_data:
            battleye = "green battleye"
        elif 'battleye' in battleye_data:
            battleye = 'yelow battleye'
        else:
            battleye = ' nonprotected'
        worlds = data_worlds[0].get_text()
        location = data_worlds[2].get_text()
        pvp_type = data_worlds[3].get_text()

        data_world[worlds]= (location, pvp_type, battleye)


    for all_data_worlds in html_all_data_worlds_2:
        data_worlds = all_data_worlds.findAll('td')
        battleye_data = all_data_worlds.find('img')['src']
        if 'battleyeinitial' in battleye_data:
            battleye = "green battleye"
        elif 'battleye' in battleye_data:
            battleye = 'yelow battleye'
        else:
            battleye = ' nonprotected'
        world = data_worlds[0].get_text()
        location = data_worlds[2].get_text()
        pvp_type = data_worlds[3].get_text()
        data_world[world]= (location, pvp_type, battleye)

    for world, data in data_world.items():
        data[1]


        try:
            Server.objects.create(server=world, server_type=data[1], location=data[0], battlEye=data[2])
        except IntegrityError:
            pass


tibia_worlds()

