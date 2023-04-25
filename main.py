import discord
from discord import default_permissions, webhook
import toxicity as tox
import utils
import re
from config import discord_token, conn, c, toxicity_definitions, toxicity_names, bot

from discord.ext.pages import Paginator, Page
import json
import os
import check

@bot.command(name="setthreshold", description="Set the threshold for a toxicity")
@discord.option(name="toxicity", description="The toxicity threshold", required=False)
@discord.option(name="severe_toxicity", description="The severe toxicity threshold", required=False)
@discord.option(name="identity_attack", description="The identity attack threshold", required=False)
@discord.option(name="insult", description="The insult threshold", required=False)
@discord.option(name="profanity", description="The profanity threshold", required=False)
@discord.option(name="threat", description="The threat threshold", required=False)
@discord.option(name="sexually_explicit", description="The sexually explicit threshold", required=False)
@discord.option(name="flirtation", description="The flirtation threshold", required=False)
@discord.option(name="obscene", description="The obscene threshold", required=False)
@discord.option(name="spam", description="The spam threshold", required=False)
@default_permissions(administrator=True)
async def setthreshold(ctx: discord.ApplicationContext, toxicity: float = None, severe_toxicity: float = None, identity_attack: float = None, insult: float = None, profanity: float = None, threat: float = None, sexually_explicit: float = None, flirtation: float = None, obscene: float = None, spam: float = None):
    try: 
        data = c.execute("SELECT * FROM moderation WHERE guild_id = ?", (str(ctx.guild.id),))
        data = c.fetchone()
    except: data = None
    if data is None:
        #first we check if any of the values is none. If it's none, we set it to 0.40
        if toxicity is None: toxicity = 0.70
        if severe_toxicity is None: severe_toxicity = 0.50
        if identity_attack is None: identity_attack = 0.60
        if insult is None: insult = 0.80
        if profanity is None: profanity = 0.70
        if threat is None: threat = 0.80
        if sexually_explicit is None: sexually_explicit = 0.80
        if flirtation is None: flirtation = 0.90
        if obscene is None: obscene = 0.80
        if spam is None: spam = 0.80
        c.execute("INSERT INTO moderation VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (str(ctx.guild.id), toxicity, severe_toxicity, identity_attack, insult, profanity, threat, sexually_explicit, flirtation, obscene, spam))
        conn.commit()
        embed = discord.Embed(title="Settings successfully set", description="The settings have been successfully set. You can get a list of definitions for the toxicity types with the `/help` command", color=discord.Color.og_blurple()) #og_blurple is the discord blurple color, why? because it's cool and it's the color of discord a lot of people like it
        data = c.execute("SELECT * FROM moderation WHERE guild_id = ?", (str(ctx.guild.id),))
        data = c.fetchone()
        for field in toxicity_names:
            embed.add_field(name=field, value=data[toxicity_names.index(field) + 1])
        await ctx.respond(embed=embed, ephemeral=True)
        return
    else:
        if toxicity is None and data[1] is not None: toxicity = data[1]
        elif toxicity is None and data[1] is None: toxicity = 0.40
        if severe_toxicity is None and data[2] is not None: severe_toxicity = data[2]
        elif severe_toxicity is None and data[2] is None: severe_toxicity = 0.40
        if identity_attack is None and data[3] is not None: identity_attack = data[3]
        elif identity_attack is None and data[3] is None: identity_attack = 0.40
        if insult is None and data[4] is not None: insult = data[4]
        elif insult is None and data[4] is None: insult = 0.40
        if profanity is None and data[5] is not None: profanity = data[5]
        elif profanity is None and data[5] is None: profanity = 0.40
        if threat is None and data[6] is not None: threat = data[6]
        elif threat is None and data[6] is None: threat = 0.40
        if sexually_explicit is None and data[7] is not None: sexually_explicit = data[7]
        elif sexually_explicit is None and data[7] is None: sexually_explicit = 0.40
        if flirtation is None and data[8] is not None: flirtation = data[8]
        elif flirtation is None and data[8] is None: flirtation = 0.40
        if obscene is None and data[9] is not None: obscene = data[9]
        elif obscene is None and data[9] is None: obscene = 0.40
        if spam is None and data[10] is not None: spam = data[10]
        elif spam is None and data[10] is None: spam = 0.40
        c.execute("UPDATE moderation SET toxicity = ?, severe_toxicity = ?, identity_attack = ?, insult = ?, profanity = ?, threat = ?, sexually_explicit = ?, flirtation = ?, obscene = ?, spam = ? WHERE guild_id = ?", (toxicity, severe_toxicity, identity_attack, insult, profanity, threat, sexually_explicit, flirtation, obscene, spam, str(ctx.guild.id)))
        conn.commit()
        embed = discord.Embed(title="Settings successfully updated", description="The settings have been successfully updated. You can get a list of definitions for the toxicity types with the `/help` command", color=discord.Color.og_blurple()) #og_blurple is the discord blurple color, why? because it's cool and it's the color of discord a lot of people like it
        data = c.execute("SELECT * FROM moderation WHERE guild_id = ?", (str(ctx.guild.id),))
        data = c.fetchone()
        for field in toxicity_names:
            embed.add_field(name=field, value=data[toxicity_names.index(field) + 1])
        await ctx.respond(embed=embed, ephemeral=True)
        return

@bot.command(name="help", description="Get help with the moderation settings")
@default_permissions(administrator=True)
async def help(ctx: discord.ApplicationContext):
    embed = discord.Embed(title="Help", description="Here is a list of all the toxicity types and their definitions. You can set the toxicity thresholds with the `/moderation` command", color=discord.Color.og_blurple())
    for definition in toxicity_definitions:
        embed.add_field(name=tox.toxicity_names[toxicity_definitions.index(definition)], value=definition, inline=False)
    commands_embed = discord.Embed(title="Commands", description="Here is a list of all the commands", color=discord.Color.og_blurple())
    for command in bot.commands:
        commands_embed.add_field(name=command.name, value=command.description, inline=False)
    embeds = [embed, commands_embed]
    await ctx.respond(embeds=embeds, ephemeral=True)

@bot.command(name="get_toxicity", description="Get the toxicity of a message")
@discord.option(name="message", description="The message you want to check", required=True)
@default_permissions(administrator=True)
async def get_toxicity(ctx: discord.ApplicationContext, message: str):
    response = tox.get_toxicity(message)
    would_have_been_deleted = []
    would_have_been_suspicous = []
    c.execute("SELECT * FROM moderation WHERE guild_id = ?", (str(ctx.guild.id),))
    data = c.fetchone()
    for i in response:
        if i >= float(data[response.index(i)+1]):
            would_have_been_deleted.append(toxicity_names[response.index(i)])
        elif i >= float(data[response.index(i)+1])-0.1:
            would_have_been_suspicous.append(toxicity_names[response.index(i)])
    if would_have_been_deleted !=[]: embed = discord.Embed(title="Toxicity", description=f"Here are the different toxicity scores of the message\n***{message}***", color=discord.Color.red())
    elif would_have_been_suspicous !=[] and would_have_been_deleted ==[]: embed = discord.Embed(title="Toxicity", description=f"Here are the different toxicity scores of the message\n***{message}***", color=discord.Color.orange())
    else: embed = discord.Embed(title="Toxicity", description=f"Here are the different toxicity scores of the message\n***{message}***", color=discord.Color.green())
    for i in response: embed.add_field(name=tox.toxicity_names[response.index(i)], value=f"{str( float(i)*100)}%", inline=False)
    if would_have_been_deleted != []: embed.add_field(name="Would have been deleted", value=f"Yes, the message would have been deleted because of the following toxicity scores: **{'**, **'.join(would_have_been_deleted)}**", inline=False)
    if would_have_been_suspicous != [] and would_have_been_deleted == []: embed.add_field(name="Would have been marked as suspicious", value=f"Yes, the message would have been marked as suspicious because of the following toxicity scores: {', '.join(would_have_been_suspicous)}", inline=False)
    await ctx.respond(embed=embed, ephemeral=True)

@bot.command(name="setup", description="Setup the moderation settings")
@default_permissions(administrator=True)
@discord.option(name="log_channel", description="The channel where the moderation logs will be sent", required=True)
@discord.option(name="enable", description="Enable the moderation", required=True)
@discord.option(name="mod_role", description="The role of the moderators", required=True)
async def setup(ctx: discord.ApplicationContext, log_channel: discord.TextChannel, enable: bool, mod_role: discord.Role):
    old_log_channel = None
    try:
        data = c.execute("SELECT * FROM data WHERE guild_id = ?", (str(ctx.guild.id),))
        data = c.fetchone()
        old_log_channel = bot.get_channel(int(data[1]))
    except: data = None
    if data is not None:
        c.execute("UPDATE data SET logs_channel_id = ?, is_enabled = ?, moderator_role_id = ? WHERE guild_id = ?", (str(log_channel.id), enable, str(mod_role.id), str(ctx.guild.id)))
    else:
        c.execute("INSERT INTO data VALUES (?, ?, ?, ?)", (str(ctx.guild.id), str(log_channel.id), enable, str(mod_role.id)))
    announcements_channel = bot.get_channel(1072194862012706887)

    if old_log_channel is None or old_log_channel != log_channel:
        await announcements_channel.follow(destination=log_channel, reason="Moderator bot logs and updates channel")
        if old_log_channel is not None and old_log_channel != log_channel:
            pass 
        #HERE I WANT TO UNFOLLOW THE OLD LOG CHANNEL
    conn.commit()
    data = c.execute("SELECT * FROM moderation WHERE guild_id = ?", (str(ctx.guild.id),))
    data = c.fetchone()
    await ctx.respond("The moderation has been successfully setup", ephemeral=True)

@bot.command(name="get_settings", description="Get the moderation settings")
@default_permissions(administrator=True)
async def get_settings(ctx: discord.ApplicationContext):
    c.execute("SELECT * FROM moderation WHERE guild_id = ?", (str(ctx.guild.id),))
    data = c.fetchone()
    c.execute("SELECT * FROM data WHERE guild_id = ?", (str(ctx.guild.id),))
    data2 = c.fetchone()
    embed = discord.Embed(title="Settings", description="Here are the moderation settings", color=discord.Color.og_blurple())
    embed.add_field(name="Log channel", value=f"<#{data2[1]}>", inline=False)
    embed.add_field(name="Enabled", value=data2[2], inline=False)
    embed.add_field(name="Moderator role", value=f"<@&{data2[3]}>", inline=False)
    for field in toxicity_names:
        embed.add_field(name=field, value=data[toxicity_names.index(field)+1], inline=False)
    await ctx.respond(embed=embed, ephemeral=True)

###############################################EXEPTIONS###############################################
addordel = ["add", "delete"]
async def complete_add_del(ctx: discord.AutocompleteContext):
    return [option for option in addordel if option.startswith(ctx.value.lower())]

word = bot.create_group("word", "Commands for handling the blacklist and whitelist.")

@word.command(name="whitelist", description="Add or delete a word from the whitelist")
@discord.option(name="add_or_delete", description="Add or delete a word from the whitelist", autocomplete=complete_add_del)
@discord.option(name="word", description="The word you want to add or delete from the whitelist")
@default_permissions(administrator=True)
async def whitelst(ctx: discord.ApplicationContext, add_or_delete: str, exp: str):
    await ctx.respond(await utils.process_bw(add_or_delete, exp, ctx.guild_id, "whitelist"), ephemeral=True)

@word.command(name="blacklist", description="Add or delete a word from the blacklist")
@discord.option(name="add_or_delete", description="Add or delete a word from the blacklist", autocomplete=complete_add_del)
@discord.option(name="word", description="The word you want to add or delete from the blacklist")
@default_permissions(administrator=True)
async def blacklst(ctx: discord.ApplicationContext, add_or_delete: str, exp: str):
    await ctx.respond(await utils.process_bw(add_or_delete, exp, ctx.guild_id, "blacklist"), ephemeral=True)

w_b = ["whitelist", "blacklist"]
async def complete_w_b(ctx: discord.AutocompleteContext):
    return [option for option in w_b if option.startswith(ctx.value.lower())]
@word.command(name="list", description="List the words in the whitelist and blacklist")
@discord.option(name="whitelist_or_blacklist", description="List the words in the whitelist or blacklist", autocomplete=complete_w_b)
@default_permissions(administrator=True)
async def list_words(ctx: discord.ApplicationContext, whitelist_or_blacklist: str):
    interaction = await ctx.respond("Loading...", ephemeral=True)
    #check if the data folder exists
    if not os.path.exists("./data"): return await ctx.respond("The data folder doesn't exist, please add a word to the whitelist or blacklist first", ephemeral=True)
    if not os.path.exists("./data/words"): return await ctx.respond("The words folder doesn't exist, please add a word to the whitelist or blacklist first", ephemeral=True)
    #check if the file exists
    if not os.path.exists(f"./data/words/{ctx.guild_id}.json"): return await ctx.respond("The file doesn't exist, please add a word to the whitelist or blacklist first", ephemeral=True)
    with open(f"./data/words/{ctx.guild_id}.json", "r") as f:
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
    whitelist = sorted(whitelist)
    blacklist = sorted(blacklist)
    my_pages = []
    if len(whitelist) == 0 and len(blacklist) == 0: return await ctx.respond("The whitelist and blacklist are empty, please add a word to the whitelist or blacklist first", ephemeral=True)
    if len(whitelist) !=0 and whitelist_or_blacklist == "whitelist":
        number = 1
        while len(whitelist) != 0:
            #if it's greater or equal to 25, we set length to 25, else we set it to the length of the whitelist
            if len(whitelist) >= 24: length = 24
            else: length = len(whitelist)
            #we create the embed called embed{number of the page}
            exec(f"embed{number} = discord.Embed(title=f\"Whitelist - Page {number}\", description=\"\", color=0x00ff00)")
            #we add the words to the embed
            for i in range(length):
                field_name = whitelist[i-1]
                value = ""
                if len(field_name) > 256: 
                    field_name = field_name[:252] + "..."
                    value = whitelist[i-1]
                exec(f"embed{number}.add_field(name=\"{field_name}\", value=\"{value}\", inline=False)")
            #now we remove the words from the whitelist
            for i in range(length):
                whitelist.remove(whitelist[0])
            #we add the embed to the list of pages
            exec(f"my_pages.append(Page(embeds=[embed{number}]))")
            number += 1
        paginator = Paginator(pages=my_pages)
        await paginator.respond(interaction=interaction, ephemeral=True)
    elif len(whitelist) == 0 and whitelist_or_blacklist == "whitelist":
        return await ctx.respond("The whitelist is empty, please add a word to the whitelist first", ephemeral=True)
    if len(blacklist) !=0 and whitelist_or_blacklist == "blacklist":
        number = 1
        while len(blacklist) != 0:
            #if it's greater or equal to 25, we set length to 25, else we set it to the length of the blacklist
            if len(blacklist) >= 24: length = 24
            else: length = len(blacklist)
            #we create the embed called embed{number of the page}
            exec(f"embed{number} = discord.Embed(title=f\"Blacklist - Page {number}\", description=\"\", color=0x00ff00)")
            #we add the words to the embed
            for i in range(length):
                field_name = blacklist[i-1]
                value = ""
                if len(field_name) > 256:
                    field_name = field_name[:252] + "..."
                    value = blacklist[i-1]
                exec(f"embed{number}.add_field(name=\"{field_name}\", value=\"{value}\", inline=False)")
            #now we remove the words from the blacklist
            for i in range(length):
                blacklist.remove(blacklist[0])
            #we add the embed to the list of pages
            exec(f"my_pages.append(Page(embeds=[embed{number}]))")
            number += 1
        paginator = Paginator(pages=my_pages)
        await paginator.respond(interaction=interaction, ephemeral=True)
    elif len(blacklist) == 0 and whitelist_or_blacklist == "blacklist":
        return await ctx.respond("The blacklist is empty, please add a word to the blacklist first", ephemeral=True)


####################### EVENTS #######################
@bot.event
async def on_message( message: discord.Message):
    if message.author == bot.user: return
    await check.validate(message)

@bot.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    if after.author == bot.user: return
    await check.validate(after)

@bot.event
#when the bot is added to a new server, we want to send a message to the user who added the bot to the server
async def on_guild_join(guild: discord.Guild):
    #we get the audit log entry of the bot being added to the server
    audit_log_entry = await guild.audit_logs(limit=1, action=discord.AuditLogAction.bot_add).flatten()
    #we get the user who added the bot to the server
    user = audit_log_entry[0].user
    #we send a message to the user who added the bot to the server
    await user.send(f"Thank you for adding me to your server! You can use the `/setup` command to setup the , and the `/setthreshold` command to set the toxicity threshold. You'll need to run that command at least once to setup the bot. You can use the `/help` command to get a list of all commands and their usage. If you need help, you can join our support server: https://discord.gg/pB6hXtUeDv")

@bot.event
async def on_ready():
    print("Bot is ready!")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="out for toxic people!"))
@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, error: Exception):
    if str(error) == "Application Command raised an exception: Forbidden: 403 Forbidden (error code: 50013): Missing Permissions":
        await ctx.respond("I don't have the permissions to do that", ephemeral=True)
    else:   
        await ctx.respond("An unknown error occured; please try again later. If the error persists, you can contact us in our support server: https://discord.gg/pB6hXtUeDv . Please send the following LOGS to the support server: ```py\n"+str(error)+"```", ephemeral=True)
        raise error #raise the error so that it can be seen in the console


###############################################EXECUTION###############################################

bot.run(discord_token)