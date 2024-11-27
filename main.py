import discord
import random
import json
import os

from discord.ext import commands
permissao = discord.Intents.default()
permissao.message_content = True
permissao.members = True
permissao.message_content = True
permissao.guilds = True

PREFIX = "l."
TOKEN = "MTEwNjc3OTE5NTMwMTk1MzUzNw.G9kVNF.J9vD0XBVS9v4X6book5B49zttTBoRRE94-baEI"

bot = commands.Bot(command_prefix= PREFIX, intents=permissao)

config_file = "config.json"

# Função para carregar ou criar o arquivo bem vindo JSON
def load_channels():
    if not os.path.exists("channels.json"):
        with open("channels.json", "w") as file:
            json.dump({}, file)
    with open("channels.json", "r") as file:
        return json.load(file)

# Função para salvar no arquivo bem vindo JSON
def save_channels(data):
    with open("channels.json", "w") as file:
        json.dump(data, file, indent=4)

# Função para carregar ou criar o arquivo JSON
def load_channels():
    if not os.path.exists("channels.json"):
        with open("channels.json", "w") as file:
            json.dump({}, file)
    with open("channels.json", "r") as file:
        return json.load(file)

# Função para salvar no arquivo JSON
def save_channels(data):
    with open("channels.json", "w") as file:
        json.dump(data, file, indent=4)

channels = load_channels()

