from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from market.models import Character, Server
from market.serializers import (
    CharacterSerializer,
    ServerSerializer,
    DataFilterSerializer,
)


class CharacterListAPIView(ListAPIView):
    serializer_class = CharacterSerializer
    queryset = Character.objects.all()


class ServerListAPIView(ListAPIView):
    serializer_class = ServerSerializer
    queryset = Server.objects.all()


class AuctionsDataView(APIView):
    def get(self, request, *args, **kwargs):

        characters_auctions = Character.objects.filter(commission__gt=0)
        data_auction = []

        filter_serializer = DataFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        nickname = filter_serializer.validated_data.get("nickname")
        from_date = filter_serializer.validated_data.get("from_date")
        to_date = filter_serializer.validated_data.get("to_date")

        # nickname_qs = Character.objects.filter(character_name=nickname)
        # date_qs = Character.objects.filter(auction_end__gte=from_date, auction_end__lte=to_date)
        dict_filter = {}
        if nickname:
            dict_filter["character_name"] = nickname
        if from_date:
            dict_filter["auction_end__gte"] = from_date
        if to_date:
            dict_filter["auction_end__lte"] = to_date

        for auction in characters_auctions.filter(**dict_filter):
            data_auction.append(
                {
                    "id": auction.id,
                    "Auction_link": auction.auction_link,
                    "Character_nick": auction.character_name,
                    # "server": auction.server,
                    "Character_lvl": auction.level,
                    "Character_vocation": auction.vocation,
                    "Auction_date": auction.auction_end,
                    "Bid_status": auction.bid_status,
                    "Price": auction.price,
                    "Auctions_status": auction.auctions_status,
                    "Commission": auction.commission,
                }
            )
        return Response(data={"result": data_auction})


class CipSoftCommissionView(APIView):
    def get(self, request, *args, **kwargs):

        filter_serializer = DataFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        from_date = filter_serializer.validated_data.get("from_date")
        to_date = filter_serializer.validated_data.get("to_date")
        # date_qs = Character.objects.filter(auction_end__gte=from_date, auction_end__lte=to_date)

        dict_filter = {}
        if from_date:
            dict_filter["auction_end__gte"] = from_date
        if to_date:
            dict_filter["auction_end__lte"] = to_date

        auctions = Character.objects.filter(**dict_filter)

        earnings = {
            "all_auctions": auctions.count(),
            "purchased_characters": auctions.filter(bid_status="Winning Bid:").count()
            - auctions.filter(auctions_status="cancelled").count(),
            "un_purchased_characters": auctions.filter(
                bid_status="Minimum Bid:"
            ).count(),
            "unpaid_auctions": auctions.filter(auctions_status="cancelled").count(),
            "from_date": from_date,
            "to_date": to_date,
            "commission_balance": sum(auctions.values_list("commission", flat=True)),
        }

        return Response(
            data={"result": earnings, "from_date": from_date, "to date": to_date}
        )
