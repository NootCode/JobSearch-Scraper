import os
import csv
import discord
from dotenv import load_dotenv
from discord.ext import commands
from itertools import islice
import linkedInScraper

load_dotenv('./data/bot_token.env')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!', intents = discord.Intents().all())

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild: \n' 
        f'{guild.name} (id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@bot.command(name='links')
async def print_links(ctx, number_of_entries = 1, job_query = "Software Engineer"):
    linkedInScraper.linkedInScraper(job_query, number_of_entries).get_all_linkedin_links()
    with open('./data/linkedin-jobs.csv', encoding = 'utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader: # first 10 only
            msg = await ctx.send(embed=create_embed(row, "Pending"))
            checkM = "✅"
            redX = "❌"
            await msg.add_reaction(checkM)
            await msg.add_reaction(redX)

def create_embed(row, status):
    embed = discord.Embed(title = row['Company'], url=row['Link'], description=row['Title'], color=0x0000FF)
    embed.set_author(name= row['Source'], icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ8whb8SkaWBcWU3sUtYa_wezXAr30vM2uekWzlISCL&s")
    embed.add_field(name="Location", value= row['Location'], inline= True)
    embed.add_field(name="Status", value= status, inline= True)
    return embed

@bot.event
async def on_reaction_add(reaction, user):
    for role in user.roles:
        if role.name == 'Bot':
            return

    checkM = "✅"
    redX = "❌"
    if reaction.emoji == checkM:
        await reaction.message.clear_reactions()
        # send same message into the applied channel
        embed_dict = reaction.message.embeds[0].to_dict()
        for field in embed_dict["fields"]:
            if field["name"] == "Status":
                field["value"] = "Applied"
        embed = discord.Embed.from_dict(embed_dict)
        await reaction.message.edit(embed=embed)
        print("applied")

    if reaction.emoji == redX:
        #delete message from server
        await reaction.message.delete()

bot.run(TOKEN)