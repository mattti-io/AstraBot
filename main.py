import asyncio
from contextlib import nullcontext
from random import randint
import discord
import json
from discord.ext import commands

client = commands.Bot(command_prefix=',')


@client.event
async def on_ready():
    print('Bot is ready.')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=',help'), status=discord.Status.dnd)

# Commands


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    # check if the user has the ban_members permission
    if ctx.author.guild_permissions.ban_members:
        await member.ban(reason=reason)
        # send a message to the channel with an emoji
        await ctx.send(f'{member.mention} has been banned by {ctx.author.mention} for {reason}! :hammer:')
    else:
        await ctx.send('Nice try, but you can\'t ban people here! :smirk:')


@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.kick_members:
        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} has been kicked by {ctx.author.mention} for {reason}! :boot:')
    else:
        await ctx.send('Nice try, but you can\'t kick people here! :smirk:')


@client.command()
async def mute(ctx, member: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.kick_members:
        # check if the user already has the muted role
        if 'Muted' in [role.name for role in member.roles]:
            if not discord.utils.get(ctx.guild.roles, name='Muted'):
                muted_role = await ctx.guild.create_role(name='Muted')
                await muted_role.edit(permissions=discord.Permissions.none())
                await member.add_roles(muted_role)
            else:
                muted_role = discord.utils.get(ctx.guild.roles, name='Muted')
                await member.add_roles(muted_role)
            await ctx.send(f'{member.mention} has been muted by {ctx.author.mention} for {reason}! :mute:')
        else:
            await ctx.send(f'{member.mention} is already muted! :face_with_hand_over_mouth:')
    else:
        await ctx.send('Nice try, but you can\'t mute people here! :smirk:')

# check for any new messages, and if the author is a muted user, delete the message


@client.event
async def on_message(message):
    if message.author.guild_permissions.kick_members:
        if discord.utils.get(message.guild.roles, name='Muted'):
            muted_role = discord.utils.get(message.guild.roles, name='Muted')
            if muted_role in message.author.roles:
                await message.delete()
    await client.process_commands(message)

# create an unmute command


@client.command()
async def unmute(ctx, member: discord.Member):
    if ctx.author.guild_permissions.kick_members:
        if discord.utils.get(ctx.guild.roles, name='Muted'):
            muted_role = discord.utils.get(ctx.guild.roles, name='Muted')
            await member.remove_roles(muted_role)
            await ctx.send(f'{member.mention} has been unmuted by {ctx.author.mention}! :loud_sound:')
        else:
            await ctx.send('This user is not muted! ')
    else:
        await ctx.send('Nice try, but you can\'t unmute people here! :smirk:')

# create a coinflip command


@client.command()
async def coinflip(ctx):
    coin = ['Heads', 'Tails']
    await ctx.send(f'{ctx.author.mention} flipped {coin[randint(0,1)]}!')

# create a list where the user is the key and the value is 0
levels = {
    
}

userslevels = {
}

#create a list with digit emojis
digits = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣']

#create a dice command
@client.command()
async def dice(ctx):
    dice = randint(1,6)
    i = 0
    msg = await ctx.send(f'Rolling... ')
    while i < 3:
        random_digit = digits[randint(0,5)]
        await msg.edit(content=f'Rolling... {random_digit}')
        i += 1
        asyncio.sleep(0.5)
    await msg.edit(content=f'{ctx.author.mention} rolled a {digits[dice-1]}!')

#get the content from token.txt stored in Desktop/Projekte/Token.txt on linux
with open('/home/matti/Desktop/Projekte/token.txt', 'r') as f:
    token = f.read()

client.run(token)
