import discord

from redbot.core import commands as cmds

from discord.ext import tasks

import asyncio

import random

import datetime, time

import json

import re

ghost_url = "https://media.discordapp.net/attachments/1120678105971957790/1129029032806187098/ghost.gif?size=2048?quality=lossless"

import random

color = 0x010101
async def react(ctx, emoji):  

    try:

        await ctx.message.add_reaction(emoji)

    except:

        pass
async def new_embed(ctx, cmd):

    with open("embed.json", "r") as fp:

        data = json.load(fp)

    if str(cmd) in data:

        try:

            dt = data[str(cmd)]

            title = dt["title"]

            desc = dt["description"]

            

            color = int(dt["color"], 16)

            em = discord.Embed(title=title, description=desc, color=color)

            return em

        except KeyError:

            await ctx.reply("Could not fetch the embed, contact `dark_devil.w` or check embed format with `;embed <cmd>`")

    else:

        await ctx.reply("Could not fetch the embed, contact `dark_devil.w` or check embed format with `;embed <cmd>`")

def embed_color():  

   colors = [0x010101, 0xff0000]

   return random.choice(colors)

def get_cmd_details(cmd):

    params = ""

    for n,p in cmd.clean_params.items():

        if not p.required: s = color.make("[optional ", fg=color.colours.fg.gray, ansi=False) + color.make(n, fg=color.colours.fg.cyan, ansi=False) + color.make("]", fg=color.colours.fg.gray, ansi=False)

        else: s = color.make(f"<{n}>", fg=color.colors.fg.red, ansi=False)         

        params = params + " " + s

    syntax = f";{color.make(cmd.qualified_name, fg=color.colours.fg.blue, ansi=False)}{params}"

    aliases = f"\n**Aliases:** `{'`**,** `'.join(cmd.aliases)}`" if cmd.aliases != [] else ""

    return (syntax, aliases, params)

def util_cmd(**kwargs):

    if "extras" in kwargs: kwargs["extras"].update({"category":"utility"})

    else: kwargs["extras"] = {"category":"utility"}

    if "ignore" in kwargs.keys(): kwargs["extras"].update({"ignore":True}); del kwargs["ignore"]

    return cmds.command(**kwargs)

def dg_cmds():

    async def predicate(ctx):

        role_a = ctx.guild.get_role(1004019866531024956)

        if role_a in ctx.author.roles:

            return True

        if ctx.author.guild_permissions.administrator:

            return True

        await ctx.send("Imagine get rekt.")

        return False

    return cmds.check(predicate)

