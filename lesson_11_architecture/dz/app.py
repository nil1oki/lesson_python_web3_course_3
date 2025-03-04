import asyncio

from loguru import logger

from functions.create_files import create_files
from functions.Import import Import
from data.models import Settings
from functions.initial import initial
from functions.activity import activity


async def start_script():
    settings = Settings()

    if not settings.oklink_api_key:
        logger.error('Specify the API key for oklink explorer!')
        return

    await asyncio.wait([asyncio.create_task(initial()), asyncio.create_task(activity())])


if __name__ == '__main__':
    create_files()
    print('''  Select the action:
1) Import wallets from the spreadsheet to the DB;
2) Start the script;
3) Exit.''')

    try:
        action = int(input('> '))
        if action == 1:
            asyncio.run(Import.wallets())

        elif action == 2:
            asyncio.run(start_script())

    except KeyboardInterrupt:
        print()

    except ValueError as err:
        logger.error(f'Value error: {err}')

    except BaseException as e:
        logger.error(f'Something went wrong: {e}')
