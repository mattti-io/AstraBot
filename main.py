from contextlib import nullcontext
from random import randint
import discord
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


# create a leveling event#
@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.author.id in levels:
        levels[message.author.id] += 1
    else:
        levels[message.author.id] = 1
    if levels[message.author.id] == 10:
        if message.author.id in userslevels:
            userslevels[message.author.id] += 1
            levels[message.author.id] = 0
        else:
            userslevels[message.author.id] = 1
        await message.channel.send(f'{message.author.mention} has leveled up to level {userslevels[message.author.id]}! :tada:')
    await client.process_commands(message)

#create a command to check a user's level
@client.command()
async def level(ctx, member: discord.Member = None):
    print("level command")
    if member is not None:
        if member.id in userslevels:
            await ctx.send(f'{member.mention} is level {userslevels[member.id]}!')
        else:
            await ctx.send(f'{member.mention} is level 0!')
    else:
        #check if the author is already in the levels dict
        if ctx.author.id in userslevels:
            await ctx.send(f'{ctx.author.mention} is level {userslevels[ctx.author.id]}!')
        else:
            await ctx.send(f'You have not leveled up yet!')

client.run(TOKEN)
