from src.utils.query_runner import QueryRunner

class TownRepository:

    @staticmethod
    async def create(town_id:str,town_name:str,city_id:str,city_name:str,state_id:int):
        try:
            query = 'SELECT * FROM public.insert_town(:town_id, :town_name, :city_id, :city_name, :state_id)'
            result = await QueryRunner.execute_query(query=query,town_id=town_id,
                town_name=town_name,city_id=city_id,city_name=city_name,state_id=state_id)
            return result['insert_town']
        except Exception as e:
            raise e

    @staticmethod
    async def read(town_names:list,city_names:list,limit:int,skip:int):
        try:
            query = 'SELECT * FROM public.read_town(:town_names, :city_names, :limit, :skip)'
            result = await QueryRunner.execute_query(query=query,town_names=town_names,city_names=city_names,limit=limit,skip=skip)
            return result['read_town']
        except Exception as e:
            raise e
    
    @staticmethod
    async def update(id:int,town_id:str,town_name:str,city_id:str,city_name:str,state_id:int):
        try:
            query = 'SELECT * FROM public.update_town(:id, :town_id, :town_name, :city_id, :city_name, :state_id)'
            result = await QueryRunner.execute_query(query=query,id=id,town_id=town_id,
                town_name=town_name,city_id=city_id,city_name=city_name,state_id=state_id)
            return result['update_town']
        except Exception as e:
            raise e
    
    @staticmethod
    async def delete(id:int):
        try:
            query = 'SELECT * FROM public.delete_town(:id)'
            result = await QueryRunner.execute_query(query=query,id=id)
            return result['delete_town']
        except Exception as e:
            raise e