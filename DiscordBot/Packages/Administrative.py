try:
    import sys, os, discord, asyncio, datetime
    from discord.ext import commands
    from discord.utils import get
    from Settings import *
except Exception as e:
    print('An Error Occured: Some modules in Connections are missing, {}'.format(e))

class Administrative(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['purge', 'clean', 'delete'])
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, payload = 100):
        """Clear a large amount of Messages."""
        if ctx.message.author is self.client.user:
            return

        # Defining Variables.
        payload += 1
        Counter = 0
        List_Messages = []
        Time = datetime.datetime.now()
        
        # Message Loop
        async for message in ctx.channel.history(limit=payload):
            if ".clear" in message.content and AdminRole or ModRole in message.author.roles:
                List_Messages.append( f"\n\n[ END OF TRANSCRIPT ]" )
            elif message.author.bot:
                if len(message.content) < 1:
                    Counter += 1
                    List_Messages.append( f"[{Time}]    BOT {message.author.mention} sent a Message with no Available Content, this could be a Embed or File." )
                else:
                    Counter += 1
                    List_Messages.append( f"[{Time}]    BOT {message.author.mention} said: {message.content}" )
            else:
                Counter += 1
                List_Messages.append( f"[{Time}]    {message.author.mention} said: {message.content}" )
        List_Messages.append(
            f"This is a Message Transcript from #{ctx.channel} at {Time}\n"
            f"The Following is not representative of Glasgow Clyde and is only meant as a log.\n\n"
            f"[ BEGINING OF TRANSCRIPT ]\n\n")
        await ctx.channel.purge(limit=payload)
        Amount_Removed = Counter
        List_Messages.reverse()

        # Server Side Logging
        channel = discord.utils.get( ctx.guild.channels, name=f"{LoggingChannel}")
        embed=discord.Embed(
            title=f"Message Purge", 
            description=f"{ctx.message.author.mention} cleared {Amount_Removed} messages.", 
            timestamp=datetime.datetime.utcnow(), color=5808622)
        embed.set_footer(text=f"ID: {ctx.message.author.id}")
        await channel.send(embed=embed)
        with open('messages.txt', 'w') as filehandle:
            for listitem in List_Messages:
                filehandle.write('%s\n' % listitem)     
        await channel.send(file=discord. File('messages.txt'))

        # User Acknowledgement
        embed=discord.Embed(
            title=f"{TickEmoji} Action Complete!", 
            description=f"{ctx.message.author.mention} you have just cleared {Amount_Removed} messages.", 
            timestamp=datetime.datetime.utcnow(), color=5828229)
        message = await ctx.channel.send(embed=embed)
        await asyncio.sleep(ClientErrorTime)
        await message.delete()

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def mute(self, ctx, member: discord.Member, *, payload = "No Reason Provided."):
        """Mute a member of the Server"""
        RoleCheck = discord.utils.get( ctx.guild.roles, name=f"{MutedRole}")
        channel = discord.utils.get(ctx.guild.channels, name=f"{LoggingChannel}")

        await ctx.message.delete()
        if member is not None:
            if RoleCheck not in member.roles:
                await member.add_roles(discord.utils.get(member.guild.roles, name=f"{MutedRole}"))
                embed=discord.Embed(
                    title=f"A user has been Muted", 
                    description=f"{ctx.message.author.mention} has muted {member.mention}", 
                    timestamp=datetime.datetime.utcnow(), color=16753664)
                embed.add_field(name="Reason", value='```{}```'.format(payload), inline=False)
                embed.set_thumbnail(url=f"{member.avatar_url}")            
                embed.set_footer(text=f"TM: {ctx.message.author.id} | ID: {member.id}")
                await channel.send(embed=embed)

                embed=discord.Embed(
                    title=f"{ErrorEmoji} An Update to your account.", 
                    description=f"We're sorry but your account has been muted in '{ctx.guild.name}'.\nIf you beliebe this is in error create a ticket by sending me a message with atleast 50 Characters!", 
                    timestamp=datetime.datetime.utcnow(), color=16078422)
                embed.add_field(name="What does this mean?", value="From this point foward, your account will not be permitted to Connect to Voice Channels or Send Messages within our Guild.", inline=False)
                embed.add_field(name="Reason:", value='```{}```'.format(payload), inline=False)
                embed.set_footer(text=f"Team Member: {ctx.message.author.id} | Your ID: {member.id}")
                await member.send(embed=embed)

                embed=discord.Embed(
                    title=f"{TickEmoji} Action Complete!", 
                    description=f"{ctx.message.author.mention} you have just muted {member.mention}.", 
                    timestamp=datetime.datetime.utcnow(), color=5828229)
                embed.add_field(name="Reason:", value='```{}```'.format(payload), inline=False)
                message = await ctx.channel.send(embed=embed)
                await asyncio.sleep(ClientErrorTime)
                await message.delete()
            else:
                embed=discord.Embed(
                    title=f"{ErrorEmoji} Failed to Invoke Command!", 
                    description="The Mentioned user is already muted.", 
                    timestamp=datetime.datetime.utcnow(), color=16078422)
                message = await ctx.channel.send(embed=embed)
                await asyncio.sleep(ClientErrorTime)
                await message.delete()
        else:
            embed=discord.Embed(
                title=f"{ErrorEmoji} Failed to Invoke Command!", 
                description="You haven't mentioned a user.", 
                timestamp=datetime.datetime.utcnow(), color=16078422)
            message = await ctx.channel.send(embed=embed)
            await asyncio.sleep(ClientErrorTime)
            await message.delete()  

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def unmute(self, ctx, member: discord.Member):
        """Unmute a member of the Server"""
        RoleCheck = discord.utils.get( ctx.guild.roles, name=f"{MutedRole}")
        channel = discord.utils.get(ctx.guild.channels, name=f"{LoggingChannel}")

        await ctx.message.delete()
        if RoleCheck in member.roles:
            await member.remove_roles(discord.utils.get(member.guild.roles, name=f"{MutedRole}"))
            embed=discord.Embed(
                title="A User has been unmuted", 
                description=f"{ctx.message.author.mention} has unmuted {member.mention}", 
                timestamp=datetime.datetime.utcnow(), color=16753664)
            embed.set_footer(text=f"TM: {ctx.message.author.id} | ID: {member.id}")
            await channel.send(embed=embed)

            embed=discord.Embed(
                title=f"{TickEmoji} An Update to your account.", 
                description=f"We have great news! Your account has been unmuted in '{ctx.guild.name}'.", 
                timestamp=datetime.datetime.utcnow(), color=5828229)
            embed.set_footer(text=f"Team Member: {ctx.message.author.id} | Your ID: {member.id}")
            await member.send(embed=embed)

            embed=discord.Embed(
                title=f"{TickEmoji} Action Complete!", 
                description=f"{ctx.message.author.mention} you have just unmuted {member.mention}", 
                timestamp=datetime.datetime.utcnow(), color=5828229)
            message = await ctx.channel.send(embed=embed)
            await asyncio.sleep(ClientErrorTime)
            await message.delete()
        else:
            embed=discord.Embed(
                title=f"{ErrorEmoji} Failed to Invoke Command!", 
                description="The user quoted in your request is not muted.", 
                timestamp=datetime.datetime.utcnow(), color=16078422)
            message = await ctx.channel.send(embed=embed)
            await asyncio.sleep(ClientErrorTime)
            await message.delete()

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def limit(self, ctx, member: discord.Member, *, payload = "No Reason Provided."):
        """Disable Fileshare, and other functions for a user."""
        RoleCheck = discord.utils.get( ctx.guild.roles, name=f"{LimitedRole}")
        channel = discord.utils.get(ctx.guild.channels, name=f"{LoggingChannel}")

        await ctx.message.delete()
        if member is not None:
            if RoleCheck not in member.roles:
                await member.add_roles(discord.utils.get(member.guild.roles, name=f"{LimitedRole}"))
                embed=discord.Embed(
                    title=f"A user has been Limited", 
                    description=f"{ctx.message.author.mention} has limited {member.mention}", 
                    timestamp=datetime.datetime.utcnow(), color=16753664)
                embed.add_field(name="Reason", value='```{}```'.format(payload), inline=False)
                embed.set_thumbnail(url=f"{member.avatar_url}")            
                embed.set_footer(text=f"TM: {ctx.message.author.id} | ID: {member.id}")
                await channel.send(embed=embed)

                embed=discord.Embed(
                    title=f"{ErrorEmoji} An Update to your account.", 
                    description=f"We're sorry but your account has been limited in '{ctx.guild.name}'.\nIf you beliebe this is in error create a ticket by sending me a message with atleast 50 Characters!", 
                    timestamp=datetime.datetime.utcnow(), color=16078422)
                embed.add_field(name="What does this mean?", value="From this point foward, your account will not be permitted to send images within our Guild.", inline=False)
                embed.add_field(name="Reason:", value='```{}```'.format(payload), inline=False)
                embed.set_footer(text=f"Team Member: {ctx.message.author.id} | Your ID: {member.id}")
                await member.send(embed=embed)

                embed=discord.Embed(
                    title=f"{TickEmoji} Action Complete!", 
                    description=f"{ctx.message.author.mention} you have just limited {member.mention}.", 
                    timestamp=datetime.datetime.utcnow(), color=5828229)
                embed.add_field(name="Reason:", value='```{}```'.format(payload), inline=False)
                message = await ctx.channel.send(embed=embed)
                await asyncio.sleep(ClientErrorTime)
                await message.delete()
            else:
                embed=discord.Embed(
                    title=f"{ErrorEmoji} Failed to Invoke Command!", 
                    description="The Mentioned user is already Limited.", 
                    timestamp=datetime.datetime.utcnow(), color=16078422)
                message = await ctx.channel.send(embed=embed)
                await asyncio.sleep(ClientErrorTime)
                await message.delete()
        else:
            embed=discord.Embed(
                title=f"{ErrorEmoji} Failed to Invoke Command!", 
                description="You haven't mentioned a user.", 
                timestamp=datetime.datetime.utcnow(), color=16078422)
            message = await ctx.channel.send(embed=embed)
            await asyncio.sleep(ClientErrorTime)
            await message.delete()   

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def unlimit(self, ctx, member: discord.Member):
        """Remove Limits for a member of the Server"""
        RoleCheck = discord.utils.get( ctx.guild.roles, name=f"{LimitedRole}")
        channel = discord.utils.get(ctx.guild.channels, name=f"{LoggingChannel}")

        await ctx.message.delete()
        if RoleCheck in member.roles:
            await member.remove_roles(discord.utils.get(member.guild.roles, name=f"{LimitedRole}"))
            embed=discord.Embed(
                title="A User's Limits have been removed.", 
                description=f"{ctx.message.author.mention} has removed the limits for {member.mention}", 
                timestamp=datetime.datetime.utcnow(), color=16753664)
            embed.set_footer(text=f"TM: {ctx.message.author.id} | ID: {member.id}")
            await channel.send(embed=embed)

            embed=discord.Embed(
                title=f"{TickEmoji} An Update to your account.", 
                description=f"We have great news! Your account has been removed from the Limited List in '{ctx.guild.name}'.", 
                timestamp=datetime.datetime.utcnow(), color=5828229)
            embed.set_footer(text=f"Team Member: {ctx.message.author.id} | Your ID: {member.id}")
            await member.send(embed=embed)

            embed=discord.Embed(
                title=f"{TickEmoji} Action Complete!", 
                description=f"{ctx.message.author.mention} you have just removed the limits for {member.mention}", 
                timestamp=datetime.datetime.utcnow(), color=5828229)
            message = await ctx.channel.send(embed=embed)
            await asyncio.sleep(ClientErrorTime)
            await message.delete()
        else:
            embed=discord.Embed(
                title=f"{ErrorEmoji} Failed to Invoke Command!", 
                description="The user quoted in your request is not Limited.", 
                timestamp=datetime.datetime.utcnow(), color=16078422)
            message = await ctx.channel.send(embed=embed)
            await asyncio.sleep(ClientErrorTime)
            await message.delete()

def setup(client):
    client.add_cog(Administrative(client))