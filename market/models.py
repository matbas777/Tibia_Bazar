from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.


class Character(models.Model):

    auction_link = models.URLField
    auction_start = models.DateTimeField()
    auction_end = models.DateTimeField()
    auction_status = models.CharField(max_length=40)
    price = models.BigIntegerField()
    level = models.BigIntegerField()
    experience = models.BigIntegerField()
    gold = models.BigIntegerField()
    vocation = models.CharField(max_length=40)
    sex = models.CharField(max_length=10)
    server = models.ForeignKey('Server', on_delete=models.CASCADE)
    skills = models.JSONField()
    hp = models.IntegerField()
    mana = models.IntegerField()
    capacity = models.IntegerField()
    speed = models.IntegerField()
    all_outfit = models.IntegerField()
    basic_outfit = models.IntegerField()
    store_outfit = models.IntegerField()
    all_mount = models.IntegerField()
    basic_mount = models.IntegerField()
    store_mount = models.IntegerField()
    quantity_charms = models.IntegerField
    charm_list = ArrayField(base_field=models.CharField(max_length=200))
    charm_point = models.IntegerField()
    charm_expension = models.BooleanField()
    prey_slot = models.BooleanField()
    quest_list = ArrayField(base_field=models.CharField(max_length=300)) #mozna podac liste
    quantity_quest = models.IntegerField()


class Server(models.Model):

    server = models.CharField(max_length=20)
    server_type = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    battlEye = models.CharField(max_length=20)


class Cipsoftcalculator(models.Model):
    character = models.ForeignKey('Character', on_delete=models.CASCADE)
    mount_PLN = models.DecimalField
    date start
    date end
    amount tc
    auctions numbers
    auctions earn
    auctions commission

