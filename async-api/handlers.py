import json
from json.decoder import JSONDecodeError

import sqlalchemy as sa
from aiohttp import web
from api.model import User, Product


async def get_user(request):
    db = request.app['pg_engine']
    user_id = request.match_info['id']
    async with db.acquire() as conn:
        async for row in conn.execute(sa.select([User]).where(User.id == user_id)):
            user = dict(row)

    return web.json_response(user)


async def get_product(request):
    db = request.app['pg_engine']
    product_id = request.match_info['id']
    async with db.acquire() as conn:
        async for row in conn.execute(sa.select([Product]).where(Product.id == product_id)):
            product = dict(row)

    return web.Response(text=json.dumps(product, default=str))


async def post_user(request):
    user = User.__table__
    db = request.app['pg_engine']
    try:
        data = await request.json()
    except JSONDecodeError:
        text = await request.text()
        return web.json_response({'error': f'bad json {text}'})

    async with db.acquire() as conn:
        async for row in conn.execute(user.insert().values(data)):
            return web.json_response({'user_id': row[0]})


async def post_product(request):
    product = Product.__table__
    db = request.app['pg_engine']
    try:
        data = await request.json()
    except JSONDecodeError:
        text = await request.text()
        return web.json_response({'error': f'bad json {text}'})

    async with db.acquire() as conn:
        async for row in conn.execute(product.insert().values(data)):
            return web.json_response({'product_id': row[0]})


async def index(request):
    return web.Response(body="Main page")
