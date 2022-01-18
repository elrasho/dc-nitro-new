from discord.ext import commands
import discord
import requests, re
from bs4 import BeautifulSoup
import json
from msgs import Messages
from utils import mysql, colors
from datetime import date, datetime

msg = Messages()
clr = colors.clr()
dbs = mysql.Mysql()
class Test_Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cfg_file = open('config.json', 'r', encoding="UTF-8").read()
        self.cfg = json.loads(self.cfg_file)
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{len(self.bot.guilds)}")
        await self.bot.change_presence(status=discord.Status.offline)
    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            DISCORD_NITRO = r'discord(?:\.gift)/?(?:[a-zA-Z0-9\-]{2,40})'
            regex = re.compile(DISCORD_NITRO)
            invites = regex.findall(str(message.content))
            inv = bool(invites)
            codes = []
            if inv:
                invite = invites[0].replace("discord.gift/", "")
                # jeigu kodas buvo isbandytas 0 kartu
                if invite not in codes:
                    codes.append(invite)
                    print("--------------------------------")
                    msg.code_found(invite, "Rastas invite kodas...")
                    headers = {
                        "Authorization": self.cfg['user']['user_token'],
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"
                    }
                    r = requests.post(f"https://discord.com/api/v9/entitlements/gift-codes/{invite}/redeem", headers=headers)
                    response_time = int(r.elapsed.total_seconds())
                    bs = BeautifulSoup(r.content, 'html.parser')
                    y = json.loads(bs.prettify())
                    timestamp = datetime.now()
                    data = timestamp.strftime(r"%Y-%m-%d %H:%M:%S")
                    #######
                    try:
                        kodas = y['code']
                    except:
                        kodas = 69
                    if kodas == 10038:
                        ats = "Kodas negaliojantis."
                    elif kodas == 50050:
                        ats = "Kodas jau buvo aktyvuotas"
                    elif kodas == 50070:
                        ats = "Nepridetas mokejimo metodas"
                    elif kodas == 69:
                        ats = "Nitro buvo sėkmingai aktyvuotas!"
                    else:
                        ats = y['message']
                    if ats:
                        print(f"{data} ┃ {invite} ┃ {ats}")
                    #######
                    # MYSQL DALIS
                    #######
                    if kodas == 69:
                        scs = 1
                        spalva = 0x57d916
                        # sendinam sau msg kad zjb
                        usr = self.bot.get_user(int(self.cfg["user"]["admin_id"]))
                        await usr.send("Rastas veikiantis nitro, jis aktyvuotas xd")
                    else:
                        scs = 0
                        spalva = 0xd91616
                    #######
                    chnl = self.bot.get_channel(int(self.cfg['logging']['nitro_log_channel_id']))
                    message_link = f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"
                    embed=discord.Embed(title="Nitro sniper by Dariux", description=f"🎁 **Kodas**:  {invite} \n 💬 **Atsakymas** {ats}\n👤 **Kodas**: {kodas}\n🔗 **Žinutės nuoroda** {message_link}", color=spalva)
                    await chnl.send(embed=embed)
                    with open('log.txt', 'a', encoding="UTF-8") as f:
                        f.write(f"{r.url} : {r.content}\n")
        except Exception as e:
            print(e)
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            x = 1
def setup(bot): # a extension must have a setup function
    bot.add_cog(Test_Cog(bot)) # adding a cog