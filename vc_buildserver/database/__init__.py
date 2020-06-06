# Import In-Built Modules
import logging
import asyncio
import aiopg.sa
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from aiohttp import web
log = logging.getLogger(__name__)


async def init_pg(app: web.Application) -> None:
    """
    A function that, when the server is started, connects to postgresql,
    and after stopping it breaks the connection (after yield)
    """
    try:
        log.info(f'Initializing the PG database')
        config = app['config']['postgres']

        engine = await aiopg.sa.create_engine(**config)
        app['db'] = engine

        yield

        app['db'].close()
        await app['db'].wait_closed()
    except Exception as e:
        log.error(f'init_pg {e}')
        raise e


async def init_mongodb(app: web.Application) -> None:
    """
    Initializing the Mongo DB
    :param app:
    :return:
    """
    try:
        log.info(f'Initializing the MongoDB database Async & Sync Mongo DB')
        await asyncio.sleep(1)
        config = app['config']['mongodb']

        _url = await _construct_db_url(config)
        log.info(f'Mongo URL - {_url}')

        # Creating the Pymongo DB instance
        await _get_pymongo_instance(app, _url)

        # Creating the AsyncIOMotorClient DB instance
        await _get_asynciomotor_instance(app, _url)

    except Exception as e:
        log.error(f'init_mongodb {e}')
        raise e


async def _construct_db_url(config):
    """
    Construct the Mongo DB Url
    mongodb://[username:password@]host1[:port1][,...hostN[:portN]][/[defaultauthdb][?options]]
    :param config:
    :return:
    """
    return 'mongodb://{user}:{password}@{host}:{port}/{database}?authSource=admin'.format(
        user=config['user'],
        password=config['password'],
        database=config['database'],
        host=config['host'],
        port=config['port'],
    )


async def _get_asynciomotor_instance(app: web.Application, url) -> None:
    """
    Getting  Mongo Async-IO-motor instance for creating, updating, deleting Documents
    Async IO-motor wont support creating new collections
    :param app:
    :param url:
    :return:
    """
    try:
        log.info(f'Getting  Async-IO-motor instance')

        async_mongo_instance = dict()
        _cli = AsyncIOMotorClient(url)
        async_mongo_instance['client'] = _cli
        async_mongo_instance['db'] = _cli['versiondb']
        app['async_mongo'] = async_mongo_instance
        await asyncio.sleep(1)

    except Exception as e:
        log.error(f'_get_asynciomotor_instance {e}')
        raise e


async def _get_pymongo_instance(app: web.Application , url) -> None:
    """
    Getting  Mongo pymongo instance used for creating, updating, deleting collections
    Async IO-motor wont support creating new collections, Pymongo supports
    :param app:
    :param url:
    :return:
    """
    try:
        log.info(f'Getting pymongo instance')
        mongo_instance = dict()
        _cli = MongoClient(url)
        mongo_instance['client'] = _cli
        mongo_instance['db'] = _cli['versiondb']
        app['mongo'] = mongo_instance
        await asyncio.sleep(1)

    except Exception as e:

        log.error(f'_get_pymongo_instance {e}')
        raise e