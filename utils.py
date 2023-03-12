from config import bot
import toxicity as tox
import discord
import os
import json
async def log(title, description, color, channel, reasons_list=None, toxicity_list=None):
    embed = discord.Embed(title=title, description=description, color=color)
    if reasons_list and toxicity_list:
        for reason in reasons_list:
            value = toxicity_list[tox.toxicity_names.index(reason)]
            embed.add_field(name=reason, value=f"Found value: **{value*100}%**", inline=False)    
        await channel.send(embed=embed)
    else:
        await channel.send(embed=embed)

async def log_values(title, description, color, channel, values, titles):
    embed = discord.Embed(title=title, description=description, color=color)
    for value in values:
        embed.add_field(name=titles[values.index(value)], value=value, inline=False)
    await channel.send(embed=embed)


async def process_bw(action, exp, guild_id, context):
    #check if the data folder exists
    if not os.path.exists("./data"): os.mkdir("./data")
    if not os.path.exists("./data/words"): os.mkdir("./data/words")
    #check if the file exists
    if not os.path.exists(f"./data/words/{guild_id}.json"):
        with open(f"./data/words/{guild_id}.json", "w") as f:
            json.dump({"whitelist": [], "blacklist": []}, f)
            f.close()
    with open(f"./data/words/{guild_id}.json", "r") as f:
        try:
            data = json.load(f)
            try: whitelist = data["whitelist"]
            except: whitelist = []
            try: blacklist = data["blacklist"]
            except: blacklist = []
        except:
            whitelist = []
            blacklist = []
        f.close()
    if action == "add":
        if exp in whitelist  and context == "whitelist": return "The word is already in the whitelist"
        if exp in blacklist and context == "blacklist": return "The word is already in the blacklist"
        if exp in whitelist and context == "blacklist": return "The word is in the whitelist, you can't add it to the blacklist"
        if exp in blacklist and context == "whitelist": return "The word is in the blacklist, you can't add it to the whitelist"
        if context == "whitelist" and exp not in whitelist and exp not in blacklist: whitelist.append(exp)
        if context == "blacklist" and exp not in whitelist and exp not in blacklist: blacklist.append(exp)
        with open(f"./data/words/{guild_id}.json", "w") as f:
            json.dump({"whitelist": whitelist, "blacklist": blacklist}, f)
            f.close()
        return f"The word has been successfully added to the {context}"
    if action == "delete":
        if exp not in whitelist and context == "whitelist":
            if exp in blacklist: return "The word is in the blacklist, you can't delete it from the whitelist"
            return "The word is not in the whitelist, you can't delete it"
        if exp not in whitelist and context == "blacklist":
            if exp in blacklist: return "The word is in the blacklist, you can't delete it from the whitelist"
            return "The word is not in the whitelist, you can't delete it"
        if exp in whitelist and exp not in blacklist and context == "whitelist": whitelist.remove(exp)
        if exp in blacklist and exp not in whitelist and context == "blacklist": blacklist.remove(exp)
        with open(f"./data/words/{guild_id}.json", "w") as f:
            json.dump({"whitelist": whitelist, "blacklist": blacklist}, f)
            f.close()
        return f"The word has been successfully deleted from the {context}"