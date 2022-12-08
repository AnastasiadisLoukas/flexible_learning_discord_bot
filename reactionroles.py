import discord
import asyncio
import emoji as emojilibrary
from discord.ext import commands
import json


class ReactionRoles(commands.Cog):
    """Reaction Roles"""
    client = discord.Client()

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.last_msg = None
        self.custom_prefix = bot.command_prefix
        self.bot.rr = {}
        self.bot.rolecreator = []

    """
    rr = { server_1_id : { message_1_id : { emoji1 : role1,
                                        emoji2 : role2}
                         message_2_id : { emoji1 : role1,
                                       emoji2 : role2}
            server_2_id : {message_1_id : {emoji1 : role1,
                                     emoji2 : role2}}}

            SERVER IDS AND MESSAGE IDS AND EMOJIS ALL ARE STRINGS
    """

    @commands.command(name="rr")
    async def reactrole(self, ctx):
        if ctx.guild == None:
            await ctx.send("η εντολή δεν μπορεί να πληκτρολογηθεί εκτός guild")
            return
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("Δεν βρέθηκαν δικαιώματα διαχειριστή")
            return
        if ctx.author.id in self.bot.rolecreator:
            await ctx.send("Έχετε ήδη ξεκινήσει μια διαδικασία δημιουργίας ρόλων.")
            return
        else:
            self.bot.rolecreator.append(ctx.author.id)

        def check(msg):
            return msg.author == ctx.author

        async def check_if_it_is_custom(string_emoji):
            try:
                start = string_emoji.startswith("<:")
                end = string_emoji.endswith(">")
                count = (string_emoji.count(":") == 2)
                if start and end and count:
                    string_emoji_id = string_emoji.split(":")[-1]
                    string_emoji_id = string_emoji_id.split(">")[0]
                    return string_emoji_id, True
                else:
                    return '0', False
            except:
                return '0', False

        """
        THIS FUNCTION WILL BE NEEDED FOR UNIQUE RAW REACTION ADD



        async def permission(ctx):
            list_to_delete_in_permission = []
            perm_answer_str = "preparing for while loop.perm_answer_str initialization"
            while (perm_answer_str != "nai" and perm_answer_str != "yes" and
                   perm_answer_str != "no" and perm_answer_str != "ναι" and
                   perm_answer_str != "όχι" and perm_answer_str != "οχι" and perm_answer_str != "oxi"):
                if (perm_answer_str != "nai" and perm_answer_str != "yes" and
                        perm_answer_str != "no" and perm_answer_str != "ναι" and
                        perm_answer_str != "όχι" and perm_answer_str != "οχι" and perm_answer_str != "oxi"):
                    amessage = await ctx.channel.send("Δεκτές απαντήσεις : **(ναι/όχι)**")
                    list_to_delete_in_permission.append(amessage)

                permission_answer = await self.bot.wait_for("message", check=check)
                list_to_delete_in_permission.append(permission_answer)
                perm_answer_str = str(permission_answer.content)
                if perm_answer_str.startswith(f"{self.custom_prefix}"):
                    await ctx.author.send(
                        "Παρακαλώ μη γράφετε εντολές κατά τη διαδικασία επιβεβαίωσης.Προσπαθήστε ξανά")

            if (perm_answer_str == "nai") or (perm_answer_str == "ναι") or (perm_answer_str == "yes"):
                for i in list_to_delete_in_permission:
                    await i.delete()
                return True
            else:
                for i in list_to_delete_in_permission:
                    await i.delete()
                return False

        """

        list_to_delete = []  # TRASH CAN
        custom_emoji_dict = {}
        unicode_emoji_dict = {}
        temp_role_dict = {}

        botmessage_one = await ctx.channel.send("```Παρακαλώ δηλώστε τίτλο του πίνακα ρόλων```")
        list_to_delete.append(botmessage_one)
        answer_title = await self.bot.wait_for("message", check=check)
        list_to_delete.append(answer_title)
        title = str(answer_title.content)  # component 1
        botmessage_two = await ctx.channel.send("```Πολύ ωραία , τώρα δηλώστε μια περιγραφή για το πίνακα ρόλων,\n"
                                                "αν θέλετε κενή περιγραφή δώστε τη λέξη 'empty'```")
        list_to_delete.append(botmessage_two)
        answertwo = await self.bot.wait_for("message", check=check)
        description = str(answertwo.content)  # component 2
        list_to_delete.append(answertwo)
        botmessage_three = await ctx.channel.send("```Τώρα δηλώστε τους ρόλους στη μορφή : <@ρόλος> <εμοτζι>\n"
                                                  "Στο τέλος πατήστε done. Μέχρι 15 ρόλους.\n"
                                                  "Αν θέλετε να ακυρώσετε τη διαδικασία πατήστε 'cancel'```")
        list_to_delete.append(botmessage_three)

        string_answer = ""
        role_count = 0
        while (string_answer != 'done' and role_count < 15 and string_answer != 'cancel'):
            try:

                # INPUT

                answer = await self.bot.wait_for("message", check=check)
                list_to_delete.append(answer)
                string_answer = str(answer.content)
                if string_answer != 'done' and string_answer != 'cancel':
                    string_answer = string_answer.split()
                    role_str = string_answer[0]
                    emoji = string_answer[1]

                    # ROLE CHECKS :

                    # FIRST CHECK IF THE ROLE IS VALID.IF THE CONVERSION CANT BE DONE IT LEADS TO EXCEPTION.
                    role = await commands.RoleConverter().convert(answer, role_str)
                    is_bot_managed = role.is_bot_managed()
                    if is_bot_managed:
                        amessage = await ctx.send("Αυτός ο ρόλος χρησιμοποιείται από μποτ.Προσπαθήστε ξανά")
                        list_to_delete.append(amessage)
                        continue

                    # CHECK FOR DUPLICATE ROLE.
                    role_values = temp_role_dict.values()
                    if role.id in role_values:
                        amessage = await ctx.send("Αυτός ο ρόλος χρησιμοποιείται ήδη.Προσπαθήστε ξανά.")
                        list_to_delete.append(amessage)
                        continue

                    # EMOJI CHECKS :

                    # CHECK IF THE EMOJI IS VALID,AND IF IT IS CUSTOM OR NOT.
                    emoji_id, it_is_custom = await check_if_it_is_custom(emoji)
                    if it_is_custom:  # if it is custom it is valid
                        #await ctx.send("custom for sure")
                        pass
                    else:  # it is not custom . if it's random string it leads to exception.
                        #await ctx.send("not custom")
                        try:
                            emoji_id = emojilibrary.demojize(emoji)
                            if emoji_id in emojilibrary.UNICODE_EMOJI["en"].values():
                                pass
                            else:
                                amessage = await ctx.send("Το εμοτζι δεν είναι έγκυρο.")
                                list_to_delete.append(amessage)
                                continue


                        except:
                            amessage = await ctx.send("Το εμοτζι δεν είναι έγκυρο.")
                            list_to_delete.append(amessage)
                            continue

                    # CHECK FOR DUPLICATES NOW. IF WE REACH THIS POINT OF CODE BOTH EMOJI AND ROLE ARE VALID.
                    if it_is_custom:
                        custom_values = custom_emoji_dict.values()
                        if emoji_id in custom_values:
                            amessage = await ctx.send("Το εμοτζι υπάρχει ήδη")
                            list_to_delete.append(amessage)
                            continue
                        else:
                            temp_role_dict[role_count] = role.id
                            custom_emoji_dict[role_count] = int(emoji_id)  # everything is ok . store them temporarily.
                    else:  # if it is not custom then surely it is default emoji.
                        unicode_values = unicode_emoji_dict.values()
                        if emoji_id in unicode_values:
                            amessage = await ctx.send("Το εμοτζι υπάρχει ήδη")
                            list_to_delete.append(amessage)
                            continue
                        else:
                            temp_role_dict[role_count] = role.id
                            unicode_emoji_dict[role_count] = emoji_id  # everything is ok . store them temporarily.

                    await answer.add_reaction("💾")
                    role_count += 1
            except:
                await answer.add_reaction("❓")
                amessage = await ctx.send("Λανθασμένη είσοδος δεδομένων. Προσπαθήστε ξανά.")
                list_to_delete.append(amessage)
                continue
        else:
            if string_answer == 'cancel':

                # here we just need to delete everything
                self.bot.rolecreator.remove(ctx.author.id)
                try:
                    for i in list_to_delete:
                        await i.delete()
                except:
                    pass

            if string_answer == 'done' or role_count >= 15:

                """
                THIS IS IN CASE UNIQUE ON_RAW_REACTION_ADD IS IMPLEMENTED
                ##################################################################################################
                amessage = await ctx.send("Θα θέλατε οι ρόλοι να είναι μοναδικοί?")###############################
                list_to_delete.append(amessage)###################################################################
                permission_to_be_unique = await permission(ctx)###################################################
                ##################################################################################################
                """

                # lastmessage = await ctx.send("✅** Επιτυχία δημιουργίας ρόλων!**\n```Παρακαλώ περιμένετε μερικά δευτερόλεπτα```")
                if description == "empty":
                    embedded_roles_message = discord.Embed(title=f"{title}",colour=self.bot.colour)
                else:
                    embedded_roles_message = discord.Embed(title=f"**{title}**",
                                                           description=f"``` ```{description}\n``` ```",colour=self.bot.colour)

                """
                THIS IS IN CASE UNIQUE ON_RAW_REACTION_ADD IS IMPLEMENTED

                #######################################################################################################
                if permission_to_be_unique:############################################################################
                    embedded_roles_message.set_footer(text="Με δυνατότητα μονής επιλογής!")############################
                else:##################################################################################################
                    embedded_roles_message.set_footer(text="Με δυνατότητα πολλαπλής επιλογής!")########################
                #######################################################################################################
                """

                if str(ctx.guild.id) not in self.bot.rr:
                    self.bot.rr[str(ctx.guild.id)] = {}
                for i in range(len(temp_role_dict)):
                    if i in custom_emoji_dict:
                        embed_emoji = self.bot.get_emoji(int(custom_emoji_dict[i]))
                    else:
                        embed_emoji = emojilibrary.emojize(unicode_emoji_dict[i])
                    role = discord.utils.get(ctx.guild.roles, id=temp_role_dict[i])
                    embedded_roles_message.add_field(name="\u200B", value=f"{embed_emoji} = {role.mention}",
                                                     inline=True)

                msg = await ctx.send(embed=embedded_roles_message)

                if str(msg.id) not in self.bot.rr[str(ctx.guild.id)]:
                    self.bot.rr[str(ctx.guild.id)][str(msg.id)] = {}
                for i in range(len(temp_role_dict)):
                    if i in custom_emoji_dict:
                        self.bot.rr[str(ctx.guild.id)][str(msg.id)][str(custom_emoji_dict[i])] = temp_role_dict[i]
                        await msg.add_reaction(self.bot.get_emoji(int(custom_emoji_dict[i])))
                    else:
                        self.bot.rr[str(ctx.guild.id)][str(msg.id)][str(unicode_emoji_dict[i])] = temp_role_dict[i]
                        this_unicode_emoji = emojilibrary.emojize(unicode_emoji_dict[i])
                        await msg.add_reaction(this_unicode_emoji)
                lastmessage = await ctx.send(
                    "✅** Επιτυχία δημιουργίας ρόλων!**\n```Παρακαλώ περιμένετε μερικά δευτερόλεπτα```")

                """
                FOR UNIQUE RAW REACTION ADD

                if permission_to_be_unique:
                    self.bot.rr[str(ctx.guild.id)][str(msg.id)]['unique'] = True
                    self.bot.rr[str(ctx.guild.id)][str(msg.id)]["users"]={}
                else:
                    self.bot.rr[str(ctx.guild.id)][str(msg.id)]['unique'] = False
                """

                self.bot.rolecreator.remove(ctx.author.id)
                try:
                    for i in list_to_delete:
                        await i.delete()
                except:
                    pass
                try:
                    await lastmessage.delete()
                except:
                    pass
                try:
                    with open('reaction_role.json', 'w') as fout:

                        try:
                            json.dump(self.bot.rr, fout)

                        except:
                            await ctx.send("Αποτυχία καταγραφής ρόλων στο σκληρό δίσκο")
                            pass
                except:
                    pass

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        try:
            if payload.guild_id == None:
                return
            if payload.member != self.bot.user:
                try:
                    # if payload.guild_id not in self.bot.rr:
                    #    self.bot.users_reacted[payload.guild_id]={}
                    # member_id = payload.member.id
                    message_id = payload.message_id
                    # channel = self.bot.get_channel(payload.channel_id)
                    # message = await channel.fetch_message(message_id)
                    try:
                        payload_id = (payload.emoji.id)
                        role_id = self.bot.rr[str(payload.guild_id)][str(message_id)][str(payload_id)]

                    except:
                        payload_id = emojilibrary.demojize(payload.emoji.name)
                        role_id = self.bot.rr[str(payload.guild_id)][str(message_id)][str(payload_id)]
                    guild = self.bot.get_guild(payload.guild_id)
                    role = discord.utils.get(guild.roles, id=role_id)
                    await payload.member.add_roles(role)

                    """
                    if self.bot.rr[str(payload.guild_id)][str(payload.message_id)]['unique'] == True:


                        HERE WE CAN FIGURE OUT A WAY TO REMOVE ALL THE OTHER ROLES
                        THIS SPACE IS FOR IMPLEMENTING UNIQUE RAW REACTION ADD

                    """
                except:
                    return
        except :
            return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        try:
            if payload.guild_id == None:
                return
            if payload.member != self.bot.user:
                if str(payload.guild_id) in self.bot.rr:
                    if str(payload.message_id) in self.bot.rr[str(payload.guild_id)]:
                        # if payload.emoji.name in self.bot.rr[payload.guild_id][payload.message_id]:
                        try:
                            try:
                                payload_id = (payload.emoji.id)
                                role_id = self.bot.rr[str(payload.guild_id)][str(payload.message_id)][str(payload_id)]
                            except:
                                payload_id = emojilibrary.demojize(payload.emoji.name)
                                role_id = self.bot.rr[str(payload.guild_id)][str(payload.message_id)][str(payload_id)]

                            guild = self.bot.get_guild(payload.guild_id)
                            role = discord.utils.get(guild.roles, id=role_id)
                            member = guild.get_member(payload.user_id)
                            await  member.remove_roles(role)
                        except:
                            return

        except Exception as error:
            try:
                channel_id = payload.channel_id
                channel = self.bot.get_channel(channel_id)
                await channel.send(error)
            except:
                return
            return

    @commands.Cog.listener()
    async def on_ready(self):

        try:
            with open('reaction_role.json') as fin:

                self.bot.rr = json.load(fin)

        except:
            pass

        print('Reaction Roles cog ready')


# Now, we need to set up this cog somehow, and we do that by making a setup function:
def setup(bot: commands.Bot):
    bot.add_cog(ReactionRoles(bot))