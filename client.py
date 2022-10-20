import asyncio
import json

import nextcord
from nextcord.ext import commands
import tweepy
import time
loop = ""

from config import API_SECRECT, API_KEY, BEARER_TOKEN, account_list, DISCORD_TOKEN

TESTING_GUILD_ID = 721374983837974570  # Replace with your guild ID
intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.slash_command(description="list of all accounts followed by bot", guild_ids=[TESTING_GUILD_ID])
async def list(interaction: nextcord.Interaction):
    with open("list.json") as f:
        jsondata = json.load(f)
    f.close()
    if str(interaction.guild.id) not in jsondata.keys():
        jsondata[str(interaction.guild.id)] = []
    if jsondata[str(interaction.guild.id)] == []:
        with open("list.json","w") as f:
            json.dump(jsondata,f)
        f.close()
        await interaction.channel.send("It's seems there aren't any followed accounts in your server. Add one with /addaccount")
        await interaction.response.send_message("here you are")
        return
    embed = nextcord.Embed(title="Followed accounts", description="Bot will send tweets from theese accounts")
    account_list = jsondata[str(interaction.guild.id)]
    for account in account_list:
        user = api.get_user(screen_name=account)
        embed.add_field(name=user.name, value=f"[@{user.screen_name}](https://twitter.com/{user.screen_name})",
                        inline=False)
    await interaction.channel.send(embed=embed)
    await interaction.response.send_message("here you are",ephermal=True)
    return 0

@commands.is_owner()
@bot.slash_command(description="Add new account to follow",guild_ids=[TESTING_GUILD_ID])
async def addaccount(interaction:nextcord.Interaction, screen_name:str):



    with open("list.json") as f:
        jsondata = json.load(f)
    f.close()
    if not str(interaction.guild.id) in jsondata.keys():
       jsondata[str(interaction.guild.id)] = []
    if screen_name in jsondata[str(interaction.guild.id)]:
        m = await interaction.send("This user is alredy followed")
        await m.delete(delay=2)
        return
    try:
        user = api.get_user(screen_name=screen_name)

    except:
        await interaction.send(f"Cannot find user:{screen_name}")
        return
    embed = nextcord.Embed(title="Adding new account")
    embed.add_field(name="username", value=user.screen_name)
    embed.add_field(name="name", value=user.name, inline=False)
    if user.description:
        embed.add_field(name="description", value=user.description, inline=False)
    message = await interaction.channel.send(embed=embed)

    await message.add_reaction(emoji="✅")
    await message.add_reaction(emoji="❌")

    if(not screen_name in account_list):
        stream.add_rules(tweepy.StreamRule(f"from: {screen_name}"))
    account_list.add(screen_name)
    temp_list.append(screen_name)
    with open("list.json", "w") as f:
        jsondata[str(str(interaction.guild.id))].append(user.screen_name)
        json.dump(jsondata, f)
    f.close()
@commands.is_owner()
@bot.slash_command(description="stop follow accaunt", guild_ids=[TESTING_GUILD_ID])
async def removeaccount(interaction: nextcord.Interaction, screen_name: str):

    with open("list.json") as f:
        jsondata = json.load(f)
    f.close()
    if not str(interaction.guild.id) in jsondata.keys():
        jsondata[str(interaction.guild.id)] = []
    if screen_name not in jsondata[str(interaction.guild.id)]:
        m = await interaction.send("This server doesn't follow this accaunt")
        await m.delete(delay=2)
        return
    try:
        user = api.get_user(screen_name=screen_name)
        print(user.id)
    except:
        await interaction.send(f"Cannot find user:{screen_name}")
        return
    embed = nextcord.Embed(title="Adding new account")
    embed.add_field(name="username", value=user.screen_name)
    embed.add_field(name="name", value=user.name, inline=False)
    if user.description:
        embed.add_field(name="description", value=user.description, inline=False)
    message = await interaction.channel.send(embed=embed)

    await message.add_reaction(emoji="✅")
    await message.add_reaction(emoji="❌")

    temp_list.remove(user.screen_name)

    global account_list
    account_list = set(temp_list)

    with open("list.json", "w") as f:
        jsondata[str(str(interaction.guild.id))].remove(user.screen_name)

        json.dump(jsondata, f)
    f.close()
    if not user.screen_name in account_list:
        for rule in stream.get_rules()[0]:
            if(rule[0] == f"from: {user.screen_name}"):
                stream.delete_rules(rule)








with open("list.json") as f:
    jsondata = json.load(f)
f.close()
temp_list =[]
account_list = []

for guild in jsondata.keys():
    for account in jsondata[guild]:
        temp_list.append(str(account))

account_list = set(temp_list)
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRECT)
api = tweepy.API(auth)

class MyStream(tweepy.StreamingClient):

    # This function gets called when the stream is working
    def on_connect(self):
        print("Connected")


    # This function gets called when a tweet passes the stream
    def on_tweet(self, tweet):
        # Displaying tweet in console
        if tweet.referenced_tweets == None:

            print(tweet.text)

            #send_tweet(tweet)

            for guild in bot.guilds:
                channel = nextcord.utils.get(guild.channels, name="political_bot")

                user = api.get_user(id=tweet.author_id)


                bot.loop.create_task(channel.send(f"https://twitter.com/{user.screen_name}/status/{tweet.id}"))
            time.sleep(0.5)





intents = nextcord.Intents.default()
intents.message_content = True
loop = ""

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRECT)
api = tweepy.API(auth)






stream = MyStream(bearer_token=BEARER_TOKEN)




def get_stream():
    return stream
print(account_list)

# for rule in stream.get_rules()[0]:
#     stream.delete_rules(rule)


for user in account_list:

    stream.add_rules(tweepy.StreamRule(f"from: {user}"))





# y = threading.Thread(target=lambda: stream.filter(is_async=True))
# y.start()

thread = stream.filter(threaded=True,tweet_fields=['author_id'])

bot.run(DISCORD_TOKEN)



