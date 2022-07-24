from bs4 import BeautifulSoup
import requests
from market.models import Character
from time import sleep


def update_character():
    for link in Character.objects.filter(commission=0).values_list(
        "auction_link", flat=True
    ):
        sleep(0.4)
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

        option_1 = round(int(auction.price) * 0.12 + 50)
        option_2 = 50
        option_3 = round(int(auction.price) * 0.1)
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
