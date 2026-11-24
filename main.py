from telethon import TelegramClient
from telethon.tl.types import User
import os
import json


# =========================
# CONFIG
# =========================

api_id = 12345678
api_hash = ""

client = TelegramClient(
    "session",
    api_id,
    api_hash
)


# =========================
# BANNER
# =========================

BANNER = r"""

███╗   ███╗ ██████╗ ████████╗██╗   ██╗ ██████╗  █████╗
████╗ ████║██╔═══██╗╚══██╔══╝╚██╗ ██╔╝██╔════╝ ██╔══██╗
██╔████╔██║██║   ██║   ██║    ╚████╔╝ ██║  ███╗███████║
██║╚██╔╝██║██║   ██║   ██║     ╚██╔╝  ██║   ██║██╔══██║
██║ ╚═╝ ██║╚██████╔╝   ██║      ██║   ╚██████╔╝██║  ██║
╚═╝     ╚═╝ ╚═════╝    ╚═╝      ╚═╝    ╚═════╝ ╚═╝  ╚═╝

              MOTYGA SCANNER

"""


# =========================
# SAVE
# =========================

def save_json(name, data):

    filename = f"{name}.json"

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"\n[+] Сохранено {filename}"
    )


def save_txt(name, data):

    filename = f"{name}.txt"


    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as f:


        for msg in data:

            f.write(
                "\n====================\n"
            )

            f.write(
                f"Дата: {msg['date']}\n"
            )

            f.write(
                f"ID: {msg['id']}\n\n"
            )

            f.write(
                msg["text"]
            )


    print(
        f"\n[+] Сохранено {filename}"
    )



# =====================================================
# 1. USERNAME SCANNER
# =====================================================


async def username_scanner():


    print(
        "\n=== USERNAME SCANNER ==="
    )


    chat = input(
        "Введите ID чата: "
    )


    username = input(
        "Введите username без @: "
    )


    try:

        chat = int(chat)

    except:

        print(
            "[-] Неверный ID"
        )

        return



    mode = input(
        """
1 - терминал
2 - JSON
3 - TXT

Выбор:
"""
    )


    entity = await client.get_entity(chat)



    stats = {}
    messages = {}
    cache = {}


    print(
        "\nСканирование...\n"
    )



    async for msg in client.iter_messages(
        entity,
        limit=None
    ):


        if not msg.sender_id:
            continue



        if msg.sender_id in cache:

            sender = cache[msg.sender_id]

        else:

            sender = await msg.get_sender()
            cache[msg.sender_id] = sender



        if not isinstance(sender, User):
            continue



        if (sender.username or "").lower() != username.lower():
            continue



        uid = sender.id


        if uid not in stats:

            stats[uid] = {

                "name": sender.first_name or "",

                "username": sender.username or "",

                "count": 0

            }


            messages[uid] = []



        stats[uid]["count"] += 1



        messages[uid].append({

            "id": msg.id,

            "date": str(msg.date),

            "text": msg.text or "[медиа]"

        })



    if not stats:

        print(
            "[-] Пользователь не найден"
        )

        return



    users = list(stats.items())



    while True:


        print(
            "\n=== USERS ==="
        )


        for i,(_,u) in enumerate(users,1):

            print(
                f"{i}. {u['name']} "
                f"(@{u['username']}) "
                f"{u['count']} сообщений"
            )


        print(
            "\n0 - назад"
        )


        choice = int(
            input(
                "Выбор: "
            )
        )


        if choice == 0:
            break



        uid = users[choice-1][0]


        data = messages[uid]



        if mode == "1":

            for m in data:

                print(
                    f"\n[{m['date']}]"
                )

                print(
                    m["text"]
                )


        elif mode == "2":

            save_json(
                username,
                data
            )


        elif mode == "3":

            save_txt(
                username,
                data
            )


        input(
            "\nEnter..."
        )




# =====================================================
# 2. CHAT ID TAKER
# =====================================================


async def chat_id_taker():


    print(
        "\n=== CHAT ID TAKER ==="
    )


    mode = input(
        """
1 - с фильтром
2 - все чаты

Выбор:
"""
    )


    word = None


    if mode == "1":

        word = input(
            "Фильтр: "
        ).lower()



    dialogs = await client.get_dialogs()



    for d in dialogs:


        name = d.name or ""


        if word:

            if word not in name.lower():
                continue



        print(
            "\nNAME:",
            name
        )

        print(
            "ID:",
            d.id
        )

        print(
            "-"*30
        )



    input(
        "\nEnter..."
    )





# =====================================================
# 3. USER STATISTICS
# =====================================================


async def user_statistics():


    print(
        "\n=== USER STATISTICS ==="
    )


    chat = input(
        "Введите CHAT ID: "
    )


    try:

        chat = int(chat)

    except:

        return



    entity = await client.get_entity(chat)



    stats={}
    messages={}
    cache={}


    print(
        "Сканирование..."
    )



    async for msg in client.iter_messages(
        entity,
        limit=None
    ):


        if not msg.sender_id:
            continue



        if msg.sender_id in cache:

            sender = cache[msg.sender_id]

        else:

            sender = await msg.get_sender()
            cache[msg.sender_id]=sender



        if isinstance(sender, User):


            uid=sender.id


            if uid not in stats:

                stats[uid]={

                    "name":sender.first_name or "",

                    "username":sender.username or "",

                    "count":0

                }


                messages[uid]=[]



            stats[uid]["count"]+=1


            if msg.text:

                messages[uid].append(msg.text)



    users=sorted(
        stats.items(),
        key=lambda x:x[1]["count"],
        reverse=True
    )



    while True:


        print(
            "\n=== USERS ==="
        )


        for i,(_,u) in enumerate(users,1):

            print(
                f"{i}. {u['name']} "
                f"@{u['username']} "
                f"{u['count']}"
            )


        print(
            "0 - выход"
        )


        c=int(
            input("Выбор: ")
        )


        if c==0:
            break



        uid=users[c-1][0]


        for m in messages[uid][-50:]:

            print(
                "-",
                m
            )


        input(
            "Enter..."
        )





# =====================================================
# MENU
# =====================================================


async def main():


    while True:


        os.system(
            "cls" if os.name=="nt" else "clear"
        )


        print(BANNER)


        print(
"""
1 - MOTYGA Username Scanner
2 - MOTYGA Chat ID Taker
3 - MOTYGA User Statistics

0 - Выход
"""
        )


        choice=input(
            "Выбор: "
        )



        if choice=="1":

            await username_scanner()


        elif choice=="2":

            await chat_id_taker()


        elif choice=="3":

            await user_statistics()


        elif choice=="0":

            break




with client:

    client.loop.run_until_complete(main())