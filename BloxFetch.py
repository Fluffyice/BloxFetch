import discord
from discord.ext import commands
import asyncio
import requests
import json

token = ""  # Stores the bot's token. Used to pass the bot's token into bot.run in order to run the bot.
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
bot.Prefix = "!"  # Defines the bot's command prefix.


def getUserId(user):  # Defines function getUserId and requires user to be passed into it when used.
    req = requests.get("https://api.roblox.com/users/get-by-username?username=" + user)  # Fetches the user's information via a Roblox API request.
    arr = req.json()  # Stores the data from the Roblox API request as a JSON object.
    userId = arr["Id"]  # Stores the value of the Id key from the json object.
    return str(userId)  # Returns the userId to the caller.


def fetch(user):  # Defines function fetch and requires user to be passed into it when used.
    userId = getUserId(user)  # Stores the userId retrieved from getUserId.
    response = requests.get("https://groups.roblox.com/v2/users/" + userId + "/groups/roles")  # Fetches the user's group data via a Roblox API Request using their ID stored in the userId variable.
    jsonObj = response.json()  # Stores the data from the Roblox API request as a JSON object.
    data = ""  # Defines data as an empty string. This is defined outside of the for loop in order to prevent it from continually setting the data as an empty string.
    for GroupDat in jsonObj["data"]:  # Loops through the data under the data key in jsonObj.
        groupName = GroupDat["group"]["name"]  # Stores the value of the name key.
        groupRole = GroupDat["role"]["name"]  # Stores the value of the role key.
        data += ("**Group Name:** {}\n").format(groupName)  # Formats the string to say "Group Name: Name of group"
        data += ("**Role:** {}\n\n").format(groupRole)  # Formats the string to say "Role: Name of role"

    return data  # Returns the data from the data variable to the caller.


@bot.event  # Initializes a bot event
async def on_connect():  # Runs the code when the bot connects.
    print("Logged in as " + bot.user.name)  # Prints a message in the console.
    return


@bot.event  # Initializes a bot event.
async def on_message(message):  # Runs the code whenever a message is sent in the server.
    args = str(message.content).lower().split(" ")  # Converts the message.content into an str, lowers the case of all the characters, splits the data into separate keys wherever there's a space, and stores the keys in an array.
    username = str(message.content).split(" ")  # Converts the message.content into an str, splits the data into separate keys wherever there's a space, and stores the keys in an array.
    if args[0] == bot.Prefix + "fetch":  # Runs the code within the if statement if the first key within the args array is equal to bot.Prefix + "fetch".
        if len(args) > 1:  # Runs the code within the if statement if there's more than one key in the args array.
            user = args[1]  # Stores the second key from the args array in the user variable.
            data = fetch(user)  # Passes the user variable into fetch and stores the data it returns in the data variable.
            dataEmbed = discord.Embed(title=username[1] + "'s Group Data", description=data, color=0x2f3136)  # Creates a discord.Embed object with [Username]'s Group Data as the title, the data from the data variable as the description, and 0x2f3136 as the color.
            await message.channel.send(embed=dataEmbed)  # Sends the embed from dataEmbed in the channel the command was triggered in.
        elif len(args) < 2:  # Runs the code in the elif statement if there's less than 2 keys in the args array.
            await message.channel.send("**Correct usage:** `!fetch [User]`")  # Sends a message containing the correct command usage in the channel the command was triggered in.

    elif args[0] == bot.Prefix + "info":  # Runs the code in the elif statement if first key in the args array is bot.Prefix + "info".
        infoEmbed = discord.Embed(description=
                                """**__Commands:__**
                                **!fetch [User!]** - Fetches and displays the Roblox group data for any given user.
                                **!help** - Displays this info message.
                        
                                **__About:__
                                **BloxFetch is a bot designed to fetch the Roblox group data for any given user. The source code can be found at **<https://github.com/Fluffyice/BloxFetch>.**""",
                                  color=0x2f3136)  # Creates a discord.Embed object with a list of commands and information about the bot as the description and 0x2f3136 as the color.
        await message.channel.send(embed=infoEmbed)  # Sends the embed from infoEmbed in the channel the command was triggered in.
    return


bot.run(token)  # Passes is in the token from the token variable and runs the bot.