try:
    import sys, os, discord, asyncio, datetime
    from discord.ext import commands
    from discord.utils import get
    from Settings import *
except Exception as e:
    print('An Error Occured: Some modules in Connections are missing, {}'.format(e))

class Connections(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member is self:
            print(f"I've connected to {member.guild}")
            return
        
        ConnectAssign = discord.utils.get( member.guild.roles, name=f"{JoinRole}")
        channel = discord.utils.get( member.guild.channels, name=f"{WelcomeChannel}")

        await member.add_roles(ConnectAssign)
        embed=discord.Embed(title="User Authentication Required. Please Read.", description=f"Hey there, {member.mention}!\nWelcome to '*{member.guild.name}*', a Glasgow Clyde community.\n\nYou will be required to authenticate yourself before approval. You can do this by sending your college reference number followed with the '@myclyde.ac.uk' extension.\n\nIf you don't know what this is you will find it in your personal email under the title 'Glasgow Clyde College: Enrolment Acknowledgement' if you accepted your unconditional offer, unfortunately, if you do not currently have an unconditional offer with us you cannot be admitted.\n\nThanks, the Safety Team.", timestamp=datetime.datetime.utcnow(), color=15635133)
        embed.set_thumbnail(url=f"{member.avatar_url}")
        embed.set_footer(text="'.approve (@MentionedMember) (ReferenceNO)' Connected:")
        await channel.send(embed=embed)

        channel = discord.utils.get( member.guild.channels, name=f"{LoggingChannel}")
        print(f'{member}({member.id}) has connected.')
        embed=discord.Embed(title="User connected", description=f"{member.mention} has connected, and was assigned {JoinRole}.", timestamp=datetime.datetime.utcnow(), color=5828229)
        embed.set_thumbnail(url=f"{member.avatar_url}")
        embed.set_footer(text=f"ID: {member.id}")
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member}({member.id}) has disconnected from {member.guild.name}.')
        channel = discord.utils.get( member.guild.channels, name=f"{LoggingChannel}")
        embed=discord.Embed(title="User disconnected", description=f"{member} has disconnected from the guild.", timestamp=datetime.datetime.utcnow(), color=16078422)
        embed.set_thumbnail(url=f"{member.avatar_url}")
        embed.set_footer(text=f"ID: {member.id}")
        await channel.send(embed=embed)

    @commands.command(aliases=['accept','authenticate'])
    @commands.has_any_role(AdminRole, ModRole)
    async def approve(self, ctx, member: discord.Member, payload):
        """Approve a Inbound member into the Server!"""
        RoleCheck = discord.utils.get( ctx.guild.roles, name=f"{ApproveRole}")
        channel = discord.utils.get( ctx.guild.channels, name=f"{LoggingChannel}")

        if RoleCheck not in member.roles:
            if len(payload) > 7:
                await member.add_roles(discord.utils.get(member.guild.roles, name=f"{ApproveRole}"))
                await member.remove_roles(discord.utils.get(member.guild.roles, name=f"{JoinRole}"))
                    
                embed=discord.Embed(title="User Authenticated", description=f"The team member {ctx.message.author.mention} has approved {member.mention}, their reference number is: {payload}", timestamp=datetime.datetime.utcnow(), color=15635133)
                embed.set_thumbnail(url=f"{member.avatar_url}")
                embed.set_footer(text=f"Team Member: {ctx.message.author.id} | Member: {member.id}")
                await channel.send(embed=embed)
                    
                print(f'{ctx.message.author}({ctx.message.author.id}) approved {member}({member.id}) as {payload} in {ctx.guild.name}({ctx.guild.id}).')
                embed=discord.Embed(title=f"{TickEmoji} User Authenticated!", description=f"You have just approved {member.mention}, their reference number is: {payload}", timestamp=datetime.datetime.utcnow(), color=5828229)
                embed.set_thumbnail(url=f"{member.avatar_url}")            
                embed.set_footer(text=f"Team Member: {ctx.message.author.id} | Member: {member.id}")
                message = await ctx.channel.send(embed=embed)
                await asyncio.sleep(ClientErrorTime)
                await message.delete()
            else: # Insufficent Lenth
                embed=discord.Embed(title=f"{ErrorEmoji} Failed to Invoke Command!", description="The College ID submitted with your request was not the correct lenth.", timestamp=datetime.datetime.utcnow(), color=16078422)
                embed.add_field(name="You sent me:", value='```{}```'.format(ctx.message.content), inline=False)
                message = await ctx.channel.send(embed=embed)
                await asyncio.sleep(ClientErrorTime)
                await message.delete()
        else: # User is approved
            embed=discord.Embed(title=f"{ErrorEmoji} Failed to Invoke Command!", description="The user quoted in your request has already been approved.", timestamp=datetime.datetime.utcnow(), color=16078422)
            embed.add_field(name="You sent me:", value='```{}```'.format(ctx.message.content), inline=False)
            message = await ctx.channel.send(embed=embed)
            await asyncio.sleep(ClientErrorTime)
            await message.delete()
        
def setup(client):
    client.add_cog(Connections(client))