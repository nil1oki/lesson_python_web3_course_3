import asyncio

from evm_explorers.explorer_api import APIFunctions
from evm_explorers import config


async def main():
    api = APIFunctions(key=config.ETHEREUM_API_KEY, url='https://api.etherscan.io/api')

    # print(
    #     int((await api.account.balance(address='0x36F302d18DcedE1AB1174f47726E62212d1CcEAD'))['result']) / 10 ** 18
    # )

    # addresses = ['0x36F302d18DcedE1AB1174f47726E62212d1CcEAD', '0xDAFEA492D9c6733ae3d56b7Ed1ADB60692c98Bc5']
    # print(
    #     await api.account.balancemulti(address=addresses)
    # )

    # print(
    #     await api.account.txlist(address='0x36F302d18DcedE1AB1174f47726E62212d1CcEAD')
    # )
    # res = (await api.account.txlist(address='0x36F302d18DcedE1AB1174f47726E62212d1CcEAD'))['result']
    # for r in res:
    #     print(r)

    # print(
    #     await api.contract.getabi(address='0x32400084C286CF3E17e7B677ea9583e60a000324')
    # )

    # print(
    #     await api.contract.get_contract_source_code(contract_address='0x32400084C286CF3E17e7B677ea9583e60a000324')
    # )

    # print(
    #     await api.transaction.get_status(tx_hash='0xb2ce71dc50d728fe0da43db1cc86c5df628588e53824a4d01374bf7e784b4f86')
    # )


if __name__ == '__main__':
    asyncio.run(main())
