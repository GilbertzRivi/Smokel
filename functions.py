from discord import Embed, File, Member
from os import getenv, path
from io import BytesIO
from database import Database
from datetime import datetime

def read(file_path):
    file_path = path.join(f'{path.dirname(path.abspath(__file__))}', file_path)
    with open(file_path) as f:
        return f.read()

def read_b(file_path):
    file_path = path.join(f'{path.dirname(path.abspath(__file__))}', file_path)
    with open(file_path, 'rb') as f:
        return f.read()

def write(file_path, data):
    file_path = path.join(f'{path.dirname(path.abspath(__file__))}', file_path)
    with open(file_path, 'w') as f:
        f.write(data)

def discord_file(path, name, spoiler):
    return File(BytesIO(read_b(path)), filename=name, spoiler=spoiler)

def user_info(author, member: Member, new=False):
    
    e = Embed(color=member.color)
    
    if new:
        e.set_footer(text=f"Na potrzeby serwera", icon_url=author.avatar_url)
    else:
        e.set_footer(text=f"Na prośbę {author}", icon_url=author.avatar_url)

    d_joined, h_joined, m_joined, s_joined = time_to_days(datetime.utcnow().timestamp() - member.joined_at.timestamp())
    d_created, h_created, m_created, s_created = time_to_days(datetime.utcnow().timestamp() - member.created_at.timestamp())

    on_serv = f'{d_joined} dni, {h_joined} godzin, {m_joined} minut i {s_joined} sekund temu'

    acc_age = f'{d_created} dni, {h_created} godzin, {m_created} minut i {s_created} sekund temu'

    e.set_author(name=f"informacje na temat użytkownika {member.name}")
    e.set_thumbnail(url=member.avatar_url)
    e.add_field(name="ID:", value=member.id, inline=False)
    e.add_field(name="Nick:", value=member.name, inline=False)
    e.add_field(name="Dołączyl do discorda:", value=member.created_at.strftime("%H:%M - %d.%m.%Y"), inline=False)
    e.add_field(name="Dołączyl na serwer:", value=member.joined_at.strftime("%H:%M - %d.%m.%Y"), inline=False)
    e.add_field(name="Na serwerze jest:", value=on_serv, inline=False)
    e.add_field(name="Konto ma:", value=acc_age, inline=False)
    return e

def time_to_days(time):

    days = int(time / 86400)
    rest = time % 86400
    hours = int(rest / 3600)
    rest = rest % 3600
    minutes = int(rest / 60)
    seckonds = int(rest % 60)

    return days, hours, minutes, seckonds

def check_moderator_permissions(roles):
    db = Database(getenv('DB_NAME'))
    moderator_role_id = db.fetch('value', 'config', 'name = "moderation_role_id"').fetchone()
    if moderator_role_id[0] in [role.id for role in roles]:
        return True
    else: 
        return False
