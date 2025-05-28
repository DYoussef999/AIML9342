#------------------------------------------------import libraries-------------------------------------------------------

import discord
import dotenv
import os
import openai
import asyncio
import random
import csv

#---------------------------------------access sensitive info from .env file--------------------------------------------

dotenv.load_dotenv()
my_bot_token = os.getenv('DISCORD_TOKEN')
print(my_bot_token)
open_ai_api_key = os.getenv('OPENAI_API_KEY')
open_ai_assistant_id = os.getenv('OPENAI_ASSISTANT_ID')
ai = openai.OpenAI(api_key=open_ai_api_key)

#-------------------------------------------------bot permissions-------------------------------------------------------

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#---------------------------------------------run when bot goes online--------------------------------------------------

@client.event
async def on_ready():
    print(f'{client.user} is online')

#----------------------------------------------set command functions----------------------------------------------------

def flip():
    return f'It landed on {random.choice(["heads", "tails"])}!'

def roll():
    return f'You rolled a {random.randint(1, 6)}!'

def rps_rock():
    botRPS = random.choice(["rock", "paper", "scissors"])
    if botRPS == "rock":
        return f'I played {botRPS}, it\'s a tie.'
    elif botRPS == "paper":
        return f'I played {botRPS}, I win!'
    else:
        return f'I played {botRPS}, you win...'

def rps_paper():
    botRPS = random.choice(["rock", "paper", "scissors"])
    if botRPS == "rock":
        return f'I played {botRPS}, you win...'
    elif botRPS == "paper":
        return f'I played {botRPS}, it\'s a tie.'
    else:
        return f'I played {botRPS}, I win!'

def rps_scissors():
    botRPS = random.choice(["rock", "paper", "scissors"])
    if botRPS == "rock":
        return f'I played {botRPS}, I win!'
    elif botRPS == "paper":
        return f'I played {botRPS}, you win...'
    else:
        return f'I played {botRPS}, it\'s a tie.'

def farewell():
    return 'Goodbye...'

def greeting():
    return f'Hello there, I am {client.user}!'

#--------------------------wait for a max of 30 secs or until AI response is generated----------------------------------

async def wait_for_response(thread_id):
    for i in range(30):
        await asyncio.sleep(1)
        messages = ai.beta.threads.messages.list(thread_id=thread_id)
        if len(messages.data) > 1 and len(messages.data[0].content) > 0:
            return messages.data[0].content[0].text.value

#-----------------------------read each row of my_movies.csv into singular string---------------------------------------

async def ask_assistant(channel):
    movie_string = ""
    with open("my_movies.csv", 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            movie_string += f"{row}, "

    #--------------------------------------------clean up string--------------------------------------------------------
    movie_string = movie_string.replace("['', '0'], ","")
    movie_string = movie_string.replace("'","")
    # movie_string = movie_string.replace("[","")
    # movie_string = movie_string.replace("]","")

    #-----------------------------formulate question for AI and set token limits----------------------------------------
    list_of_messages = []
    message = {}
    message['role'] = 'user'
    message['content'] = f'Please recommend me a movie based on my ratings (X/10) of these movies: \"{movie_string}\".'
    list_of_messages.append(message)

    thread = ai.beta.threads.create(messages=list_of_messages)
    ai.beta.threads.runs.create(
        assistant_id=open_ai_assistant_id,
        max_prompt_tokens=300,
        max_completion_tokens=300,
        thread_id=thread.id
    )

    response = await wait_for_response(thread.id)
    await channel.send(response)

#--------------------------------------run when non-bot user sends message----------------------------------------------

async def send_message(message):
    #------------------------take the message content and ensure correct permissions------------------------------------
    message_string = message.content
    if not message_string:
        print("The intents were not set up correctly")

    #--------------------------------make sure not all commands are sent to AI------------------------------------------
    if message_string == '!recommend':
        await ask_assistant(message.channel)
        return

    #-------------------------------------set commands with set responses-----------------------------------------------
    commands = {'!hi':greeting(),
                '!bye':farewell(),
                '!roll': roll(),
                '!flip': flip(),
                '!rpsR': rps_rock(),
                '!rpsP': rps_paper(),
                '!rpsS': rps_scissors(),
                }

    #------------------------------------------check for key error------------------------------------------------------
    try:
        response_message = commands[message_string]
    except KeyError:
        await message.channel.send('Sorry, I don\'t understand that')

    #---------------------------------call function based commands dict key---------------------------------------------
    response_message = commands[message_string]
    await message.channel.send(response_message)

#--------------------------------------run when message is sent in channel----------------------------------------------

@client.event
async def on_message(message):
    #---------------------------------make sure message is not sent from bot--------------------------------------------
    if message.author == client.user:
        return
    await send_message(message)

#--------------------------------------main function (run when code starts)---------------------------------------------

def start():
    client.run(my_bot_token)

#------------------------(only run this python file when play is pressed from within it)--------------------------------

if __name__ == '__main__':
    start()