# Evento de boas-vindas
@bot.event
async def on_member_join(member):
    guild_id = str(member.guild.id)
    if guild_id in channels and "welcome" in channels[guild_id]:
        channel_id = channels[guild_id]["welcome"]
        channel = bot.get_channel(channel_id)
        if channel:
            embed = discord.Embed(
                title="Bem-vindo(a) ao servidor! 🎉",
                description=f"Olá, {member.mention}! Estamos felizes em ter você aqui!",
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_footer(text=f"Usuário: {member}", icon_url=member.avatar.url)
            await channel.send(embed=embed)

# Evento de despedida
@bot.event
async def on_member_remove(member):
    guild_id = str(member.guild.id)
    if guild_id in channels and "farewell" in channels[guild_id]:
        channel_id = channels[guild_id]["farewell"]
        channel = bot.get_channel(channel_id)
        if channel:
            embed = discord.Embed(
                title="Adeus! 💔",
                description=f"{member.mention} saiu do servidor. Sentiremos sua falta!",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_footer(text=f"Usuário: {member}", icon_url=member.avatar.url)
            await channel.send(embed=embed)

# Comando para definir o canal de boas-vindas
@bot.command()
@commands.has_permissions(administrator=True)
async def set_welcome_channel(ctx, channel: discord.TextChannel):
    guild_id = str(ctx.guild.id)
    if guild_id not in channels:
        channels[guild_id] = {}
    channels[guild_id]["welcome"] = channel.id
    save_channels(channels)
    await ctx.send(f"Canal de boas-vindas definido para {channel.mention}")

# Comando para definir o canal de despedida
@bot.command()
@commands.has_permissions(administrator=True)
async def set_farewell_channel(ctx, channel: discord.TextChannel):
    guild_id = str(ctx.guild.id)
    if guild_id not in channels:
        channels[guild_id] = {}
    channels[guild_id]["farewell"] = channel.id
    save_channels(channels)
    await ctx.send(f"Canal de despedida definido para {channel.mention}")

# Evento de erro para permissões
@set_welcome_channel.error
@set_farewell_channel.error
async def channel_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Você precisa ser administrador para usar este comando.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Por favor, mencione o canal corretamente.")

## Função para carregar as configurações de ticket do arquivo JSON
def load_ticket_config():
    try:
        if not os.path.exists("ticket_config.json"):
            return {}
        with open("ticket_config.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Erro ao carregar o arquivo de configuração: {e}")
        return {}

# Função para salvar as configurações de ticket no arquivo JSON
def save_ticket_config(channel_id, emoji):
    config = {
        "ticket_channel_id": channel_id,
        "emoji": emoji
    }
    with open("ticket_config.json", "w") as file:
        json.dump(config, file, indent=4)

# Carregar as configurações ao iniciar o bot
ticket_config = load_ticket_config()

def load_config():
    """Carrega a configuração do arquivo JSON"""
    if not os.path.exists(config_file):
        # Se o arquivo não existir, cria um novo com valores padrão
        save_config({"ticket_category_id": None, "ticket_channel_id": None})
        return {"ticket_category_id": None, "ticket_channel_id": None}
    
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Se houver erro de decodificação JSON, cria um novo arquivo com valores padrão
        save_config({"ticket_category_id": None, "ticket_channel_id": None})
        return {"ticket_category_id": None, "ticket_channel_id": None}

def save_config(data):
    """Salva a configuração no arquivo JSON"""
    with open(config_file, 'w') as f:
        json.dump(data, f, indent=4)

#Carregar informações da categoria e canal do ticket
config = load_config()
ticket_category_id = config.get("ticket_category_id", None)
ticket_channel_id = config.get("ticket_channel_id", None)
#Salvar mensagens dos tickets
def save_transcript(messages):
    transcript = ""
    for message in messages:
        transcript += f"[{message.created_at}] {message.author}: {message.content}\n"
    return transcript

# Comando para configurar o canal de tickets
@bot.command(name="set_ticket_channel")
@commands.has_permissions(administrator=True)
async def set_ticket_channel(ctx, channel: discord.TextChannel):
    global ticket_channel_id
    ticket_channel_id = channel.id
    config["ticket_channel_id"] = ticket_channel_id
    save_config(config)
    await ctx.send(f"Canal para criação de tickets configurado para: {channel.name}")

@bot.command()
@commands.has_permissions(administrator=True)
async def ticket_help(ctx):
    embed = discord.Embed(
        title="🎫 Comandos Do Ticket",
        color=discord.Color.blue()
    )

     # Adicionando múltiplos campos
    embed.add_field(name="Configuração do canal e categoria:", value=f"Use `{PREFIX}set_ticket_channel` #canal para definir o canal de tickets.\n Use `{PREFIX}set_ticket_category` #categoria para definir a categoria onde os canais de ticket serão criados.", inline=False)
    embed.add_field(name="Mensagem de tickets:", value=f"Use `{PREFIX}setup_ticket` para criar a mensagem de tickets com o emoji 📩. \n Caso o bot seja reiniciado terá que execultar o comando novamente", inline=False)
    embed.add_field(name="Fechar ticket:", value=f"O comando `{PREFIX}close_ticket` pode ser usado no canal do ticket para encerrá-lo e enviar o relatório ao usuário.", inline=False)
    embed.add_field(name="Permissões:", value="Apenas administradores podem configurar o bot e encerrar tickets.", inline=False)

    embed.set_footer(text="Ajuda")
    await ctx.send(embed=embed)

# Comando para configurar a categoria de tickets
@bot.command(name="set_ticket_category")
@commands.has_permissions(administrator=True)
async def set_ticket_category(ctx, category: discord.CategoryChannel):
    global ticket_category_id
    ticket_category_id = category.id
    config["ticket_category_id"] = ticket_category_id
    save_config(config)
    await ctx.send(f"Categoria de tickets configurada para: {category.name}")

# Comando para criar a mensagem de tickets
@bot.command()
@commands.has_permissions(administrator=True)
async def setup_ticket(ctx):
    global ticket_channel_id
    if not ticket_channel_id:
        await ctx.send("Primeiro configure o canal de tickets usando !set_ticket_channel.")
        return

    channel = bot.get_channel(ticket_channel_id)
    embed = discord.Embed(
        title="Suporte",
        description="Reaja com 📩 para abrir um ticket de suporte.",
        color=discord.Color.blue()
    )
    message = await channel.send(embed=embed)
    await message.add_reaction("📩")

# Evento para criar um ticket ao reagir com o emoji
@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    if reaction.message.channel.id == ticket_channel_id and str(reaction.emoji) == "📩":
        guild = reaction.message.guild
        category = guild.get_channel(ticket_category_id) if ticket_category_id else None

        # Verificar se o canal do usuário já existe
        existing_channel = discord.utils.get(guild.text_channels, name=f"ticket-{user.id}")
        if existing_channel:
            await user.send("Você já possui um ticket aberto.")
            return

        # Criar o canal de ticket
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        channel = await guild.create_text_channel(name=f"ticket-{user.id}", category=category, overwrites=overwrites)
        await channel.send(f"Olá {user.mention}, um administrador estará com você em breve.")
        await user.send(f"Seu ticket foi criado: {channel.mention}")

 # Encerrar o canal de ticket
@bot.command(name="close_ticket")
async def close_ticket(ctx):
    try:
        # Verifica se o bot tem permissão para deletar o canal
        if not ctx.channel.permissions_for(ctx.guild.me).manage_channels:
            await ctx.send("O bot não tem permissão para deletar este canal.")
            return

        if not ctx.channel.category:
            await ctx.send("Este canal não pertence a nenhuma categoria.")
            return

        if ctx.channel.category.id != ticket_category_id:
            await ctx.send(f"Este canal não pertence à categoria de tickets configurada ({ticket_category_id}).")
            return

        user = None
        for overwrite in ctx.channel.overwrites:
            if isinstance(overwrite, discord.Member):
                user = overwrite
                break

        # Coletando o histórico de mensagens corretamente
        messages = [message async for message in ctx.channel.history(limit=200)]
        messages.reverse()  # Reverte a ordem das mensagens para exibir do mais antigo ao mais recente

        # Formatação do log das mensagens
        log = "Histórico do Ticket:\n"
        log += "-" * 40 + "\n"
        
        for message in messages:
            timestamp = message.created_at.strftime("%d/%m/%Y %H:%M:%S")
            author = message.author.name
            content = message.content if message.content else "(sem mensagem)"
            log += f"[{timestamp}] {author}: {content}\n"
            log += "-" * 40 + "\n"
        
        # Enviando o log para o usuário
        if user:
            try:
                await user.send(f"Seu ticket foi encerrado. Aqui está o histórico da conversa:\n\n```\n{log}\n```")
            except discord.Forbidden:
                await ctx.send("Não foi possível enviar a mensagem ao usuário.")

        # Deletando o canal do ticket
        await ctx.channel.delete(reason="Ticket encerrado")

    except Exception as e:
        await ctx.send(f"Ocorreu um erro ao tentar fechar o ticket: {e}")
        print(f"Erro ao fechar o ticket: {e}")

@bot.command(name="get_config")
async def get_config(ctx):
    await ctx.send(f"Ticket Category ID: {ticket_category_id}\nTicket Channel ID: {ticket_channel_id}")


# Evento para garantir permissões
@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    config = load_ticket_config()

bot.remove_command("kick")

# Comando: Banir usuário
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member} foi banido. Razão: {reason}")

# Comando: Expulsar usuário
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member} foi expulso. Razão: {reason}")

