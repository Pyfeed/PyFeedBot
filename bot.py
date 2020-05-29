import discord

TOKEN = ""
DEVID = 579298652938305551

bot = commands.Bot(
    command_prefix="??",
    description='PyFeed Bot',
    owner_id=DEVID,
    case_insensitive=True
)
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"
bot.load_extension("jishaku")
bot.launch_time = datetime.datetime.utcnow()

cogs = []
system_extensions = []


@bot.event
async def on_ready():
        print(f'{bot.user} has connected to Discord! ID:{bot.user.id}')
        await bot.change_presence(activity=discord.Game(name="Spoonfedding"),
                                  status=discord.Status.online)
        for cog in cogs:
            bot.load_extension(cog)
        for extension in system_extension:
          bot.load_extension(extension)
        print("Total Users: " + str(len(bot.users)))
        print("Total Servers: " + str(len(bot.guilds)))

@bot.event
async def on_message(message):
    if not bot.on_ready_fired:
        return
    else:

bot.run(TOKEN, reconnect=True)

