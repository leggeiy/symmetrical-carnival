import discord
from discord.ext import commands
from config import token
from logic import Pokemon, Wizard, Fighter
import random

# Setting up intents for the bot
intents = discord.Intents.default()  # Getting the default settings
intents.messages = True              # Allowing the bot to process messages
intents.message_content = True       # Allowing the bot to read message content
intents.guilds = True                # Allowing the bot to work with servers (guilds)

# Creating a bot with a defined command prefix and activated intents
bot = commands.Bot(command_prefix='!', intents=intents)

# An event that is triggered when the bot is ready to run
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')  # Outputs the bot's name to the console

# The '!go' command
@bot.command()
async def go(ctx):
    author = ctx.author.name  # Getting the name of the message's author
    # Check whether the user already has a Pokémon. If not, then...
    if author not in Pokemon.pokemons.keys():
        chance = random.randint(1,3)
        if chance == 1:
            pokemon = Pokemon(author, "None") 
        elif chance == 2:
            pokemon = Wizard(author, "None")
        elif chance == 3:
            pokemon = Fighter(author, "None")
        await ctx.send(await pokemon.info())  # Sending information about the Pokémon
        await ctx.send(str(chance))
        image_url = await pokemon.show_img()  # Getting the URL of the Pokémon image
        if image_url:
            embed = discord.Embed()  # Creating an embed message
            embed.set_image(url=image_url)  # Setting up the Pokémon's image
            await ctx.send(embed=embed)  # Sending an embedded message with an image
        else:
            await ctx.send("Failed to upload an image of the pokémon.")
        m = random.randint(1,1000000000000)
        if m == 1:
            await ctx.send("Congrats! you got a special Pokemon, you got 20-ish more levels!")
            pokemon.level = pokemon.level + 20.48
    else:
        await ctx.send("You've already created your own Pokémon.")  # A message that is printed whether a Pokémon has already been created
# Running the bot
@bot.command()
async def upgrade(ctx):
    author = ctx.author.name
    if author not in Pokemon.pokemons.keys():
        await ctx.send("You have No Pokemon, use !go to make one")
    else:
        brokemon = Pokemon.pokemons[author]
        
        await ctx.send(await brokemon.givm())
        await ctx.send(f"Your Pokemon is now Level {brokemon.level}")

@bot.command()
async def feed(ctx):
    author = ctx.author.name
    if author not in Pokemon.pokemons.keys():
        await ctx.send("You have No Pokemon, use !go to make one")
    else:
        brokemon = Pokemon.pokemons[author]
        await ctx.send(await brokemon.feed())

@bot.command()
async def attack(ctx):
    target = ctx.message.mentions[0] if ctx.message.mentions else None
    if target:
        if target.name in Pokemon.pokemons and ctx.author.name in Pokemon.pokemons:
            enemy = Pokemon.pokemons[target.name]
            attacker = Pokemon.pokemons[ctx.author.name]
            result = await attacker.attack(enemy)
            await ctx.send(result)
        else:
            await ctx.send("Kedua pemain harus memiliki Pokémon untuk pertarungan!")
    else:
        await ctx.send("Tetapkan pemain yang ingin Anda serang dengan menyebutnya.")

@bot.command()
async def get_crystals(ctx):
    author = ctx.author.name
    if author not in Pokemon.pokemons.keys():
        await ctx.send("You have No Pokemon, so you are sad, use !go to do the thing.")
    else:
        brokemon = Pokemon.pokemons[author]
        await brokemon.goodier()
        await ctx.send(f"Getting Food..")
        await ctx.send(f"you now have {brokemon.food} food things")    
@bot.command()
async def nickname(ctx, *, nicky: str = "None"):
    author = ctx.author.name
    if author not in Pokemon.pokemons:
        await ctx.send("You have no Pokémon! Use `!go` to make one.")
    else:
        bokemon = Pokemon.pokemons[author]
        await bokemon.changenickname(nicky)
        await ctx.send(f"Your Pokémon has been nicknamed {nicky}!")
@bot.command()
async def info(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons.keys():
        bokemon = Pokemon.pokemons[author]
        await ctx.send(await bokemon.info())  # Sending information about the Pokémon
        image_url = await bokemon.show_img()  # Getting the URL of the Pokémon image
        if image_url:
            embed = discord.Embed()  # Creating an embed message
            embed.set_image(url=image_url)  # Setting up the Pokémon's image
            await ctx.send(embed=embed)  # Sending an embedded message with an image
        else:
            await ctx.send("Failed to upload an image of the pokémon.")        
    else:
        await ctx.send("You have no Pokemon, use !go to make one")
bot.run(token)
