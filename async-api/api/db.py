import psycopg2
from aiopg.sa import create_engine
from sqlalchemy.sql.ddl import CreateTable, DropTable

from .model import Base


async def delete_tables(pg, tables):
    async with pg.acquire() as conn:
        for table in reversed(tables):
            drop_expr = DropTable(table)
            try:
                await conn.execute(drop_expr)
            except psycopg2.ProgrammingError:
                pass


async def prepare_tables(pg):
    tables = Base.metadata.tables.values()
    await delete_tables(pg, tables)
    async with pg.acquire() as conn:
        for table in tables:
            create_expr = CreateTable(table)
            await conn.execute(create_expr)


async def create_aiopg(app):
    app['pg_engine'] = await create_engine(
        user='postgres',
        database='async',
        host='db',
        port=5432,
        password='postgres'
    )
    await prepare_tables(app['pg_engine'])


async def dispose_aiopg(app):
    app['pg_engine'].close()
    await app['pg_engine'].wait_closed()
