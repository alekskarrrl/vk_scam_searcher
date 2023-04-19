

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

