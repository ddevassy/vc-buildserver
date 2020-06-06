# Import In-Built Modules
import datetime
import json
import logging
import pathlib
import asyncio
from typing import Awaitable
from typing import Callable
from aiohttp import web

import vc_buildserver.routes.version_handler as vh
import vc_buildserver.routes.product_handler as ph
from vc_buildserver.main.views import index

log = logging.getLogger(__name__)


PROJECT_PATH = pathlib.Path(__file__).parent.parent

# Route definition table
routes = web.RouteTableDef()
# Import In-Built Modules


async def init_routes(app: web.Application) -> None:
    """
    Initializing the Routes
    :param app:
    :return:
    """
    try:
        log.info(f'Initializing the routes')
        base_prefix = '/product'

        add_route = app.router.add_route
        add_route('*', '/', index, name='index')

        # added static dir
        app.router.add_static(
            '/static/',
            path=(PROJECT_PATH / 'static'),
            name='static',
        )
        await vh.init_version_routes(app, base_prefix)
        await ph.init_product_routes(app, base_prefix)

        # Updating the version server routes
        app.add_routes(routes)

    except Exception as e:
        log.error('init_routes Error {}'.format(e))


@web.middleware
async def error_middleware(
    request: web.Request,
    handler: Callable[[web.Request], Awaitable[web.StreamResponse]],
) -> web.StreamResponse:
    try:
        return await handler(request)
    except web.HTTPException:
        raise
    except asyncio.CancelledError:
        raise
    except Exception as ex:
        return web.json_response(
            {'status': 'failed', 'reason': str(ex)}, status=400,
        )

#
# @web.middleware
# async def database_handle_middleware(
#     request: web.Request,
#     handler: Callable[[web.Request], Awaitable[web.StreamResponse]],
# ) -> web.StreamResponse:
#     try:
#         return await handler(request)
#     except web.HTTPException:
#         raise
#     except asyncio.CancelledError:
#         raise
#     except Exception as ex:
#         return web.json_response(
#             {'status': 'failed', 'reason': str(ex)}, status=400,
#         )