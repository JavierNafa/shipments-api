from src.utils.query_runner import QueryRunner

class StateRepository():

    @staticmethod
    async def create(code:str,name:str):
        try:
            query = 'SELECT * FROM public.insert_state(:code, :name)'
            result = await QueryRunner.execute_query(query=query,code=code,name=name)
            return result['insert_state']
        except Exception as e:
            raise e

    @staticmethod
    async def read(names:list,limit:int,skip:int):
        try:
            query = 'SELECT * FROM public.read_state(:names, :limit, :skip)'
            result = await QueryRunner.execute_query(query=query,names=names,limit=limit,skip=skip)
            return result['read_state']
        except Exception as e:
            raise e
    
    @staticmethod
    async def update(id:int,code:str,name:str):
        try:
            query = 'SELECT * FROM public.update_state(:id, :code, :name)'
            result = await QueryRunner.execute_query(query=query,id=id,code=code,name=name)
            return result['update_state']
        except Exception as e:
            raise e
    
    @staticmethod
    async def delete(id:int):
        try:
            query = 'SELECT * FROM public.delete_state(:id)'
            result = await QueryRunner.execute_query(query=query,id=id)
            return result['delete_state']
        except Exception as e:
            raise e