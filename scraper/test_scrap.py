from bs4 import BeautifulSoup
from psycopg2 import IntegrityError
from requests import get
import requests
import dateparser
import re
from market.models import Character


def update_character():
    # Character.objects.filter(commission=0).values_list('auction_link', flat=True) # filtracja po prwizji(commission) kiedy jest rowna zero i zwraca linki w liscie[]
    for link in Character.objects.filter(commission=0).values_list(
        "auction_link", flat=True
    ):
        r = requests.get(link)
        soup = BeautifulSoup(r.content, "html.parser")
        basic_data = soup.find("div", class_="ShortAuctionDataBidRow")
        status_bid = basic_data.find("div", class_="ShortAuctionDataLabel").get_text()
        data_price = basic_data.find("div", class_="ShortAuctionDataValue").get_text()
        data_price = int(data_price.replace(" ", "").replace(",", ""))
        basic_data = soup.find("div", class_="AuctionBodyBlock CurrentBid")
        try:
            auction_status = basic_data.find("div", class_="AuctionInfo").get_text()
        except AttributeError:
            auction_status = None
        auction = Character.objects.get(auction_link=link)
        if not int(data_price) == int(auction.price):
            auction.price = data_price
        if not status_bid == auction.bid_status:
            auction.bid_status = status_bid
        if not auction_status == auction.auctions_status:
            auction.auctions_status = auction_status
        auction.save()

        print("-------------------------")
        print("-------------------------")
        print(auction.price)
        print(type(auction.price))
        print("-------------------------")
        print(0.12)
        print(type(0.12))
        print("-------------------------")
        result = round(int(auction.price) * 0.12)
        print(result)
        print(type(result))
        print("-------------------------")
        print("-------------------------")

        option_1 = round(auction.price * 0.12 + 50)
        option_2 = 50
        option_3 = round(auction.price * 0.1)
        option_4 = 0

        if (
            auction.auctions_status == "finished"
            and auction.bid_status == "Winning Bid:"
            and auction.commission == 0
        ):
            auction.commission = option_1
        if (
            auction.auctions_status == "will be transferred at the next server save"
            and auction.bid_status == "Winning Bid:"
            and auction.commission == 0
        ):
            auction.commission = option_1
        if (
            auction.auctions_status == "currentlyprocessed"
            and auction.bid_status == "Winning Bid:"
            and auction.commission == 0
        ):
            auction.commission = option_4
        if (
            auction.auctions_status == "finished"
            and auction.bid_status == "Minimum Bid:"
            and auction.commission == 0
        ):
            auction.commission = option_2
        if (
            auction.auctions_status == "cancelled"
            and auction.bid_status == "Winning Bid:"
            and auction.commission == 0
        ):
            auction.commission = option_3
        auction.save()


update_character()
