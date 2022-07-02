from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.


class Character(models.Model):

    auction_link = models.URLField(unique=True)
    Character_name = models.CharField(max_length=80)
    auction_start = models.DateTimeField(null=True, blank=True)
    auction_end = models.DateTimeField(null=True, blank=True)
    bid_status = models.CharField(max_length=40, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    level = models.CharField(max_length=24, null=True, blank=True)
    experience = models.CharField(max_length=36, null=True, blank=True)
    gold = models.CharField(max_length=36, null=True, blank=True)
    vocation = models.CharField(max_length=40, null=True, blank=True)
    sex = models.CharField(max_length=10, null=True, blank=True)
    server = models.ForeignKey('Server', on_delete=models.CASCADE, null=True, blank=True)
    skills = models.JSONField(null=True, blank=True)
    hp = models.CharField(max_length=42, null=True, blank=True)
    mana = models.CharField(max_length=42, null=True, blank=True)
    capacity = models.CharField(max_length=42, null=True, blank=True)
    speed = models.CharField(max_length=42, null=True, blank=True)
    all_outfit = models.CharField(max_length=42, null=True, blank=True)
    basic_outfit = models.CharField(max_length=42, null=True, blank=True)
    store_outfit = models.IntegerField(null=True, blank=True)
    all_mount = models.CharField(max_length=42, null=True, blank=True)
    basic_mount = models.CharField(max_length=42, null=True, blank=True)
    store_mount = models.IntegerField(null=True, blank=True)
    quantity_charms = models.IntegerField(null=True, blank=True)
    charm_list = ArrayField(base_field=models.CharField(max_length=200), null=True, blank=True)
    charm_point = models.CharField(max_length=42, null=True, blank=True)
    charm_expension = models.BooleanField(null=True, blank=True)
    prey_slot = models.BooleanField(null=True, blank=True)
    quest_list = ArrayField(base_field=models.CharField(max_length=300), null=True, blank=True) #mozna podac liste
    quantity_quest = models.IntegerField(null=True, blank=True)
    auctions_status = models.CharField(max_length=264, null=True, blank=True)
    commission = models.IntegerField(default=0)


class Server(models.Model):

    def __str__(self):
        return self.server

    server = models.CharField(max_length=20, unique=True)
    server_type = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    battlEye = models.CharField(max_length=20)



