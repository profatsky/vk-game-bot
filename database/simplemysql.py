import pymysql


class SimplePymysqlError(Exception):
    def __init__(self, text):
        self.text = text


class Pymysql:

    def __init__(self, host: str = None, port: int = 3336, user: str = None, password: str = None, db: str = None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db

    def request(self, request: str, types='fetchone', size: int = 1):

        connect = None
        try:
            connect = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                                      db=self.db, cursorclass=pymysql.cursors.DictCursor)
            with connect.cursor() as cursor:
                result = cursor.execute(request)
                if types == 'fetchone':
                    return cursor.fetchone()
                elif types == 'fetchall':
                    return cursor.fetchall()
                elif types == 'result':
                    return result
                elif types == 'fetchmany':
                    return cursor.fetchmany(size)
                else:
                    raise SimplePymysqlError(f"{type} not found")

        except pymysql.err.OperationalError as e:
            if e.args[0] == 2003:
                raise SimplePymysqlError(f"Ошибка подключения к Базе Данных")

        finally:
            if connect:
                connect.commit()
                connect.close()
