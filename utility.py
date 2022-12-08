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

    @commands.command(name='help',aliases =['βοήθεια','hint','βοηθεια','commands','εντολες','εντολές'])
    async def help(self,ctx,typeofhelp=None):

        if typeofhelp!=None:
            k = typeofhelp.lower()
            if k == "moderation" or k == 'διαχείριση':
                embed = discord.Embed(title=f"**ΕΝΤΟΛΕΣ ΓΙΑ ΔΙΑΧΕΙΡΙΣΤΕΣ**",
                                      description=f"Είναι προσβάσιμές μόνο από διαχειριστές.", colour=self.bot.colour,
                                      timestamp=datetime.datetime.now())
                embed.add_field(name="**enable**", value=f"```Ενεργοποιεί βασικές λειτουργίες του μποτ.Αυτές μπορεί να είναι : η διαδικασία 'verify',ή"
                                                         f" η διαδικασία 'agent' ή η διαδικασία 'bannedwords'```", inline=False)
                embed.add_field(name="**disable**", value=f"```Απενεργοποιεί βασικές λειτουργίες```", inline=False)
                embed.add_field(name="**clear**", value=f"```Διαγράφει προκαθορισμένο αριθμό μηνυμάτων```",
                                inline=False)
                embed.add_field(name="**clearbot**",
                                value=f"```Διαγράφει σε προκαθορισμένο όγκο μηνυμάτων μόνο τα μηνύματα που προέρχονται από το μποτ```", inline=False)
                embed.add_field(name="**addbadword**",
                                value=f"```Προσθέτει την απαγορευμένη λέξη στη βάση δεδομένων που δίνεται ως όρισμα```",
                                inline=False)
                embed.add_field(name="**deletebadword**",
                                value=f"```Αφαιρεί από τη βάση δεδομένων την απαγορευμένη λέξη που δίνεται ως όρισμα```",
                                inline=False)
                embed.add_field(name="**restart**",
                                value=f"```Κάνει επανεκκίνηση το μποτ.Όλα τα δεδομένα φορτωμένα στη μνήμη χάνονται```",
                                inline=False)
                embed.add_field(name="**pc**",
                                value=f"```Παίρνει ως όρισμα τις λέξεις : 'shutdown' ή 'restart' και ανάλογα επανεκκινεί ή τερματίζει τον υπολογιστή```",
                                inline=False)
                embed.add_field(name="**setstatus**",
                                value=f"```Παίρνει ως όρισμα μία πρόταση για να τη θέσει ως προσωπικό μήνυμα του μποτ.```",
                                inline=False)
                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"Βοήθεια προς τον χρήστη {ctx.author.name}")
                await ctx.send(embed=embed)
            elif k == "utility":
                embed = discord.Embed(title=f"**ΧΡΗΣΙΜΕΣ ΕΝΤΟΛΕΣ**",
                                      description=f"Εντολές που μπορεί να χρειαστεί κάποιος χρήστης", colour=self.bot.colour,
                                      timestamp=datetime.datetime.now())
                embed.add_field(name="**sendmail**", value=f"```Ξεκινά διαδικασία αποστολής ηλεκτρονικού μηνύματος```", inline=False)
                embed.add_field(name="**help**", value=f"```Βοηθά το χρήστη να κατανοήσει τη χρήση του μποτ."
                                                       f"Μπορεί επίσης να ενεργοποιηθεί με τις λέξεις 'βοήθεια' και 'hint'```", inline=False)
                embed.add_field(name="**alarm**", value=f"```Δημιουργεί προσωπική ειδοποίηση για μια συγκεκριμένη στιγμή.Αν το περιεχόμενο του μηνύματος είναι 'shutdown' και ο χρήστης της εντολής έχει δικαιώματα διαχειριστή κλείνει το pc την επιλεγμένη ώρα.```",inline=False)
                embed.add_field(name="**myalarm**", value=f"```Δείχνει τη προσωπική ειδοποίηση στο χρήστη```",inline=False)

                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"Βοήθεια προς τον χρήστη {ctx.author.name}")
                await ctx.send(embed=embed)
            elif k == "contacts" or k == 'επαφές' :
                embed = discord.Embed(title=f"**ΕΝΤΟΛΕΣ ΣΧΕΤΙΚΕΣ ΜΕ ΤΙΣ ΕΠΑΦΕΣ ΤΩΝ ΧΡΗΣΤΩΝ**",
                                      description=f"Μερικές είναι διαθέσιμες μόνο από διαχειριστές για την εξασφάλιση ανωνυμίας",
                                      colour=self.bot.colour,
                                      timestamp=datetime.datetime.now())
                embed.add_field(name="**user**", value=f"```Ανάκτηση στοιχείων χρήστη με όρισμα ένα τετραψήφιο αριθμό```",
                                inline=False)
                embed.add_field(name="**aem**", value=f"```Ανάκτηση στοιχείων χρήστη με όρισμα την αναφορά (mention-tag) τον χρήστη```",
                                inline=False)
                embed.add_field(name="**verify**", value=f"```Ξεκινά διαδικασία πιστοποίησης και εγγραφής χρήστη στη βάση δεδομένων```",
                                inline=False)

                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"Βοήθεια προς τον χρήστη {ctx.author.name}")
                await ctx.send(embed=embed)
            elif k == "somecommands":
                embed = discord.Embed(title=f"**ΜΕΡΙΚΕΣ ΕΝΤΟΛΕΣ**",
                                      description=f"Διαθέσιμες προς όλους τους χρήστες",
                                      colour=self.bot.colour,
                                      timestamp=datetime.datetime.now())
                embed.add_field(name="**echo**",
                                value=f"```Δέχεται ως όρισμα μια πρόταση την οποία το μποτ στέλνει στο κανάλι.Επειτα το αρχικό"
                                      f"μήνυμα του χρήστη διαγράφεται```",
                                inline=False)
                embed.add_field(name="**calculateage**",
                                value=f"```Ξεκινά διαδικασία υπολογισμού ηλικίας του χρήστη```",
                                inline=False)
                embed.add_field(name="**countdown**",
                                value=f"```Αντίστροφη μέτρηση από αριθμό που έχει δοθεί ως όρισμα```",
                                inline=False)
                embed.add_field(name="**clock**",
                                value=f"```Αντίστροφη μέτρηση από αριθμό που έχει δοθεί ως όρισμα```",
                                inline=False)
                embed.add_field(name="**hungergames**",
                                value=f"```<prefix>hungergames <emoji> <seconds> <number_of_winners>```",
                                inline=False)

                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"Βοήθεια προς τον χρήστη {ctx.author.name}")
                await ctx.send(embed=embed)
            elif k == "agentchat" or k=="agent" or k=="πράκτορας":
                embed = discord.Embed(title=f"**ΕΝΤΟΛΕΣ ΠΡΑΚΤΟΡΑ**",
                                      description=f"Εφικτές μόνο αν υπάρχει το σχετικό αρχείο στο φάκελο.",
                                      colour=self.bot.colour,
                                      timestamp=datetime.datetime.now())
                embed.add_field(name="**loadagent**",
                                value=f"```Δέχεται ως όρισμα το όνομα του πράκτορα. "
                                      f"Φορτώνει το πράκτορα στη μνήμη . Χρήση : <prefix>loadagent <name_of_agent>.docx```",
                                inline=False)
                embed.add_field(name="**agentstart**",
                                value=f"```Ξεκινά διαδικασία συνομιλίας με το πράκτορα.Πρέπει υποχρεωτικά να πληκτρολογηθεί στο κανάλι που θα"
                                      f"ξεκινήσει η συνομιλία με την ομάδα. Χρήση : <prefix>agentstart <name_of_agent>.docx```",
                                inline=False)
                embed.add_field(name="**agentfinish**",
                                value=f"```Πληκτρολογείται από τους συμμετέχοντες μόλις τελειώσουν ένα πράκτορα.Δεν είναι υποχρεωτική και δεν"
                                      f"δέχεται κάποιο όρισμα.```",
                                inline=False)
                embed.add_field(name="**teamanswers**",
                                value=f"```Επιλέγει ένα αντιπρόσωπο της ομάδας και δημιουργεί αρχεία με τις απαντήσεις της ομάδας σε φάκελο"
                                      f"!!! Η εντολή agentfinish δεν πρέπει να έχει χρησιμοποιηθεί!!!. Η εντολή teamanswers"
                                      f" καλό είναι να χρησιμοποιείται λίγο πριν τη λήξη της διαδικασίας του πράκτορα."
                                      f"Δέχεται επίσης ως όρισμα το όνομα του πράκτορα.Χρήση : <prefix>teamanswers <name_of_agent>.docx```",
                                inline=False)
                embed.add_field(name="**agentanswers**",
                                value=f"```Δημιουργεί αρχεία σε φάκελο με τις απαντήσεις όσων έχουν συμμετέχει στο πράκτορα."
                                      f"Χρήση : <prefix>agentanswers <name_of_agent>.docx```",
                                inline=False)
                embed.add_field(name="**agentparticipants**",
                                value=f"```Πληκτρολογείται από διαχειριστές και δείχνει τις ομάδες με τους συμμετέχοντες στο πράκτορα```",
                                inline=False)

                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"Βοήθεια προς τον χρήστη {ctx.author.name}")
                await ctx.send(embed=embed)
            elif k == "test" or k == 'τεστ':
                embed = discord.Embed(title=f"**ΕΝΤΟΛΕΣ ΤΕΣΤ**",
                                      description=f"Εφικτές μόνο αν υπάρχει το σχετικό αρχείο στο φάκελο.",
                                      colour=self.bot.colour,
                                      timestamp=datetime.datetime.now())
                embed.add_field(name="**loadtest**",
                                value=f"```Φορτώνει το τεστ στη μνήμη. Χρήση : <prefix>loadtest <name_of_doc>.docx"
                                      f"Μη ξεχνάτε τη κατάληξη .docx```",
                                inline=False)
                embed.add_field(name="**teststart**",
                                value=f"```Ξεκινά διαδικασία εξέτασης.Η εντολή πληκτρολογείται από τον εξεταζόμενο"
                                      f"Δέχεται ως όρισμα το όνομα του τεστ όπως η εντολή loadtest```",
                                inline=False)
                embed.add_field(name="**participants**",
                                value=f"```Εντολή διαθέσιμη μόνο προς διαχειριστές.Δείχνει όσους συμμετέχουν στο τεστ.```",
                                inline=False)
                embed.add_field(name="**showme**",
                                value=f"```Δέχεται ως όρισμα το όνομα του τεστ και το discord id του εξεταζόμενου."
                                      f"Δείχνει τις απαντήσεις του εξεταζόμενου ως προς ένα συγκεκριμένο τεστ."
                                      f"Εντολή διαθέσιμη μόνο προς τους διαχειριστές.```",
                                inline=False)
                embed.add_field(name="**stats**",
                                value=f"```Δέχεται ως όρισμα το όνομα του τεστ όπως η εντολή loadtest."
                                      f"Δείχνει στατιστικά απαντήσεων μονής και πολλαπλής επιλογής από χρήστες σε ένα"
                                      f"συγκεκριμένο τεστ. Μπορεί να χρησιμοποιηθεί για τεστ που έχουν τη μορφή ερωτηματολογίου```",
                                inline=False)
                embed.add_field(name="**printanswers**",
                                value=f"```Δέχεται ως όρισμα το όνομα του τεστ που κάποιοι χρήστες εξετάστηκαν."
                                      f"Δημιουργεί φάκελο με τις απαντήσεις χρηστών.Αν κάποιος χρήστης έχει ήδη καταγεγραμμένη"
                                      f"απάντηση γίνεται αντικατάσταση με τη καινούρια.```",
                                inline=False)

                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"Βοήθεια προς τον χρήστη {ctx.author.name}")
                await ctx.send(embed=embed)
            elif k == "reactionroles" or k == 'ρόλοι':
                embed = discord.Embed(title=f"**ΕΝΤΟΛΕΣ ΑΝΤΙΣΤΟΙΧΙΣΗΣ ΡΟΛΩΝ**",
                                      description=f"Η χρήση τους διευκολύνει το προσδιορισμό των ρόλων των χρηστών",
                                      colour=self.bot.colour,
                                      timestamp=datetime.datetime.now())
                embed.add_field(name="**rr**",
                                value=f"```Δημιουργία πίνακα ρόλων. Χρήση : <prefix>rr```",
                                inline=False)
                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"Βοήθεια προς τον χρήστη {ctx.author.name}")
                await ctx.send(embed=embed)
            else:
                await ctx.send("Δεν υπάρχει τέτοιου είδους λειτουργεία .\n"
                               "Συμβουλευτείτε τις λειτουργίες πατώντας την εντολή ``help``")
        else:
            embed = discord.Embed(title=f"**ΚΑΤΗΓΟΡΙΕΣ ΕΝΤΟΛΩΝ {(self.bot.user.name).upper()}**", description=f"Οι επιμέρους κατηγορίες λειτουργιών.\n"
                                                                                                       f"Πληκτρολόγησε την εντολή help μαζί με μία από αυτές για επιπλέον πληροφορίες.", colour=self.bot.colour,
                                  timestamp=datetime.datetime.now())
            embed.add_field(name="**Moderation**", value=f"```Εντολές μόνο για Διαχειριστές```", inline=True)
            embed.add_field(name="**Utility**", value=f"```Χρήσιμες εντολές```", inline=True)
            embed.add_field(name="**Contacts**", value=f"```Εντολές για επικοινωνία με τη βάση δεδομένων```", inline=True)
            embed.add_field(name="**SomeCommands**", value=f"```Εντολές που μπορούν να χρησιμοποιηθούν από όλους```", inline=True)
            embed.add_field(name="**AgentChat**", value=f"```Εντολές ειδικές για την έναρξη συνομιλίας σε δωμάτιο με πράκτορα```", inline=True)
            embed.add_field(name="**Test**", value=f"```Εντολές ειδικές για την έναρξη εξέτασης από διαμορφωμένο τεστ```", inline=True)
            embed.add_field(name="**ReactionRoles**",value=f"```Εντολές ειδικές για την αντιστοίχιση ρόλων με αντιδάσεις```", inline=True)
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.set_footer(text=f"Βοήθεια προς τον χρήστη {ctx.author.name}")
            await ctx.send(embed=embed)

    @commands.command(name="alarm",aliases =['ξυπνητήρι','ειδοποίηση','ring'])
    async def alarm(self,ctx):
        if ctx.guild==None:
            await ctx.author.send("H εντολή αυτή πληκτρολογείται εντός του σέρβερ")
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
                await ctx.author.send("Η ημερομηνία που ορίσατε είναι ανέφικτο να οριστεί.Η διαδικασία τερματίστηκε.")
                return False
            elif user_input["month"] == current_status["month"] and user_input["day"] == current_status["day"] and \
                    user_input["minutes"] <= current_status["minutes"]:
                await ctx.author.send("Η ώρα που ορίσατε είναι ανέφικτο να οριστεί.H διαδικασία τερματίστηκε.")
                return False
            else:
                user_input["year"] = current_status["year"]
                user_input["allmonths"]=disekto(user_input["year"])
                return True
        await ctx.author.send("Γράψτε τι θα θέλατε να λέει η ειδοποίησή σας")
        alarm_text = await self.bot.wait_for("message", check=check)
        alarm_text = str(alarm_text.content)
        bad_user_input = True
        tries = -1
        while bad_user_input:
            tries += 1
            await ctx.author.send("Δώστε μήνυμα στη μορφή **μμηηωωλλ** δηλαδή μήνα,μέρα,ώρα,λεπτά.``πχ 05251030 σημαίνει 25 Μαΐου 10:30 το πρωί``")
            msg = await self.bot.wait_for("message", check=check)
            try:
                alarm = int(msg.content)
            except:
                await ctx.author.send("Λανθασμένη είσοδος δεδομένων.Προσπαθήστε ξανά.")
                continue
            if len(str(msg.content))!=8:
                await ctx.author.send("Δεν έγινε σωστή εισαγωγή δεδομένων.Ο προβλεπόμενος αριθμός που πρέπει να εισαχθεί θα πρέπει να έχει 8 ψηφία.Προσπαθήστε ξανά.")
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
                await ctx.author.send("Λανθασμένη είσοδος για ``μήνα``.Προσπαθήστε ξανά.")
                continue
            elif user_input["day"]>user_input["allmonths"][user_input["month"]-1] or user_input["day"]<=0:
                await ctx.author.send("Λανθασμένη είσοδος για ``μέρα``.Προσπαθήστε ξανά.")
                continue
            elif user_input["minutes"]<0 or user_input["minutes"]>59:
                await ctx.author.send("Λανθασμένη είσοδος για ``λεπτά``.Προσπαθήστε ξανά.")
                continue
            elif user_input["hour"]<0 or user_input["hour"]>23:
                await ctx.author.send("Λανθασμένη είσοδος για ``ώρα``.Προσπαθήστε ξανά.")
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
            day_event = 'το μεσημέρι'
        elif user_input['hour']>16 and user_input['hour']<=20:
            day_event = 'το απόγευμα'
        elif user_input['hour']>20 and user_input['hour']<=23:
            day_event = 'το βράδυ'
        elif user_input['hour']>=0 and user_input['hour']<=3:
            day_event = 'μετά τα μεσάνυχτα'
        elif user_input['hour']>3 and user_input['hour']<=6:
            day_event = 'τα χαράματα'
        elif user_input['hour']>6 and user_input['hour']<=12:
            day_event = 'το πρωί'
        else:
            return
        await ctx.author.send(f"Θέσατε ξυπνητήρι για τις {user_input['day']} του μήνα {user_input['month']} στις {user_input['hour']}:{user_input['minutes']} {day_event}")



        try:
            with open('alarms.json', 'w') as those_alarms:

                try:
                    json.dump(self.alarms, those_alarms)

                except:
                    await ctx.send("Αποτυχία καταγραφής ειδοποιήσεων στο σκληρό δίσκο")
                    pass
        except:
            pass
        """
        
        Αυτός ο κώδικας ίσως χρειαστεί εαν γίνει η επιλογή οι ειδοποιήσεις να μην γράφονται στο σκληρό δίσκο.Απλώς θα βγάλουμε τα
        κομμάτια που γίνεται η καταγραφή με json και ότι σχετικό κώδικα υπάρχει στο on_ready . ίσως αργότερα αν υλοποιηθεί κάποια εντολή όπως το 
        enable alarms ,disable alarms να χρειαστεί. για να υπάρχει η δυνατότητα επιλογής αν οι ειδοποιήσεις θα αποθηκεύονται στο σκληρό ή όχι.

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
                string_to_send = f"Θέσατε ειδοποίηση για : **{current_day}**/**{current_month}** και ώρα **{current_hour}**:**{current_minute}**\n"
                string_to_send+=f"H ειδοποίησή σας :\n" \
                                f"```{alarm_text}```"
                await ctx.author.send(f"{ctx.author.mention} {string_to_send}")
                self.alarms.pop(ctx.author.id)




                if alarm_text == 'shutdown' and ctx.author.guild_permissions.administrator:
                    await ctx.author.send("Ο υπολογιστής θα κλείσει σε 60 δευτερόλεπτα. Πιέστε 'cancel' αν αλλάξατε γνώμη.")
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
                    string_to_send = f"Θέσατε ειδοποίηση για : **{current_day}**/**{current_month}** και ώρα **{current_hour}**:**{current_minute}**\n"
                    string_to_send+=f"H ειδοποίησή σας :\n" \
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
                                await this_member.send("Αποτυχία καταγραφής ειδοποιήσεων στο σκληρό δίσκο")
                                pass
                    except:
                        pass




                    if alarm_text == 'shutdown' and is_admin:
                        await this_member.send("Ο υπολογιστής θα κλείσει σε 60 δευτερόλεπτα. Πιέστε 'cancel' αν αλλάξατε γνώμη.")
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