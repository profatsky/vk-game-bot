import aiomysql


class DataBaseError(Exception):
    def __init__(self, text):
        self.text = text


class DataBase:
    def __init__(self, host: str = None, port: int = 3336, user: str = None, password: str = None, db: str = None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db

    async def request(self, request: str, types='fetchone', size: int = 1):

        pool = None
        try:
            pool = await aiomysql.create_pool(host=self.host, port=self.port,
                                              user=self.user, password=self.password,
                                              db=self.db)
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    result = await cur.execute(request)
                    await conn.commit()
                    if types == 'fetchone':
                        data = await cur.fetchone()
                        if data:
                            return dict(zip(tuple(map(lambda x: x[0], cur.description)), data))
                    elif types == 'fetchall':
                        data = await cur.fetchall()
                        return tuple(dict(zip(tuple(map(lambda x: x[0], cur.description)), item)) for item in data)
                    elif types == 'result':
                        return result
                    elif types == 'fetchmany':
                        data = await cur.fetchmany(size)
                        return tuple(dict(zip(tuple(map(lambda x: x[0], cur.description)), item)) for item in data)
                    else:
                        raise DataBaseError(f"{type} not found")
        except aiomysql.OperationalError as e:
            if e.args[0] == 2003:
                raise DataBaseError(f"Ошибка подключения к Базе Данных")
        finally:
            if pool:
                pool.close()
                await pool.wait_closed()
