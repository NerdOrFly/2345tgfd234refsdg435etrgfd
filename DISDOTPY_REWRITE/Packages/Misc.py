try:
    import sys, os, discord, asyncio, datetime
    from discord.ext import commands
    from discord.utils import get
    from Settings import *
except Exception as e:
    print('An Error Occured: Some modules in Connections are missing, {}'.format(e))

class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        """Check if the bots Online!"""
        await ctx.send('Pong!')

    @commands.command()
    async def dmcleanup(self, ctx):
        """Clean up the bot's messages in your DMs"""
        if ctx.message.guild is None:
            async for message in ctx.channel.history(limit=100):
                if message.author.id == 670330094904147968:
                    await message.delete()
        else:
            message = await ctx.send('This is a DM only Command,')
            asyncio.sleep(ClientErrorTime)
            await message.delete()

def setup(client):
    client.add_cog(Misc(client))