from rest_framework import serializers

from market.models import Character, Server


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = (
            "id",
            "auction_link",
            "character_name",
            "auction_start",
            "auction_end",
            "bid_status",
            "price",
            "level",
            "experience",
            "gold",
            "vocation",
            "sex",
            "server",
            "skills",
            "hp",
            "mana",
            "capacity",
            "speed",
            "all_outfit",
            "basic_outfit",
            "store_outfit",
            "all_mount",
            "basic_mount",
            "store_mount",
            "quantity_charms",
            "charm_list",
            "charm_point",
            "charm_expension",
            "prey_slot",
            "quest_list",
            "quantity_quest",
            "auctions_status",
            "commission",
        )


class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = ("id", "server", "server_type", "location", "battlEye")


class DataFilterSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=80, required=False)
    from_date = serializers.DateField(required=False)
    to_date = serializers.DateField(required=False)
