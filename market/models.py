from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.


class Character(models.Model):

    auction_link = models.URLField(unique=True)
    auction_start = models.DateTimeField()
    auction_end = models.DateTimeField()
    bid_status = models.CharField(max_length=40)
    price = models.IntegerField()*
    level = models.CharField(max_length=24)
    experience = models.CharField(max_length=36)
    gold = models.CharField(max_length=36)
    vocation = models.CharField(max_length=40)
    sex = models.CharField(max_length=10)
    server = models.ForeignKey('Server', on_delete=models.CASCADE)
    skills = models.JSONField()
    hp = models.CharField(max_length=42)
    mana = models.CharField(max_length=42)
    capacity = models.CharField(max_length=42)
    speed = models.CharField(max_length=42)
    all_outfit = models.IntegerField()*
    basic_outfit = models.IntegerField()*
    store_outfit = models.IntegerField()*
    all_mount = models.IntegerField()*
    basic_mount = models.IntegerField()*
    store_mount = models.IntegerField()*
    quantity_charms = models.IntegerField()*
    charm_list = ArrayField(base_field=models.CharField(max_length=200))
    charm_point = models.CharField(max_length=42)
    charm_expension = models.BooleanField()
    prey_slot = models.BooleanField()
    quest_list = ArrayField(base_field=models.CharField(max_length=300)) #mozna podac liste
    quantity_quest = models.IntegerField()*
    auctions_status = models.CharField(max_length=264, null=True, blank=True)
    commission = models.IntegerField(default=0)


class Server(models.Model):

    server = models.CharField(max_length=20, unique=True)
    server_type = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    battlEye = models.CharField(max_length=20)



