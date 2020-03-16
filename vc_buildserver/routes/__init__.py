# Import In-Built Modules
import datetime
import json
import logging
import pathlib

from aiohttp import web
from aiohttp.web import json_response
from aiohttp.web import Response

import vc_buildserver.routes.version_handler as vh
from vc_buildserver.main.views import index

log = logging.getLogger(__name__)


PROJECT_PATH = pathlib.Path(__file__).parent.parent

# Route definition table
routes = web.RouteTableDef()
# Import In-Built Modules


async def init_routes(app: web.Application) -> None:
    try:
        log.info(f'Initializing the routes')
        base_prefix = '/product'
        add_route = app.router.add_route

        add_route('*', '/', index, name='index')
        app.router.add_get(
            base_prefix + '/{product}/version/latest', vh.get_latest_version, name='get_latest_version',
        )
        app.router.add_get(
            base_prefix + '/{product}/version', vh.get_all_version, name='get_all_version',
        )

        # added static dir
        app.router.add_static(
            '/static/',
            path=(PROJECT_PATH / 'static'),
            name='static',
        )

        # Route definition table
        routes = web.RouteTableDef()

        # Updating the version server routes
        app.add_routes(routes)

    except Exception as e:
        log.error('init_routes Error {}'.format(e))
