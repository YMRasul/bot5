import shlex
from datetime import datetime
from aiogram import Dispatcher, types
from aiogram.types import Message
from create_bot import bot, con, superuser
from .user import rootpath
from tgbot.keyboards.client_kb import kb_client, mas
from tgbot.config import Config
import os


# @dp.message_handler(commands=["start"], state="*", is_admin=True)
async def admin_start(message: Message):
    await message.answer(
        "Скрепки ни босинг !\n Fayl   'NNNNNNNNN_gggg_mm.xls'  ko'rinishida bo'lishi kerak\n Misol 200918719_2022_11.xls")


async def adm_reg(message: Message):
    text = message.text[10:]
    s = text[0:].strip()
    if message.from_user.id == superuser:
        try:
            id = int(s)
            print("Регистрация по команде /regadmin", id)
            if await con.admin_exists(id):
                await message.answer("Bu Admin registrasiya qilingan id=" + str(id))
                print("Bu Admin registrasiya qilingan id=" + str(id))
            else:
                await  con.admin_add(id)
                await message.answer(str(id) + " admin registrasiya qilindi")
                print(str(id) + " admin registrasiya qilindi")
        except:
            await message.answer("Registrasiya ketmadi id=" + s)
    else:
        print("Не SuperUser дает команду /regadmin")
        await message.answer("Это команда SuperUserа")


async def adm_del(message: Message):
    text = message.text[10:]
    s = text[0:].strip()
    if message.from_user.id == superuser:  # superUser
        try:
            id = int(s)
            print("Удаление по команде /deladmin", id)
            if await con.admin_exists(id):
                await con.admin_del(id)
                await message.answer("Удален Admin id=" + str(id))
                print("Удален Admin id=" + str(id))
            else:
                await message.answer(str(id) + " admin ro'yhatda mavjud emas")
                print(str(id) + " такой админ в списке нет")
        except:
            await message.answer("Noto'g'ri id=" + s)
    else:
        print("Не SuperUser дает команду /regadmin")
        await message.answer("Это команда SuperUserа")


async def adm_info(message: Message):
    text = ''
    print('superuser=' + str(superuser))
    if message.from_user.id == superuser:  # superUser
        r = await con.admins_info()
        if len(r) != 0:
            print("Результат команды /admins")
            for m in r:
                print(m[0], m[1], m[2], m[3])
                if m[1] is None:
                    inn = '?????????'
                else:
                    inn = str(m[1])

                if m[2] is None:
                    tel = '998???????'
                else:
                    tel = str(m[2])

                if m[3] is None:
                    fio = '??????????????????'
                else:
                    fio = m[3]
                text = text + str(m[0]) + " " + inn + " " + tel + " " + fio + "\n"
            await message.answer(text)
        else:
            await message.answer("Список админов пустой...")
    else:
        print("Не SuperUser дает команду /admins")
        await message.answer("Это команда SuperUserа")


async def user_reg(message: Message):
    user_id = message.from_user.id
    text = message.text[5:]
    try:
        print(text[0:9], text[10:], "-----> Регистрация по команде /reg 123456789 998937850078")
        inn = int(text[0:9])
        tel = int(text[10:])
        if await con.inn_exists2(inn):
            await  con.reg_id(user_id, inn, tel)
            await message.answer("Registrasiya qilindingiz ..." + str(user_id))
        else:
            await message.answer(
                "Registrasiya ketmadi\nQaytadan registrasiya qiling !\n " + str(inn) + "ORG da mavjud emas")
    except:
        await message.answer("Registrasiya ketmadi\nQaytadan registrasiya qiling ! " + str(user_id))


async def user_info(message: Message):
    inn = await con.get_inn(message.chat.id)
    print(inn)
    await message.answer("Ma'lumot olish\n" + str(inn[0]), reply_markup=kb_client)


# @dp.message_handler(commands=["sendinn"], state="*", is_admin=True)
async def send_inn(message: Message):
    text = message.text[9:]
    mess = "/sendiin dan keyin probel\n" \
           "INN 9 hona raqam probel\n" \
           "va 1 hona raqam\n" \
           "123456789 1\n" \
           "********* * "
    if message.from_user.id == superuser:  # superUser
        if len(text) == 11:
            try:
                inn = int(text[0:9])
                prz = int(text[10:11])

                if prz == 9:
                    await message.answer("Delete INN " + str(inn))
                else:
                    await message.answer("Insert or Update INN " + str(inn))

                await con.inn_add(inn, prz)
            except:
                await message.answer(mess)
        else:
            await message.answer(mess)
    else:
        print("Не SuperUser дает команду /sendinn")
        await message.answer("Это команда SuperUserа")

