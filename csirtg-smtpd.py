import logging
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import textwrap
import os
import json
from pprint import pprint
import sys
import asyncio
from aiosmtpd.controller import Controller

from csirtgsdk.indicator import Indicator

USER = os.getenv('CSIRTG_USER', '')
FEED = os.getenv('CSIRTG_FEED', '')
TOKEN = os.getenv('CSIRTG_TOKEN', '')
PORT = os.getenv('SMTP_PORT', 2525)
PORT = int(PORT)

TRACE = os.getenv('TRACE', False)

# logging configuration
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s[%(lineno)s] - %(message)s'
logger = logging.getLogger(__name__)

if TRACE == '1':
    logger.setLevel(logging.DEBUG)


# https://aiosmtpd.readthedocs.io/en/latest/aiosmtpd/docs/controller.html
class SinkholeHandler:

    def _log_indicator(self, indicator, content=None):
        i = {
            "user": USER,
            "feed": FEED,
            "indicator": indicator,
            "tags": ['smtp', 'spam', 'relay'],
            "description": 'peer using open smtp relay',
            "portlist": "25",
            "content": content,
        }

        logger.debug(json.dumps(i, indent=4))

        if TOKEN != '':
            try:
                ret = Indicator(i).submit()
                logger.debug(ret)
            except Exception as e:
                logger.error(e)

    async def handle_RCPT(self, server, session, envelope, address,
                          rcpt_options):
        envelope.rcpt_tos.append(address)
        return '250 OK'

    # https://aiosmtpd.readthedocs.io/en/latest/aiosmtpd/docs/concepts.html#sessions-and-envelopes
    async def handle_DATA(self, server, session, envelope):
        logger.debug('Message from %s' % envelope.mail_from)
        logger.debug('Message for %s' % envelope.rcpt_tos)

        logger.debug(f"{envelope.original_content}")

        content = envelope.content.decode('utf8', errors='replace')

        self._log_indicator(session.peer[0], content)

        sys.stdout.flush()

        return '250 Message accepted for delivery'


async def amain(loop):
    cont = Controller(SinkholeHandler(), hostname='', port=PORT)
    cont.start()


def main():
    p = ArgumentParser(
        description=textwrap.dedent('''\
                example usage:
                    $ csirtg-smtpd -d
                    $ csirtg-smtpd
                '''),
        formatter_class=RawDescriptionHelpFormatter,
    )

    p.add_argument('-d', '--debug', action='store_true')
    p.add_argument('--log')

    args = p.parse_args()

    loglevel = logging.INFO
    if args.debug:
        loglevel = logging.DEBUG

    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter(LOG_FORMAT))
    console.setLevel(loglevel)
    logger.addHandler(console)
    # logging.propagate = False

    logger.info(f'listening on {args.listen}:{args.port}')

    if TOKEN != '':
        if USER == '':
            raise SystemError('Missing envvar: CSIRTG_USER')
        if FEED == '':
            raise SystemError('Missing envvar: CSIRTG_FEED')

        logger.info(f"Logging indicators to {USER}/{FEED}")

    loop = asyncio.get_event_loop()
    loop.create_task(amain(loop=loop))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info('shutting down..')


if __name__ == '__main__':
    main()
