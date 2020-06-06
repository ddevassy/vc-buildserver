import logging
from pathlib import Path
from typing import List
from typing import Optional

import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp_apispec import docs
from aiohttp_apispec import request_schema
from aiohttp_apispec import setup_aiohttp_apispec

from .common.log_utils import _setup_logging
from vc_buildserver.database import init_mongodb
from vc_buildserver.database import init_pg
from vc_buildserver.routes import init_routes, error_middleware
from vc_buildserver.utils.common import init_config


log = logging.getLogger(__name__)
path = Path(__file__).parent


def init_jinja2(app: web.Application) -> None:
    '''
    Initialize jinja2 template for application.
    '''
    log.info(f'Initializing the jinja2 template')
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(str(path / 'templates')),
    )


async def init_app(config: Optional[List[str]] = None) -> web.Application:
    _setup_logging()
    log.info(f'Setting up init_app Logging')
    app = web.Application(
        client_max_size=64 * 1024 ** 2, middlewares=[error_middleware]
    )
    # init docs with all parameters, usual for ApiSpec
    setup_aiohttp_apispec(
        app=app,
        title='VC Build Server Documentation',
        version='v1',
        url='/api/docs/swagger.json',
        swagger_path='/api/docs',
    )

    init_jinja2(app)
    init_config(app, config=config)
    await init_mongodb(app)
    await init_routes(app)
    app.cleanup_ctx.extend([
        init_pg,
    ])

    return app
