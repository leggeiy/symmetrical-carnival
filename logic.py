import aiohttp  # A library for asynchronous HTTP requests
import random

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
        self.moves = []
        self.power = random.randint(30, 60)
        self.hp = random.randint(200, 400)
        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]
            

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

    async def foodie(self):
        if self.food > 0:
            self.food = self.food- 50
            self.level = self.level + 1
            return "Feeding your pokemon"
        else:
            return "There is No Food!"

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
    
    async def get_moves(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    for move_entry in data["moves"]:
                        for detail in move_entry["version_group_details"]:
                            if (detail["level_learned_at"] == self.level and
                                detail["move_learn_method"]["name"] == "level-up"):
                                move_name = move_entry["move"]["name"]
                                if move_name not in self.abilities:
                                    self.abilities.append(move_name)
                    m = ", ".join(self.abilities)
                    return f"Your Pokemon's Current Moves are: {m}"

    async def attack(self, enemy):
        if isinstance(enemy, Wizard):
            chance = random.randint(1, 5)
            if chance == 1:
                return "Pokemon Penyihir menggunakan perisai dalam pertarungan"
        
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Pertarungan @{self.pokemon_trainer} dengan @{enemy.pokemon_trainer}"
        else:
            enemy.hp = 0
            return f"@{self.pokemon_trainer} menang melawan @{enemy.pokemon_trainer}!"


    async def info(self):
        # A method that returns information about the pokémon
        if not self.name:
            self.name = await self.get_name()  # Retrieving a name if it has not yet been uploaded
        return f"""The name of your Pokémon: {self.name} 
        The Nickname of your pokemon: {self.nickname}
        The Level of your Pokemon: {self.level}
        The Power of your Pokemon: {self.power}
        The HP of your pokemon: {self.hp}"""  # Returning the string with the Pokémon's name

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
    pass


class Fighter(Pokemon):
    async def attack(self, enemy):
        super_power = random.randint(5, 15)
        self.power += super_power
        result = await super.attack(enemy)
        self.power -= super_power
        return result + f"\nPetarung menggunakan serangan super dengan kekuatan:{super_power}"