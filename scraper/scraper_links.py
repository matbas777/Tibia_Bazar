from bs4 import BeautifulSoup
from psycopg2 import IntegrityError
import requests
import re

from market.models import Character

url = "https://www.tibia.com/charactertrade/?subtopic=currentcharactertrades"
def get_all_pages_links():
    r = requests.get(url) # przypusijemy do zmiennej r zapytanie do servera o dany url
    soup = BeautifulSoup(r.content, "html.parser") # zmienna soup da nam caly kod html z danego urla ( dzieki metodzien "content")
    selector = soup.find_all("span", class_="PageLink FirstOrLastElement")[-1] # w tym momencie bierzemy danego taga ktory nas interesuje i biwrzemy jego ostatni element ( poniewaz on nas interesuje)
    last_page_url = selector.find("a", href=True)["href"] # ta metoda obiera nam nasz link z taga "a" i href ( wypluwa nam goly link, na koncu tego linka mamy podany numer ostatneie strony. o ten numer nam chodzi zeby wiedziec ile jest tron do przeskrapowania)
    regex = r"page=([\s\S]*)$" # ten regex wyrzucam nam to co wystepuje po teksie "page=" ktory znajduje sie w linku. po tym teksie jest masza liczba ktora jest zapisana do listy
    last_number = re.findall(regex, last_page_url)[0] # aby odebrac stringa z naszej listy z jednym elementem, pobieramy z niego index [0] i daje nam masz liczbe jako int. zmienna last_number bedzie przechowywac naszego inta

    all_links = [] # w tej liscie biedziemy przechowywac wszystkie linki do aukcji postaci
    print(all_links)
    for nr in range(1, int(last_number) + 1):
        for nr in range(1, 10): # w tej petli zmienna nr jest numerem (po kolei) w przedziale od 1 do numeru ostatniej strony
            r = requests.get(f"https://www.tibia.com/charactertrade/?currentpage={nr}") # zmienna r pobiera zapytanie z servera dla kazdego linka\
            soup = BeautifulSoup(r.content, "html.parser") # wtswietla nam caly kod html z danego url-a
            selector = soup.find_all("div", class_="AuctionCharacterName") # zmienna 'selector' precyzuje nam taga ktory nas interesuje w tym przypadku dag "div" z klasa AuctionCharacterName

            for auction in selector: # pojedynczy div jest przypisany do zmiennej auction, jest literowany po selectorze w ktorym znajduje sie wiele divow
                auction_link = auction.find("a", href=True)["href"] # do zmiennej auction_link jest przypisany link juz obrany z tagow a i href
                all_links.append(auction_link) # obrane (czyste) linki do naszych aukcji sa dodawane do listy "all_links"

    for link in all_links:
        try:
            Character.objects.create(auction_link=link)
        except IntegrityError:
            pass

get_all_pages_links()