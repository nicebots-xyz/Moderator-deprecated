import discord
from discord import default_permissions
import toxicity as tox
from config import discord_token, conn, c, toxicity_definitions, toxicity_names
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(intents=intents)

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
        if toxicity is None: toxicity = 0.40
        if severe_toxicity is None: severe_toxicity = 0.40
        if identity_attack is None: identity_attack = 0.40
        if insult is None: insult = 0.40
        if profanity is None: profanity = 0.40
        if threat is None: threat = 0.40
        if sexually_explicit is None: sexually_explicit = 0.40
        if flirtation is None: flirtation = 0.40
        if obscene is None: obscene = 0.40
        if spam is None: spam = 0.40
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
    await ctx.respond(embed=embed, ephemeral=True)

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
    try: c.execute("UPDATE data SET logs_channel_id = ?, is_enabled = ?, moderator_role_id = ? WHERE guild_id = ?", (str(log_channel.id), enable, str(mod_role.id), str(ctx.guild.id)))
    except: c.execute("INSERT INTO data VALUES (?, ?, ?, ?)", (str(ctx.guild.id), str(log_channel.id), enable, str(mod_role.id)))
    conn.commit()
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

@bot.event
async def on_message( message: discord.Message):
    if message.author == bot.user: return #if the message is sent by the bot, we don't want to moderate it, we don't want to moderate the bot,
    try: c.execute("SELECT * FROM moderation WHERE guild_id = ?", (str(message.guild.id),))
    except: return
    data = c.fetchone()
    try: c.execute("SELECT * FROM data WHERE guild_id = ?", (str(message.guild.id),))
    except: return
    data2 = c.fetchone()
    if data is None: return
    channel = message.guild.get_channel(int(data2[1]))
    is_enabled = data2[2]
    moderator_role_id = data2[3]
    #we also do that with the manage_messages permission, so the moderators can't be moderated
    if message.author.guild_permissions.manage_messages: return #if the user is a moderator, we don't want to moderate him because he is allowed to say whatever he wants because he is just like a dictator
    if message.author.guild_permissions.administrator: return #if the user is an administrator, we don't want to moderate him because he is allowed to say whatever he wants because he is a DICTATOR
    if not is_enabled: return
    content = message.content
    message_toxicity = tox.get_toxicity(content)
    reasons_to_delete = []
    reasons_to_suspicous = []
    for value in message_toxicity: 
        if value >= float(data[message_toxicity.index(value)+1]):
             print(value)
             reasons_to_delete.append(tox.toxicity_names[message_toxicity.index(value)])
    for i in message_toxicity:
        if float(data[message_toxicity.index(i)+1]-0.1) <= i < float(data[message_toxicity.index(i)+4]): reasons_to_suspicous.append(tox.toxicity_names[message_toxicity.index(i)])
    if reasons_to_delete != []:
        embed = discord.Embed(title="Message deleted", description=f"Your message was deleted because it was too toxic. The following reasons were found: **{'**, **'.join(reasons_to_delete)}**", color=discord.Color.red())
        await message.reply(f"{message.author.mention}", embed=embed, delete_after=15)
        await message.delete()
        embed = discord.Embed(title="Message deleted", description=f"**{message.author}**'s message ***{content}*** was deleted because it was too toxic. The following reasons were found:", color=discord.Color.red())
        for i in reasons_to_delete:
            toxicity_value = message_toxicity[tox.toxicity_names.index(i)]
            embed.add_field(name=i, value=f"Found toxicity value: **{toxicity_value*100}%**", inline=False)
        await channel.send(embed=embed)
    elif len(reasons_to_suspicous) > 0:
        await message.reply(f"<@&{moderator_role_id}> This message might be toxic. The following reasons were found: **{'**, **'.join(reasons_to_suspicous)}**", delete_after=15, mention_author=False)
        embed = discord.Embed(title="Message suspicious", description=f"**{message.author}**'s message [***{content}***]({message.jump_url}) might be toxic. The following reasons were found:", color=discord.Color.orange())
        for i in reasons_to_suspicous:
            toxicity_value = message_toxicity[tox.toxicity_names.index(i)]
            embed.add_field(name=i, value=f"Found toxicity value: **{toxicity_value*100}%**", inline=False)
        await channel.send(embed=embed)
        #we add a reaction to the message so the moderators can easily find it orange circle emoji
        await message.add_reaction("🟠")
    else:
        return

bot.run(discord_token)