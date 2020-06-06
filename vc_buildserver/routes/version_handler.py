# Import In-Built Modules
import asyncio
import datetime
import json
import logging
from typing import Any
from typing import AsyncIterator
from typing import Awaitable
from typing import Callable
from typing import Dict

from aiohttp import web
from aiohttp.web import json_response
from aiohttp.web import Response
from aiohttp_apispec import (
    docs,
)

log = logging.getLogger(__name__)
tags = ['Version Handler Routes']
# Route definition table
routes = web.RouteTableDef()


async def init_version_routes(app, prefix):
    """

    :param app:
    :param prefix:
    :return:
    """
    try:
        app.router.add_get(
            prefix + '/{product}/version/latest', get_latest_version, name='get_latest_version',
        )
        app.router.add_get(
            prefix + '/{product}/version', get_all_version, name='get_all_version'
        )
        app.router.add_post('/{product}/version', new_version, name='new_version')

    except Exception as e:
        log.error(f'Error is {e}')
        raise

@docs(tags=tags, summary='Get the latest Version')
def get_latest_version(request):
    """
    Get the latest Version info from the Mongo DB
    :param request:
    :return:
    """
    version = ''
    try:
        product = request.match_info['product']
        _branch_header = request.query.get('BRANCH', 'master')
        log.info('Getting the latest Version... from branch {}'.format(
            _branch_header,
        ))

        log.info('Latest Version - {}'.format(version))
    except Exception as e:
        log.error('get_latest_version Error - {}'.format(e))
    finally:
        return json_response(version)


@docs(tags=tags, summary='Get the all the Version info from the Mongo DB which is specific to a branch')
def get_all_version(request):
    """
    Get the all the Version info from the Mongo DB which is specific to a branch
    :param request:
    :return:
    """
    version = ''
    try:
        product = request.match_info['product']
        _branch_header = request.query.get('BRANCH', 'master')
        log.info('Getting the all the Version... from branch {}'.format(
            _branch_header,
        ))

        log.info('Return all version {}'.format(version))
    except Exception as e:
        log.error('get_all_version Error - {}'.format(e))
    finally:
        return Response(text=str(version))


@docs(tags=tags, summary='Get the component versions of specific fw version - branch has to be mentioned in headers')
def get_specific_version(request):
    """
    Get the component versions of specific fw version - branch has to be mentioned in headers
    :param request:
    :return:
    """
    version = ''
    try:
        product = request.match_info['product']
        id = request.match_info['id']

        _branch_header = request.query.get('BRANCH', 'master')
        log.info('Getting a {} from {} Version... from branch {}'.format(
            id, product, _branch_header,
        ))

        log.info('Return Specific version {}'.format(version))
    except Exception as e:
        log.error('get_specific_version Error - '.format(e))
    finally:
        return Response(text=str(version))


@docs(tags=tags, summary='Get the New version. either appending the existing version if nothing is specified else use what is mentioned the body')
async def new_version(request):
    """
    Get the New version. either appending the existing version if nothing is specified else
    use what is mentioned the body
    :param request:
    :return:
    """

    product = request.match_info['product']
    _branch_header = request.query.get('BRANCH', 'master')
    log.info(
        'Getting a New Version...from - branch {} - product {}'.format(
            _branch_header, product,
        ),
    )
    data = dict()
    id = None
    try:
        if request.content_length:
            _req_data = await request.read()
            new_version_dict = json.loads(_req_data)
            log.info('Before inserting new version - {}'.format(new_version_dict))
            new_version_dict['timestamp'] = str(datetime.datetime.now())
            new_version_dict['branch'] = str(_branch_header)
            id = new_version_dict['_id']
            log.info('After inserting new version - {}'.format(data))
        else:
            log.info('Incrementing new version using bump version logic....')

            _temp_version = data.split('.')
            log.info('New Version No {}'.format(_temp_version))
            _temp_version[2] = str(int(_temp_version[2]) + 1)
            _version = '.'.join(_temp_version)

            # Add timestamp, new version and branch into the new version dictionary
            new_version_data = {
                '_id': _version,
                'timestamp': str(datetime.datetime.now()),
                'branch': _branch_header,
            }

            log.info('Incremented new version - {}'.format(data))
            id = _version
    except Exception as e:
        log.error('new_version branch - {} - Error - {}'.
                  format(_branch_header, e))
    finally:
        return Response(text=str(id))


@docs(tags=tags, summary='Update the component versions into the existing new version')
def update_version(request):
    """
    Update the component versions into the existing new version
    :param request:
    :return:
    """
    version = dict()
    # Read the product and id info that has to be updated
    product = request.match_info['product']
    new_id = request.match_info['new_id']
    _branch_header = request.query.get('BRANCH', 'master')
    log.info('Updating the new Version {} with Components on branch {}...'.format(
        _branch_header, new_id,
    ))
    try:
        # Read the contents of POST message
        if request.content_length:
            _data = request.read()
            new_version_dict = json.loads(_data)
            # POST Get the version details from mongo DB

            log.info('Updated the new Version - {}'.format(version))
        else:
            log.error('Data is None, Need to pass the updated values')
    except Exception as e:
        log.error('update_version Error - {}'.format(e))
    finally:
        return json_response(version)


@docs(tags=tags, summary='Bulk update')
def bulk_update(request):
    """

    :param request:
    :return:
    """
    version = dict()
    # Read the product and id info that has to be updated
    product = request.match_info['product']
    log.info('bulk_update [reading directly from S3] ')
    # _branch_header = 'master' if not request.rel_url.query \
    #                     else request.rel_url.query['branch']
    try:
        # Read the contents of POST message
        if request.content_length:
            _data = request.read()
            new_version_dict = json.loads(_data)

            log.info('bulk_update to Mongo DB')
        else:
            log.error('update_many_data is None')
    except Exception as e:
        log.error('update_version - {}'.format(e))
    finally:
        return json_response(None)

@docs(tags=tags, summary='Remove all the versions from a collection specific to a branch')
def remove_all_versions(request):
    """
    Remove all the versions from a collection specific to a branch
    :param request:
    :return:
    """
    # Read the product and id info that has to be updated
    product = request.match_info['product']

    _branch_header = request.query.get('BRANCH', 'master')
    log.info(
        'remove_all_versions on product - {} branch {} started'.format(
            product, _branch_header,
        ),
    )

    try:
        log.info('remove_all_versions deleted')
    except Exception as e:
        log.error('remove_all_versions Error {}'.format(e))
    finally:
        return Response(text='remove_all_versions')
