"""GEF CORE RUNNER"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import ee
import os
import logging

from google.oauth2 import service_account

from gefcore.loggers import get_logger_by_env
from gefcore.api import patch_execution

logging.basicConfig(
    level='DEBUG',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y%m%d-%H:%M%p',
)

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV = os.getenv('ENV')

logging.info('Authenticating earth engine')
# gee_credentials = service_account.Credentials.from_service_account_file(
#     os.path.join(PROJECT_DIR, 'service_account.json'),
#     scopes = ee.oauth.SCOPES
# )
gee_credentials = ee.ServiceAccountCredentials(
    email=None,
    key_file=os.path.join(PROJECT_DIR, 'service_account.json')
)
ee.Initialize(gee_credentials)

def change_status_ticket(status):
    """Ticket status changer"""
    if ENV != 'dev':
        patch_execution(json={"status": status})
    else:
        logging.info('Channing to RUNNING')

def send_result(results):
    """Results sender"""
    if ENV != 'dev':
        patch_execution(json={"results": results, "status": "FINISHED"})
    else:
        logging.info('Finished -> Results:')
        logging.info(results)


def run(params):
    """Runs the user script"""
    try:
        logging.debug('Creating logger')
        # Getting logger
        logger = get_logger_by_env()
        change_status_ticket('RUNNING')  # running
        params['ENV'] = os.getenv('ENV', None)
        params['EXECUTION_ID'] = os.getenv('EXECUTION_ID', None)
        from gefcore.script import main
        result = main.run(params, logger)
        send_result(result)
    except Exception as error:
        change_status_ticket('FAILED')  # failed
        logger.error(str(error))
        raise error
