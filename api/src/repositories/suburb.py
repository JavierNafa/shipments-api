from src.utils.query_runner import QueryRunner

class SuburbRepository:

    @staticmethod
    async def create(unique_suburb_town_id:str,name:str,postal_code:int,postal_code_administration:int,postal_code_office:int,
        cp:str,code_type:str,type_:str,zone:str,town_id:int):
        try:
            query = '''SELECT * FROM public.insert_suburb(:unique_suburb_town_id, :name, :postal_code, 
                :postal_code_administration, :postal_code_office, :cp, :code_type, :type_, :zone, :town_id)'''
            result = await QueryRunner.execute_query(query=query,unique_suburb_town_id=unique_suburb_town_id,
                name=name,postal_code=postal_code,postal_code_administration=postal_code_administration,
                postal_code_office=postal_code_office,cp=cp,code_type=code_type,type_=type_,zone=zone,town_id=town_id)
            return result['insert_suburb']
        except Exception as e:
            raise e

    @staticmethod
    async def read(postal_codes:list,names:list,limit:int,skip:int):
        try:
            query = 'SELECT * FROM public.read_suburb(:postal_codes, :names, :limit, :skip)'
            result = await QueryRunner.execute_query(query=query,postal_codes=postal_codes,names=names,limit=limit,skip=skip)
            return result['read_suburb']
        except Exception as e:
            raise e
    
    @staticmethod
    async def update(id:int,unique_suburb_town_id:str,name:str,postal_code:int,postal_code_administration:int,postal_code_office:int,
        cp:str,code_type:str,type_:str,zone:str,town_id:int):
        try:
            query = '''SELECT * FROM public.update_suburb(:id, :unique_suburb_town_id, :name, :postal_code, 
                :postal_code_administration, :postal_code_office, :cp, :code_type, :type_, :zone, :town_id)'''
            result = await QueryRunner.execute_query(query=query,id=id,unique_suburb_town_id=unique_suburb_town_id,
                name=name,postal_code=postal_code,postal_code_administration=postal_code_administration,
                postal_code_office=postal_code_office,cp=cp,code_type=code_type,type_=type_,zone=zone,town_id=town_id)
            return result['update_suburb']
        except Exception as e:
            raise e
    
    @staticmethod
    async def delete(id:int):
        try:
            query = 'SELECT * FROM public.delete_suburb(:id)'
            result = await QueryRunner.execute_query(query=query,id=id)
            return result['delete_suburb']
        except Exception as e:
            raise e