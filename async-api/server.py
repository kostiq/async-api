from aiohttp import web
from api.db import create_aiopg, dispose_aiopg
from handlers import index, get_user, post_user, post_product, get_product

if __name__ == '__main__':
    app = web.Application()
    app.on_startup.append(create_aiopg)
    app.on_cleanup.append(dispose_aiopg)

    app.add_routes([
        web.get('/', index),
        web.get('/user/{id}', get_user),
        web.post('/user/', post_user),
        web.get('/product/{id}', get_product),
        web.post('/product/', post_product),
    ])

    web.run_app(app)
