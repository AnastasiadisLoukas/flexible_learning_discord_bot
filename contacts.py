import discord
import datetime
from discord.ext import commands # Again, we need this imported
import random
import asyncio
import smtplib ,ssl
import sqlite3

class Contacts(commands.Cog):
    """A couple of simple commands"""
    client = discord.Client()
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.last_msg = None

    @commands.command(name="user")
    async def user(self, ctx, member: discord.Member):
        """Find a user by mentioning him in a channel"""
        try:
            if ctx.author.guild_permissions.administrator:
                try :
                    connection = sqlite3.connect("studentsdata.db")
                    cursor = connection.cursor()
                    finduser = f"SELECT * FROM students WHERE DISCORD_ID = '{str(member.id)}'"
                    cursor.execute(finduser)
                    result = cursor.fetchall()
                    connection.close()
                    for i in range(len(result[0])):
                        if i == 0:
                            user_discord_id = f"{str(result[0][i])}"
                        elif i == 1 :
                            user_name = f"{str(result[0][i])}"
                        elif i == 2 :
                            user_surname = f"{str(result[0][i])}"
                        elif i == 3 :
                            user_aem = f"{str(result[0][i])}"
                        elif i == 4 :
                            user_type = f"{str(result[0][i])}"
                        elif i == 5 :
                            user_mail = f"{str(result[0][i])}"
                        else :
                            break
                    try:
                        if member.guild_permissions.administrator:
                            user_colour = 0xd1c200
                        elif user_type =="student":
                            user_colour = 0x00ad8e
                        else:
                            user_colour = 0xff8400
                    except:
                        user_colour = 0x00ad8e

                    embed = discord.Embed(title=f"**{member.name}**", description=f"is a {user_type}", colour=user_colour,timestamp=datetime.datetime.now())


                    embed.add_field(name="NAME", value=f"{user_name}", inline=True)
                    embed.add_field(name="SURNAME", value=f"{user_surname}",inline=True)
                    embed.add_field(name="AEM", value=f"```{user_aem}```", inline=False)
                    embed.add_field(name="DISCORD_ID", value=f"{user_discord_id}", inline=False)
                    embed.add_field(name="EMAIL", value=f"```{user_mail}```", inline=False)
                    embed.set_thumbnail(url=member.avatar_url)
                    embed.set_footer(text=f"{member.guild.name}")
                    await ctx.author.send(embed=embed)
                except:
                    await ctx.author.send("something went wrong , maybe there is no such user in the database")
            else:
                message = await ctx.channel.send("error 404 , no administration priviledges found")
                await asyncio.sleep(2)
                await message.delete()
                return
        except:
            await ctx.author.send("something went wrong . or you didn't type the command in a channel ")

    @commands.command(name="aem")
    async def aem(self, ctx, member: int):
        """Find a user by his identical number"""
        try:
            if ctx.author.guild_permissions.administrator:
                try :
                    connection = sqlite3.connect("studentsdata.db")
                    cursor = connection.cursor()
                    finduser = f"SELECT * FROM students WHERE AEM = '{str(member)}'"
                    cursor.execute(finduser)
                    result = cursor.fetchall()
                    connection.close()
                    for i in range(len(result[0])):
                        if i == 0:
                            user_discord_id = f"{str(result[0][i])}"
                        elif i == 1 :
                            user_name = f"{str(result[0][i])}"
                        elif i == 2 :
                            user_surname = f"{str(result[0][i])}"
                        elif i == 3 :
                            user_aem = f"{str(result[0][i])}"
                        elif i == 4 :
                            user_type = f"{str(result[0][i])}"
                        elif i == 5 :
                            user_mail = f"{str(result[0][i])}"
                        else :
                            break
                    this_guild = ctx.guild
                    member = this_guild.get_member(int((user_discord_id)))
                    try:
                        if member.guild_permissions.administrator:
                            user_colour = 0xd1c200
                        elif user_type =="student":
                            user_colour = 0x00ad8e
                        else:
                            user_colour = 0xff8400
                    except:
                        user_colour = 0x00ad8e

                    embed = discord.Embed(title=f"**{member.name}**", description=f"is a {user_type}", colour=user_colour,timestamp=datetime.datetime.now())
                    embed.add_field(name="NAME", value=f"{user_name}", inline=True)
                    embed.add_field(name="SURNAME", value=f"{user_surname}",inline=True)
                    embed.add_field(name="AEM", value=f"```{user_aem}```", inline=False)
                    embed.add_field(name="DISCORD_ID", value=f"{user_discord_id}", inline=False)
                    embed.add_field(name="EMAIL", value=f"```{user_mail}```", inline=False)
                    embed.set_thumbnail(url=member.avatar_url)
                    embed.set_footer(text=f"{member.guild.name}")
                    await ctx.author.send(embed=embed)
                except:
                    await ctx.author.send("something went wrong , maybe there is no such user in the database or in this server")
            else:
                message = await ctx.channel.send("error 404 , no administration priviledges found")
                await asyncio.sleep(2)
                await message.delete()
                return
        except:
            await ctx.author.send("something went wrong , or you didn't type the command in a channel")

    @commands.command(name = "verify")
    async def verify(self,ctx ):
        if self.bot.send_mail_to_verify == False:
            await ctx.author.send("Η διαδικασία πιστοποίησης χρηστών μέσω mail είναι **ανενεργή**\n"
                                  f"Ζητήστε να γίνει ενεργοποίηση από κάποιο διαχειριστή με την εντολή <custom_prefix>enable verify")
            return
        member = ctx.author
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
                #this is also part of the setup ( contains private information)
                smtp.login(botemail,botpassword)
                mail_to_be_sent = f'Subject : {subject}\n\n{body}'
                smtp.sendmail(botemail, receiver, mail_to_be_sent)

        def check(msg):
            return msg.author == member

        #this function is called when the user is completely new , in no other servers.
        async def ask_user_data(email ,member_id,guild_id):
            await member.send("Please insert your name")
            username = await self.bot.wait_for("message", check=check)
            await member.send("very good , now your surname please")
            usersurname = await self.bot.wait_for("message",check=check)
            await member.send("very good , your aem please")
            useraem = await self.bot.wait_for("message",check=check)

            connection = sqlite3.connect("studentsdata.db")
            cursor = connection.cursor()

            #inserting the user's data inside students table
            sql = ("INSERT INTO students(DISCORD_ID,NAME,SURNAME,AEM,TYPE,STUDENT_EMAIL) VALUES(?,?,?,?,?,?)")
            val = (str(member_id),str(username.content),str(usersurname.content),str(useraem.content),"student",str(email))
            cursor.execute(sql,val)
            connection.commit()

            now = datetime.datetime.now()
            current_day = int(now.strftime('%d'))
            current_month = int(now.strftime('%m'))
            current_year = int(now.strftime('%y')) + 2000
            usertimestamp = f"{current_day} / {current_month} / {current_year}"

            #inserting data refering to what server the user is member of and when .
            sql = ("INSERT INTO students_in_servers(EMAILSTUDENT,IDSERVER,TIMESTAMP) VALUES(?,?,?)")
            val = (str(email),str(guild_id),str(usertimestamp))
            cursor.execute(sql,val)
            connection.commit()
            connection.close()

        async def checkuserindatabase(user_email,user_discord_id,this_guild_id):
            connection=sqlite3.connect("studentsdata.db")
            cursor=connection.cursor()
            findmail = f"SELECT STUDENT_EMAIL FROM students WHERE STUDENT_EMAIL = '{user_email}'"
            cursor.execute(findmail)
            result = cursor.fetchall()
            #1 means new user in all the servers
            #fetchall function returns a list . so if no elements are returned the list is empty . that is why we check this with len.
            if len(result)==0:
                connection.close()
                return 1
            finddiscordid = f"SELECT STUDENT_EMAIL,DISCORD_ID FROM students WHERE STUDENT_EMAIL = '{user_email}' AND DISCORD_ID = '{user_discord_id}'"
            cursor.execute(finddiscordid)
            result = cursor.fetchall()
            #3 means mail matches but not discord id . user is trying to create a double account.
            if len(result)==0 :
                connection.close()
                return 3
            findguildid = f"SELECT EMAILSTUDENT,IDSERVER FROM students_in_servers WHERE EMAILSTUDENT = '{user_email}' AND IDSERVER = '{this_guild_id}'"
            cursor.execute(findguildid)
            result = cursor.fetchall()

            #2 means user is new to this particular server but not in all the database.
            if len(result)==0 :
                connection.close()
                return 2
            #4 means user is already in the server. There is no reason to take action.
            else:
                connection.close()
                return 4

        async def giveverifyroleto(member):
            thisguild = member.guild
            try:
                role = discord.utils.get(member.guild.roles, name="verified")
                await member.add_roles(role)
                await member.send("you are now verified")
            except:
                # in case there is no role verified add one to the server and give one to the member that joined.
                guild_owner = thisguild.owner
                await guild_owner.send(
                    "something went wrong ,a new member joined and maybe there is no role 'verified' in server")
                await guild_owner.send("i will add one for you , you must only set its permissions")
                await thisguild.create_role(name="verified")
                role = discord.utils.get(member.guild.roles, name="verified")
                await member.add_roles(role)
                await member.send("you are now verified")

        try:
            member = ctx.author
            #a little string manipulation to get the user's domain from the answer he provides
            await member.send('Type your email please')
            receiver = await self.bot.wait_for("message", check=check)
            email_string =str(receiver.content)
            email_domain = email_string.split("@")
            email_domain = email_domain[1]

            connection = sqlite3.connect("studentsdata.db")
            cursor = connection.cursor()
            finddomain = f"SELECT DOMAIN FROM domains WHERE DOMAIN = '{email_domain}'"
            cursor.execute(finddomain)
            result = cursor.fetchall()
            connection.close()

            #check if the domain is in the list of valid domains
            if len(result)!=0:
                #if the user has a valid email we send the following message and an email with a random number
                await member.send('your email has a valid domain')




                #sending member's mail , member's id and the id of the server he is trying to join to check the member through
                #the sql database.
                is_ok = await checkuserindatabase(str(receiver.content),str(member.id),str(member.guild.id))
                #4 means he/she is already in this database and in this server. no need to take action.
                #3 means he/she has a double account ,trying to enter with a different discord id. we don't allow access
                #2 means his/her email and discord id is in the database already . but not linked in this particular server.
                #1 means his/her email is not in the database so it's a new user.
                thisguild = member.guild
                if is_ok== 1:
                    await member.send('please copy and paste the number sent to email to verify account')
                    await member.send("also check your spam folders")
                    # this is a totally random formula randomizer , you can build one better than this .
                    random_number = int(datetime.date.today().day) * random.randint(35, 992) * random.randint(4,
                                                                                                                  100)
                    subject = "Password to verify your account!"
                    body = random_number

                    # we start the send_mail_sequence , it's the function above.we must get the mail
                    # and password of the bot_mail from the database

                    await sendmailsequense(str(receiver.content), str(subject), str(body))
                    # we wait for the user's answer , if his/her guess is correct(is the number
                    # sent to his/her email) he/she will be verified.
                    random_number = await self.bot.wait_for("message", check=check)

                    if (int(body) == int(random_number.content)):

                        await ask_user_data(str(receiver.content),str(member.id),str(member.guild.id))
                        await giveverifyroleto(member)
                    else:
                        await member.send("this is not the correct password, would you like to try again? ")
                        try:
                            answer = await self.bot.wait_for("message", timeout=600.0, check=check)
                            if answer.content == ('yes' or 'y' or 'yeah'):
                                await self.on_member_join(member)
                            else:
                                await member.send("alright , as you wish :D")
                                await member.send(
                                    "if you wish to verify in the future just type the <prefix>verify command ! , bye for now")
                                return
                        except asyncio.TimeoutError:
                            await member.send("pfff i waited too long for an answer . try the command verify later ")
                            return
                elif is_ok == 2 :
                    await member.send('please copy and paste the number sent to email to verify account')
                    await member.send("also check your spam folders")
                    # this is a totally random formula randomizer , you can build one better than this .
                    random_number = int(datetime.date.today().day) * random.randint(35, 992) * random.randint(4,
                                                                                                                  100)
                    subject = "Password to verify your account!"
                    body = random_number

                    # we start the send_mail_sequence , it's the function above.we must get the mail
                    # and password of the bot_mail from the database

                    await sendmailsequense(str(receiver.content), str(subject), str(body))
                    # we wait for the user's answer , if his/her guess is correct(is the number
                    # sent to his/her email) he/she will be verified.
                    random_number = await self.bot.wait_for("message", check=check)

                    if (int(body) == int(random_number.content)):
                        now = datetime.datetime.now()
                        current_day = int(now.strftime('%d'))
                        current_month = int(now.strftime('%m'))
                        current_year = int(now.strftime('%y')) + 2000
                        usertimestamp = f"{current_day} / {current_month} / {current_year}"

                        connection = sqlite3.connect("studentsdata.db")
                        cursor = connection.cursor()
                        sql = ("INSERT INTO students_in_servers(EMAILSTUDENT,IDSERVER,TIMESTAMP) VALUES(?,?,?)")
                        val = (str(receiver.content), str(member.guild.id), str(usertimestamp))
                        cursor.execute(sql, val)
                        connection.commit()
                        connection.close()
                        await giveverifyroleto(member)
                    else:
                        await member.send("this is not the correct password, would you like to try again? ")
                        try:
                            answer = await self.bot.wait_for("message", timeout=600.0, check=check)
                            if answer.content == ('yes' or 'y' or 'yeah'):
                                await self.on_member_join(member)
                            else:
                                await member.send("alright , as you wish :D")
                                await member.send(
                                    "if you wish to verify in the future just type the <prefix>verify command ! , bye for now")
                                return
                        except asyncio.TimeoutError:
                            await member.send("pfff i waited too long for an answer . try the command verify later ")
                            return
                elif is_ok == 3  :
                    await member.send("You are already connected in the database with a different account.Double accounts are not permitted.")
                    await member.guild.owner.send(f"Someone with the name : {member.name} and id : {member.id} tried to create a double account")
                    await member.kick()
                else:
                    await member.send("Looks like you are already verified.")

            else:
                await member.send("You don't have a valid domain ,please try again")
                await self.on_member_join(member)
        except:
            await member.send("Maybe you run out of time or something is off ,maybe you didn't type the command in a channel, who knows ?. if you see anything not normal contact the server owner or admins")

    @commands.Cog.listener()
    async def on_member_join(self, member : discord.Member):
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
                #this is also part of the setup ( contains private information)
                smtp.login(botemail,botpassword)
                mail_to_be_sent = f'Subject : {subject}\n\n{body}'
                smtp.sendmail(botemail, receiver, mail_to_be_sent)

        def check(msg):
            return msg.author == member

        #this function is called when the user is completely new , in no other servers.
        async def ask_user_data(email ,member_id,guild_id):
            await member.send("Please insert your name")
            username = await self.bot.wait_for("message", check=check)
            await member.send("very good , now your surname please")
            usersurname = await self.bot.wait_for("message",check=check)
            await member.send("very good , your aem please")
            useraem = await self.bot.wait_for("message",check=check)

            connection = sqlite3.connect("studentsdata.db")
            cursor = connection.cursor()

            #inserting the user's data inside students table
            sql = ("INSERT INTO students(DISCORD_ID,NAME,SURNAME,AEM,TYPE,STUDENT_EMAIL) VALUES(?,?,?,?,?,?)")
            val = (str(member_id),str(username.content),str(usersurname.content),str(useraem.content),"student",str(email))
            cursor.execute(sql,val)
            connection.commit()

            now = datetime.datetime.now()
            current_day = int(now.strftime('%d'))
            current_month = int(now.strftime('%m'))
            current_year = int(now.strftime('%y')) + 2000
            usertimestamp = f"{current_day} / {current_month} / {current_year}"

            #inserting data refering to what server the user is member of and when .
            sql = ("INSERT INTO students_in_servers(EMAILSTUDENT,IDSERVER,TIMESTAMP) VALUES(?,?,?)")
            val = (str(email),str(guild_id),str(usertimestamp))
            cursor.execute(sql,val)
            connection.commit()
            connection.close()

        async def checkuserindatabase(user_email,user_discord_id,this_guild_id):
            connection=sqlite3.connect("studentsdata.db")
            cursor=connection.cursor()
            findmail = f"SELECT STUDENT_EMAIL FROM students WHERE STUDENT_EMAIL = '{user_email}'"
            cursor.execute(findmail)
            result = cursor.fetchall()
            #1 means new user in all the servers
            #fetchall function returns a list . so if no elements are returned the list is empty . that is why we check this with len.
            if len(result)==0:
                connection.close()
                return 1
            finddiscordid = f"SELECT STUDENT_EMAIL,DISCORD_ID FROM students WHERE STUDENT_EMAIL = '{user_email}' AND DISCORD_ID = '{user_discord_id}'"
            cursor.execute(finddiscordid)
            result = cursor.fetchall()
            #3 means mail matches but not discord id . user is trying to create a double account.
            if len(result)==0 :
                connection.close()
                return 3
            findguildid = f"SELECT EMAILSTUDENT,IDSERVER FROM students_in_servers WHERE EMAILSTUDENT = '{user_email}' AND IDSERVER = '{this_guild_id}'"
            cursor.execute(findguildid)
            result = cursor.fetchall()

            #2 means user is new to this particular server but not in all the database.
            if len(result)==0 :
                connection.close()
                return 2
            #4 means user is already in the server. There is no reason to take action.
            else:
                connection.close()
                return 4

        async def giveverifyroleto(member):
            thisguild = member.guild
            try:
                role = discord.utils.get(member.guild.roles, name="verified")
                await member.add_roles(role)
                await member.send("you are now verified")
            except:
                # in case there is no role verified add one to the server and give one to the member that joined.
                guild_owner = thisguild.owner
                await guild_owner.send(
                    "something went wrong ,a new member joined and maybe there is no role 'verified' in server")
                await guild_owner.send("i will add one for you , you must only set its permissions")
                await thisguild.create_role(name="verified")
                role = discord.utils.get(member.guild.roles, name="verified")
                await member.add_roles(role)
                await member.send("you are now verified")

        try:
            #a little string manipulation to get the user's domain from the answer he provides
            await member.send('Type your email please')
            receiver = await self.bot.wait_for("message", check=check)
            email_string =str(receiver.content)
            email_domain = email_string.split("@")
            email_domain = email_domain[1]

            connection = sqlite3.connect("studentsdata.db")
            cursor = connection.cursor()
            finddomain = f"SELECT DOMAIN FROM domains WHERE DOMAIN = '{email_domain}'"
            cursor.execute(finddomain)
            result = cursor.fetchall()
            connection.close()

            #check if the domain is in the list of valid domains
            if len(result)!=0:
                #if the user has a valid email we send the following message and an email with a random number
                await member.send('your email has a valid domain')




                #sending member's mail , member's id and the id of the server he is trying to join to check the member through
                #the sql database.
                is_ok = await checkuserindatabase(str(receiver.content),str(member.id),str(member.guild.id))
                #4 means he/she is already in this database and in this server. no need to take action.
                #3 means he/she has a double account ,trying to enter with a different discord id. we don't allow access
                #2 means his/her email and discord id is in the database already . but not linked in this particular server.
                #1 means his/her email is not in the database so it's a new user.
                thisguild = member.guild
                if is_ok== 1:
                    if self.bot.send_mail_to_verify == True:
                        await member.send('please copy and paste the number sent to email to verify account')
                        await member.send("also check your spam folders")
                        # this is a totally random formula randomizer , you can build one better than this .
                        random_number = int(datetime.date.today().day) * random.randint(35, 992) * random.randint(4,
                                                                                                                  100)
                        subject = "Password to verify your account!"
                        body = random_number

                        # we start the send_mail_sequence , it's the function above.we must get the mail
                        # and password of the bot_mail from the database

                        await sendmailsequense(str(receiver.content), str(subject), str(body))
                        # we wait for the user's answer , if his/her guess is correct(is the number
                        # sent to his/her email) he/she will be verified.
                        random_number = await self.bot.wait_for("message", check=check)
                        random_number_content = int(random_number.content)
                    else:
                        body = 1
                        random_number_content = 1 #this is done for the next check . Somehow random_number_content must be defined.

                    if (int(body) == random_number_content) or self.bot.send_mail_to_verify==False:

                        await ask_user_data(str(receiver.content),str(member.id),str(member.guild.id))
                        await giveverifyroleto(member)
                    else:
                        await member.send("this is not the correct password, would you like to try again? ")
                        try:
                            answer = await self.bot.wait_for("message", timeout=600.0, check=check)
                            if answer.content == ('yes' or 'y' or 'yeah'):
                                await self.on_member_join(member)
                            else:
                                await member.send("alright , as you wish :D")
                                await member.send(
                                    "if you wish to verify in the future just type the <prefix>verify command ! , bye for now")
                                return
                        except asyncio.TimeoutError:
                            await member.send("pfff i waited too long for an answer . try the command verify later ")
                            return
                elif is_ok == 2 :
                    if self.bot.send_mail_to_verify == True:
                        await member.send('please copy and paste the number sent to email to verify account')
                        await member.send("also check your spam folders")
                        # this is a totally random formula randomizer , you can build one better than this .
                        random_number = int(datetime.date.today().day) * random.randint(35, 992) * random.randint(4,
                                                                                                                  100)
                        subject = "Password to verify your account!"
                        body = random_number

                        # we start the send_mail_sequence , it's the function above.we must get the mail
                        # and password of the bot_mail from the database

                        await sendmailsequense(str(receiver.content), str(subject), str(body))
                        # we wait for the user's answer , if his/her guess is correct(is the number
                        # sent to his/her email) he/she will be verified.
                        random_number = await self.bot.wait_for("message", check=check)
                        random_number_content = int(random_number.content)
                    else:
                        body = 1
                        random_number_content = 1

                    if (int(body) == random_number_content) or (self.bot.send_mail_to_verify == False):
                        now = datetime.datetime.now()
                        current_day = int(now.strftime('%d'))
                        current_month = int(now.strftime('%m'))
                        current_year = int(now.strftime('%y')) + 2000
                        usertimestamp = f"{current_day} / {current_month} / {current_year}"

                        connection = sqlite3.connect("studentsdata.db")
                        cursor = connection.cursor()
                        sql = ("INSERT INTO students_in_servers(EMAILSTUDENT,IDSERVER,TIMESTAMP) VALUES(?,?,?)")
                        val = (str(receiver.content), str(member.guild.id), str(usertimestamp))
                        cursor.execute(sql, val)
                        connection.commit()
                        connection.close()
                        await giveverifyroleto(member)
                    else:
                        await member.send("this is not the correct password, would you like to try again? ")
                        try:
                            answer = await self.bot.wait_for("message", timeout=600.0, check=check)
                            if answer.content == ('yes' or 'y' or 'yeah'):
                                await self.on_member_join(member)
                            else:
                                await member.send("alright , as you wish :D")
                                await member.send(
                                    "if you wish to verify in the future just type the <prefix>verify command ! , bye for now")
                                return
                        except asyncio.TimeoutError:
                            await member.send("pfff i waited too long for an answer . try the command verify later ")
                            return
                elif is_ok == 3  :
                    await member.send("You are already connected in the database with a different account.Double accounts are not permitted.")
                    await member.guild.owner.send(f"Someone with the name : {member.name} and id : {member.id} tried to create a double account")
                    await member.kick()
                else:
                    await member.send("Looks like you are already verified.")

            else:
                await member.send("You don't have a valid domain ,please try again")
                await self.on_member_join(member)
        except:
            await member.send("Maybe you run out of time or something is off . if you see anything not normal contact the server owner or admins")

    @commands.Cog.listener()
    async def on_member_remove(self,member : discord.Member):
        async def checkuserindatabase(user_discord_id,this_guild_id):
            connection = sqlite3.connect("studentsdata.db")
            cursor = connection.cursor()
            find_user = f"SELECT STUDENT_EMAIL FROM students WHERE DISCORD_ID = '{user_discord_id}' "
            cursor.execute(find_user)
            result = cursor.fetchall()
            if len(result)==0:
                connection.close()
                return 0
            else:
                find_user_server = "SELECT EMAILSTUDENT FROM students_in_servers WHERE EMAILSTUDENT = (?) "
                val = str(result[0][0])
                cursor.execute(find_user_server,(val,))
                result2 = cursor.fetchall()
                connection.close()
                if len(result2)==1:
                    return 1
                else:
                    return 2

                # if len(result) is 0 no need to take action . probably someone who entered never made a link with a server
                # if len(result) is 1 then we remove the student's link with the server and the student from the database. only 1 link found
                # if len(result) is 2 means the member has multiple links with servers , we only remove the link , not the student.

        result = await checkuserindatabase(str(member.id),str(member.guild.id))
        if result == 0:
            return
        elif result == 1:
            connection = sqlite3.connect("studentsdata.db")
            cursor = connection.cursor()
            findmail = f"SELECT STUDENT_EMAIL FROM students WHERE DISCORD_ID = '{str(member.id)}'"
            cursor.execute(findmail)
            query_found_mail = cursor.fetchall()
            query_found_mail = str(query_found_mail[0][0])
            deleteserver = f"DELETE  FROM students_in_servers WHERE EMAILSTUDENT = '{query_found_mail}'"
            cursor.execute(deleteserver)
            connection.commit()
            deletestudent = f"DELETE FROM students WHERE STUDENT_EMAIL = '{query_found_mail}'"
            cursor.execute(deletestudent)
            connection.commit()
            connection.close()
        else:
            if result == 2:
                connection = sqlite3.connect("studentsdata.db")
                cursor = connection.cursor()
                findmail = f"SELECT STUDENT_EMAIL FROM students WHERE DISCORD_ID = '{str(member.id)}'"
                cursor.execute(findmail)
                query_found_mail = cursor.fetchall()
                query_found_mail = str(query_found_mail[0][0])
                deleteserver = f"DELETE  FROM students_in_servers WHERE IDSERVER = '{str(member.guild.id)}' AND EMAILSTUDENT = '{query_found_mail}'"
                cursor.execute(deleteserver)
                connection.commit()
                connection.close()


    @commands.Cog.listener()
    async def on_ready(self):
        print('Contacts cog ready')

# Now, we need to set up this cog somehow, and we do that by making a setup function:
def setup(bot: commands.Bot):
    bot.add_cog(Contacts(bot))