# Comando: Avatar
@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(member.avatar.url)

# Comando: Gerar convite
@bot.command()
async def invite(ctx):
    invite = await ctx.channel.create_invite(max_age=3600, max_uses=10)
    await ctx.send(f"Aqui está um convite para este servidor: {invite}")

# Comando: Ping
@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! Latência: {round(bot.latency * 1000)}ms")

# Comando: Clear (limpar mensagens)
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    if amount <= 0:
        await ctx.send("Por favor, especifique um número maior que 0.")
    else:
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"{amount} mensagens apagadas!", delete_after=5)

# Comando: Informar membros do servidor
@bot.command()
async def members(ctx):
    guild = ctx.guild
    await ctx.send(f"Este servidor possui {guild.member_count} membros!")

# Comando: Criar enquetes
@bot.command()
@commands.has_permissions(administrator=True)
async def enquete(ctx, *, pergunta: str):
    """
    Comando para criar uma enquete com reações.
    Apenas administradores podem usar este comando.
    Formato: {PREFIX}enquete <pergunta | opção1 | opção2 | ...>
    Exemplo: {PREFIX}enquete Qual sua cor favorita? | Azul | Vermelho | Verde
    """
    try:
        # Divide a pergunta e as opções
        partes = pergunta.split("|")
        if len(partes) < 2:
            await ctx.send(f"❌ Formato inválido! Use: `{PREFIX}enquete <pergunta | opção1 | opção2 | ...>`")
            return

        titulo = partes[0].strip()
        opcoes = [op.strip() for op in partes[1:]]
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

        if len(opcoes) > len(emojis):
            await ctx.send("❌ Máximo de 10 opções permitidas.")
            return

        # Cria o embed da enquete
        embed = discord.Embed(
            title="📊 Enquete",
            description=f"**{titulo}**\n\n" + "\n".join(f"{emojis[i]} {op}" for i, op in enumerate(opcoes)),
            color=discord.Color.blue(),
            timestamp=ctx.message.created_at
        )
        embed.set_footer(text=f"Criada por {ctx.author.display_name}", icon_url=ctx.author.avatar.url)

        # Envia o embed e adiciona reações para votação
        mensagem = await ctx.send(embed=embed)
        for i in range(len(opcoes)):
            await mensagem.add_reaction(emojis[i])

    except Exception as e:
        await ctx.send(f"❌ Ocorreu um erro ao criar a enquete: {e}")

