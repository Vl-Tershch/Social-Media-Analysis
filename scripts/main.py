import vk_api
import secret

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
    cur_response = []
    offs = 0
    cur_response = vk.wall.get(owner_id=owner_id, offset=offs, count=100)
    all_posts = cur_response.get('count')
    rez_responce.extend(cur_response.get('items'))
    offs += 101

    while offs < 10000:
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

