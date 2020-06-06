# Import In-Built Modules
import asyncio
import datetime
import json
import logging


from aiohttp import web
from aiohttp.web import json_response
from aiohttp.web import Response
from aiohttp_apispec import (
    docs,
)

log = logging.getLogger(__name__)
tags = ['Product Handler Routes']
# Route definition table
routes = web.RouteTableDef()


async def init_product_routes(app, prefix):
    """

    :param app:
    :param prefix:
    :return:
    """
    try:
        app.router.add_put(
            prefix + '/{product}', create_new_product, name='create_new_product'
        )
        app.router.add_get(
            prefix, list_of_all_products, name='list_of_all_products'
        )
    except Exception as e:
        log.error(f'Error is {e}')
        raise e


@docs(tags=tags, summary='Create a New Product')
async def create_new_product(request):
    """
    Creating a New Product
    :param request:
    :return:
    """
    product = None
    try:
        await asyncio.sleep(1)
        product = request.match_info['product']
        log.info(f'Creating new Product {product}')

        _new_product = request.app['mongo']['db'][product]

        log.info(f'Created {_new_product} Mongo Collection')

    except Exception as e:
        log.error(f'Error is {e}')
        raise e

    finally:
        return json_response(product)


@docs(tags=tags, summary='list of All Product')
async def list_of_all_products(request):
    """

    :param request:
    :return:
    """
    try:
        await asyncio.sleep(1)
        _db = request.app['mongo']['db']
        names = _db.list_collection_names()
        log.info(f'Name of Collections {names} {_db}')

    except Exception as e:
        log.error(f'Error is {e}')
        raise e

    finally:
        return json_response({})