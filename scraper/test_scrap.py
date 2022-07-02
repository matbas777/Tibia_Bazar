import dateparser
from bs4 import BeautifulSoup
# from psycopg2 import IntegrityError
from requests import get
import requests
import re

from market.models import Character, Server


def collect_data():

    links = Character.objects.values_list('auction_link', flat=True)

    for link in links:
        '''sekcja ponizej sprawdza: nazwe postaci, level postaci, server na jakies jest postac, profesje postaci, plec.'''
        # for link in all_links: # dla kazdego linku ( z wielu linkow -> all_links)na naszej aukcj
        r = requests.get(link) # jest wysylane zapytanie do servera
        soup = BeautifulSoup(r.content, "html.parser") # wyswietla nam caly kod html z danego linku
        character_name_div = soup.find("div", class_="AuctionCharacterName") # w argumentach precyzujemy ktory tak i klasa nasz interesuje
        data_name = character_name_div.get_text() # wyswitla nam nick postaci
        basic_data = soup.findAll("tr", class_="Even") # do zmiennej przypisujemy wszystkie znajdujace sie w kodzie html tagi tr i klasy Even. w naszej petli for wybieramy jeden element( czyli jeden tag tri klase even i patrzymy czy jest w niej zawarty element/ tekst ktory szukamy. jezeli znejdziemy w nik ten element to odczytujemy jego dalsza czesc czyli wartosc np szykamy hp i odcytujemy ile tam jest tego hp
        data_hp = None
        data_capacity = None
        data_gold = None
        data_outfit = None
        data_available_charm_point = None
        data_charm_expension = None
        data_prey_slot = None
        data_mount = None
        data_mana = None
        data_speed = None
        data_experience = None
        for element in basic_data:
            try:
                element_span = element.find("span").get_text()
                if element_span == 'Hit Points:':
                    data_hp = element.find("div").get_text()
                elif element_span == "Capacity:":
                    data_capacity = element.find("div").get_text()
                elif element_span == "Gold:":
                    data_gold = element.find("div").get_text()
                elif element_span == "Outfits:":
                    data_outfit = element.find("div").get_text()
                elif element_span == "Available Charm Points:":
                    data_available_charm_point = element.find("div").get_text()
                if all([data_hp, data_available_charm_point, data_capacity, data_gold, data_outfit]):
                    break
            except AttributeError:
                continue
        basic_data = soup.findAll("tr", class_="Odd")
        for element in basic_data:
            try:
                element_span = element.find("span").get_text()
                if element_span == 'Mana:':
                    data_mana = element.find("div").get_text()
                elif element_span == "Speed:":
                    data_speed = element.find("div").get_text()
                elif element_span == "Mounts:":
                    data_mount = element.find("div").get_text()
                elif element_span == "Experience:":
                    data_experience = element.find("div").get_text()
                elif element_span == "Charm Expansion:":
                    data_charm_expension = element.find("div").get_text()
                elif element_span == "Permanent Prey Slots:":
                    data_prey_slot = element.find("div").get_text()
            except AttributeError:
                continue
            if all([data_charm_expension, data_prey_slot, data_mount, data_mana, data_speed, data_experience]):
                break
        # if data_charm_expension == ' yes':
        #     charm_bol = True
        # else:
        #     charm_bol = False
        charm_bol = True if data_charm_expension == ' yes' else False
        prey_bol = True if data_prey_slot == '1' else False
        # if data_prey_slot == '1':
        #     prey_bol = True
        # else:
        #     prey_bol = False


        print('------------------------------------')
        print(f'I{data_name}I')
        print(type(data_name))
        print('------------------------------------')
        print('------------------------------------')



collect_data()
