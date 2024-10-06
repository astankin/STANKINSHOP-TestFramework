import configparser
import os

config = configparser.RawConfigParser()
config.read(os.path.abspath(os.curdir) + '\\configurations\\config.ini')


class ReadConfig:
    @staticmethod
    def get_application_url():
        url = config.get('commonInfo', 'base_url')
        return url

    @staticmethod
    def get_password():
        password = config.get('commonInfo', 'password')
        return password

    @staticmethod
    def get_email():
        email = config.get('commonInfo', 'email')
        return email

    @staticmethod
    def get_name():
        name = config.get('commonInfo', 'name')
        return name

    @staticmethod
    def get_chars_list():
        chars = config.get('commonInfo', 'chars').split(', ')
        return chars

    @staticmethod
    def get_common_passwords_list():
        common_passwords = config.get('commonInfo', 'common_passwords').split(', ')
        return common_passwords




