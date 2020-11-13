try:
    import sys, os, discord, asyncio, datetime
    from discord.ext import commands
    from discord.utils import get
    from Settings import *
except Exception as e:
    print('An Error Occured: Some modules in Connections are missing, {}'.format(e))

class Embeds(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def guidelines(self, ctx):
        """Print out the current version of the guidelines"""
        await ctx.message.delete()
        embed=discord.Embed(title="Bulletin Board", description="Welcome to the Langside College Guild! We're a community primarily of Students from Langside; here you'll be able to find tips & tricks, helpful resources and be able to get involved with our growing community!", color=15635133)
        embed.add_field(name="Show us your true colours!", value="Visit [#available-roles](https://discord.com/channels/727964808321695835/776562198746365963) to claim any of our available roles!", inline=False)
        embed.add_field(name="Having an Issue?", value="Why not get in touch with a member of our Safety Team! You can do this by messaging [@GlasgowClyde](https://discord.com/channels/@me/734556356861886545) with a message of atleast 50 Characters.", inline=False)
        embed.add_field(name="Important notes and Disclaimers:", value="• Our *Safety Team* are a group of volunteers, and their actions are not representative of [Glasgow Clyde College](https://www.glasgowclyde.ac.uk).\n• GCC's [Code of Conduct](https://www.glasgowclyde.ac.uk/assets/000/002/582/Student-Code-of-Conduct_original.pdf?1499943976#:~:text=You%20are%20expected%20to%20treat,offence%20or%20harm%20to%20others.&text=The%20Health%20%26%20Safety%20at%20Work,uses%20Glasgow%20Clyde%20College%20facilities.) and 'Remote Learning: Expectations' apply.\n• Discord's [Terms of Service](https://discord.com/new/terms) and [Guidelines](https://discord.com/new/guidelines) apply.\n• Guidelines apply within all interactions, Including Direct Messages.", inline=False)
        embed.set_footer(text="Scottish Charity No. SC021182 © 2020 Glasgow Clyde College")
        await ctx.send(embed=embed)
        embed=discord.Embed(title="Our Guidelines", timestamp=datetime.datetime.utcnow(), color=15635133)
        embed.add_field(name="Conduct", value="Any unlawful, racist, harassing, threatening, abusive, hateful, xenophobic, sexist, discriminatory, abusive, defamatory or otherwise obscene content, actions, or communications are prohibited.", inline=False)
        embed.add_field(name="Privacy", value="Being invasive of another's privacy is prohibited, this includes releasing the private information of another otherwise known as 'doxing' is prohibited.", inline=False)
        embed.add_field(name="Spamming", value="Spam, or otherwise mass committing an action with/out the intent to misuse or harras a system or person is prohibited.", inline=False)
        embed.add_field(name="Inappropriate Content", value="Any of the following content is strictly prohibited:\n> • 'Not Safe for Work' content, including in media where the image may be altered to hide inappropriate content.\n> • Flashing, strobing, or other content which could induce harm to another.\n> • Sexual, Religious, Political or other inappropriate content is prohibited.\n> • User's profiles(usernames, nicknames, avatars, linked accounts and status) are required to adhere to other guidelines and must be clear, easily quotable and visible.", inline=False)
        embed.add_field(name="Safety Team Notes", value="Our Safety Team is a group of volunteers who are quite good Human Exception handlers, as such they are authorised to handle specific situations that may not be covered by our guidelines. This is so that our rules are not to exhausting. Due to this you are requested to respect our volunteers and not backchat or back seat moderate for them.", inline=False)
        embed.set_footer(text="We're constantly updating our guidelines, however these are in effect as of")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Embeds(client))