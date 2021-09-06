from keep_alive import keep_alive
from replit import db

import discord
import os

client = discord.Client()

#print(f"The Teams are: \n {db['t1name']} & {db['t2name']} \n {db['t1score']} & {db['t2score']}")

client.keywords = {"nt", "newteams", "teams", "t", "reset", "1", "2", "sm", "scoremode", "one", "two", "help", "h", "r"}

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    ###Displays current teams and their score
    if message.content == "!teams" or message.content == "!t":
      await message.channel.send(f'Team One: {db["t1name"]} : {db["t1score"]} Points \nTeam Two: {db["t2name"]} : {db["t2score"]} Points ')

    ###Resets both teams scores to 0
    if message.content == "!reset" or message.content == "!r":
      
      db["t1score"] = 0
      db["t2score"] = 0

      await message.channel.send(f'Both teams ({db["t1name"]} & {db["t2name"]}) have been reset to 0 points.')
    
    ###Creates new teams
    if message.content.startswith("!newteams ") or message.content.startswith("!nt "):
      discordMessage = message.content
      splitMessageOnce = discordMessage.split(" ", 1)      
      splitMessageTwice = splitMessageOnce[1].split(" & ", 1)

      try:
        if(splitMessageTwice[0] == splitMessageTwice[1]):
          await message.channel.send("Can't have two teams of the same name. Because then you would be part of the same team silly.")

        elif(splitMessageTwice[0].lower() in client.keywords):
          await message.channel.send(f"Team name ({splitMessageTwice[0]}) is a reserved keyword. ")

        elif(splitMessageTwice[1].lower() in client.keywords):
          await message.channel.send(f"Team name ({splitMessageTwice[1]}) is a reserved keyword. ")

        else:  
          db["t1name"] = splitMessageTwice[0]
          db["t2name"] = splitMessageTwice[1]
          db["t1score"] = 0
          db["t2score"] = 0
          await message.channel.send(f'The teams for this round are {db["t1name"]} & {db["t2name"]}.')
      except:
        await message.channel.send("To add new teams you need to use one of the following commands: \n \n !newteams TEAMNAME1 & TEAMNAME2 \n !nt TEAMNAME1 & TEAMNAME2 \n \n Ensure there is a space on either side of the & symbol.")
        return;
    
    ###Adds/Removes Points to Team One using 1 or one
    lowerCaseMessage = message.content.lower()
    if lowerCaseMessage.startswith("!1 ") or lowerCaseMessage.startswith("!one "):      
      stripMessage = lowerCaseMessage.split(' ', 1)[1]

      negativeNumber = False;
      if("-" in stripMessage[0]):
        strippedNegative = stripMessage.replace("-", "")
        if(strippedNegative.isnumeric()):
          negativeNumber = True;

      if(len(stripMessage) >= 1):
        if(stripMessage.isnumeric() or negativeNumber == True):

          if(negativeNumber == True):
            db["t1score"] = db["t1score"] +  int(stripMessage)
          elif(negativeNumber == False):
            db["t1score"] = db["t1score"] +  int(stripMessage)

          if(db["sm"] == True and negativeNumber == False):
            await message.channel.send(f'{db["t1name"]} has gained   {stripMessage} points and now has a score of {db["t1score"]}.')

          if(db["sm"] == True and negativeNumber == True):
            stripNegative = stripMessage.replace('-', '')
            await message.channel.send(f'{db["t1name"]} has lost  {stripNegative} points and now has a score of {db["t1score"]}.')

          if(db["sm"] == False and negativeNumber == False):
            await message.channel.send(f'{db["t1name"]} has gained {stripMessage} points.')

          if(db["sm"] == False and negativeNumber == True):
            stripNegative = stripMessage.replace('-', '')
            await message.channel.send(f'{db["t1name"]} has lost {stripMessage} points.')

        if(len(stripMessage) > 1):
          if(negativeNumber == False and stripMessage[1].isnumeric() == False):
            await message.channel.send("Invalid number. To add points to a team, use the following command: \n \n !TEAMNAME X \n or \n !1 X \n or !one X \n or \n \n Where X is the value of the points you want to add.")
            return;

    ###Adds/Removes Points to Team Two using 2 or two
    lowerCaseMessage = message.content.lower()
    if lowerCaseMessage.startswith("!2 ") or lowerCaseMessage.startswith("!two "):      
      stripMessage = lowerCaseMessage.split(' ', 1)[1]

      negativeNumber = False;
      if("-" in stripMessage[0]):
        strippedNegative = stripMessage.replace("-", "")
        if(strippedNegative.isnumeric()):
          negativeNumber = True;

      if(len(stripMessage) >= 1):

        if(stripMessage.isnumeric() or negativeNumber == True):

          if(negativeNumber == True):
            db["t2score"] = db["t2score"] +  int(stripMessage)
          elif(negativeNumber == False):
            db["t2score"] = db["t2score"] +  int(stripMessage)

          if(db["sm"] == True and negativeNumber == False):
            await message.channel.send(f'{db["t2name"]} has gained  {stripMessage} points and now has a score of {db["t2score"]}.')

          if(db["sm"] == True and negativeNumber == True):
            stripNegative = stripMessage.replace('-', '')
            await message.channel.send(f'{db["t2name"]} has lost  {stripNegative} points and now has a score of {db["t2score"]}.')

          if(db["sm"] == False and negativeNumber == False):
            await message.channel.send(f'{db["t2name"]} has gained {stripMessage} points.')

          if(db["sm"] == False and negativeNumber == True):
            stripNegative = stripMessage.replace('-', '')
            await message.channel.send(f'{db["t2name"]} has lost {stripMessage} points.')

        if(len(stripMessage) > 1):
          if(negativeNumber == False and stripMessage[1].isnumeric() == False):
            await message.channel.send("Invalid number. To add points to a team, use the following command: \n \n !TEAMNAME X \n or \n !1 X \n or !one X \n or \n \n Where X is the value of the points you want to add.")
            return;

    ###Toggles whether score displays with each change
    if message.content == "!scoremode" or message.content == "!sm":
      db["sm"] = not db["sm"]

      if(db["sm"]):
        await message.channel.send("The Score will be displayed each time the score is updated.")

      if(not db["sm"]):
        await message.channel.send("The Score will remain a secret until the end of the game.")
        return;

    ###Displays Help Commands
    if message.content == "!help" or message.content == "!h":
      await message.channel.send("WhatsThePoint tracks points between two teams. The available commands are as follows (Replace the capitalized words with your own values): \n \n ==========Creating Teams========== \n !newteams TEAMNAME1 & TEAMNAME2          Creates two new teams with 0 points. \n !nt TEAMNAME1 & TEAMNAME2                Creates two new teams with 0 points. \n \n ==========Add/Remove Points=========== \n !1 POINTS          Adds points to team one.\n !2 -POINTS         Removes points from team two. \n \n ==========Reset Points=========== \n !reset          Resets all points to zero. \n !r              Resets all points to zero. \n \n ==========Show Team Info=========== \n !teams          Shows team names and score. \n !t              Shows team names and score. \n \n ==========Toggle Scoremode=========== \n !scoremode          Changes whether total score is shown each round. \n !sm                 Changes whether total score is shown each round. \n \n =====================")

keep_alive()
client.run(os.getenv('TOKEN'))


