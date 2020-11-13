try:
    import sys, os, discord, asyncio, datetime
    from discord.ext import commands
    from discord.utils import get
    from Settings import *
except Exception as e:
    print('An Error Occured: Some modules in Connections are missing, {}'.format(e))

class Events(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member == self:
            return

        if before.channel is None and after.channel is not None:
            role = discord.utils.get(member.guild.roles, name=F"{VoiceRole}")
            await member.add_roles(role)
            channel = discord.utils.get( member.guild.channels, name=f"{LoggingChannel}")
            print(f"{member} has connected to a Voice Channel")
            embed=discord.Embed(
                title=f"Voice Channel Connection", 
                description=f"{member} has connected to a Voice Channel", 
                timestamp=datetime.datetime.utcnow(), color=5808622)
            embed.set_footer(text=f"ID: {member.id}")
            await channel.send(embed=embed)
            
        if before.channel is not None and after.channel is None:
            role = discord.utils.get(member.guild.roles, name=F"{VoiceRole}")
            await member.remove_roles(role)
            channel = discord.utils.get( member.guild.channels, name=f"{LoggingChannel}")
            print(f"{member} has disconnected from a Voice Channel")
            embed=discord.Embed(
                title=f"Voice Channel Disconnection", 
                description=f"{member} has disconnected from a Voice Channel", 
                timestamp=datetime.datetime.utcnow(), color=5808622)
            embed.set_footer(text=f"ID: {member.id}")
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message, pass_context=True):
        channel = discord.utils.get( message.guild.channels, name=f"{LoggingChannel}")
        if message.guild is not None:
            if message.author.id != ClientID:
                if ".approve" in message.content and AdminRole or ModRole in message.author.roles:
                    return
                elif ".ban" in message.content and AdminRole or ModRole in message.author.roles:
                    return
                elif ".kick" in message.content and AdminRole or ModRole in message.author.roles:
                    return
                elif ".mute" in message.content and AdminRole or ModRole in message.author.roles:
                    return
                elif ".unmute" in message.content and AdminRole or ModRole in message.author.roles:
                    return 
                elif ".limit" in message.content and AdminRole or ModRole in message.author.roles:
                    return 
                elif ".unlimit" in message.content and AdminRole or ModRole in message.author.roles:
                    return 
                elif ".rrcolours" in message.content and AdminRole or ModRole in message.author.roles:
                    return
                elif ".rrcourses" in message.content and AdminRole or ModRole in message.author.roles:
                    return
                else:
                    print(f"{message.author} deleted a message in {message.channel}: {message.content}")
                    embed=discord.Embed(title=f"{message.author} deleted a message.", description=f"The following message was deleted in #{message.channel}: ```{message.content}```", timestamp=datetime.datetime.utcnow(), color=5808622)
                    embed.set_thumbnail(url=f"{message.author.avatar_url}")
                    embed.set_footer(text=f"ID: {message.author.id}")
                    await channel.send(embed=embed) 

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id == 670330094904147968:
            return

        if message is not None and message.guild is not None and not message.author.bot:
            print(f'{message.guild}({message.guild.id}) #{message.channel}({message.channel.id}) - {message.author}({message.author.id}) said: {message.content}')

        if message.guild is None: # Modmail
            channel = channel = self.client.get_channel(TicketChannel)
            print(f'DIR MESSAGE: {message.author}({message.author.id}) said: {message.content}')
            if len(message.content) > 49:
                if channel is not None:
                    #Server Side
                    embed=discord.Embed(title="{} has submitted a report.".format(message.author), timestamp=datetime.datetime.utcnow(), color=15635133)
                    embed.add_field(name="They have messaged me the following:", value='```{}```'.format(message.content), inline=False)
                    embed.set_footer(text=f"Complainant ID: {message.author.id}")
                    await channel.send(embed=embed)

                    #Client Side
                    embed=discord.Embed(title="Hey {}!".format(message.author), description=f"We've just successfully recieved your report. One of our Available Team Members will soon review your report and may ask for more information on it later!\n\nThanks for getting in contact!", timestamp=datetime.datetime.utcnow(), color=5828229)
                    embed.add_field(name="YOUR RECIEPT", value='```{}```'.format(message.content), inline=False)
                    embed.set_footer(text=f"Complainant ID: {message.author.id}")
                    await message.author.send( embed = embed)
                else:
                    embed=discord.Embed(title=f"{ErrorEmoji} Your message has not been submitted.", description="We're sorry but your message has not been submitted due to a Technical Error, Please report this to Senior Managment.", timestamp=datetime.datetime.utcnow(), color=16078422)
                    embed.add_field(name="You sent me:", value='```{}```'.format(message.content), inline=False)
                    embed.set_footer(text=f"Message ID: {message.id}")
                    await message.author.send( embed = embed)
            else:
                embed=discord.Embed(title=f"{ErrorEmoji} Your message has not been submitted.", description="We're sorry but your message has not been submitted because it was not atleast 50 Characters in lenth. Feel free to try again but make sure you include the minimum requirements.", timestamp=datetime.datetime.utcnow(), color=16078422)
                embed.add_field(name="You sent me:", value='```{}```'.format(message.content), inline=False)
                embed.set_footer(text=f"Message ID: {message.id}")
                await message.author.send( embed = embed)

def setup(client):
    client.add_cog(Events(client))