from config import c
import re
import json
import discord
import toxicity as tox
import utils
async def validate(message):
    try: 
        c.execute("SELECT * FROM moderation WHERE guild_id = ?", (str(message.guild.id),))
        data = c.fetchone()
    except: return
    try: 
        c.execute("SELECT * FROM data WHERE guild_id = ?", (str(message.guild.id),))
        data2 = c.fetchone()
    except: return
    if data is None: return
    channel = message.guild.get_channel(int(data2[1]))
    is_enabled = data2[2]
    moderator_role_id = data2[3]
    content = message.content
    if not content.startswith("MOD TEST"):
        try:
            if message.author.guild_permissions.manage_messages: return #if the user is a moderator, we don't want to moderate him because he is allowed to say whatever he wants because he is just like a dictator
            if message.author.guild_permissions.administrator: return #if the user is an administrator, we don't want to moderate him because he is allowed to say whatever he wants because he is a DICTATOR
        except: pass
    else:
        content = content.replace("MOD TEST ", "")
        content = content.replace("MOD TEST", "")
    if not is_enabled: return
    #now we get the json file with the whit
    with open(f"./data/words/{message.guild.id}.json", "r") as f:
        try:
            data3 = json.load(f)
            try: whitelist = data3["whitelist"]
            except: whitelist = []
            try: blacklist = data3["blacklist"]
            except: blacklist = []
        except:
            whitelist = []
            blacklist = []
    for word in whitelist:
        if content.lower().find(word.lower()) != -1: 
            return
    for word in blacklist:
        if content.lower().find(word.lower()) != -1:
            embed = discord.Embed(title="Message deleted", description=f"Your message was deleted because it was too toxic. The following reasons were found: **Blacklisted word**", color=discord.Color.red())
            await message.reply(f"{message.author.mention}", embed=embed, delete_after=15)
            await message.delete()
            await utils.log_values(title="Message deleted", description=f"**{message.author.mention}**'s message ***[{content}]({message.jump_url})*** in <#{message.channel.id}> was deleted because it was too toxic. The following reasons were found:", color=discord.Color.red(), titles=["Blacklisted word"], values=[f"The word **||{word}||** is blacklisted"], channel=channel)
            return
    message_toxicity = tox.get_toxicity(content)
    reasons_to_suspicous = []
    reasons_to_delete = []
    for value in message_toxicity:
        if value >= float(data[message_toxicity.index(value)+1]):
            reasons_to_delete.append(tox.toxicity_names[message_toxicity.index(value)])
    for i in message_toxicity:
        if float(data[message_toxicity.index(i)+1]-0.1) <= i < float(data[message_toxicity.index(i)+1]): reasons_to_suspicous.append(tox.toxicity_names[message_toxicity.index(i)])
    if reasons_to_delete != []:
        await message.delete()
        embed = discord.Embed(title="Message deleted", description=f"Your message was deleted because it was too toxic. The following reasons were found: **{'**, **'.join(reasons_to_delete)}**", color=discord.Color.red())
        await message.channel.send(f"{message.author.mention}", embed=embed, delete_after=15)
        return await utils.log(title="Message deleted", description=f"**{message.author.mention}**'s message ***[{content}]({message.jump_url})*** in <#{message.channel.id}> was deleted because it was too toxic. The following reasons were found:", color=discord.Color.red(), channel=channel, reasons_list=reasons_to_delete, toxicity_list=message_toxicity)
    elif len(reasons_to_suspicous) > 0:
        await message.reply(f"<@&{moderator_role_id}> This message might be toxic. The following reasons were found: **{'**, **'.join(reasons_to_suspicous)}**", delete_after=15, mention_author=False)
        await utils.log(title="Message suspicious", description=f"**{message.author.mention}**'s message ***[{content}]({message.jump_url})*** in <#{message.channel.id}> might be toxic. The following reasons were found:", color=discord.Color.orange(), channel=channel, reasons_list=reasons_to_suspicous, toxicity_list=message_toxicity)
        await message.add_reaction("🟠")
    else:
        return