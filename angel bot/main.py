import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
import zalgoify

client = discord.Client()

detect_words = [
    "Im sad", "oh my god", "sin", "depressing", "omg", "sad", "Sad", "OMG",
    "I\'m sad", "i\'m sad", "help me", "Help me"
]

angel_encouragements = [
    "Cheer up!", "Hang in there, buddy!",
    "There are people who care about you!", "You're awesome", "I love you"
]

if "responding" not in db.keys():
    #creates the key in the database
    db["responding"] = True


def update_angel_encouragements(amessage):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(amessage)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [amessage]


def delete_angel_encouragements(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
        db["encouragements"] = encouragements


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")

    json_data = json.loads(response.text)

    quote = "\'" + json_data[0]['q'] + "\'" + "\n" + " -" + json_data[0]['a']

    return (quote)


def devilQuote():
    response = requests.get(
        "https://evilinsult.com/generate_insult.php?lang=en&type=json")

    json_data = json.loads(response.text)

    quote = json_data['insult']

    quote = zalgoify.process(quote.upper())

    return (quote)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(msg):
    if msg.author == client.user:
        return

    msg1 = msg.content

    if msg1.startswith('$pray'):
        quote1 = get_quote()
        await msg.channel.send(quote1)

    if msg1.startswith('$demon'):
        quote2 = devilQuote()
        await msg.channel.send(quote2)

    if db["responding"] == True:
        options = angel_encouragements
        if "encouragements" in db.keys():
            options = options + db["encouragements"]

    if msg1.startswith('$new'):
        newmessage = msg1.split("$new ", 1)[1]
        update_angel_encouragements(newmessage)
        await msg.channel.send("New message added")

    if msg1.startswith('$del'):
        encouragements = []
        if "encouragements" in db.keys():
            index = int(msg1.split("$del ", 1)[1])
            delete_angel_encouragements(index)
            encouragements = db["encouragements"]
        await msg.channel.send(encouragements)

    if any(word in msg1 for word in detect_words):
        await msg.channel.send(random.choice(options))

    if msg1.startswith("$rules"):
        await msg.channel.send(
            '\'$pray\' Summons the Angel.' + "\n" +
            "\'$new\' allows the user to add to the Angel Bot\'s responses." +
            "\n" + "\'$del\' Deletes a user submitted quote" + "\n" +
            "\'$responding\' Makes the Angel stop or start responding." +
            "\n" + "\'$demon\' Summons an mean-spirited demon!" + '\n' +
            "Any mention of saddness makes the Angel act.")

    if msg1.startswith("$list"):
        encouragements = []
        if "encouragements" in db.keys():
            encouragements = db["encouragements"]
        await msg.channel.send(encouragements)

    if msg1.startswith("$responding"):
        value = msg1.split("$responding", 1)[1]

        if value.lower() == "true":
            db["responding"] = True
            await msg.channel.send("Responding is on")
        else:
            db["responding"] = False
            await msg.channel.send("Responding is off")


keep_alive()
client.run(os.getenv("TOKEN"))
