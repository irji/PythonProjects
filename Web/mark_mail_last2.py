import imaplib
import email
from email.utils import parsedate_to_datetime
from datetime import datetime, timedelta

# Конфигурация
IMAP_SERVER = 'imap.your-zimbra-server.com'
USERNAME = 'your_username'
PASSWORD = 'your_password'
TARGET_SENDERS = ['target1@example.com', 'target2@example.com']
DAYS_BACK = 7
TAG = 'TargetSenderLast'

# Подключение к IMAP и выбор папки

def connect_to_imap():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(USERNAME, PASSWORD)
    mail.select('INBOX')
    return mail

# Поиск цепочек писем (тредов) не старше N дней

def search_recent_threads(mail):
    date_since = (datetime.now() - timedelta(days=DAYS_BACK)).strftime('%d-%b-%Y')
    result, data = mail.search(None, f'(SINCE {date_since})')
    if result != 'OK':
        print('Ошибка поиска писем')
        return []
    return data[0].split()

# Получение информации о письме

def fetch_email(mail, msg_id):
    result, data = mail.fetch(msg_id, '(RFC822)')
    if result != 'OK':
        return None
    msg = email.message_from_bytes(data[0][1])
    return msg

# Группировка по тредам с использованием заголовка "Message-ID" и "In-Reply-To"

def build_threads(mail, msg_ids):
    threads = {}
    msg_map = {}

    for msg_id in msg_ids:
        msg = fetch_email(mail, msg_id)
        if not msg:
            continue
        message_id = msg.get('Message-ID')
        in_reply_to = msg.get('In-Reply-To')
        msg_map[message_id] = (msg_id, msg)

        thread_key = in_reply_to if in_reply_to else message_id
        if thread_key not in threads:
            threads[thread_key] = []
        threads[thread_key].append((msg_id, msg))

    return threads

# Определение, от нужного ли отправителя последнее письмо в треде

def process_threads(mail, threads):
    for thread_key, msgs in threads.items():
        msgs_sorted = sorted(msgs, key=lambda m: parsedate_to_datetime(m[1]['Date']))
        last_msg = msgs_sorted[-1][1]
        sender = email.utils.parseaddr(last_msg.get('From'))[1]

        if sender in TARGET_SENDERS:
            print(f"Thread with last sender {sender} - tagged ({TAG})")
            # Здесь можно реализовать добавление тега или пометку письма флагом, если сервер поддерживает
            # Например: mail.store(msgs_sorted[-1][0], '+FLAGS', '\Flagged')

# Основная логика

def main():
    mail = connect_to_imap()
    msg_ids = search_recent_threads(mail)
    threads = build_threads(mail, msg_ids)
    process_threads(mail, threads)
    mail.logout()

if __name__ == '__main__':
    main()
