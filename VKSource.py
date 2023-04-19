import requests
from VKUser import VKUser


# may be personal account or vk group
class VKSource:
    def __init__(self, account_id, vk_token):
        self.__account_id = account_id
        self.__vk_token = vk_token

    @property
    def account_id(self):
        return self.__account_id

    def get_last_posts(self, post_count):
        param = {'access_token': self.__vk_token, 'v': 5.131, 'owner_id': self.account_id, 'count': post_count}
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
        likes_params = {'access_token': self.__vk_token, 'v': 5.131, 'owner_id': self.account_id, 'type': 'post',
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

