from imap_tools import MailBox, A
import datetime

# Настройки
EMAIL = "georgii.kostin@rfdyn.com"
PASSWORD = "GEBXMOKHWJVIVUKZ"
IMAP_SERVER = "mail.rfdyn.ru"  # Например: imap.gmail.com
TARGET_SENDER_LIST = {"konstantin.vorobev",
                      "polina.tsvetkova",
                      "german.nepotasov",
                      "dmitrii.bevzenko",
                      "olga.fedyaeva",
                      "dmitry.kliymenko",
                      "pavel.koryuzlov",
                      "andrey.spiridonov",
                      "aleksandr.timoshenko"}
TAG_NAME = "LastInThread"

dt_now = datetime.datetime.now()
since_dt = dt_now + datetime.timedelta(days=-7)

print(since_dt)

# Подключение к почте
with MailBox(IMAP_SERVER).login(EMAIL, PASSWORD) as mailbox:
    # Получаем все треды (группировка по заголовку 'Thread-Topic' или 'References')
    threads = {}
    msg_map = {}

    for f in mailbox.folder.list():
        # проходимся по всем папкам в ящике
        if str.__contains__(f.name, "INBOX"):
            mailbox.folder.set(f.name)

            # находим сообщения/цепочки начатые созданные за последнюю неделю
            for msg in mailbox.fetch(A(date_gte=since_dt.date())):
                #thread_id = msg.thread_id  # Или msg.references или msg.subject
                #thread_id = msg.headers.get('thread-index')

#                'in-reply-to'
#                '<1608023397.54051206.1748850774911.JavaMail.zimbra@rfdyn.com>'
#
#                'message-id'
#                '<996037314.54237093.1748858059457.JavaMail.zimbra@rfdyn.com>'
#
#                'references'
#                < AUXP273MB091156E0BEC235777AF2615AB562A @ AUXP273MB0911.AREP273.PROD.OUTLOOK.COM > < 1392893491.53990335
#                .1748847361114.JavaMail.zimbra @ rfdyn.com > < AUXP273MB0911AF8BD732CD7D4E3A13A6B562A @ AUXP273MB0911.AREP273.PROD.OUTLOOK.COM > < 1608023397.54051206
#                .1748850774911.JavaMail.zimbra @ rfdyn.com >

                thread_in_reply_to = msg.headers.get('in-reply-to')
                thread_reference = msg.headers.get('references')

                thread_id = msg.headers.get('thread-index')
                #threads.setdefault(thread_id, []).append(msg)

                #if thread_id != None:
                #    #print("{}  |  {}  |  {}  |  {}  |  {}".format(msg.subject, msg.date, thread_id, msg.headers.get('message-id'), thread_reference))
                #    print("{}  |  {}  |  {}  |  {}  |  {}".format(msg.subject, msg.date, thread_id,
                #                                                  msg.headers.get('message-id'), thread_in_reply_to))


                message_id = msg.headers.get('message-id')
                in_reply_to = msg.headers.get('in-reply-to')

                msg_map[message_id] = (message_id, msg)

                thread_key = in_reply_to if in_reply_to else message_id
                if thread_key not in threads:
                     threads[thread_key] = []
                threads[thread_key].append((message_id, msg))

            # Проверяем каждый тред
            for thread_id, messages in threads.items():
                # Сортируем письма по дате (последнее = самое новое)
                if len(messages) > 1:
                    last_msg2 = sorted(messages, key=lambda x: x.date, reverse=True)

                    last_msg = last_msg2[1]

                    for sender in TARGET_SENDER_LIST:
                    # Если последнее письмо от нужного отправителя
                        if str.__contains__(last_msg.from_, sender) == True:
                            print(f"В цепочке '{thread_id}' последнее письмо от {sender}")
                            # Добавляем метку (если поддерживается IMAP)
                            mailbox.flag(last_msg.uid, TAG_NAME, True)



# # Группировка по тредам с использованием заголовка "Message-ID" и "In-Reply-To"
#
# def build_threads(mail, msg_ids):
#     threads = {}
#     msg_map = {}
#
#     for msg_id in msg_ids:
#         msg = fetch_email(mail, msg_id)
#         if not msg:
#             continue
#         message_id = msg.get('Message-ID')
#         in_reply_to = msg.get('In-Reply-To')
#         msg_map[message_id] = (msg_id, msg)
#
#         thread_key = in_reply_to if in_reply_to else message_id
#         if thread_key not in threads:
#             threads[thread_key] = []
#         threads[thread_key].append((msg_id, msg))
#
#     return threads

