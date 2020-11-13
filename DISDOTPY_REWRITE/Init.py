try:
    import sys, os, discord, asyncio, datetime
    from discord.ext import commands
    from Settings import ClientPrefix, ClientToken, ClientVersion, ClientErrorTime
except Exception as e:
    print('An Error Occured: Some modules in __Init__ are missing, {}'.format(e))

client = commands.Bot(command_prefix = ClientPrefix)
os.system('cls')

@client.command()
@commands.is_owner()
async def load(ctx, extention):
    """Loads a Package"""
    client.load_extension(f'Packages.{extention}')
    ctx.send('Packages.{extention} is now Loaded')

@client.command()
@commands.is_owner()
async def unload(ctx, extention):
    """Unloads a Package"""
    client.unload_extension(f'Packages.{extention}')
    ctx.send('Packages.{extention} is now Unloaded')

for filename in os.listdir('./Packages'):
    if filename.endswith('.py'):
        client.load_extension(f'Packages.{filename[:-3]}')
        print('Loaded {}'.format(filename))

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds)
    print(
        f'\n{client.user} has logged in and is authorised to run on:\n'
        f'{guild.name}(ID: {guild.id}) while running Version {ClientVersion}.\n'
    )
    await client.change_presence(activity=discord.Game(f'Message me for Help!'))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        embed=discord.Embed(
            title="<:cross:747123528385560646> Your Request was missing some Arguments.", 
            description="We're sorry but your request was not successful because it was Missing Arguments.", 
            timestamp=datetime.datetime.utcnow(), color=16078422)
        embed.add_field(name="You sent me:", value='```{}```'.format(ctx.message.content), inline=False)
        embed.set_footer(text=f"Message ID: {ctx.message.id}")
        message = await ctx.send(embed=embed)
        print(f'Missing ARGS: {ctx.message.author}: `{ctx.message.content}`')
        await asyncio.sleep(ClientErrorTime)
        await message.delete()

client.run(ClientToken)