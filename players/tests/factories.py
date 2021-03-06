import random
import factory
from factory.django import DjangoModelFactory
from players.models import Player

emoji_list = ['sweat_smile','smile_cat','smiley','confused','muscle','woman_shrugging','black_heart','purple_heart','blue_heart','ok','ok_hand']
pronoun_list = ['they/them', 'she/her', 'he/him']

class PlayerFactory(DjangoModelFactory):
    
    class Meta:
        model = Player

    user = factory.SubFactory('buzz.tests.factories.UserFactory')
    name_phonetic = factory.LazyAttribute(lambda obj: f'{obj.user.username} how it sounds')
    pronouns = factory.LazyAttribute(lambda x: random.choice(pronoun_list))
    twitch_username = factory.LazyAttribute(lambda obj: obj.user.username)
    discord_username = factory.LazyAttribute(lambda obj: obj.user.username)
    bio = factory.Faker('sentence', nb_words=20)
    emoji = factory.LazyAttribute(lambda a: random.choice(emoji_list))
                

