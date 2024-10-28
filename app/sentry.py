import os
import sentry_sdk
import logging
from sentry_sdk.integrations.logging import LoggingIntegration
from urllib.parse import urlparse

# SENTRY LOGGER
sentry_logging = LoggingIntegration(
    level=logging.INFO,
    event_level=logging.ERROR
)

IGNORED_ENDPOINTS = [
    "/",
    "/docs",
    "/openapi.json",
    "/redoc",
    "/favicon.ico",
]


def traces_sampler(sampling_context) -> float:
    path = None
    # sampling_context is a dictionary that contains the transaction and its context
    if 'asgi_scope' in sampling_context and 'path' in sampling_context['asgi_scope']:
        path = sampling_context['asgi_scope']['path']
    # Check if the transaction name is in the IGNORED_ENDPOINTS
    if path and path in IGNORED_ENDPOINTS:
        return 0  # None of these transactions will be sent
    else:
        return 1.0  # 100% of these transactions will be sent


def before_send(event, hint):
    # This function is called before an event is sent to Sentry.
    if 'request' in event and 'url' in event['request']:
        url_path = urlparse(event['request']['url']).path
        # Avoid event in IGNORED_ENDPOINTS
        if url_path in IGNORED_ENDPOINTS:
            return None
    return event


def before_send_transaction(transaction, hint):
    # This function is called before a transaction is sent to Sentry.
    transaction_name = transaction['name']
    # Avoid event in IGNORED_ENDPOINTS
    if transaction_name in IGNORED_ENDPOINTS:
        return None
    return transaction


def initialize_sentry():
    # avoid adding the env variables when working on local
    sentry_dashboard_url = os.environ.get('SENTRY_INGEST_URL', '').strip()
    sentry_enviroment = os.environ.get('SENTRY_ENVIRONMENT', '').strip()
    if sentry_dashboard_url and sentry_enviroment:
        sentry_sdk.init(
            dsn=sentry_dashboard_url,
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # traces_sample_rate=1.0,
            traces_sampler=traces_sampler,
            # Set profiles_sample_rate to 1.0 to profile 100%
            # of sampled transactions.
            # We recommend adjusting this value in production.
            # profiles_sample_rate=0.1,
            integrations=[sentry_logging],
            environment=sentry_enviroment,
            before_send=before_send,
            # before_send_transaction=before_send_transaction,
        )
        print("loggend in sentry env:{sentry_enviroment}, url={sentry_dashboard_url}".format(
            sentry_enviroment=sentry_enviroment, sentry_dashboard_url=sentry_dashboard_url))
    else:
        logging.warning("Sentry is not initialized")
