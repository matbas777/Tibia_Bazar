import dateparser
from bs4 import BeautifulSoup
from psycopg2 import IntegrityError
from requests import get
import requests
import re
from time import sleep

from market.models import Character, Server


def collect_data():

    links = Character.objects.filter(commission=0).values_list(
        "auction_link", flat=True
    )

    for link in links:
        sleep(0.5)
        """sekcja ponizej sprawdza: nazwe postaci, level postaci, server na jakies jest postac, profesje postaci, plec."""
        # for link in all_links: # dla kazdego linku ( z wielu linkow -> all_links)na naszej aukcj
        r = requests.get(link)  # jest wysylane zapytanie do servera
        soup = BeautifulSoup(
            r.content, "html.parser"
        )  # wyswietla nam caly kod html z danego linku
        character_name_div = soup.find(
            "div", class_="AuctionCharacterName"
        )  # w argumentach precyzujemy ktory tak i klasa nasz interesuje
        try:
            data_name = character_name_div.get_text()  # wyswitla nam nick postaci
        except AttributeError:
            print(link)
            data_name = None
        basic_data = soup.find("div", class_="AuctionHeader").get_text()
        regex = r"([0-9]+)"
        data_level = re.findall(regex, basic_data)[
            0
        ]  # dostajemy liste z jednym elementem, aby wyciagnac parametr level to mucimy wyciagnac pierwszy index z listy
        regex = r"World: ([\s\S]+)"  # ten regeks wyciaga to co jest po elemencie tekstu "world:"
        data_world = re.findall(
            regex, basic_data
        )  # szykamy naszego regeksa w teksiecie i wypluwa na nasz server
        data_world = data_world[0]
        world = Server.objects.get(server=data_world)
        data_world = world
        regex = r"Vocation: ([\s\S]+)"
        data_vocation = re.findall(regex, basic_data)[0].split(" | ")[
            0
        ]  # podzielilismy nasz teks na liste i wyciagamy pierwszy (zerowy index) element ktorym jest nazwa vokacji
        data_sex = re.findall(regex, basic_data)[0].split(" | ")[1]
        """sekcja ponizej sprawdza: ilosc zycia, ilosc many, ilosc udzwigu, szybkosc, ilosc doswiadczenia, ulosc zlota, dostepne punkty charmowe, czy postac posiada charm expension, czy postac posiada dodatkowy prey slot, ilosc wszystkich mountow"""
        basic_data = soup.findAll(
            "tr", class_="Even"
        )  # do zmiennej przypisujemy wszystkie znajdujace sie w kodzie html tagi tr i klasy Even. w naszej petli for wybieramy jeden element( czyli jeden tag tri klase even i patrzymy czy jest w niej zawarty element/ tekst ktory szukamy. jezeli znejdziemy w nik ten element to odczytujemy jego dalsza czesc czyli wartosc np szykamy hp i odcytujemy ile tam jest tego hp
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
                if element_span == "Hit Points:":
                    data_hp = element.find("div").get_text()
                elif element_span == "Capacity:":
                    data_capacity = element.find("div").get_text()
                elif element_span == "Gold:":
                    data_gold = element.find("div").get_text()
                elif element_span == "Outfits:":
                    data_outfit = element.find("div").get_text()
                elif element_span == "Available Charm Points:":
                    data_available_charm_point = element.find("div").get_text()
                if all(
                    [
                        data_hp,
                        data_available_charm_point,
                        data_capacity,
                        data_gold,
                        data_outfit,
                    ]
                ):
                    break
            except AttributeError:
                continue
        basic_data = soup.findAll("tr", class_="Odd")
        for element in basic_data:
            try:
                element_span = element.find("span").get_text()
                if element_span == "Mana:":
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
            if all(
                [
                    data_charm_expension,
                    data_prey_slot,
                    data_mount,
                    data_mana,
                    data_speed,
                    data_experience,
                ]
            ):
                break

        """sekcja ponizej sprawdza ilosc wykupionych charmow ma postac na aukcji"""

        basic_data = soup.findAll("div", class_="TableContentContainer")
        charm_list = basic_data[21]
        charms_list1 = charm_list.find_all("tr", class_="Odd")
        charms_list2 = charm_list.find_all("tr", class_="Even")

        data_charms = []
        for charms_list in charms_list1:
            charms = charms_list.findAll("td")
            for charm in charms:
                char = charm.get_text()
                data_charms.append(char.replace(",", ""))
        data_charms = [
            charm_name for charm_name in data_charms if not charm_name.isdigit()
        ]

        for charms_list in charms_list2:
            charms = charms_list.findAll("td")
            for charm in charms:
                char = charm.get_text()
                data_charms.append(char.replace(",", ""))
        data_charms = [
            charm_name for charm_name in data_charms if not charm_name.isdigit()
        ]
        for _ in data_charms:
            if "No charms." in _:
                data_charms = []

        """sekcja ponizej sprawdza ilosc zrobionych questow ma postac na aukcji"""
        quests_list = basic_data[23]
        quest_list1 = quests_list.findAll("tr", class_="Even")
        quest_list2 = quests_list.findAll("tr", class_="Odd")

        data_quests_list = []
        for quest in quest_list1:
            add_quest = quest.get_text()
            data_quests_list.append(add_quest)

        for quest in quest_list2:
            add_quest = quest.get_text()
            data_quests_list.append(add_quest)

        for _ in data_quests_list:
            if "No quest line finished." in _:
                data_quests_list = []

        # sekcja ponizej sprawdza ilosc podstawowych mountaow jaka posiada postac na aukcji. Roznica pozmiedzy total_mounts a basic_mounts da nam ilosc store_mounts'''
        basic_mount_list = basic_data[14]
        mount_list = basic_mount_list.findAll("div")

        mount = 0
        quantity_basic_mount = 0

        if (
            mount_list
        ):  # w tym momencie jezeli if jest jest falsem to nie wykona sie petla. w przeciwnym wypadku jak bedie true to petla nadpisze zmienna mount
            for quantity_mount in mount_list:
                mount = quantity_mount.get_text()
                if "Results: " in mount:
                    break
            regex = r"Results: ([\s\S]+)"
            quantity_basic_mount = re.findall(regex, mount)[0]

        """sekcja ponizej sprawdza ilosc podstawowych outfitow jaka posiada postac na aukcji. Roznica pozmiedzy total_mounts a basic_mounts da nam ilosc store_mounts"""

        basic_outfit_list = basic_data[16]
        outfits_list = basic_outfit_list.findAll("div")

        outfit = 0

        if (
            outfits_list
        ):  # w tym momencie jezeli if jest jest falsem to nie wykona sie petla. w przeciwnym wypadku jak bedie true to petla nadpisze zmienna mount
            for quantity_outfits in outfits_list:
                outfit = quantity_outfits.get_text()
                if "Results: " in outfit:
                    break

        regex = r"Results: ([\s\S]+)"
        quantity_basic_outfit = re.findall(regex, outfit)[0]
        # print(quantity_basic_outfit)

        """sekcja ponizej zapisuje do slownika/jasona poziomy i procenty do nastepnego lvla danego skila"""

        basic_outfit_list = basic_data[2]
        skills_list_1 = basic_outfit_list.findAll("tr", class_="Even")
        skills_list_2 = basic_outfit_list.findAll("tr", class_="Odd")

        data_skills = {}

        for type_of_skill in skills_list_1:
            name_skill = type_of_skill.find("td", class_="LabelColumn").get_text()
            lvl_skill = type_of_skill.find("td", class_="LevelColumn").get_text()
            percentage_skill = type_of_skill.find(
                "td", class_="PercentageColumn"
            ).get_text()
            data_skills[name_skill] = (lvl_skill, percentage_skill)

        for type_of_skill in skills_list_2:
            name_skill = type_of_skill.find("td", class_="LabelColumn").get_text()
            lvl_skill = type_of_skill.find("td", class_="LevelColumn").get_text()
            percentage_skill = type_of_skill.find(
                "td", class_="PercentageColumn"
            ).get_text()
            data_skills[name_skill] = (lvl_skill, percentage_skill)

        """sekcja ponizej zapisuje do zmiennej data_price aktualna cene postaci"""
        basic_data = soup.find("div", class_="ShortAuctionDataBidRow")
        status_bid = basic_data.find("div", class_="ShortAuctionDataLabel").get_text()
        data_price = basic_data.find("div", class_="ShortAuctionDataValue").get_text()
        data_price = int(data_price.replace(" ", "").replace(",", ""))

        basic_data = soup.find("div", class_="AuctionBodyBlock ShortAuctionData")
        auction_start = basic_data.find(
            "div", class_="ShortAuctionDataValue"
        ).get_text()
        auction_end = basic_data.findAll("div", class_="ShortAuctionDataValue")[
            1
        ].get_text()

        data_auction_start = dateparser.parse(auction_start)
        data_auction_end = dateparser.parse(auction_end)

        store_mounts = int(data_mount) - int(quantity_basic_mount)
        store_outfits = int(data_outfit) - int(quantity_basic_outfit)

        try:
            basic_data = soup.find("div", class_="AuctionBodyBlock CurrentBid")
            data_auction_status = basic_data.find(
                "div", class_="AuctionInfo"
            ).get_text()
        except AttributeError:
            data_auction_status = None

        char = Character.objects.get(auction_link=link)

        # if not data_name == char.Character_name:
        #     char.Character_name = data_name
        # char.save()

        char.level = data_level
        char.experience = data_experience
        char.gold = data_gold
        char.vocation = data_vocation
        char.sex = data_sex
        char.server = data_world
        char.skills = data_skills
        char.mana = data_mana
        char.hp = data_hp
        char.character_name = data_name
        char.capacity = data_capacity
        char.speed = data_speed
        char.all_outfit = data_outfit
        char.basic_outfit = quantity_basic_outfit
        char.store_outfit = store_outfits
        char.all_mount = (data_mount,)
        char.basic_mount = quantity_basic_mount
        char.store_mount = store_mounts
        char.charm_list = data_charms
        char.quantity_charms = len(data_charms)
        char.charm_point = data_available_charm_point
        char.quest_list = data_quests_list
        char.quantity_quest = len(data_quests_list)
        char.charm_expension = True if data_charm_expension == " yes" else False
        char.prey_slot = True if data_prey_slot == "1" else False
        char.bid_status = status_bid
        char.price = data_price
        char.auction_start = data_auction_start
        char.auction_end = data_auction_end
        # char.auctions_status=data_auction_status)
        char.save()


