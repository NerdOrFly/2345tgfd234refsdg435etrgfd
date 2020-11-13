try:
    import sys, os, discord, asyncio, datetime
    from discord.ext import commands
    from discord.utils import get
    from Settings import *
except Exception as e:
    print('An Error Occured: Some modules in Connections are missing, {}'.format(e))

class Administrative(commands.Cog): #Administrative on Purpose.

    def __init__(self, client):
        self.client = client
    
def setup(client):
    client.add_cog(Administrative(client))