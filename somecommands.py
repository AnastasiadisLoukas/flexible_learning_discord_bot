import discord
import datetime
from discord.ext import commands # Again, we need this imported
import random
import asyncio




class SomeCommands(commands.Cog):
    """Additional commands or commands for fun"""
    client = discord.Client()


    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.last_msg = None
        self.custom_prefix = bot.command_prefix





    @commands.command(name="echo")
    async def echo(self, ctx , * , message:str):
        try:
            if not (str(message).startswith(f"{self.custom_prefix}")):
                await ctx.message.delete()
                await ctx.channel.send(message)
            else:
                await ctx.author.send("Δεν μπορείτε να χρησιμοποιήσετε αυτή την εντολή για να εκτελέσετε άλλες εντολές")
        except Exception as error:
            await ctx.author.send(f"{error}")

    # Not going to include this in help for obvious reasons :D
    @commands.command(name="spam")
    @commands.cooldown(1, 30 , commands.BucketType.user)
    async def spam(self,ctx, member:discord.Member):
        rannge = range(1, 21)
        await ctx.channel.send('how many times to spam this user chose 1-20')
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and \
                   int(msg.content) in rannge
        msg = await self.bot.wait_for("message", check=check)
        times = int(msg.content)
        while True:
            #await ctx.channel.send(f"haha i spam  {member.mention}!")
            await member.send( "hahahhaa  i spam you :D , i spam you hahahah")
            times = times - 1
            await asyncio.sleep(2)
            if times == 0:
                break


    @commands.command(name="calculateage")
    async def calculate_age(self, ctx):
        now = datetime.datetime.now()
        current_day = int(now.strftime('%d'))
        current_month = int(now.strftime('%m'))
        current_year = int(now.strftime('%y')) + 2000
        await ctx.author.send('Type your age in this form : yyyymmdd')
        rannge = range(19500101, 20211231)

        def check(msg):
            return msg.author == ctx.author and \
                   int(msg.content) in rannge
        def disekto(current_year):
            disekto = (current_year % 4 == 0 and current_year % 100 != 0) or (current_year % 400 == 0)
            if disekto:
                month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            else:
                month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            return month


        msg = await self.bot.wait_for("message", check=check)
        age = int(msg.content)
        user_year = int(age / 10000)
        user_month = int((age % 10000) / 100)
        user_day = int(age % 100)
        month = disekto(user_year)
        this_month = disekto(current_year)
        days_left = month[user_month-1] - user_day
        months_left = 0
        days_calculated = days_left
        for i in range(user_month,12):
            months_left += 1
            days_calculated+=month[i]
        years_left  = current_year - user_year - 1
        months_forward = current_month
        days_forward = current_day
        days_calculated+=current_day
        for i in range(current_month,0,-1):
            days_calculated+=this_month[i]
        total_days = days_forward + days_left
        total_months = months_left + months_forward -1
        if total_days>=30 or total_days >=31:
            total_months+=1
            total_days-=30
        if total_months>=12:
            total_months-=12
            years_left+=1
        for i in range(user_year+1,current_year):
            month = disekto(i)
            for element in month:
                days_calculated+=element
        if total_days>=1:
            total_days-=1

        string_to_send = f"Γενέθλια : {user_day}  / {user_month} / {user_year}  "
        string_to_send+= f"\nΣήμερα : {current_day} / {current_month} / {current_year}"
        string_to_send+=f"\nΗ ηλικία σας είναι :\n{years_left}  χρονών"
        string_to_send+=f"\n{total_months} μηνών και "
        string_to_send+=f"\n{total_days}   ημερών "
        string_to_send +=f"\nΓια την ακρίβεια έχουν περάσει {days_calculated} ημέρες από τη γέννησή σας"
        await ctx.author.send(string_to_send)




    @commands.command(name="countdown")
    async def countdown(self, ctx, limit: int = None):
        message = await ctx.send(f"```"
                                 f"\n{limit}---{limit}---{limit}---{limit}"
                                 f"\n{limit}---{limit}---{limit}---{limit}"
                                 f"\n{limit}---{limit}---{limit}---{limit}"
                                 f"\n{limit}---{limit}---{limit}---{limit}"
                                 f"```")
        for i in range(limit):
            limit = limit - 1
            await message.edit(content=f"```"
                                       f"\n{limit}---{limit}---{limit}---{limit}"
                                       f"\n{limit}---{limit}---{limit}---{limit}"
                                       f"\n{limit}---{limit}---{limit}---{limit}"
                                       f"\n{limit}---{limit}---{limit}---{limit}"
                                       f"```")
            await asyncio.sleep(1)
        await message.delete()

    @commands.command(name="clock")
    async def clock(self, ctx,time=None):
        message = await ctx.send(f"{datetime.datetime.now()}")
        if time!=None:
            try:
                if (int(time) in range(0,3650)):
                    for i in range(int(time)):
                        now = datetime.datetime.now()
                        await message.edit(content=f"**DATE:**  {now.day} / { now.month} / {now.year}\n"
                                                f""
                                                f"**CLOCK:**  {now.hour} : {now.minute} : {now.second}              ")
                        await asyncio.sleep(1)
                    await message.delete()
                else:
                    await ctx.send("Αυτός ο αριθμός δεν μπορεί να γίνει δεκτός. Τα δευτερόλεπτα θα πρέπει να είναι μεταξύ 0 και 3650")
            except:
                return


    @commands.command(name="hungergames")
    async def hunger_games(self, ctx, emoji=None, seconds:int=False, number_of_winners: int=False):
        if (number_of_winners!=False and seconds!=False and emoji!=None) :
            await ctx.send(" @here ")
            colours = [0x7289da ,0x0d9dff, 0x21e7ac , 0xe721d5 , 0xeb4a4a,0xff7600 , 0xfff900 , 0x20ff00 , 0xff0c00 , 0xff29c2]
            randcolour= random.choice(colours)
            #end = datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds)
            embed= discord.Embed(title="HUNGER GAMES", description=f"There can only be **{number_of_winners}**  winners !",colour=randcolour, timestamp=datetime.datetime.now())
            embed.set_author(name=ctx.author.name,
                             icon_url=ctx.author.avatar_url)
            #embed.add_field(name="Ends At : ",value= f"{end} UTC")
            embed.set_footer(text=f"Ends {seconds} seconds from now !")
            message = await ctx.send(embed=embed)
            reasons_of_dying = [" stepped into a field of poisonous mushrooms and had a horrible death ",
                                "got stomped by a rhyno , now serves as a carpet",
                                "got deleted from the database , now is a stranger",
                                "lost in the casino and owes a lot of money, now is a wanted person",
                                "forgot it is saturday and went to work , WASTED ! ",
                                "bought the wrong medicine from the drugstore, cheers! ",
                                "lost in pvp in csgo , what a noob! ",
                                "forgot to buy food in his/her way home , will be hungry soon, sad ! ",
                                "was a sitting tomato on a railway ,the sound he/she made was 'flie' ! ",
                                "stole money from the church and got busted by the police , naughty naughty!",
                                "slipped at the stairs because of cat shit , ewwww , gross! ",
                                "ate a lot of potato chips , now he/she is a potato chip , chip chip potato chip"]

            reasons_of_winning = ["stumbled upon gold , foot hurts , but worth it",
                                  "won all super mario levels , what a pro ! ",
                                  "inspired a lot of people and then ate a cake",
                                  "got selected among 10.000.000 people to be the new sex symbol",
                                  "won because he/she is a winner since birth",
                                  "says oblivion is better than skyrim and is absolutely right",
                                  "can beat every obstacle in life and he/she knows it "]

            try:

                await message.add_reaction(f"{emoji}")
            except:
                    await ctx.send(f"failed to add reaction")
            await asyncio.sleep(seconds)
            channel=ctx.channel
            new_msg = await self.bot.get_channel(channel.id).fetch_message(message.id)
            users = await new_msg.reactions[0].users().flatten()
            users.pop(users.index(self.bot.user)) #the bot can't be the winner
            winner_list = []
            while len(winner_list)<(number_of_winners) and len(winner_list)<(len(users)) :
                winner=random.choice(users)
                if winner not in winner_list:   #we don't want to get the same winner multiple times
                    winner_list.append(winner)
            counter = 0
            for i in users:
                if i not in winner_list:
                    counter=counter+1
                    randcolour= random.choice(colours)
                    embed = discord.Embed(title=(f"Round {counter}"),
                                          description=f"{i.mention}  {random.choice(reasons_of_dying)}",colour=randcolour,timestamp=datetime.datetime.now())
                    embed.set_author(name=i.name,
                                     icon_url=i.avatar_url)
                    # embed.add_field(name="Ends At : ",value= f"{end} UTC")
                    embed.set_footer(text=f"{len(users)-counter} players remaining ")
                    await ctx.send(embed=embed)
                    await asyncio.sleep(2)
            for i in range(len(winner_list)):
                choicew=random.choice(reasons_of_winning)
                await ctx.send(f" {winner_list[i].mention} {choicew}  ")

        else:
            await ctx.send(""" ``Arguments not provided correctly.``
    **Correct argument form** : {custom_prefix}hungergames <emoji> <seconds> <number_of_winners>""")



    @spam.error
    async def spam_error(self,ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("slow it down please")

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        self.last_msg = message

    @commands.Cog.listener()
    async def on_ready(self):
        print('SomeCommands cog ready')













# Now, we need to set up this cog somehow, and we do that by making a setup function:
def setup(bot: commands.Bot):
    bot.add_cog(SomeCommands(bot))