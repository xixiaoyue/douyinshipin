# -*- coding:utf-8 -*-
# 作者：thomas
# 日期：2023.11.23
# 文件名称：config.py

import configparser
import os


class Conf:
    def __init__(self, path="./config.ini",):
        self.conf = configparser.ConfigParser()
        # self.root_path = os.path.dirname(os.path.abspath(__file__))
        self.f = os.path.join( path)
        self.conf.read(self.f, encoding='utf-8')

    def read_sections(self):
        self.conf.sections()

    def read_options(self, sections_name):
        return self.conf.options(sections_name)

    def read_conf(self, sections_name, option_name):
        return self.conf.get(sections_name, option_name)

    def set_option(self, sections_name, option_name, value: str):
        self.conf.set(sections_name, option_name, value)
        self.conf.write(open(self.f, "w"))


Config = Conf()
if __name__ == "__main__":
    Config.read_sections()
    Config.read_options('config')
    print(Config.read_conf('config', 'open_ai_key'))
    Config.set_option('config', 'open_ai_key', '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')
