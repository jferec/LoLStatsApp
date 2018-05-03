
# Create your models here.
from django.db import models
from django.contrib.postgres.fields import ArrayField

REGION_CHOICES = (
    ('ru', 'Russia'),
    ('kr', 'Korea'),
    ('br1', 'Brazil'),
    ('oc1', 'Oceania'),
    ('jp1', 'Japan'),
    ('na1', 'North America'),
    ('eun1', 'Europe Nordic & East'),
    ('euw1', 'Europe West'),
    ('tr', 'Turkey'),
    ('la1', 'Latin America North'),
    ('la2', 'Latin America South'),
)


class Game(models.Model):

    #   ts - timestamp  ||  final - at the end of the game
    id = models.BigIntegerField(primary_key=True)
    region = models.CharField(
        max_length=4,
        choices=REGION_CHOICES,
        default='na1',
    )
    # duration of a game in seconds
    game_duration = models.PositiveSmallIntegerField()
    # date of the game in UNIX time
    game_date = models.BigIntegerField()
    # true if blue team won
    blue_team_win = models.BooleanField()
    # array of 10 values stating champion ids
    champion = ArrayField(models.PositiveSmallIntegerField())
    # array of 10 positions of players
    lane = ArrayField(models.CharField(max_length=6))
    # array of 10 arrays that include final items id
    final_item_set = ArrayField(ArrayField(models.PositiveSmallIntegerField()))
    # array of 10 creep scores
    final_creep_score = ArrayField(models.PositiveIntegerField())
    # 10 arrays of timestamps with creep scores
    ts_creep_score = ArrayField(ArrayField(models.PositiveSmallIntegerField()))
    ts_experience = ArrayField(ArrayField(models.PositiveIntegerField()))
    final_level = ArrayField(models.PositiveSmallIntegerField())
    ts_level = ArrayField(ArrayField(models.PositiveSmallIntegerField()))
    final_gold = ArrayField(models.PositiveIntegerField())
    ts_gold = ArrayField(ArrayField(models.PositiveIntegerField()))
    final_dmg_to_champions = ArrayField(ArrayField(models.PositiveIntegerField()))
    final_dmg_taken = ArrayField(ArrayField(models.PositiveIntegerField()))
    final_kda = ArrayField(ArrayField(models.PositiveSmallIntegerField()))
    final_vision_score = ArrayField(models.PositiveSmallIntegerField())
    created = models.BigIntegerField()

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ('created',)
        unique_together = (('id', 'region'),)


class Player(models.Model):

    TIER_CHOICES = (
        ('Unranked', 'Unranked'),
        ('Bronze', 'Bronze'),
        ('Silver', 'Silver'),
        ('Gold', 'Gold'),
        ('Platinum', 'Platinum'),
        ('Diamond', 'Diamond'),
        ('Master', 'Master'),
        ('Challenger', 'Challenger'),
    )
    DIVISION_CHOICES = (
        ('', ''),
        ('I', 'I'),
        ('II', 'II'),
        ('III', 'III'),
        ('IV', 'IV'),
        ('V', 'V'),
    )
    id = models.BigIntegerField(primary_key=True)
    account_id = models.BigIntegerField(unique=True)
    region = models.CharField(
        max_length=4,
        choices=REGION_CHOICES,
        default='EUW',
    )
    summoner_name = models.TextField(max_length=16)
    profile_icon_id = models.PositiveSmallIntegerField()
    summoner_level = models.PositiveSmallIntegerField()
    ranked_tier = models.CharField(
        max_length=10,
        choices=TIER_CHOICES,
        default= 'Unranked',
        null=True,
    )
    ranked_division = models.CharField(
        max_length=3,
        choices=DIVISION_CHOICES,
        default=None,
        null=True,
    )
    ranked_wins = models.PositiveIntegerField()
    ranked_losses = models.PositiveIntegerField()
    league_points = models.PositiveSmallIntegerField()
    last_update = models.BigIntegerField()

    def __str__(self):
        return str(self.summoner_name)

    class Meta:
        ordering = ('last_update',)
        unique_together = (('id', 'region'),)
