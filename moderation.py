import discord
from discord.ext import commands # Again, we need this imported
import asyncio
import sqlite3

class Moderation(commands.Cog):
    """Moderation commands"""
    client = discord.Client()
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.last_msg = None
        self.custom_prefix = bot.command_prefix

    @commands.command(name='clear')
    async def clear(self, ctx, num_messages=None):
        """Clear <n> messages from current channel"""
        try:
            if num_messages == None:
                error_message = await ctx.send("Δεν προσδιορίσθηκε ο αριθμός των στοιχείων που απαιτούν διαγραφή")
                await asyncio.sleep(5)
                await error_message.delete()
                return
            else:
                try:
                    num_messages = int(num_messages)
                except:
                    error_message = await ctx.send("Μάλλον δεν δόθηκε ακέραιος ως όρισμα")
                    await asyncio.sleep(5)
                    await error_message.delete()
                    return

            if ctx.author.guild_permissions.administrator:
                await ctx.channel.purge(limit=num_messages + 1, check=None, before=None)
                message = await ctx.channel.send(f"✅** Διαγράφηκαν {num_messages} μηνύματα **")
                await asyncio.sleep(5)
                await message.delete()
            else:
                message = await ctx.channel.send("Δεν βρέθηκαν δικαιώματα διαχειριστή γι αυτή την εντολή")
                await asyncio.sleep(5)
                await message.delete()
                return
        except Exception as error:
            error_message = await ctx.send(error)
            await asyncio.sleep(5)
            await error_message.delete()


    @commands.command(name='clearbot')
    async def clearbot(self, ctx, num_messages: int):
        """Clear bot messages from current channel searching <n> messages"""
        def is_bot(msg):
            return msg.author == self.bot.user
        if ctx.author.guild_permissions.administrator:

            await ctx.channel.purge(limit=num_messages + 1, check=is_bot, before=None)
            message = await ctx.channel.send(f"deleted {num_messages} messages")
            await asyncio.sleep(2)
            await message.delete()
        else:
            message = await ctx.channel.send("error 404 , no administration priviledges found")
            await asyncio.sleep(2)
            await message.delete()
            return

    @commands.command(name="enable")
    async def enable(self, ctx, keyword):
        try:
            if ctx.author.guild_permissions.administrator:
                if str(keyword) == "verify":
                    self.bot.send_mail_to_verify = True
                    await ctx.author.send(f"Η διαδικασία πιστοποίησης χρήστη μέσω email είναι **ενεργή**")
                elif str(keyword)=="bannedwords":
                    self.bot.banned_words = True
                    await ctx.author.send(f"Η διαδικασία φιλτραρίσματος λέξεων είναι **ενεργή**")
                elif str(keyword)=="agent":
                    self.bot.agent = True
                    await ctx.author.send(f"Ο πράκτορας βοηθητικής εκμάθησης είναι **ενεργός**")
            else:
                await ctx.author.send("Η εντολή αυτή είναι εκτελέσιμη μόνο από διαχειριστές σε κανάλι σέρβερ")
        except Exception as error:
            await ctx.author.send(f"{error}")

    @commands.command(name="disable")
    async def disable(self, ctx, keyword):
        try:
            if ctx.author.guild_permissions.administrator:
                if str(keyword) == "verify":
                    self.bot.send_mail_to_verify = False
                    await ctx.author.send(f"Η διαδικασία πιστοποίησης χρήστη μέσω email είναι **ανενεργή**")
                elif str(keyword)=="bannedwords":
                    self.bot.banned_words = False
                    await ctx.author.send(f"Η διαδικασία φιλτραρίσματος λέξεων είναι **ανενεργή**")
                elif str(keyword)=="agent":
                    self.bot.agent = False
                    await ctx.author.send(f"Ο πράκτορας βοηθητικής εκμάθησης είναι **ανενεργός**")
            else:
                await ctx.author.send("Η εντολή αυτή είναι εκτελέσιμη μόνο από διαχειριστές σε κανάλι σέρβερ")
        except Exception as error:
            await ctx.author.send(f"{error}")


    @commands.command(name="setstatus")
    async def setstatus(self, ctx: commands.Context, *, text: str):
        """Set the bot's status"""
        if ctx.author.guild_permissions.administrator:
            await self.bot.change_presence(activity=discord.Game(text))


    @commands.command(name="addbadword")
    async def addbadword(self,ctx,*,word_to_be_banned:str):
        if ctx.author.guild_permissions.administrator:
            connection = sqlite3.connect("studentsdata.db")
            cursor = connection.cursor()
            find_banned_word = f"SELECT banned_word FROM banned_words WHERE banned_word = '{word_to_be_banned}'"
            cursor.execute(find_banned_word)
            result = cursor.fetchall()
            if len(result) == 0:
                """banned word does not exist , then we insert it"""
                insert_banned_word = f"INSERT INTO banned_words(banned_word) VALUES (?)"
                val = f"{word_to_be_banned}"
                cursor.execute(insert_banned_word, (val,))
                connection.commit()
                connection.close()
                await ctx.author.send(f"bad word '{word_to_be_banned}' added in database")
            else:
                connection.close()
                await ctx.author.send("word is already banned")
        else:
            await ctx.author.send("administration priviledges not found")

    @commands.command(name="deletebadword")
    async def deletebadword(self, ctx, *, word_to_be_unbanned: str):
        if ctx.author.guild_permissions.administrator:
            connection = sqlite3.connect("studentsdata.db")
            cursor = connection.cursor()
            find_banned_word = f"SELECT banned_word FROM banned_words WHERE banned_word = '{word_to_be_unbanned}'"
            cursor.execute(find_banned_word)
            result = cursor.fetchall()
            if len(result) != 0:
                """banned  exists , then we delete it"""
                remove_banned_word = f"DELETE  FROM banned_words WHERE banned_word = '{word_to_be_unbanned}'"
                cursor.execute(remove_banned_word)
                connection.commit()
                connection.close()
                await ctx.author.send("bad word removed from database")
            else:
                connection.close()
                await ctx.author.send("i didn't find the word you mentioned")
        else:
            await ctx.author.send("administration priviledges not found")

    @commands.command(name="restart")
    async def restart(self,ctx):
        try:
            def check(msg):
                return msg.author == ctx.author
            async def permission(ctx):

                perm_answer_str = "preparing for while loop.perm_answer_str initialization"
                while (perm_answer_str!= "nai" and perm_answer_str!="yes" and
                    perm_answer_str!="no" and perm_answer_str!="ναι" and
                    perm_answer_str!="όχι" and perm_answer_str!="οχι" and perm_answer_str!="oxi"):

                        permission_answer = await self.bot.wait_for("message", check=check)
                        perm_answer_str = str(permission_answer.content)
                        if perm_answer_str.startswith(f"{self.custom_prefix}"):
                            await ctx.author.send(
                                "Παρακαλώ μη γράφετε εντολές κατά τη διαδικασία επιβεβαίωσης.Προσπαθήστε ξανά\n"
                                "Δεκτές απαντήσεις : **(ναι/όχι)**")

                if (perm_answer_str == "nai") or (perm_answer_str=="ναι") or (perm_answer_str=="yes"):
                    return True
                else:
                    return False
            if ctx.author.guild_permissions.administrator:
                try:
                    await ctx.send(f"Σίγουρα θέλετε να κάνετε επανεκκίνηση το μποτάκι?"
                                          f"\nΔεκτές απαντήσεις : **(ναι/όχι)**")
                    permission_to_restart_bot = await permission(ctx)
                    if permission_to_restart_bot:
                        import os
                        os.system("python bot.py")
                        exit()
                except Exception as error:
                    await ctx.send(f"{error}")
                    return


            else:
                await ctx.author.send("Δεν έχεις δικαιώματα διαχειριστή γι αυτή την ενέργεια")
        except Exception as error:
            await ctx.send(f"{error}")
            return

    @commands.command(name="pc")
    async def pc(self,ctx,command=None):
        try:
            def check(msg):
                return msg.author == ctx.author
            async def permission(ctx):

                perm_answer_str = "preparing for while loop.perm_answer_str initialization"
                while (perm_answer_str!= "nai" and perm_answer_str!="yes" and
                    perm_answer_str!="no" and perm_answer_str!="ναι" and
                    perm_answer_str!="όχι" and perm_answer_str!="οχι" and perm_answer_str!="oxi"):

                        permission_answer = await self.bot.wait_for("message", check=check)
                        perm_answer_str = str(permission_answer.content)
                        if perm_answer_str.startswith(f"{self.custom_prefix}"):
                            await ctx.author.send(
                                "Παρακαλώ μη γράφετε εντολές κατά τη διαδικασία επιβεβαίωσης.Προσπαθήστε ξανά\n"
                                "Δεκτές απαντήσεις : **(ναι/όχι)**")

                if (perm_answer_str == "nai") or (perm_answer_str=="ναι") or (perm_answer_str=="yes"):
                    return True
                else:
                    return False
            if ctx.author.guild_permissions.administrator:
                import os
                if command!=None:
                    if command == "shutdown":
                        await ctx.send(f"Σίγουρα θέλετε να τερματήσετε τον υπολογιστή σας?"
                                              f"\nΔεκτές απαντήσεις : **(ναι/όχι)**")
                        permission_to_shutdown = await permission(ctx)
                        if permission_to_shutdown:
                            os.system("shutdown /s")
                    elif command =="restart":
                        await ctx.send(f"Σίγουρα θέλετε να κάνετε επανεκκίνηση τον υπολογιστή σας?"
                                              f"\nΔεκτές απαντήσεις : **(ναι/όχι)**")
                        permission_to_restart = await permission(ctx)
                        if permission_to_restart:
                            os.system("shutdown /r")
                    else:
                        return
                else:
                    await ctx.send("Δεν προσδιορίσατε επιθυμητή ενέργεια. \n"
                                   "Οι επιλογές είναι :"
                                   "**shutdown/restart**\n"
                                   "``Η εντολή δεν εκτελέστηκε``")
            else:
                await ctx.author.send("Δεν έχεις δικαιώματα διαχειριστή γι αυτή την ενέργεια")
        except Exception as error:
            await ctx.send(f"{error}")
            return


    #basically checks for bad words
    @commands.Cog.listener()
    async def on_message(self, ctx):
        try:
            async def getbannedwords(ctx):
                connection = sqlite3.connect("studentsdata.db")
                cursor = connection.cursor()
                sql = f"SELECT banned_word FROM banned_words"
                cursor.execute(sql)
                mylist = list(cursor.fetchall())
                connection.close()
                for i in range(len(mylist)):
                    mylist[i] = mylist[i][0]
                return (mylist)

            if self.bot.banned_words == False:
                return
            elif (ctx.author != self.bot.user):
                banned_words = await getbannedwords(ctx)

                for x in banned_words:
                    if (ctx.content.find(str(x)) != -1):
                        await ctx.delete()
                        break
            else:
                return
        except:
            return


    @commands.Cog.listener()
    async def on_ready(self):
        print('Moderation cog ready')





# Now, we need to set up this cog somehow, and we do that by making a setup function:
def setup(bot: commands.Bot):
    bot.add_cog(Moderation(bot))