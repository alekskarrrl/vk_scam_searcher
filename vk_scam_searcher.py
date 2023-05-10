import requests
import time
import datetime
import os
from dotenv import load_dotenv
from VKUser import VKUser
from VKSource import VKSource
from TelegramBot import TelegramBot

load_dotenv()

SOURCE_ID = os.getenv("SOURCE_ID")
ORIGIN_OWNER_ID = os.getenv("ORIGIN_OWNER_ID")
ORIGIN_OWNER_FIRST_NAME = os.getenv("ORIGIN_OWNER_FIRST_NAME")
ORIGIN_OWNER_LAST_NAME = os.getenv("ORIGIN_OWNER_LAST_NAME")
APP_TOKEN = os.getenv("APP_TOKEN")
TLG_BOT_TOKEN = os.getenv("TLG_BOT_TOKEN")
BOT_CHAT_ID = os.getenv("BOT_CHAT_ID")


def main():

    tg_bot = TelegramBot(TLG_BOT_TOKEN, BOT_CHAT_ID)
    fake_history = []
    source_id = SOURCE_ID
    source = VKSource(source_id, APP_TOKEN)
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
                print(acc_link)

        if len(fakes_list) == 0:
            fake_history.clear()

        time.sleep(60 * 15)


if __name__ == '__main__':
    main()

