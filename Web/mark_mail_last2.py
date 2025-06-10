import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# Конфигурация
ZIMBRA_API_URL = 'https://mail.rfdyn.ru/service/soap'
USERNAME = 'georgii.kostin'
PASSWORD = 'GEBXMOKHWJVIVUKZ'
TARGET_SENDERS = ["polina.tsvetkova"]  # Список адресатов
DAYS_BACK = 7  # Период в днях

# Получение токена авторизации
def get_auth_token():
    body = f"""
    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
      <soap:Body>
        <AuthRequest xmlns="urn:zimbraAccount">
          <account by="name">{USERNAME}</account>
          <password>{PASSWORD}</password>
        </AuthRequest>
      </soap:Body>
    </soap:Envelope>
    """
    headers = {'Content-Type': 'application/soap+xml'}
    response = requests.post(ZIMBRA_API_URL, data=body, headers=headers)
    root = ET.fromstring(response.content)
    token = root.find('.//{urn:zimbraAccount}authToken').text
    return token

# Получение списка всех тредов

def get_threads(auth_token):
    since = int((datetime.now() - timedelta(days=DAYS_BACK)).timestamp() * 1000)
    headers = {'Content-Type': 'application/soap+xml', 'Authorization': f'ZM_AUTH_TOKEN {auth_token}'}
    body = f"""
    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
      <soap:Body>
        <SearchRequest xmlns="urn:zimbraMail" types="conversation" limit="1000">
          <query>in:inbox after:{since}</query>
        </SearchRequest>
      </soap:Body>
    </soap:Envelope>
    """
    response = requests.post(ZIMBRA_API_URL, data=body, headers=headers)
    root = ET.fromstring(response.content)
    return root.findall('.//{urn:zimbraMail}c')

# Получение сообщений внутри треда

def get_messages_in_thread(auth_token, thread_id):
    headers = {'Content-Type': 'application/soap+xml', 'Authorization': f'ZM_AUTH_TOKEN {auth_token}'}
    body = f"""
    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
      <soap:Body>
        <GetConversationRequest xmlns="urn:zimbraMail" id="{thread_id}" />
      </soap:Body>
    </soap:Envelope>
    """
    response = requests.post(ZIMBRA_API_URL, data=body, headers=headers)
    root = ET.fromstring(response.content)
    return root.findall('.//{urn:zimbraMail}m')

# Пометка треда (например, тегом)

def tag_thread(auth_token, thread_id, tag_name='TargetSenderLast'):
    headers = {'Content-Type': 'application/soap+xml', 'Authorization': f'ZM_AUTH_TOKEN {auth_token}'}
    # Создаём тег (можно один раз вне цикла)
    body_create_tag = f"""
    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
      <soap:Body>
        <CreateTagRequest xmlns="urn:zimbraMail">
          <tag name="{tag_name}" color="1"/>
        </CreateTagRequest>
      </soap:Body>
    </soap:Envelope>
    """
    requests.post(ZIMBRA_API_URL, data=body_create_tag, headers=headers)

    # Назначаем тег треду
    body_tag = f"""
    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
      <soap:Body>
        <ItemActionRequest xmlns="urn:zimbraMail">
          <action id="{thread_id}" op="tag" tag="{tag_name}"/>
        </ItemActionRequest>
      </soap:Body>
    </soap:Envelope>
    """
    requests.post(ZIMBRA_API_URL, data=body_tag, headers=headers)

# Основная логика

def main():
    token = get_auth_token()
    threads = get_threads(token)

    for thread in threads:
        thread_id = thread.attrib['id']
        messages = get_messages_in_thread(token, thread_id)
        if not messages:
            continue
        last_msg = max(messages, key=lambda m: int(m.attrib['d']))
        msg_xml = ET.tostring(last_msg).decode()
        if any(sender in msg_xml for sender in TARGET_SENDERS):
            tag_thread(token, thread_id)
            print(f"Thread {thread_id} tagged.")

if __name__ == '__main__':
    main()