class Grinders(cmds.Cog):

    def __init__(self, bot):

        self.bot = bot

        self.looping.start()

    def cog_unload(self):

        self.looping.cancel()

       

    @cmds.group(aliases=["g"], extras={"category":"utility"}, invoke_without_command=True, description="Grinder")

    @dg_cmds()

    @cmds.has_permissions(administrator=True)

    async def grinder(self, ctx):
        """
        Basic grinder embed
        run `;grinder` `;g` for basic grinder embed
        """
        await ctx.message.delete()
        await ctx.send(embed=await new_embed(ctx, ctx.command.name))

    @grinder.command(name="add", aliases=["a"], description="Adds the grinder's next due date and reminder")

    @dg_cmds()

    @cmds.has_permissions(administrator=True)

    async def grinder_add(self, ctx, member:discord.Member, days:int):            
        """
        Adds a grinder due date  

        run `;grinder add` `;g a` to add a due date (they adds up)
        """

        timer = days * 86400

        due_time = time.time() + timer

        

        with open("user.json", "r") as fp:

            data = json.load(fp)

            if str(member.id) not in data:      

                data[str(member.id)] = {}

                data[str(member.id)]["g_due"] = due_time

                new = str(due_time).split(".")

                await ctx.send(f"`{member.name}`'s next grinder due date will be <t:{new[0]}:R>\nManager - `{ctx.author.name}`")   
                
                channel = self.bot.get_channel(1198943434413711411)
                glog = discord.Embed(title="Grinder Add Logging", description=f"**Manager :** {ctx.author.name}\n\u200B\n**Days :** {days}\n\u200B\n**Added To :**  {member.name}", color=0x010101)
              
                await channel.send(embed=glog)
            else:

                

                due = data[str(member.id)]["g_due"] 

                new_due = due - time.time()

                newer = due_time + new_due

                

                data[str(member.id)]["g_due"] = newer

                new = str(newer).split(".")

                await ctx.send(f"`{member.name}`'s next grinder due date will be <t:{new[0]}:R>\nManager - `{ctx.author.name}`")
                channel = self.bot.get_channel(1198943434413711411)
                glog = discord.Embed(title="Grinder Add Logging", description=f"**Manager :** {ctx.author.name}\n\u200B\n**Days :** {days}\n\u200B\n**Added To :**  {member.name}", color=0x010101)
                await channel.send(embed=glog)
            

                   

            

        with open("user.json", "w") as fp:

            json.dump(data, fp, indent=4)

        

    

    @tasks.loop(minutes=5)

    async def looping(self):

        guild = self.bot.get_guild(872822492295733279)      

        mini = guild.get_role(994364547878097026)

        medium = guild.get_role(994364566614061196)

        elite = guild.get_role(1029874759221129237)

        grinder = guild.get_role(981912789973086248)

        for member in grinder.members:

            if member in elite.members:

                tier = "9mil"

            elif member in medium.members:

                tier = "6mil"

            elif member in mini.members:

                tier = "3mil"        

            else:

                tier = "Error fetching data"

                    

            em = discord.Embed(title=f" <a:DG_blueheartpop:1140017122265800755> __**Grinders Payment**__ <a:DG_blueheartpop:1140017122265800755> ", description=f"<:DG_reply_blue:1195900702208295003> Your __**Grinder Payments**__ are **Pending**\n<:DG_reply_cont:1195900722227707984> Make sure to inform staff if you have any trouble with donations.\n<:DG_reply_cont:1195900722227707984> **Amount due:** \u23e3 `{tier}`\n<:DG_reply_end:1195900753311707267> **Channel:** [Pay Here](https://discord.com/channels/872822492295733279/1085497621902266388)", color=0x010101)

            em.set_footer(text=f"{guild.name}", icon_url=ghost_url)

                    

            em.set_author(name=f"{guild.name}", icon_url=self.bot.user.avatar.url)        

            channel = guild.get_channel(1196092998673498253)      

            with open("user.json", "r") as fp:

                data = json.load(fp)                

                now = time.time()

                if str(member.id) in data and "g_due" in data[str(member.id)]:

                    g_due = data[str(member.id)]["g_due"]                      

                    if g_due is not None and now > g_due:

                        try: 

                            await member.send(embed=em)
                            
                            chnl = self.bot.get_channel(1198943434413711411)
                            glog = discord.Embed(title="Grinder Reminder Logging", description=f"**Reminder to :** {member.name}\n\u200B\n**Tier :** {tier}\n\u200B\n**DMed :** Success", color=0x010101)
                            await chnl.send(embed=glog)
                            await asyncio.sleep(5)

                        except discord.Forbidden:

                            await channel.send(f"{member.mention}'s dms are closed.\nSending reminder here.")
                            chnl = self.bot.get_channel(1198943434413711411)
                            glog = discord.Embed(title="Grinder Reminder Logging", description=f"**Reminder to :** {member.name}\n\u200B\n**Tier :** {tier}\n\u200B\n**DMed :** Failed", color=0x010101)
                            await chnl.send(embed=glog)

                        await channel.send(f"{member.mention}", embed=em)

                        del data[str(member.id)]

            with open("user.json", "w") as fp:

                json.dump(data, fp, indent=4)

    

    @grinder.command(name="dm", description="Dms the grinders for their due money")

    @dg_cmds()

    @cmds.has_permissions(administrator=True)

    async def grinder_dm(self, ctx, member:discord.Member, tier:str, *, note:str):
        """

       dms the grinder for due date

        run `;grinder dm` `;g dm` to send a grinder dm about due date

        """

        emt = "grinder_"

        em = await new_embed(ctx, emt+ctx.command.name)

        em.set_footer(text=f"{ctx.guild.name}", icon_url=ghost_url)         

        em.set_author(name=f"{ctx.guild.name}", icon_url=self.bot.user.avatar.url)

        if "{tier}" and "{note}" in em.description:

            em.description = em.description.replace("{tier}", tier)

            em.description = em.description.replace("{note}", note)

        try:

            await member.send(embed=em)

            await ctx.message.add_reaction("<:done:1197946210066112585>")
            
            channel = self.bot.get_channel(1198943434413711411)
            glog = discord.Embed(title="Grinder DM logging", description=f"**Reminder to :** {member.name}\n\u200B\n**Tier :** {tier}\n\u200B\n**Note :** {note}\n\u200B\n**Manager :** {ctx.author.name}\n\u200B\n**DMed :** Success", color=0x010101)
                
            await channel.send(embed=glog)

        except discord.Forbidden:

            await ctx.reply(f"{member} has dms closed.")
            channel = self.bot.get_channel(1198943434413711411)
            glog = discord.Embed(title="Grinder DM logging", description=f"**Reminder to :** {member.name}\n\u200B\n**Tier :** {tier}\n\u200B\n**Note :** {note}\n\u200B\n**Manager :** {ctx.author.name}\n\u200B\n**DMed :** Failed", color=0x010101)
                
            await channel.send(embed=glog)
            



    @grinder.command(name="check", aliases=["c"], description="Checks the next due date for grinders")

    @dg_cmds()

    @cmds.has_permissions(administrator=True)

    async def grinder_check(self, ctx, member:discord.Member):
        """

        Shows due date  

        run `;grinder check` `;g c` for checking a member's due date

        """

        with open("user.json", "r") as fp:

            data = json.load(fp)

        try:

            g_due = data[str(member.id)]["g_due"]

            due = str(g_due).split('.')
            await ctx.send(f"{member.name}'s next due is in <t:{due[0]}:f>")
            
        except KeyError:

            await ctx.reply("no data available")

        

    @grinder.command(name="heist", aliases=["h"])

    @dg_cmds()

    @cmds.has_permissions(administrator=True)

    async def grinder_heist(self, ctx):
        """

        Heist - only grinder embed 

        run `;grinder heist` `;g h` for heist only grinder embed

        """

        em = "grinder_"
        await ctx.message.delete()
        await ctx.send(embed=await new_embed(ctx, em+ctx.command.name))

    

    @grinder.command(name="lb", description="shows all grinders leaderboard")

    @dg_cmds()

    @cmds.has_permissions(administrator=True)

    async def grinder_lb(self, ctx):
        """
        Shows all grinder's due date
        run `;grinder lb` `;g lb` to show all grinder's (who are in database) due date 
        """


        gtest = []

        gtest2 = []

        rev = []

        due = []
        
        
        mini = ctx.guild.get_role(994364547878097026)

        medium = ctx.guild.get_role(994364566614061196)

        elite = ctx.guild.get_role(1029874759221129237)

        for member in ctx.guild.members:

            with open("user.json", "r") as fp:

                data = json.load(fp)

            try:

                g_due = data[str(member.id)]["g_due"] 

                due = str(g_due).split(".")

                if member in mini.members:

                    gtest.append(f"{member.mention} (`3mil`) - <t:{due[0]}:R>\n")
                    rev.append("3")
                    
                    
                  

                elif member in medium.members:

                    gtest.append(f"{member.mention} (`6mil`) - <t:{due[0]}:R>\n")
                    rev.append("6")

                                      
                    

                    
                       

                elif member in elite.members:

                    gtest.append(f"{member.mention} (`9mil`) - <t:{due[0]}:R>\n")
                    rev.append("9")

                    

            except KeyError:

                pass
        g = ctx.guild.get_role(981912789973086248)
        for member in g.members:

            with open("database/user.json", "r") as fp:

                data = json.load(fp)

            try:

                g_due = data[str(member.id)]["g_due"]

            except KeyError:
                if member in mini.members:

                    gtest2.append(f"{member.mention} (`3mil`) - (`No data`)\n")

                    due.append("3")

                    

                  

                elif member in medium.members:

                    gtest2.append(f"{member.mention} (`6mil`) - (`No data`)\n")

                    due.append("6")
                       
                 

                    
                       

                elif member in elite.members:

                    gtest2.append(f"{member.mention} (`9mil`) - (`No data`)\n")

                    due.append("9")

                    
                

            

        em = discord.Embed(title="All Grinders Check", description="\n".join(gtest), color=embed_color())

        em1 = discord.Embed(title="No Data", description="\n".join(gtest2), color=embed_color())
        total = 0
        for el in rev:
            if el.isdigit():
                total += int(el)
        ot = total * 7
        du = 0
        for ele in due:
            if ele.isdigit():
                if int(ele) <= 10:
                    du += int(ele)
                
        totrev = total + du
        tot = totrev * 7
        nog = len(rev) + len(due)
        em2 = discord.Embed(title="Revenue", description=f"Total No. Of Grinders : {nog}\n\u200B\nTotal Revenue (incl. dues) : {totrev} Mil/Day or {tot} Mil/Week\n\u200B\nTotal Revenue (W/O dues) : {total} Mil/Day or {ot} Mil/Week", color=embed_color())

        await ctx.send(embed=em)

        await ctx.send(embed=em1)
        
        await ctx.send(embed=em2)
         

    

async def setup(bot):

    await bot.add_cog(Grinders(bot))
