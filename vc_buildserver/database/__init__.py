# Import In-Built Modules
import logging
import pathlib

import aiopg.sa
import motor.motor_asyncio
from aiohttp import web
log = logging.getLogger(__name__)


async def init_pg(app: web.Application) -> None:
    '''
    A function that, when the server is started, connects to postgresql,
    and after stopping it breaks the connection (after yield)
    '''
    try:
        log.info(f'Initializing the PG database')
        config = app['config']['postgres']

        engine = await aiopg.sa.create_engine(**config)
        app['db'] = engine

        yield

        app['db'].close()
        await app['db'].wait_closed()
    except Exception as e:
        log.error(f'init_database {e}')
        raise e


async def init_mongodb(app: web.Application) -> None:
    '''

    :param app:
    :return:
    '''
    try:
        log.info(f'Initializing the MongoDB database')
        config = app['config']['mongodb']
        _url = construct_db_url(config)
        app['motor_db'] = motor.motor_asyncio.AsyncIOMotorClient(_url)
        log.info(f'Mongo URL - {app["motor_db"]}')
    except Exception as e:
        log.error(f'init_database {e}')
        raise e


def construct_db_url(config):
    '''

    mongodb://[username:password@]host1[:port1][,...hostN[:portN]][/[defaultauthdb][?options]]
    :param config:
    :return:
    '''
    return 'mongodb://{user}:{password}@{host}:{port}/{database}'.format(
        user=config['user'],
        password=config['password'],
        database=config['database'],
        host=config['host'],
        port=config['port'],
    )


def create_db(config):
    '''

    :param config:
    :return:
    '''