# Tratamento de erros de permissão
@enquete.error
async def enquete_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Você não tem permissão para usar este comando. Apenas administradores podem criar enquetes.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Uso incorreto do comando! O formato correto é: `!enquete <pergunta | opção1 | opção2 | ...>`.")
    else:
        await ctx.send(f"❌ Ocorreu um erro: {error}")

# Comando: Dizer algo
@bot.command()
async def say(ctx, *, message):
    await ctx.send(message)

# Comando: Informações do servidor
@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(
        title=f"✨ {guild.name} ✨",
        description="**Informações do Servidor**",
        color=discord.Color.blue(),
        timestamp=ctx.message.created_at
    )
    
    # Ícone do servidor
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)

    # Adiciona informações do servidor
    embed.add_field(name="👑 Dono", value=guild.owner.mention, inline=True)
    embed.add_field(name="🆔 ID do Servidor", value=guild.id, inline=True)
    embed.add_field(name="📆 Criado em", value=guild.created_at.strftime("%d/%m/%Y"), inline=True)
    embed.add_field(name="👥 Membros", value=guild.member_count, inline=True)
    embed.add_field(name="💬 Canais", value=f"{len(guild.text_channels)} texto, {len(guild.voice_channels)} voz", inline=True)
    embed.add_field(name="🚀 Nível de Boost", value=guild.premium_tier, inline=True)
    embed.add_field(name="🔮 Boosts Ativos", value=guild.premium_subscription_count or "0", inline=True)
    embed.add_field(name="🔒 Nível de Verificação", value=str(guild.verification_level).capitalize(), inline=True)
    
    # Adiciona uma imagem no rodapé, se disponível
    if guild.banner:
        embed.set_image(url=guild.banner.url)
    
    # Rodapé com o nome do bot e avatar
    embed.set_footer(text=f"Solicitado por {ctx.author.display_name}", icon_url=ctx.author.avatar.url)

    # Envia o embed
    await ctx.send(embed=embed)

