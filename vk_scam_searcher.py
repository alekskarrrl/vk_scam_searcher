import json
from pprint import pprint
import requests
import config
import time
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("APP_ID")
SOURCE_ID = os.getenv("SOURCE_ID")
ORIGIN_OWNER_ID = os.getenv("ORIGIN_OWNER_ID")
ORIGIN_OWNER_FIRST_NAME = os.getenv("ORIGIN_OWNER_FIRST_NAME")
ORIGIN_OWNER_LAST_NAME = os.getenv("ORIGIN_OWNER_LAST_NAME")
APP_TOKEN = os.getenv("APP_TOKEN")
TLG_BOT_TOKEN = os.getenv("TLG_BOT_TOKEN")
BOT_CHAT_ID = os.getenv("BOT_CHAT_ID")


class TelegramBot:
    api_base_url = "https://api.telegram.org/bot"

    def __init__(self, token, chat_id, api_base_url=api_base_url):
        self.__token = token
        self.__chat_id = chat_id
        self.__api_base_url = api_base_url

    @property
    def token(self):
        return self.__token

    @property
    def chat_id(self):
        return self.__chat_id

    @property
    def api_base_url(self):
        return self.__api_base_url

    def telegram_bot_sendtext(self, text):
        request_url = "".join([self.__api_base_url,
                               self.__token,
                               '/sendMessage?chat_id=',
                               self.__chat_id,
                               '&parse_mode=None&text=',
                               text])
        try:
            response = requests.get(request_url).json()
            return response
        except requests.exceptions.RequestException as e:
            print(e)


class VKUser:

    def __init__(self, user_id, first_name, last_name):
        self.__user_id = user_id
        self.__first_name = first_name
        self.__last_name = last_name

    @property
    def user_id(self):
        return self.__user_id

    @property
    def first_name(self):
        return self.__first_name

    @property
    def last_name(self):
        return self.__last_name

    def __eq__(self, other):
        if self.__user_id == other.user_id:
            return True
        else:
            return False

    def __str__(self):
        return f"id: {self.user_id}, first_name: {self.first_name}, last_name: {self.last_name}"

    def __hash__(self):
        return hash((self.user_id, self.first_name, self.last_name))

    def is_similar_user(self, some_user):
        if ((self.__last_name.lower() in some_user.last_name.lower()
                    and self.__first_name.lower() in some_user.first_name.lower())
                or (self.__last_name.lower() in some_user.first_name.lower()
                    and self.__first_name.lower() in some_user.last_name.lower())):
            return True


# may be personal account or vk group
class VKSource:
    def __init__(self, account_id):
        self.__account_id = account_id

    @property
    def account_id(self):
        return self.__account_id

    def get_last_posts(self, post_count):
        param = {'access_token': APP_TOKEN, 'v': 5.131, 'owner_id': self.account_id, 'count': post_count}
        try:
            request = requests.get(url='https://api.vk.com/method/wall.get', params=param)
            response = request.json()
        except requests.exceptions.RequestException as e:
            print("get_last_posts - request failed - ", e)
        else:
            try:
                post_ids = [item['id'] for item in response['response']['items']]
            except KeyError as e:
                print("get_last_posts - KeyError - ", e)
            else:
                return post_ids

    def get_post_likes(self, post_id):
        likes_params = {'access_token': APP_TOKEN, 'v': 5.131, 'owner_id': self.account_id, 'type': 'post',
                        'item_id': post_id, 'extended': 1}
        try:
            likes_request = requests.get(url='https://api.vk.com/method/likes.getList', params=likes_params)
            response = likes_request.json()
        except requests.exceptions.RequestException as e:
            print("get_post_likes - request failed - ", e)
        else:
            try:
                users = [VKUser(user['id'], user['first_name'], user['last_name']) for user in
                         response['response']['items'] if 'deactivated' not in user.keys()]
            except KeyError as e:
                print("get_post_likes - KeyError - ", e)
            else:
                return users



def main():

    tg_bot = TelegramBot(TLG_BOT_TOKEN, '281231111')
    fake_history = []
    source_id = SOURCE_ID
    source = VKSource(source_id)
    origin_owner = VKUser(ORIGIN_OWNER_ID, ORIGIN_OWNER_FIRST_NAME, ORIGIN_OWNER_LAST_NAME)
    while True:
        fakes_list = []
        # Получаем последние 10 постов аккаунта
        last_posts_ids = source.get_last_posts(10)
        print("Owner id: ", source_id)

        # Под каждым постом смотрим лайки и отбираем аккаунты, похожие на оригинал
        for item in last_posts_ids:
            print(item)
            likes = source.get_post_likes(item)
            print(*likes)
            similar_users = [like for like in likes if (origin_owner.is_similar_user(like) and origin_owner != like)]
            fakes_list.extend(similar_users)
            time.sleep(1)

        # Отберем только уникальные аккаунты из фейков
        fakes_list = list(set(fakes_list))
        print("#########  Not blocked fake ##############", datetime.datetime.now())
        print(*fakes_list)
        print(len(fakes_list))

        new_to_block = []
        for item in fakes_list:
            if item not in fake_history:
                new_to_block.append(item)
                fake_history.append(item)

        if len(new_to_block) > 0:
            for item in new_to_block:
                acc_link = f"http://vk.com/id{item.user_id}"
                tg_bot.telegram_bot_sendtext(acc_link)

        time.sleep(60 * 15)












if __name__ == '__main__':
    main()

