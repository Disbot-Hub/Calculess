import discord, asyncio, datetime, json, random, os, math
from discord.ext import commands
from discord.ext.commands import BucketType
from discord import Embed, Guild 

# Global Variables
owners = ["569397766996885525", "554882868091027456", "637629713518690334"]
cmd_list = ['help', 'invite', 'ping', 'gamble', 'deposit']

invite_link = "https://discord.com/api/oauth2/authorize?client_id=735912554873749565&permissions=8&scope=bot"

reddit_link = "https://www.reddit.com/r/DisBot_Lab/"
currency_unit = 'dimes'
default_prefixes = ["get ", "c.", "c. ", "C.", "C. "]
trigs = {"anurag" : 'Thandi !!', "gholap" : "Naav nako gheu tyacha bc", "prince" : 'Potato man!'}

class General (commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # hello event
    """@commands.Cog.listener()
    async def on_message(self, message):

        greets = ["hello", "hi", "hey", "hola"]
        msg = message.content.lower ()

        start = msg.split(" ")[0]

        if start in greets and not message.author.bot :
            if str(message.author.id) in owners:
                await message.channel.send ("Hey Boss, Nice to see you :)")
            else:
                await message.channel.send (f"Hey {message.author.mention}, ssup")"""
    @commands.Cog.listener()
    async def on_message(self, message):
        msg = message.content.lower()
        mentions = ['<@!735912554873749565>', '<@735912554873749565>']
        if message.author != self.bot.user :
        	for i in msg.split(" "):
				if i in mentions:
            		await message.channel.send(f"Hey, my prefixes are : `{'; '.join(default_prefixes)}`")
                elif i in trigs.keys():
					await message.channel.send(trigs[i])
				else:
					break
        
    @commands.command(name = "leave", aliases = ["goaway", "begone", "bhagmc"])
    @commands.has_permissions(manage_guild = True, kick_members = True) 
    async def leave(self, ctx):
        """Leaves the server (requires manage server and kick members perms)"""
        await ctx.send (f"Ok {ctx.author.mention}, leaving the server :wave:")
        await asyncio.sleep(1)
        await ctx.guild.leave()
    
    @leave.error
    async def leave_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions ):
            await ctx.send(error)

    @commands.command(name = "info", aliases = ["owner", "madeby", "about"])
    @commands.cooldown(1, 10, type = BucketType.user)
    async def info(self, ctx):
        """Shows info about the bot"""
        
        madeby = await self.bot.fetch_user(569397766996885525)
        a = discord.Embed(title = "Gathering Info...", colour = discord.Color.gold() )

        inf = discord.Embed(title = "DIsBot Lab test bot", colour = discord.Color.blue() )
        inf.add_field(name = "Bot id : ", value = f"{self.bot.user.id}", inline = 0)
        inf.add_field(name = "prefixes", value = f"`{'; '.join(default_prefixes)}`" )
        inf.add_field(name = "Made by :", value = f"{madeby}", inline = 0)
        inf.add_field(name = "Owned by : ", value = f"DisBot Lab", inline = 0)

        msg = await ctx.send(embed = a)
        await asyncio.sleep(1.5)
        await msg.edit(embed = inf)

    @info.error
    async def info_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = "You need to wait for {:.3f}s before using this command again".format(error.retry_after)
            await ctx.send(msg)
        else:
            raise error

    @commands.command(name = "showgd", hidden = 1)
    async def showgd(self, ctx):
        await ctx.send(ctx.guild)
    # commands
    # help
    @commands.command (name = "support")
    @commands.is_owner()
    async def support(self, ctx):
        global bot, bot_mention, bot_user_name
        bot = self.bot
        bot_user_name = self.bot.user.name
        bot_mention = self.bot.user.mention

        help_embed = discord.Embed (title = f"Need help with a bot? Join our support server", 
		description = f"To get a list of commands send `do commands`", 
		colour = discord.Color.green ())

        # Link to Website
        help_embed.add_field (name = f"DisBot Lab website", value = f"[here]()", inline = False)

        """# Link to join DisBot Lab Support server
        help_embed.add_field (name = f"Join DisBot Lab Support Server",
                              value = f"[Here]({support_server_invite})",
                              inline = False)"""
        # Link to Reddit Page
        help_embed.add_field (name = f"Follow us on Reddit", value = f"[here]({reddit_link})", inline = True)

        # Link to add bot
        help_embed.add_field (name = f"Add Bot ",
                              value = f"[Here]({invite_link})",
                              inline = False)
        help_embed.set_author (name = f"{bot_user_name}",
                               icon_url = "https://cdn.discordapp.com/avatars/735912554873749565"
                                          "/7b51449699ad36349f958f2dc70b3d97.jpg?size=1024")
        help_embed.set_footer (text = f"To know more about other bots we make, visit our website")
        await ctx.channel.send (embed = help_embed)

    # commands list
   
    # invite the bot
    @commands.command(name = "invite", aliases = ["inv"])
    async def invite(self, ctx):
        """Sends a link to invite bot to your server"""
        inv_embed = discord.Embed (title = f"Add {self.bot.user.name} to your server",
                             description = f"[Invite Link]({invite_link})",
                             color = discord.Color.dark_blue ())
        await ctx.channel.send (embed = inv_embed)

    # clear messages
    @commands.command (name = "clear", aliases = ['clr', 'purge'])
    @commands.has_permissions (manage_messages = True)
    async def clear(self, ctx, amount: int = 1):
            await ctx.channel.purge (limit = int (amount + 1))
            await ctx.send (f'{amount} messages deleted successfully.', delete_after = 5)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions ):
            await ctx.send(error)

    # Ping check
    @commands.command ()
    async def ping(self, ctx):
        bot = self.bot
        checking_ping_embed = discord.Embed (title = 'Checking Ping', color = discord.Color.dark_blue ())
        message = await ctx.send (embed = checking_ping_embed)

        low_p_embed = discord.Embed (title = 'Pong! 🏓',
                                     description = f'Response Time : {round (bot.latency * 1000)} ms.'
                                                   f'\nWow! I\'m speed', color = discord.Color.green ())
        low_p_embed.set_thumbnail (url = 'https://cdn.discordapp.com/attachments/736050289253154849/736097523978207272/'
                                         'PicsArt_07-24-07.52.41.png')

        low_p_embed.set_footer (text = 'DisBot Lab Team')

        high_p_embed = discord.Embed (title = 'Pong! 🏓', description = f'Response Time : ms. \n' 'Oof! High Ping.',
                                      color = discord.Color.red ())

        high_p_embed.set_thumbnail (url = 'https://cdn.discordapp.com/attachments/736050289253154849/'
                                          '736097523978207272/PicsArt_07-24-07.52.41.png')

        high_p_embed.set_footer (text = 'BOT Development Team',
                                 icon_url = 'https://cdn.discordapp.com/attachments/736050289253154849/'
                                            '736097523978207272/PicsArt_07-24-07.52.41.png')
        await asyncio.sleep (1)
        if bot.latency < 0.5:
            await message.edit (content = None, embed = low_p_embed)
        else:
            await message.edit (content = None, embed = high_p_embed)


def setup(bot):
    bot.add_cog (General (bot))
