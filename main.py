import discord
from discord.ext import commands
from config import token
from logic import Pokemon

# Bot için niyetleri (intents) ayarlama
intents = discord.Intents.default()  # Varsayılan ayarların alınması
intents.messages = True              # Botun mesajları işlemesine izin verme
intents.message_content = True       # Botun mesaj içeriğini okumasına izin verme
intents.guilds = True                # Botun sunucularla (loncalar) çalışmasına izin verme

# Tanımlanmış bir komut önekine ve etkinleştirilmiş amaçlara sahip bir bot oluşturma
bot = commands.Bot(command_prefix='!', intents=intents)

# Bot çalışmaya hazır olduğunda tetiklenen bir olay
@bot.event
async def on_ready():
    print(f'Giriş yapıldı:  {bot.user.name}')  # Botun adını konsola çıktı olarak verir

# '!go' komutu
@bot.command()
async def go(ctx):
    author = ctx.author.name  # Mesaj yazarının adını alma
    # Kullanıcının zaten bir Pokémon'u olup olmadığını kontrol edin. Eğer yoksa, o zaman...
    if author not in Pokemon.pokemons.keys():
        pokemon = Pokemon(author)  # Yeni bir Pokémon oluşturma
        await pokemon.get_name()  # Pokémon ismini almak için API'yi çağırıyoruz
        await ctx.send(await pokemon.info())  # Pokémon hakkında daha fazla bilgi gönderilmesi
        image_url = await pokemon.show_img()  # Pokémon resminin URL'sini alma
        if image_url:
            embed = discord.Embed()  # Gömülü mesajı oluşturma
            embed.set_image(url=image_url)  # Pokémon'un görüntüsünün ayarlanması
            await ctx.send(embed=embed)  # Görüntü içeren gömülü bir mesaj gönderme
        else:
            await ctx.send("Pokémonun görüntüsü yüklenemedi!")
    else:
        await ctx.send("Zaten kendi Pokémonunuzu oluşturdunuz!")  # Bir Pokémon'un daha önce yaratılıp yaratılmadığını gösteren bir mesaj

@bot.command()
async def besle(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[author]
        result = await pokemon.besle()
        await ctx.send(result)
    else:
        await ctx.send("Henüz bir Pokémon oluşturmadınız! Lütfen !go komutunu kullanın.")

@bot.command()
async def bırak(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons.keys():
        del Pokemon.pokemons[author]  # Kullanıcının Pokémon'unu sil
        await ctx.send(f"{author}, Pokémon'unuzu başarıyla bıraktınız.")
    else:
        await ctx.send("Henüz bir Pokémon oluşturmadınız! Lütfen !go komutunu kullanın.")

@bot.command()
async def pokedex(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[author]
        description = await pokemon.get_pokedex_data()  # Pokémon hakkında açıklama almak
        await ctx.send(f"Pokémon hakkında açıklama: {description}")
    else:
        await ctx.send("Henüz bir Pokémon oluşturmadınız! Lütfen !go komutunu kullanın.")

@bot.command()
async def info(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[author]
        info = await pokemon.info()  # Pokémon'un bilgilerini almak
        await ctx.send(info)
    else:
        await ctx.send("Henüz bir Pokémon oluşturmadınız! Lütfen !go komutunu kullanın.")

# Botun çalıştırılması
bot.run(token)
