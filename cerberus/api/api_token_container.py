from os.path import exists
import secrets
import hashlib
import pickle

class APITokenContainer:
    __api_tokens: dict = {}

    def __init__(self):
        if not exists('api_tokens.pkl'):
            self.__save()

        self.__load()

        # print(self.__api_tokens)

    def __add(self, name: str, prefix: str, hash: str) -> None:
        self.__api_tokens[hash] = {
            'name': name,
            'prefix': prefix,
            'hash': hash
        }

        self.__save()

    def remove(self, name: str) -> None:
        hash_dict = self.__get_hash_dict_by_name(name)

        if hash_dict is not None:
            self.__api_tokens.pop(hash_dict['hash'])
            self.__save()
            print('API Token \'%s\' removed' % (name))
        else:
            print('API Token \'%s\' does not exist' % (name))

    def __get_hash_dict_by_name(self, name: str) -> dict:
        for key in self.__api_tokens:
            if self.__api_tokens[key]['name'] == name:
                return self.__api_tokens[key]
        
        return None

    def __save(self) -> None:
        with open('api_tokens.pkl', 'wb') as api_tokens_file:
            pickle.dump(self.__api_tokens, api_tokens_file)

    def __load(self) -> None:
        with open('api_tokens.pkl', 'rb') as api_tokens_file:
            self.__api_tokens = pickle.load(api_tokens_file)

    def check(self, api_token: str) -> bool:
        hash = self.__create_hash(api_token)
        return self.__check_hash(hash)

    def __check_hash(self, hash: str) -> bool:
        return hash in self.__api_tokens

    def __create_hash(self, api_token: str) -> str:
        m = hashlib.sha256()
        m.update(bytes(api_token, encoding='utf8'))
        return m.hexdigest()

    def __generate_token(self) -> str:
        prefix: str = secrets.token_urlsafe(27)
        content: str = secrets.token_urlsafe(109)
        return [prefix, '%s.%s' % (prefix, content)]

    def generate(self, name: str) -> list[str]:
        existing_hash_dict = self.__get_hash_dict_by_name(name)

        if existing_hash_dict is None:
            prefix, api_token = self.__generate_token()
            hash = self.__create_hash(api_token)
            self.__add(name, prefix, hash)
            print('API Token \'%s\' saved: %s' % (name, api_token))
        else:
            print('API Token \'%s\' already exists' % (name))

    def list(self) -> None:
        for key in self.__api_tokens:
            hash_dict = self.__api_tokens[key]
            print('%s\t %s | %s' % (hash_dict['name'], hash_dict['prefix'], hash_dict['hash']))
        
    

    