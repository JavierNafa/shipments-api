from sqlalchemy.sql import text
from src.database.shipments import DatabaseShipments

class QueryRunner:

    @staticmethod
    async def execute_query(query:str,**params):
        try:
            result = await DatabaseShipments.session.execute(text(query),params)
            await DatabaseShipments.session.commit()
            return dict(result.fetchone())
        except Exception as e:
            await DatabaseShipments.session.rollback()
            raise e