bot.remove_command("help")
@bot.command()
async def help(ctx):
    commands_list = [
        {"name": f"{PREFIX}ping", "description": "Exibe a latência do bot."},
        {"name": f"{PREFIX}ticket_help", "description": "Mostra ajuda de tickets."},
        {"name": f"{PREFIX}kick [@usuario]", "description": "Expulsa um membro do servidor."},
        {"name": f"{PREFIX}ban [@usuario]", "description": "Bane um membro do servidor."},
        {"name": f"{PREFIX}enquete [opção 1] [opção 2] [...]", "description": "Cria uma Enquete."},
        {"name": f"{PREFIX}roll [n]", "description": "Role um dado com um numero personalizado [padrão 6]"},
        {"name": f"{PREFIX}serverinfo", "description": "Mostre as informações do servidor"},
        {"name": f"{PREFIX}avatar [@usuario]", "description": "Puxa a foto do usuario"},
        {"name": f"{PREFIX}say [mensagem]", "description": "Bot Envia uma mensagem por você"},
        {"name": f"{PREFIX}anuncio [#canal] [mensagem]", "description": "Bot cria uma mensagem em fortado de anuncio"},
        {"name": f"{PREFIX}poll [enquete]", "description": "Cria uma Enquete."},
        {"name": f"{PREFIX}poll [enquete]", "description": "Cria uma Enquete."},
        {"name": f"{PREFIX}poll [enquete]", "description": "Cria uma Enquete."},
        {"name": f"{PREFIX}poll [enquete]", "description": "Cria uma Enquete."},
        {"name": f"{PREFIX}poll [enquete]", "description": "Cria uma Enquete."},
    ]
    
    # Configuração de paginação
    items_per_page = 10
    pages = [commands_list[i:i + items_per_page] for i in range(0, len(commands_list), items_per_page)]
    total_pages = len(pages)

    current_page = 0

    # Cria embed inicial
    embed = discord.Embed(title="Comandos do Bot", color=discord.Color.blue())
    for cmd in pages[current_page]:
        embed.add_field(name=cmd["name"], value=cmd["description"], inline=False)
    embed.set_footer(text=f"Página {current_page + 1}/{total_pages}")

    # Envia a mensagem com reações para navegação
    message = await ctx.send(embed=embed)
    await message.add_reaction("⬅️")
    await message.add_reaction("➡️")

    # Função para verificar reações
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["⬅️", "➡️"] and reaction.message.id == message.id

    # Loop para atualizar páginas
    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=60.0, check=check)
            
            if str(reaction.emoji) == "⬅️" and current_page > 0:
                current_page -= 1
            elif str(reaction.emoji) == "➡️" and current_page < total_pages - 1:
                current_page += 1
            
            # Atualiza o embed
            embed.clear_fields()
            for cmd in pages[current_page]:
                embed.add_field(name=cmd["name"], value=cmd["description"], inline=False)
            embed.set_footer(text=f"Página {current_page + 1}/{total_pages}")
            await message.edit(embed=embed)

            # Remove reação do usuário
            await message.remove_reaction(reaction.emoji, user)

        except discord.errors.Forbidden:
            break
        except discord.errors.HTTPException:
            break
        except:
            break


@bot.command()
@commands.has_permissions(administrator=True)
async def anuncio(ctx, canal: discord.TextChannel, *, mensagem: str):
    """
    Comando para enviar um anúncio em nome do bot.
    Apenas administradores podem usá-lo.
    Formato do comando: !anuncio <#canal> <mensagem>
    """
    try:
        # Cria o embed do anúncio
        embed = discord.Embed(
            title="📢 Anúncio",
            description=mensagem,
            color=discord.Color.gold()
        )
        embed.set_footer(text=f"Anunciado por {ctx.author.display_name}", icon_url=ctx.author.avatar.url)

        # Envia o embed no canal especificado
        await canal.send(embed=embed)
        await ctx.send(f"✅ Anúncio enviado com sucesso no canal {canal.mention}!")

    except Exception as e:
        await ctx.send(f"❌ Ocorreu um erro ao tentar enviar o anúncio: {e}")

# Tratamento de erros de permissão
@anuncio.error
async def anuncio_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Você não tem permissão para usar este comando.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Uso incorreto do comando! O formato correto é: `!anuncio <#canal> <mensagem>`.")
    else:
        await ctx.send(f"❌ Ocorreu um erro: {error}")

# Comando: Jogar dado
@bot.command()
async def roll(ctx, sides: int = 6):
    if sides < 1:
        await ctx.send("O dado precisa ter pelo menos 1 lado.")
    else:
        result = random.randint(1, sides)
        await ctx.send(f"Você rolou um dado de {sides} lados e tirou: {result}")

# Tratamento de erros
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Você não tem permissão para usar este comando.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Por favor, forneça todos os argumentos necessários.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Comando não encontrado. Use {PREFIX}help para ver os comandos disponíveis.")
    else:
        await ctx.send("Ocorreu um erro ao executar o comando. ")


bot.run(TOKEN)