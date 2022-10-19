import vk_api
import emoji
import secret
import re
import string
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

# Функция для двухфакторной аутентификации
def auth_handler():
    # Код двухфакторной аутентификации
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True
    return key, remember_device

# Получение постов с личной стены
def get_personal_wall_posts(vk_session):
    vk = vk_session.get_api()
    response = vk.wall.get(count=1)
    if response['items']:
        print(response['items'][0])

# Получение опреденного количества постов со стены группы по id
def get_public_posts_by_count(vk_session, owner_id, count=100):
    vk = vk_session.get_api()
    response = vk.wall.get(owner_id=owner_id, count=count)
    print(response)

# Получение всех постов со стены группы по id
def get_public_posts_all(vk_session, owner_id):
    vk = vk_session.get_api()
    rez_responce =[]
    offs = 0
    cur_response = vk.wall.get(owner_id=owner_id, offset=offs, count=100)
    all_posts = cur_response.get('count')
    rez_responce.extend(cur_response.get('items'))
    offs += 101

    while offs < 2000: # изменить значение на all_posts
        print(offs)
        cur_response = vk.wall.get(owner_id=owner_id, offset=offs, count=100)
        rez_responce.extend(cur_response.get('items'))
        offs += 101
    return rez_responce

# Удаление всех рекламных постов
def posts_dataset(all_posts):
    for i in all_posts:
        if (i['marked_as_ads'] == 1):
            all_posts.remove(i)

# Нормализация текста
def text_preparation(dataset):
    rezult_text = []
    for i in dataset:
        cur_text = i['text']
        cur_text = emoji.replace_emoji(cur_text, ' ')                                       # Delete emoji
        cur_text = re.sub(r'^https?:\/\/.*[\r\n]*', '', cur_text, flags=re.MULTILINE)       # Delete links
        cur_text = re.sub(r'\S*@\S*\s?', '', cur_text, flags=re.MULTILINE)                  # Delete emails
        cur_text = cur_text.lower()                                                         # Lower text
        cur_text = cur_text.translate(str.maketrans('', '', string.punctuation))            # Delete punctuation
        cur_text = cur_text.translate(str.maketrans('', '', string.digits))                 # Delete digits
        cur_text = cur_text.strip()                                                         # Delete spaces
        rezult_text.append(cur_text)
    return rezult_text

# Лемматизация текста
def lemmatization(text):
    rez_words = {}
    for i in text:
        for j in i.split():
            p = morph.parse(j)[0]
            rez_words[p.normal_form] = rez_words.setdefault(p.normal_form, 0) + 1
    sort_words = sorted(rez_words.items(), key=lambda x: x[1], reverse=True)
    return sort_words

if __name__ == '__main__':
    vk_session = vk_api.VkApi(secret.login, secret.password, auth_handler=auth_handler)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)

    # get_personal_wall_posts(vk_session)
    print('---------------------------')
    # get_public_posts_by_count(vk_session, '-297836', 100)
    print('---------------------------')
    rez = get_public_posts_all(vk_session, '-297836')
    posts_dataset(rez)
    print(len(rez))
    rez_text = text_preparation(rez)
    rez_words = lemmatization(rez_text)
    print(rez_words)
