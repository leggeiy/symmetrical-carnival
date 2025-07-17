import aiohttp  # A library for asynchronous HTTP requests
import random
from datetime import datetime, timedelta
class Pokemon:
    pokemons = {}
    # Object initialisation (constructor)
    def __init__(self, pokemon_trainer, nickname):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.abilities = []
        self.nickname = nickname
        self.level = 0
        self.food = 200
        self.lastfeedtime = datetime.now()
        self.power = random.randint(30, 60)
        self.hp = random.randint(200, 400)
        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]
            
        

    async def feed(self, feedinterval=60, hp_increase=10):
        nowtime = datetime.now()
        deltatime = timedelta(seconds=feedinterval)
        if (nowtime - self.lastfeedtime) > deltatime:
            self.hp += hp_increase
            return f"Health Increased to {self.hp}"
        else:
            return f"Too Early!"

    async def get_name(self):
        # An asynchronous method to get the name of a pokémon via PokeAPI
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # URL API for the request
        async with aiohttp.ClientSession() as session:  # Opening an HTTP session
            async with session.get(url) as response:  # Sending a GET request
                if response.status == 200:
                    data = await response.json()  # Receiving and decoding JSON response
                    return data['forms'][0]['name']  # Returning a Pokémon's name
                else:
                    return "Pikachu"  # Return the default name if the request fails



    async def changenickname(self, a):
        self.nickname = a

    async def givm(self):
        if self.food > 0:
            self.food = self.food- 50
            self.level = self.level + 1
            return "Upgrading your pokemon"
        else:
            return "You have no Crystals!"

    async def goodier(self):
        self.food = self.food + 200

    async def get_abilities(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    for ability_entry in data["abilities"]:
                        self.abilities.append(ability_entry["ability"]["name"])
                    x = ", ".join(self.abilities)
                    y = f"Your Pokemon's Abilities are: {x}"
                    return y

    async def attack(self, enemy):
        if isinstance(enemy, Wizard):
            chance = random.randint(1, 5)
            if chance == 1:
                return "Pokemon Penyihir menggunakan perisai dalam pertarungan"
        ehp = enemy.hp * (enemy.level *5)
        spwr = self.power * (self.level * 2.5)
        if ehp > spwr:
            enemy.hp -= spwr
            return f"Pertarungan @{self.pokemon_trainer} dengan @{enemy.pokemon_trainer}"
        else:
            enemy.hp <= 0
            return f"@{self.pokemon_trainer} menang melawan @{enemy.pokemon_trainer}!"


    async def info(self):
        # A method that returns information about the pokémon
        #self = await self.get_name()
        #self = await self.get_abilities()  # Retrieving a name if it has not yet been uploaded
        return f"""
        The Name of your Pokémon:  
        The Nickname of your Pokémon: {self.nickname}
        The Level of your Pokémon: {self.level}
        The Power of your Pokémon: {self.power}
        The HP of your Pokémon: {self.hp}
        The Abilities of your Pokémon:"""  # Returning the string with the Pokémon's name

    async def show_img(self):
        # An asynchronous method to retrieve the URL of a pokémon image via PokeAPI
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # URL API for the request
        async with aiohttp.ClientSession() as session:  # Opening an HTTP session
            async with session.get(url) as response:  # Sending a GET request
                if response.status == 200:
                    data = await response.json()  # Receiving and decoding JSON response
                    return data['sprites']['front_default']  # Returning a Pokémon's image
                else:
                    return None  # Return the default name if the re
                


class Wizard(Pokemon):
    async def feed(self):
        return await super().feed(hp_increase=20)


class Fighter(Pokemon):
    async def feed(self):
        return await super().feed(feedinterval=40)
    async def attack(self, enemy):
        super_power = random.randint(5, 15)
        self.power += super_power
        result = await super().attack(enemy)
        self.power -= super_power
        return result + f"\nPetarung menggunakan serangan super dengan kekuatan:{super_power}"