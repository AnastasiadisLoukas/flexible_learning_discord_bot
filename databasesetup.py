import discord
from discord.ext import commands # Again, we need this imported
import asyncio
import sqlite3


#https://repl.it/talk/learn/How-to-create-an-SQLite3-database-in-Python-3/15755
class DatabaseSetup(commands.Cog):
    """Cog that sets up the database"""



    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.last_msg = None
        """These booleans represent if bot's functions are online or not"""
        self.bot.banned_words = False
        self.bot.send_mail_to_verify = False
        self.bot.agent = False
        self.bot.colour = 0xcc0567
        self.bot.remove_command('help')

    @commands.command(name="functions")
    async def settings(self,ctx):
        if self.bot.banned_words == False:
            banned_words_state = "``OFFLINE`` :red_circle:"
        else:
            banned_words_state = "``ONLINE`` :green_circle:"
        if self.bot.send_mail_to_verify == False:
            verification_state = "``OFFLINE`` :red_circle:"
        else:
            verification_state = "``ONLINE`` :green_circle:"
        if self.bot.agent == False:
            agent_state = "``OFFLINE`` :red_circle:"
        else:
            agent_state = "``ONLINE`` :green_circle:"
        if ctx.author.guild_permissions.administrator:
            await ctx.send(f"**Banned words** : {banned_words_state}\n"
                           f"**Verification** : {verification_state}\n"
                           f"**Agent**        : {agent_state}\n")
        else:
            return

    @commands.command(name="setupdatabase")
    async def setupdatabase(self,ctx):
        if ctx.author.guild_permissions.administrator:
            # Setup a connection with our database file
            connection = sqlite3.connect("studentsdata.db")
            # Create a cursor for the database to execute statements
            cursor = connection.cursor()
            try:
                cursor.execute("DROP TABLE emailsetup")
                connection.commit()
            except:
                print("there were no data to delete in emailsetup")
            create_bot_email_table = ("""CREATE TABLE IF NOT EXISTS emailsetup(
                                                                BOT_EMAIL text,
                                                                BOT_EMAIL_PASSWORD text
                                                                                            )""")
            cursor.execute(create_bot_email_table)
            connection.commit()
            sql = ("INSERT INTO emailsetup(BOT_EMAIL,BOT_EMAIL_PASSWORD) VALUES(?,?)")
            val = ("rosinantecorazon41@gmail.com", "yerhtlkshtnf245fd")
            cursor.execute(sql, val)
            connection.commit()

            banned_words = ["xazos", "xaze", "xazi"]
            create_banned_words_table = ("""CREATE TABLE IF NOT EXISTS banned_words(banned_word text)""")
            cursor.execute(create_banned_words_table)
            connection.commit()
            for banned_word in range(len(banned_words)):
                find_banned_word = f"SELECT banned_word FROM banned_words WHERE banned_word = '{banned_words[banned_word]}'"
                cursor.execute(find_banned_word)
                result = cursor.fetchall()
                if len(result) == 0:
                    """banned word does not exist , then we insert it"""
                    insert_banned_word = f"INSERT INTO banned_words(banned_word) VALUES (?)"
                    val = f"{banned_words[banned_word]}"
                    cursor.execute(insert_banned_word, (val,))
            connection.commit()

            domains = ["gmail.com", "gmail.gr", "outlook.gr", "outlook.com", "csd.auth.gr", "yahoo.com", "yahoo.gr"]
            create_domains_table = ("""CREATE TABLE IF NOT EXISTS domains(DOMAIN text)""")
            cursor.execute(create_domains_table)
            connection.commit()
            for domain in range(len(domains)):
                find_domain = f"SELECT DOMAIN FROM domains WHERE DOMAIN = '{domains[domain]}'"
                cursor.execute(find_domain)
                result = cursor.fetchall()
                if len(result) == 0:
                    """domain does not exist , then we insert it"""
                    insert_domain = f"INSERT INTO domains(DOMAIN) VALUES (?)"
                    val = f"{domains[domain]}"
                    cursor.execute(insert_domain, (val,))
            connection.commit()



            create_students_table = ("""CREATE TABLE IF NOT EXISTS students(
                                                            DISCORD_ID text,
                                                            NAME text,
                                                            SURNAME text,
                                                            AEM text,
                                                            TYPE text,
                                                            STUDENT_EMAIL text,
                                                            PRIMARY KEY("STUDENT_EMAIL"))""")
            cursor.execute(create_students_table)
            connection.commit()

            create_servers_table = ("""CREATE TABLE IF NOT EXISTS servers(
                                                                                    SERVER_ID text,
                                                                                    SERVER_NAME text,
                                                                                    INVITE_LINK text,
                                                                                    PRIMARY KEY("SERVER_ID"))""")
            cursor.execute(create_servers_table)
            connection.commit()

            create_students_in_servers_table = ("""CREATE TABLE IF NOT EXISTS students_in_servers(
                                                                                                    EMAILSTUDENT text,
                                                                                                    IDSERVER text,
                                                                                                    TIMESTAMP text,
                                                                                                    FOREIGN KEY("IDSERVER") REFERENCES "servers"("SERVER_ID"),
                                                                                                    FOREIGN KEY("EMAILSTUDENT") REFERENCES "students"("STUDENT_EMAIL"))""")
            cursor.execute(create_students_in_servers_table)
            connection.commit()

            connection.close()
        else:
            message = await ctx.channel.send("error 404 , no administration priviledges found")
            await asyncio.sleep(2)
            await message.delete()
            return
        await ctx.author.send("database ready!!!")

    @commands.Cog.listener()
    async def on_ready(self):


        # Setup a connection with our database file
        connection = sqlite3.connect("studentsdata.db")
        # Create a cursor for the database to execute statements
        cursor = connection.cursor()
        try:
            cursor.execute("DROP TABLE emailsetup")
            connection.commit()
        except:
            print("there were no data to delete in emailsetup")
        create_bot_email_table = ("""CREATE TABLE IF NOT EXISTS emailsetup(
                                                    BOT_EMAIL text,
                                                    BOT_EMAIL_PASSWORD text
                                                                                )""")
        cursor.execute(create_bot_email_table)
        connection.commit()
        sql = ("INSERT INTO emailsetup(BOT_EMAIL,BOT_EMAIL_PASSWORD) VALUES(?,?)")
        val = ("rosinantecorazon41@gmail.com", "yerhtlkshtnf245fd")
        cursor.execute(sql, val)
        connection.commit()

        banned_words = ["xazos", "xaze", "xazi"]
        create_banned_words_table = ("""CREATE TABLE IF NOT EXISTS banned_words(banned_word text)""")
        cursor.execute(create_banned_words_table)
        connection.commit()
        for banned_word in range(len(banned_words)):
            find_banned_word = f"SELECT banned_word FROM banned_words WHERE banned_word = '{banned_words[banned_word]}'"
            cursor.execute(find_banned_word)
            result = cursor.fetchall()
            if len(result)==0:
                """banned word does not exist , then we insert it"""
                insert_banned_word = f"INSERT INTO banned_words(banned_word) VALUES (?)"
                val = f"{banned_words[banned_word]}"
                cursor.execute(insert_banned_word,(val,))
        connection.commit()


        domains = ["gmail.com", "gmail.gr", "outlook.gr", "outlook.com", "csd.auth.gr", "yahoo.com", "yahoo.gr"]
        create_domains_table = ("""CREATE TABLE IF NOT EXISTS domains(DOMAIN text)""")
        cursor.execute(create_domains_table)
        connection.commit()
        for domain in range(len(domains)):
            find_domain = f"SELECT DOMAIN FROM domains WHERE DOMAIN = '{domains[domain]}'"
            cursor.execute(find_domain)
            result = cursor.fetchall()
            if len(result) == 0:
                """domain does not exist , then we insert it"""
                insert_domain = f"INSERT INTO domains(DOMAIN) VALUES (?)"
                val = f"{domains[domain]}"
                cursor.execute(insert_domain, (val,))
        connection.commit()

        create_students_table = ("""CREATE TABLE IF NOT EXISTS students(
                                                DISCORD_ID text,
                                                NAME text,
                                                SURNAME text,
                                                AEM text,
                                                TYPE text,
                                                STUDENT_EMAIL text,
                                                PRIMARY KEY("STUDENT_EMAIL"))""")
        cursor.execute(create_students_table)
        connection.commit()

        create_servers_table = ("""CREATE TABLE IF NOT EXISTS servers(
                                                                        SERVER_ID text,
                                                                        SERVER_NAME text,
                                                                        INVITE_LINK text,
                                                                        PRIMARY KEY("SERVER_ID"))""")
        cursor.execute(create_servers_table)
        connection.commit()

        create_students_in_servers_table = ("""CREATE TABLE IF NOT EXISTS students_in_servers(
                                                                                        EMAILSTUDENT text,
                                                                                        IDSERVER text,
                                                                                        TIMESTAMP text,
                                                                                        FOREIGN KEY("IDSERVER") REFERENCES "servers"("SERVER_ID"),
                                                                                        FOREIGN KEY("EMAILSTUDENT") REFERENCES "students"("STUDENT_EMAIL"))""")
        cursor.execute(create_students_in_servers_table)
        connection.commit()

        connection.close()
        print('DatabaseSetup cog ready')



# Now, we need to set up this cog somehow, and we do that by making a setup function:
def setup(bot: commands.Bot):
    bot.add_cog(DatabaseSetup(bot))