collect_data()


# # print(data_auction_start)
# # print(data_auction_end)
# print(f'auction link: {link}')
# print(f'status bid: {status_bid}')
# print(f'auctions price {data_price}')
# print(f'name: {data_name}')
# print(f'level: {data_level}')
# print(f'sex: {data_sex}')
# print(f'vocation: {data_vocation}')
# print(f'server: {data_world[0]}')
# print(f'hit points: {data_hp}')
# print(f'capacity points: {data_capacity}')
# print(f'gold balance: {data_gold}')
# print(f'available charm points: {data_available_charm_point}')
# print(f'charm expension: {data_charm_expension}')
# print(f'additional prey slot: {data_prey_slot}')
# print(f'mana points: {data_mana}')
# print(f'speed points: {data_speed}')
# print(f'experience points: {data_experience}')
# print(f'charms list: {data_charms}')
# print(f'quantity charms: {len(data_charms)}')
# print(f'quests list: {data_quests_list}')
# print(f'quantity quests: {len(data_quests_list)}')
# print(f'all outfits: {data_outfit}')
# print(f'basic outfits: {quantity_basic_outfit}')
# print(f'store outfits: {store_outfits}')
# print(f'all mounts: {data_mount}')
# print(f'basic mounts: {quantity_basic_mount}')
# print(f'store mounts: {store_mounts}')
# print(f'skils: {data_skills}')


# url = "https://www.tibia.com/charactertrade/?subtopic=currentcharactertrades&page=details&auctionid=899685&source=overview&filter_profession=0&filter_levelrangefrom=0&filter_levelrangeto=0&filter_world=&filter_worldpvptype=9&filter_worldbattleyestate=0&filter_skillid=&filter_skillrangefrom=0&filter_skillrangeto=0&order_column=101&order_direction=1&searchtype=1&currentpage=1"
# r = requests.get(url)# jest wysylane zapytanie do servera
# soup = BeautifulSoup(r.content, "html.parser") # wyswietla nam caly kod html z danego linku
#
# basic_data = soup.find('div', class_='AuctionBodyBlock CurrentBid')
# data_auction_start = basic_data.find('div', class_='AuctionInfo').get_text()
#
#
#
# print(data_auction_start)
