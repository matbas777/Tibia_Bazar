from bs4 import BeautifulSoup
from django.db import IntegrityError
import requests
import re
from market.models import Character
from time import sleep

url = "https://www.tibia.com/charactertrade/?subtopic=currentcharactertrades"


def get_all_pages_links():
    r = requests.get(url)
    soup = BeautifulSoup(
        r.content, "html.parser"
    )
    selector = soup.find_all("span", class_="PageLink FirstOrLastElement")[
        -1
    ]
    last_page_url = selector.find("a", href=True)[
        "href"
    ]
    regex = r"page=([\s\S]*)$"
    last_number = re.findall(regex, last_page_url)[
        0
    ]

    all_links = (
        []
    )

    for nr in range(
        1, int(last_number) + 1
    ):
        r = requests.get(
            f"https://www.tibia.com/charactertrade/?currentpage={nr}"
        )
        soup = BeautifulSoup(
            r.content, "html.parser"
        )
        selector = soup.find_all(
            "div", class_="AuctionCharacterName"
        )

        for (
            auction
        ) in (
            selector
        ):
            auction_link = auction.find("a", href=True)[
                "href"
            ]
            auction_link = auction_link.split("&source=overview")
            all_links.append(
                auction_link[0]
            )

    for link in all_links:
        try:
            Character.objects.create(auction_link=link)
        except IntegrityError:
            pass


get_all_pages_links()
