try:
    import sys, os, discord, asyncio, datetime
    from discord.ext import commands
    from discord.utils import get
    from Settings import *
except Exception as e:
    print('An Error Occured: Some modules in Connections are missing, {}'.format(e))

class RR(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):        
        message_id = payload.message_id
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, self.client.guilds)
        member = await guild.fetch_member(payload.user_id)

        if message_id == RRMessage:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)
        
            if role is not None:
                if member is not None:
                    await member.add_roles(role)
                    print(f'{member.name} recieved {role}.')
                else:
                    print('Member not found.')
            else:
                print('Role not found.')
            
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):  
        message_id = payload.message_id
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, self.client.guilds)
        member = await guild.fetch_member(payload.user_id)

        if message_id == RRMessage or message_id == RRCourseMessage:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)
        
            if role is not None:
                if member is not None:
                    await member.remove_roles(role)
                    print(f'{member.name} lost {role}.')
                else:
                    print('Member not found.')
            else:
                print('Role not found.')

    @commands.command()
    @commands.is_owner()                                        #<:Yellow:776566501523062795><:Red:776566501741821952><:Purple:776566501770788894><:Pink:776566501775114271><:Orange:776566498944614410><:Green:776566498851684362><:Blue:776566498583117835>
    async def rrcolours(self, ctx):
        """Colour Reaction Role Embed"""
        await ctx.message.delete()
        embed=discord.Embed(title="Current Available Colours!", description="<:Pink:776566501775114271> : **Pink**\n\n<:Red:776566501741821952> : **Red**\n\n<:Green:776566498851684362> : **Green**\n\n<:Blue:776566498583117835> : **Blue**\n\n<:Orange:776566498944614410> : **Orange**\n\n<:Yellow:776566501523062795> : **Yellow**\n\n<:Purple:776566501770788894> : **Violet**", color=15635133)
        message = await ctx.send(embed=embed)
        emoji_list = ['<:Pink:776566501775114271>','<:Red:776566501741821952>','<:Green:776566498851684362>','<:Blue:776566498583117835>','<:Orange:776566498944614410>','<:Yellow:776566501523062795>','<:Purple:776566501770788894>']
        for emoji in emoji_list:
            await message.add_reaction(emoji)

def setup(client):
    client.add_cog(RR(client))
