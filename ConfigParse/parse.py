#coding:utf8
"""
解析数据库配置信息
"""
import configparser
import os



# config file
mysql_file = os.path.join(os.path.dirname(__file__), "./_mysql.ini")



class Config:
    def __init__(self, filename):
        # create parser object
        self.parser = configparser.ConfigParser()
        self.read(filename)

    def read(self, filename):
        """解析出配置信息

        解析指定文件中的配置信息
        """
        # check file existed
        if not os.path.exists(filename):
            raise FileNotFoundError(f"{filename} doesn't exist")

        self.parser.read(filename)


    @property
    def mysql(self):
        """MySQL 配置信息
        """
        if not self.parser.has_section("mysql"):
            raise LookupError("There is not mysql Secton in configuration")

        config = {key: self.parser.get("mysql", key) for key in \
            self.parser.options("mysql")}
        
        return config

    @mysql.setter
    def mysql(self, key, value):
        """MySQL 配置信息设置

        不允许修改原始配置信息
        """

        NotImplemented
