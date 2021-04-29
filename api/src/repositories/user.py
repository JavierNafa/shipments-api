from src.utils.query_runner import QueryRunner

class UserRepository:

    @staticmethod
    async def create(name:str,last_name:str,username:str,password:bytes):
        try:
            query = 'SELECT * FROM public.insert_user(:name, :last_name, :username, :password)'
            result = await QueryRunner.execute_query(query=query,name=name,last_name=last_name,username=username,password=password)
            return result['insert_user']
        except Exception as e:
            raise e

    @staticmethod
    async def read(username:str):
        try:
            query = 'SELECT * FROM public.read_user(:username)'
            result = await QueryRunner.execute_query(query=query,username=username)
            return result['read_user']
        except Exception as e:
            raise e