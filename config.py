import sqlite3
import os
import logging
from dotenv import load_dotenv
import discord
# Set up logging
logging.basicConfig(level=logging.INFO)
toxicity_names = [
    "toxicity", 
    "severe_toxicity", 
    "identity_attack", 
    "insult", 
    "profanity", 
    "threat", 
    "sexually_explicit", 
    "flirtation", 
    "obscene", 
    "spam"
]
toxicity_definitions = [
    "A rude, disrespectful, or unreasonable message that is likely to make people leave a discussion.",
    "A very hateful, aggressive, disrespectful message or otherwise very likely to make a user leave a discussion or give up on sharing their perspective. This attribute is much less sensitive to more mild forms of toxicity, such as messages that include positive uses of curse words.",
    "Negative or hateful messages targeting someone because of their identity.",
    "Insulting, inflammatory, or negative messages towards a person or a group of people.",
    "Swear words, curse words, or other obscene or profane language.",
    "Describes an intention to inflict pain, injury, or violence against an individual or group.",
    "Contains references to sexual acts, body parts, or other lewd content. \n **English only**",
    "Pickup lines, complimenting appearance, subtle sexual innuendos, etc. \n **English only**",
    "Obscene or vulgar language such as cursing. \n **English only**",
    "Irrelevant and unsolicited commercial content. \n **English only**"
]
load_dotenv() # Load the .env file 
conn = sqlite3.connect('./data/database.db') # Connect to the database
c = conn.cursor() # Create a cursor
#now we create a database with guild_id and all the values from toxicity nams as floats
c.execute('''CREATE TABLE IF NOT EXISTS moderation (guild_id TEXT, toxicity FLOAT, severe_toxicity FLOAT, identity_attack FLOAT, insult FLOAT, profanity FLOAT, threat FLOAT, sexually_explicit FLOAT, flirtation FLOAT, obscene FLOAT, spam FLOAT)''')
#now we reate a table DATA with guild_id, logs_channel_id, is_enabled, moderator_role_id
c.execute('''CREATE TABLE IF NOT EXISTS DATA (guild_id INTEGER , logs_channel_id INTEGER, is_enabled BOOLEAN, moderator_role_id INTEGER)''')
discord_token = os.getenv('DISCORD_TOKEN') # Get the discord token from the .env file
perspective_api_key = os.getenv('PERSPECTIVE_API_KEY') # Get the perspective api key from the .env file

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(intents=intents)
