
import pymysql.cursors
import discord, json
from decimal import Decimal

MIN_CONFIRMATIONS_FOR_DEPOSIT = 2


class Mysql:
    """
    Singleton helper for complex database methods
    """
    instance = None

    def __init__(self):
        if not Mysql.instance:
            Mysql.instance = Mysql.__Mysql()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    class __Mysql:
        def __init__(self):
            cfg_file = open('config.json', 'r', encoding="UTF-8").read()
            cfg = json.loads(cfg_file)
            self.__host = cfg['mysql']['host']
            self.__port = 3306
            self.__db_user = cfg['mysql']['user']
            self.__db_pass = cfg['mysql']['pass']
            self.__db = cfg['mysql']['database']
            self.__connected = 1
            self.__setup_connection()

        def __setup_connection(self):
            self.__connection = pymysql.connect(
                host=self.__host,
                port=self.__port,
                user=self.__db_user,
                password=self.__db_pass,
                db=self.__db)

        def __setup_cursor(self, cur_type):
            # ping the server and reset the connection if it is down
            self.__connection.ping(True)
            return self.__connection.cursor(cur_type)

        def add_history(self, nitro_code, code, message, server_id, server_name, member_id, member_name, is_success, date):
            cursor = self.__setup_cursor(
                pymysql.cursors.DictCursor)
            to_exec = "INSERT INTO history (nitro_code, code, message, server_id, server_name, member_id, member_name, is_success, date) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(
                to_exec, (str(nitro_code), code, str(message), int(server_id), str(server_name), int(member_id), str(member_name), int(is_success), str(date)))
            cursor.close()
            self.__connection.commit()