#dp.register_message_handler(info_inn, commands=["inns"], state="*", is_admin=True)
async def info_inn(message: Message):
    if message.from_user.id == superuser:  # superUser
        inns = await con.inn_info()
        for inn in inns:
            await message.answer(str(inn[0]) +' ' +str(inn[1]))
            print(str(inn[0]) +' ' +str(inn[1]))
    else:
        print("Не SuperUser дает команду /inns")
        await message.answer("Это команда SuperUserа")

# @dp.message_handler(commands=["sendadm"], is_admin=True)
async def send_adm(message: Message):
    config: Config = bot.get('config')
    user_id = message.from_user.id

    if message.from_user.id == superuser:  # superUser
        adms = await con.admins_info()
        for x in config.tg_bot.admin_ids:
            adms.append(tuple([int(x),]))
#        for adm in adms:
#            print(adm[0])
        if message.chat.type == 'private':
            text = message.text[9:]
            for adm in adms:
                if adm[0] != message.from_user.id:
                    try:
                        await bot.send_message(adm[0], text)
                        await bot.send_message(message.from_user.id, 'Рассылка админу ' + str(adm[0]))
                        print("Рассылка админу " + str(adm[0]))
                    except:
                        await bot.send_message(message.from_user.id, "Admin " + str(adm[0]) + " не активен")
                        print("Admin " + str(adm[0]) + " не активен")

# @dp.message_handler(commands=["sendall"], is_admin=True)
async def send_all(message: Message):
    config: Config = bot.get('config')
    user_id = message.from_user.id
    print("Админстраторы " + str(config.tg_bot.admin_ids))
    r = await con.get_inn(user_id)
    if ((message.chat.type == 'private') and (r != None)):
        text = message.text[9:]
        users = await con.get_users()
        if (users != None):
            # idp,fio,prz,inn
            for row in users:
                try:
                    if row[1] == None:
                        row[1] = ''
                    if row[3] == r[0]:
                        await bot.send_message(row[0], text)
                        if int(row[3]) != 1:
                            await con.set_active(1, row[0])
                        await bot.send_message(message.from_user.id, 'Рассылка' + ' ' + str(row[0]) + ": " + row[1])
                        print("Рассылка юзеру " + str(row[0]) + " " + row[1])
                except:
                    await con.set_active(0, row[0])
                    print("Юзер " + str(row[0]) + " " + row[1] + " не активен")


# @dp.message_handler(content_types=[types.ContentType.DOCUMENT])
async def scan_doc(message: types.document):
    try:
        file_info = await bot.get_file(message.document.file_id)
        downloaded_file = await bot.download_file(file_info.file_path)
        path_sep = os.path.sep
        fil = rootpath() + path_sep + 'files' + path_sep
        src = fil + message.document.file_name

        now = datetime.now()  # current date and time
        date_time = now.strftime("%Y.%m.%d %H:%M:%S") + ':'

        foun = await con.poisk_id(message.from_user.id, message.document.file_name)
        if foun:
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file.getvalue())
            print(date_time, "Сохранен как " + src)
            await message.answer("Men buni saqlab qoydim, rahmat!")
        else:
            await message.answer("Fayl qabul qilinmadi !")

    except Exception as e:
        await message.answer(e)


async def help(message: types.Message):
    #    print("Help для Админа")
    hlp = "/start - Fayl jo'natish\n" \
          "/sendall - Hammaga habar yuborish\n"
    hlp = hlp + "/reg INN Tel -registratsiya\n     INN- 9 hona raqam, tel- 998 bilan\n\n/info - ma'lumot olish\n"

    if message.from_user.id == superuser:  # superUser
        hlp = hlp + "\nSuperuser\n\n/sendinn INN # \nДобавить\nИзменит\nУдалить #=9"
        hlp = hlp + "\n/inns - 'список ORG'\n"
        hlp = hlp + "\n/addadmin - 'addaamin ID'\n/deladmin - 'deladmin ID'\n/admins\n/sendadm - 'sendadm text'"

    await message.answer(hlp)


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
    dp.register_message_handler(adm_reg, commands=["addadmin"], state="*", is_admin=True)
    dp.register_message_handler(adm_del, commands=["deladmin"], state="*", is_admin=True)
    dp.register_message_handler(adm_info, commands=["admins"], state="*", is_admin=True)
    dp.register_message_handler(user_reg, commands=["reg"], state="*", is_admin=True)
    dp.register_message_handler(user_info, commands=["info"], state="*", is_admin=True)
    dp.register_message_handler(send_inn, commands=["sendinn"], state="*", is_admin=True)
    dp.register_message_handler(info_inn, commands=["inns"], state="*", is_admin=True)
    dp.register_message_handler(send_adm, commands=["sendadm"], state="*", is_admin=True)
    dp.register_message_handler(send_all, commands=["sendall"], state="*", is_admin=True)
    dp.register_message_handler(scan_doc, content_types=[types.ContentType.DOCUMENT], is_admin=True)
    dp.register_message_handler(help, commands=["help"], state="*", is_admin=True)
