import discord
from discord.ext import commands # Again, we need this imported
import smtplib ,ssl
import sqlite3
import datetime
import asyncio
import os
import json



class Utility(commands.Cog):
    """Utility commands"""
    client = discord.Client()


    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.last_msg = None
        self.alarms = {}

    @commands.command(name="sendmail")
    async def send_mail_to_user(self, ctx):
        # https://www.youtube.com/watch?v=JRCJ6RtE3xU

        async def sendmailsequense(receiver, subject, body):
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                connection = sqlite3.connect("studentsdata.db")
                cursor = connection.cursor()
                cursor.execute(f"SELECT BOT_EMAIL,BOT_EMAIL_PASSWORD FROM emailsetup")
                result = cursor.fetchall()
                botemail = result[0][0]
                botpassword = result[0][1]
                connection.close()

                context = ssl.create_default_context()
                smtp.ehlo()
                smtp.starttls(context=context)
                smtp.ehlo()
                # this is also part of the setup ( contains private information)
                smtp.login(botemail, botpassword)
                mail_to_be_sent = f'Subject : {subject}\n\n{body}'
                smtp.sendmail(botemail, receiver, mail_to_be_sent)

        def check(msg):
            return msg.author == ctx.author

        try:
            await ctx.author.send('Please type the email of the user you want to send your email')
            receiver = await self.bot.wait_for("message", check=check)
            await ctx.author.send('Type a subject please')
            subject = await self.bot.wait_for("message", check=check)
            await ctx.author.send('What is your message')
            body = await self.bot.wait_for("message", check=check)
            await sendmailsequense(str(receiver.content), str(subject.content), str(body.content))
            await ctx.author.send("very well , your email has been sent")
        except:
            await ctx.author.send("an error occured , maybe you didn't type something correctly")

    @commands.command(name='help',aliases =['??????????????','hint','??????????????','commands','??????????????','??????????????'])
    async def help(self,ctx,typeofhelp=None):

        if typeofhelp!=None:
            k = typeofhelp.lower()
            if k == "moderation" or k == '????????????????????':
                embed = discord.Embed(title=f"**?????????????? ?????? ????????????????????????**",
                                      description=f"?????????? ?????????????????????? ???????? ?????? ????????????????????????.", colour=self.bot.colour,
                                      timestamp=datetime.datetime.now())
                embed.add_field(name="**enable**", value=f"```?????????????????????? ?????????????? ?????????????????????? ?????? ????????.?????????? ???????????? ???? ?????????? : ?? ???????????????????? 'verify',??"
                                                         f" ?? ???????????????????? 'agent' ?? ?? ???????????????????? 'bannedwords'```", inline=False)
                embed.add_field(name="**disable**", value=f"```?????????????????????????? ?????????????? ??????????????????????```", inline=False)
                embed.add_field(name="**clear**", value=f"```?????????????????? ???????????????????????????? ???????????? ??????????????????```",
                                inline=False)
                embed.add_field(name="**clearbot**",
                                value=f"```?????????????????? ???? ???????????????????????????? ???????? ?????????????????? ???????? ???? ???????????????? ?????? ?????????????????????? ?????? ???? ????????```", inline=False)
                embed.add_field(name="**addbadword**",
                                value=f"```?????????????????? ?????? ???????????????????????? ???????? ?????? ???????? ?????????????????? ?????? ?????????????? ???? ????????????```",
                                inline=False)
                embed.add_field(name="**deletebadword**",
                                value=f"```?????????????? ?????? ???? ???????? ?????????????????? ?????? ???????????????????????? ???????? ?????? ?????????????? ???? ????????????```",
                                inline=False)
                embed.add_field(name="**restart**",
                                value=f"```?????????? ???????????????????????? ???? ????????.?????? ???? ???????????????? ?????????????????? ?????? ?????????? ????????????????```",
                                inline=False)
                embed.add_field(name="**pc**",
                                value=f"```?????????????? ???? ???????????? ?????? ???????????? : 'shutdown' ?? 'restart' ?????? ?????????????? ?????????????????????? ?? ???????????????????? ?????? ????????????????????```",
                                inline=False)
                embed.add_field(name="**setstatus**",
                                value=f"```?????????????? ???? ???????????? ?????? ?????????????? ?????? ???? ???? ?????????? ???? ?????????????????? ???????????? ?????? ????????.```",
                                inline=False)
                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"?????????????? ???????? ?????? ???????????? {ctx.author.name}")
                await ctx.send(embed=embed)
            elif k == "utility":
                embed = discord.Embed(title=f"**???????????????? ??????????????**",
                                      description=f"?????????????? ?????? ???????????? ???? ?????????????????? ?????????????? ??????????????", colour=self.bot.colour,
                                      timestamp=datetime.datetime.now())
                embed.add_field(name="**sendmail**", value=f"```???????????? ???????????????????? ?????????????????? ???????????????????????? ??????????????????```", inline=False)
                embed.add_field(name="**help**", value=f"```?????????? ???? ???????????? ???? ???????????????????? ???? ?????????? ?????? ????????."
                                                       f"???????????? ???????????? ???? ?????????????????????????? ???? ?????? ???????????? '??????????????' ?????? 'hint'```", inline=False)
                embed.add_field(name="**alarm**", value=f"```???????????????????? ?????????????????? ???????????????????? ?????? ?????? ???????????????????????? ????????????.???? ???? ?????????????????????? ?????? ?????????????????? ?????????? 'shutdown' ?????? ?? ?????????????? ?????? ?????????????? ???????? ???????????????????? ?????????????????????? ?????????????? ???? pc ?????? ???????????????????? ??????.```",inline=False)
                embed.add_field(name="**myalarm**", value=f"```?????????????? ???? ?????????????????? ???????????????????? ?????? ????????????```",inline=False)

                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"?????????????? ???????? ?????? ???????????? {ctx.author.name}")
                await ctx.send(embed=embed)
            elif k == "contacts" or k == '????????????' :
                embed = discord.Embed(title=f"**?????????????? ???????????????? ???? ?????? ???????????? ?????? ??????????????**",
                                      description=f"?????????????? ?????????? ???????????????????? ???????? ?????? ???????????????????????? ?????? ?????? ???????????????????? ??????????????????",
                                      colour=self.bot.colour,
                                      timestamp=datetime.datetime.now())
                embed.add_field(name="**user**", value=f"```???????????????? ?????????????????? ???????????? ???? ???????????? ?????? ???????????????????? ????????????```",
                                inline=False)
                embed.add_field(name="**aem**", value=f"```???????????????? ?????????????????? ???????????? ???? ???????????? ?????? ?????????????? (mention-tag) ?????? ????????????```",
                                inline=False)
                embed.add_field(name="**verify**", value=f"```???????????? ???????????????????? ???????????????????????? ?????? ???????????????? ???????????? ?????? ???????? ??????????????????```",
                                inline=False)

                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"?????????????? ???????? ?????? ???????????? {ctx.author.name}")
                await ctx.send(embed=embed)
            elif k == "somecommands":
                embed = discord.Embed(title=f"**?????????????? ??????????????**",
                                      description=f"???????????????????? ???????? ?????????? ???????? ??????????????",
                                      colour=self.bot.colour,
                                      timestamp=datetime.datetime.now())
                embed.add_field(name="**echo**",
                                value=f"```?????????????? ???? ???????????? ?????? ?????????????? ?????? ?????????? ???? ???????? ?????????????? ?????? ????????????.???????????? ???? ????????????"
                                      f"???????????? ?????? ???????????? ??????????????????????```",
                                inline=False)
                embed.add_field(name="**calculateage**",
                                value=f"```???????????? ???????????????????? ?????????????????????? ?????????????? ?????? ????????????```",
                                inline=False)
                embed.add_field(name="**countdown**",
                                value=f"```???????????????????? ?????????????? ?????? ???????????? ?????? ???????? ?????????? ???? ????????????```",
                                inline=False)
                embed.add_field(name="**clock**",
                                value=f"```???????????????????? ?????????????? ?????? ???????????? ?????? ???????? ?????????? ???? ????????????```",
                                inline=False)
                embed.add_field(name="**hungergames**",
                                value=f"```<prefix>hungergames <emoji> <seconds> <number_of_winners>```",
                                inline=False)

                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"?????????????? ???????? ?????? ???????????? {ctx.author.name}")
                await ctx.send(embed=embed)
            elif k == "agentchat" or k=="agent" or k=="??????????????????":
                embed = discord.Embed(title=f"**?????????????? ????????????????**",
                                      description=f"?????????????? ???????? ???? ?????????????? ???? ?????????????? ???????????? ?????? ????????????.",
                                      colour=self.bot.colour,
                                      timestamp=datetime.datetime.now())
                embed.add_field(name="**loadagent**",
                                value=f"```?????????????? ???? ???????????? ???? ?????????? ?????? ????????????????. "
                                      f"???????????????? ???? ???????????????? ?????? ?????????? . ?????????? : <prefix>loadagent <name_of_agent>.docx```",
                                inline=False)
                embed.add_field(name="**agentstart**",
                                value=f"```???????????? ???????????????????? ???????????????????? ???? ???? ????????????????.???????????? ?????????????????????? ???? ???????????????????????????? ?????? ???????????? ?????? ????"
                                      f"?????????????????? ?? ?????????????????? ???? ?????? ??????????. ?????????? : <prefix>agentstart <name_of_agent>.docx```",
                                inline=False)
                embed.add_field(name="**agentfinish**",
                                value=f"```?????????????????????????????? ?????? ???????? ?????????????????????????? ?????????? ???????????????????? ?????? ????????????????.?????? ?????????? ?????????????????????? ?????? ??????"
                                      f"?????????????? ???????????? ????????????.```",
                                inline=False)
                embed.add_field(name="**teamanswers**",
                                value=f"```???????????????? ?????? ?????????????????????? ?????? ???????????? ?????? ???????????????????? ???????????? ???? ?????? ???????????????????? ?????? ???????????? ???? ????????????"
                                      f"!!! ?? ???????????? agentfinish ?????? ???????????? ???? ???????? ????????????????????????????!!!. ?? ???????????? teamanswers"
                                      f" ???????? ?????????? ???? ?????????????????????????????? ???????? ???????? ???? ???????? ?????? ?????????????????????? ?????? ????????????????."
                                      f"?????????????? ???????????? ???? ???????????? ???? ?????????? ?????? ????????????????.?????????? : <prefix>teamanswers <name_of_agent>.docx```",
                                inline=False)
                embed.add_field(name="**agentanswers**",
                                value=f"```???????????????????? ???????????? ???? ???????????? ???? ?????? ???????????????????? ???????? ?????????? ???????????????????? ?????? ????????????????."
                                      f"?????????? : <prefix>agentanswers <name_of_agent>.docx```",
                                inline=False)
                embed.add_field(name="**agentparticipants**",
                                value=f"```?????????????????????????????? ?????? ???????????????????????? ?????? ?????????????? ?????? ???????????? ???? ???????? ?????????????????????????? ?????? ????????????????```",
                                inline=False)

                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"?????????????? ???????? ?????? ???????????? {ctx.author.name}")
                await ctx.send(embed=embed)
            elif k == "test" or k == '????????':
                embed = discord.Embed(title=f"**?????????????? ????????**",
                                      description=f"?????????????? ???????? ???? ?????????????? ???? ?????????????? ???????????? ?????? ????????????.",
                                      colour=self.bot.colour,
                                      timestamp=datetime.datetime.now())
                embed.add_field(name="**loadtest**",
                                value=f"```???????????????? ???? ???????? ?????? ??????????. ?????????? : <prefix>loadtest <name_of_doc>.docx"
                                      f"???? ?????????????? ???? ???????????????? .docx```",
                                inline=False)
                embed.add_field(name="**teststart**",
                                value=f"```???????????? ???????????????????? ????????????????.?? ???????????? ?????????????????????????????? ?????? ?????? ??????????????????????"
                                      f"?????????????? ???? ???????????? ???? ?????????? ?????? ???????? ???????? ?? ???????????? loadtest```",
                                inline=False)
                embed.add_field(name="**participants**",
                                value=f"```???????????? ?????????????????? ???????? ???????? ????????????????????????.?????????????? ?????????? ?????????????????????? ?????? ????????.```",
                                inline=False)
                embed.add_field(name="**showme**",
                                value=f"```?????????????? ???? ???????????? ???? ?????????? ?????? ???????? ?????? ???? discord id ?????? ????????????????????????."
                                      f"?????????????? ?????? ???????????????????? ?????? ???????????????????????? ???? ???????? ?????? ???????????????????????? ????????."
                                      f"???????????? ?????????????????? ???????? ???????? ???????? ????????????????????????.```",
                                inline=False)
                embed.add_field(name="**stats**",
                                value=f"```?????????????? ???? ???????????? ???? ?????????? ?????? ???????? ???????? ?? ???????????? loadtest."
                                      f"?????????????? ???????????????????? ???????????????????? ?????????? ?????? ?????????????????? ???????????????? ?????? ?????????????? ???? ??????"
                                      f"???????????????????????? ????????. ???????????? ???? ???????????????????????????? ?????? ???????? ?????? ?????????? ???? ?????????? ??????????????????????????????```",
                                inline=False)
                embed.add_field(name="**printanswers**",
                                value=f"```?????????????? ???? ???????????? ???? ?????????? ?????? ???????? ?????? ?????????????? ?????????????? ??????????????????????."
                                      f"???????????????????? ???????????? ???? ?????? ???????????????????? ??????????????.???? ?????????????? ?????????????? ???????? ?????? ????????????????????????????"
                                      f"???????????????? ?????????????? ?????????????????????????? ???? ???? ??????????????????.```",
                                inline=False)

                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"?????????????? ???????? ?????? ???????????? {ctx.author.name}")
                await ctx.send(embed=embed)
            elif k == "reactionroles" or k == '??????????':
                embed = discord.Embed(title=f"**?????????????? ?????????????????????????? ??????????**",
                                      description=f"?? ?????????? ???????? ?????????????????????? ???? ???????????????????????? ?????? ?????????? ?????? ??????????????",
                                      colour=self.bot.colour,
                                      timestamp=datetime.datetime.now())
                embed.add_field(name="**rr**",
                                value=f"```???????????????????? ???????????? ??????????. ?????????? : <prefix>rr```",
                                inline=False)
                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"?????????????? ???????? ?????? ???????????? {ctx.author.name}")
                await ctx.send(embed=embed)
            else:
                await ctx.send("?????? ?????????????? ?????????????? ???????????? ?????????????????????? .\n"
                               "???????????????????????????? ?????? ?????????????????????? ???????????????? ?????? ???????????? ``help``")
        else:
            embed = discord.Embed(title=f"**???????????????????? ?????????????? {(self.bot.user.name).upper()}**", description=f"???? ?????????????????? ???????????????????? ??????????????????????.\n"
                                                                                                       f"?????????????????????????? ?????? ???????????? help ???????? ???? ?????? ?????? ?????????? ?????? ???????????????? ??????????????????????.", colour=self.bot.colour,
                                  timestamp=datetime.datetime.now())
            embed.add_field(name="**Moderation**", value=f"```?????????????? ???????? ?????? ????????????????????????```", inline=True)
            embed.add_field(name="**Utility**", value=f"```???????????????? ??????????????```", inline=True)
            embed.add_field(name="**Contacts**", value=f"```?????????????? ?????? ?????????????????????? ???? ???? ???????? ??????????????????```", inline=True)
            embed.add_field(name="**SomeCommands**", value=f"```?????????????? ?????? ?????????????? ???? ?????????????????????????????? ?????? ??????????```", inline=True)
            embed.add_field(name="**AgentChat**", value=f"```?????????????? ?????????????? ?????? ?????? ???????????? ???????????????????? ???? ?????????????? ???? ????????????????```", inline=True)
            embed.add_field(name="**Test**", value=f"```?????????????? ?????????????? ?????? ?????? ???????????? ???????????????? ?????? ???????????????????????? ????????```", inline=True)
            embed.add_field(name="**ReactionRoles**",value=f"```?????????????? ?????????????? ?????? ?????? ???????????????????????? ?????????? ???? ????????????????????```", inline=True)
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.set_footer(text=f"?????????????? ???????? ?????? ???????????? {ctx.author.name}")
            await ctx.send(embed=embed)

    @commands.command(name="alarm",aliases =['??????????????????','????????????????????','ring'])
    async def alarm(self,ctx):
        if ctx.guild==None:
            await ctx.author.send("H ???????????? ???????? ?????????????????????????????? ?????????? ?????? ????????????")
            return
        import datetime
        def disekto(current_year):
            disekto = (current_year % 4 == 0 and current_year % 100 != 0) or (current_year % 400 == 0)
            if disekto:
                month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            else:
                month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            return month
        def check(msg):
            return msg.author == ctx.author
        def current_status_f(tries):
            now = datetime.datetime.now()
            time = datetime.datetime.now().time()
            current_status = {}

            current_day = int(now.strftime('%d'))
            current_status["day"] = current_day

            current_month = int(now.strftime('%m'))
            current_status["month"]=current_month

            current_hour = time.hour
            current_status["hour"]=current_hour

            current_minute = time.minute
            current_status["minutes"]=current_minute

            current_year = int(now.strftime('%y')) + 2000
            current_status["year"]=current_year
            if tries==0:
                return current_status
            else:
                return
        def calculate_user_input(alarm):
            try:
                month_day_data = int(alarm / 10000)
                month_data = int(month_day_data / 100)
                day_data = int(month_day_data % 100)
                hour = int((alarm % 10000) / 100)
                minutes = int(alarm % 100)
                user_input = {}
                user_input["month"]=month_data
                user_input["day"]=day_data
                user_input["hour"]=hour
                user_input["minutes"]=minutes
                return user_input
            except:
                return False
        async def calculate_user_year(current_status,user_input):
            if user_input["month"] < current_status["month"]:
                user_input["year"] = current_status["year"] + 1
                user_input["allmonths"] = disekto(user_input["year"])
                return True
            elif user_input["month"] == current_status["month"] and user_input["day"] < current_status["day"]:
                await ctx.author.send("?? ???????????????????? ?????? ?????????????? ?????????? ???????????????? ???? ??????????????.?? ???????????????????? ????????????????????????.")
                return False
            elif user_input["month"] == current_status["month"] and user_input["day"] == current_status["day"] and \
                    user_input["minutes"] <= current_status["minutes"]:
                await ctx.author.send("?? ?????? ?????? ?????????????? ?????????? ???????????????? ???? ??????????????.H ???????????????????? ????????????????????????.")
                return False
            else:
                user_input["year"] = current_status["year"]
                user_input["allmonths"]=disekto(user_input["year"])
                return True
        await ctx.author.send("???????????? ???? ???? ???????????? ???? ???????? ?? ???????????????????? ??????")
        alarm_text = await self.bot.wait_for("message", check=check)
        alarm_text = str(alarm_text.content)
        bad_user_input = True
        tries = -1
        while bad_user_input:
            tries += 1
            await ctx.author.send("?????????? ???????????? ?????? ?????????? **????????????????** ???????????? ????????,????????,??????,??????????.``???? 05251030 ???????????????? 25 ?????????? 10:30 ???? ????????``")
            msg = await self.bot.wait_for("message", check=check)
            try:
                alarm = int(msg.content)
            except:
                await ctx.author.send("???????????????????? ?????????????? ??????????????????.?????????????????????? ????????.")
                continue
            if len(str(msg.content))!=8:
                await ctx.author.send("?????? ?????????? ?????????? ???????????????? ??????????????????.?? ?????????????????????????? ?????????????? ?????? ???????????? ???? ???????????????? ???? ???????????? ???? ???????? 8 ??????????.?????????????????????? ????????.")
                continue
            user_input = calculate_user_input(alarm)
            if tries ==0:
                current_status = current_status_f(tries)
            else:
                current_status_f(tries)
            year_check = await calculate_user_year(current_status,user_input)
            if not year_check:
                return






            if user_input["month"]<=0 or user_input["month"]>=12:
                await ctx.author.send("???????????????????? ?????????????? ?????? ``????????``.?????????????????????? ????????.")
                continue
            elif user_input["day"]>user_input["allmonths"][user_input["month"]-1] or user_input["day"]<=0:
                await ctx.author.send("???????????????????? ?????????????? ?????? ``????????``.?????????????????????? ????????.")
                continue
            elif user_input["minutes"]<0 or user_input["minutes"]>59:
                await ctx.author.send("???????????????????? ?????????????? ?????? ``??????????``.?????????????????????? ????????.")
                continue
            elif user_input["hour"]<0 or user_input["hour"]>23:
                await ctx.author.send("???????????????????? ?????????????? ?????? ``??????``.?????????????????????? ????????.")
                continue
            else:
                bad_user_input = False






        self.alarms[ctx.author.id]={}
        self.alarms[ctx.author.id]["month"]=user_input["month"]
        self.alarms[ctx.author.id]["day"]=user_input["day"]
        self.alarms[ctx.author.id]["hour"]=user_input["hour"]
        self.alarms[ctx.author.id]["minutes"]=user_input["minutes"]
        self.alarms[ctx.author.id]["status"]=alarm_text
        self.alarms[ctx.author.id]["guild"]=ctx.author.guild_permissions.administrator
        if user_input['hour']>12 and user_input['hour']<=16:
            day_event = '???? ????????????????'
        elif user_input['hour']>16 and user_input['hour']<=20:
            day_event = '???? ????????????????'
        elif user_input['hour']>20 and user_input['hour']<=23:
            day_event = '???? ??????????'
        elif user_input['hour']>=0 and user_input['hour']<=3:
            day_event = '???????? ???? ??????????????????'
        elif user_input['hour']>3 and user_input['hour']<=6:
            day_event = '???? ????????????????'
        elif user_input['hour']>6 and user_input['hour']<=12:
            day_event = '???? ????????'
        else:
            return
        await ctx.author.send(f"???????????? ?????????????????? ?????? ?????? {user_input['day']} ?????? ???????? {user_input['month']} ???????? {user_input['hour']}:{user_input['minutes']} {day_event}")



        try:
            with open('alarms.json', 'w') as those_alarms:

                try:
                    json.dump(self.alarms, those_alarms)

                except:
                    await ctx.send("???????????????? ???????????????????? ???????????????????????? ?????? ???????????? ??????????")
                    pass
        except:
            pass
        """
        
        ?????????? ?? ?????????????? ???????? ?????????????????? ?????? ?????????? ?? ?????????????? ???? ???????????????????????? ???? ?????? ?????????????????? ?????? ???????????? ??????????.?????????? ???? ???????????????? ????
        ???????????????? ?????? ?????????????? ?? ?????????????????? ???? json ?????? ?????? ?????????????? ???????????? ?????????????? ?????? on_ready . ???????? ???????????????? ???? ???????????????????? ???????????? ???????????? ???????? ???? 
        enable alarms ,disable alarms ???? ??????????????????. ?????? ???? ?????????????? ?? ???????????????????? ???????????????? ???? ???? ???????????????????????? ???? ?????????????????????????? ?????? ???????????? ?? ??????.

        while ctx.author.id in self.alarms:
            now = datetime.datetime.now()
            current_day = int(now.strftime('%d'))
            current_month = int(now.strftime('%m'))
            time = datetime.datetime.now().time()
            current_hour = time.hour
            current_minute = time.minute
            check_date = current_day == self.alarms[ctx.author.id]["day"] and current_month == self.alarms[ctx.author.id]["month"]
            check_time = current_hour == self.alarms[ctx.author.id]["hour"] and current_minute == self.alarms[ctx.author.id]["minutes"]
            if check_time and check_date:
                string_to_send = f"???????????? ???????????????????? ?????? : **{current_day}**/**{current_month}** ?????? ?????? **{current_hour}**:**{current_minute}**\n"
                string_to_send+=f"H ???????????????????? ?????? :\n" \
                                f"```{alarm_text}```"
                await ctx.author.send(f"{ctx.author.mention} {string_to_send}")
                self.alarms.pop(ctx.author.id)




                if alarm_text == 'shutdown' and ctx.author.guild_permissions.administrator:
                    await ctx.author.send("?? ?????????????????????? ???? ?????????????? ???? 60 ????????????????????????. ???????????? 'cancel' ???? ???????????????? ??????????.")
                    try:
                        cancel_or_no = await self.bot.wait_for("message",check=check,timeout=60.0)
                        if str(cancel_or_no.content) == 'cancel':
                            await ctx.author.send("Proceedure canceled.Pc won't shut down.")
                        else:
                            await ctx.author.send("Shutting down now!...Bye!")
                            os.system("shutdown /s")
                    except asyncio.TimeoutError:
                        await ctx.author.send("Shutting down now!...Bye!")
                        os.system("shutdown /s")

            await asyncio.sleep(30)
        """

    @commands.command(name="myalarm")
    async def myalarm(self,ctx):
        try:
            await ctx.author.send(self.alarms[ctx.author.id])
        except:
            try:
                await ctx.author.send(self.alarms[str(ctx.author.id)])
            except:

                await ctx.author.send("not found")

    @commands.Cog.listener()
    async def on_ready(self):

        try:
            with open('alarms.json') as these_alarms:

                self.alarms = json.load(these_alarms)

        except:
            pass



        print('Utility cog ready')
        print('=====================')
        print('Logged in as')
        print(self.bot.user.name)
        print('=====================')
        print('Connected Servers:')
        print('-----------------')
        for guild in self.bot.guilds:
            print(f"name : {guild.name} , id : {guild.id}")





        while True:
            now = datetime.datetime.now()
            current_day = int(now.strftime('%d'))
            current_month = int(now.strftime('%m'))
            time = datetime.datetime.now().time()
            current_hour = time.hour
            current_minute = time.minute
            for person in list(self.alarms):

                check_date = current_day == self.alarms[person]["day"] and current_month == self.alarms[person]["month"]
                check_time = current_hour == self.alarms[person]["hour"] and current_minute == self.alarms[person]["minutes"]
                if check_time and check_date:
                    string_to_send = f"???????????? ???????????????????? ?????? : **{current_day}**/**{current_month}** ?????? ?????? **{current_hour}**:**{current_minute}**\n"
                    string_to_send+=f"H ???????????????????? ?????? :\n" \
                                    f"```{self.alarms[person]['status']}```"

                    this_member = await self.bot.fetch_user(int(person))
                    alarm_text = self.alarms[person]['status']
                    is_admin = self.alarms[person]["guild"]

                    def check(msg):
                        return msg.author == this_member



                    await this_member.send(f"{this_member.mention} {string_to_send}")
                    self.alarms.pop(person)

                    try:
                        with open('alarms.json', 'w') as those_alarms:

                            try:
                                json.dump(self.alarms, those_alarms)

                            except:
                                await this_member.send("???????????????? ???????????????????? ???????????????????????? ?????? ???????????? ??????????")
                                pass
                    except:
                        pass




                    if alarm_text == 'shutdown' and is_admin:
                        await this_member.send("?? ?????????????????????? ???? ?????????????? ???? 60 ????????????????????????. ???????????? 'cancel' ???? ???????????????? ??????????.")
                        try:
                            cancel_or_no = await self.bot.wait_for("message",check=check,timeout=60.0)
                            if str(cancel_or_no.content) == 'cancel':
                                await this_member.send("Proceedure canceled.Pc won't shut down.")
                            else:
                                await this_member.send("Shutting down now!...Bye!")
                                os.system("shutdown /s")
                        except asyncio.TimeoutError:
                            await this_member.send("Shutting down now!...Bye!")
                            os.system("shutdown /s")

            await asyncio.sleep(15)

# Now, we need to set up this cog somehow, and we do that by making a setup function:
def setup(bot: commands.Bot):
    bot.add_cog(Utility(bot))