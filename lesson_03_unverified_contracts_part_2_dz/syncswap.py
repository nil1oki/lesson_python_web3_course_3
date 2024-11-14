import asyncio
import time

from web3 import AsyncWeb3

import config
from client import Client
from data.models import ABIs, SyncSwapFullAbi, TokenAmount, Tokens, TxArgs


async def main(from_token_amount: TokenAmount, slippage: float = 5):
    client = Client(
        private_key=config.PRIVATE_KEY,
        rpc='https://mainnet.era.zksync.io',
        proxy=config.PROXY
    )

    from_token_address = Tokens.WETH
    from_token_contract = client.w3.eth.contract(
        address=from_token_address,
        abi=ABIs.TokenABI
    )
    from_token_symbol = await from_token_contract.functions.symbol().call()

    to_token_address = Tokens.USDC
    to_token_contract = client.w3.eth.contract(
        address=to_token_address,
        abi=ABIs.TokenABI
    )
    to_token_symbol = await to_token_contract.functions.symbol().call()

    # адрес свапалки
    router_address = AsyncWeb3.to_checksum_address('0x9B5def958d0f3b6955cBEa4D5B7809b2fb26b059')
    router_contract = client.w3.eth.contract(
        address=router_address,
        abi=SyncSwapFullAbi
    )

    from_token_price_dollar = await client.get_token_price(token_symbol=from_token_symbol)
    to_token_price_dollar = await client.get_token_price(token_symbol=to_token_symbol)
    amount_out_min = TokenAmount(
        amount=float(from_token_amount.Ether) * from_token_price_dollar / to_token_price_dollar * (
                100 - slippage) / 100,
        decimals=await to_token_contract.functions.decimals().call()
    )

    '''
    
[0]:  0000000000000000000000000000000000000000000000000000000000000060
[1]:  000000000000000000000000000000000000000000000000000000000027d651 – amount out min
[2]:  0000000000000000000000000000000000000000000000000000000066f2df39 – deadline
[3]:  0000000000000000000000000000000000000000000000000000000000000001
[4]:  0000000000000000000000000000000000000000000000000000000000000020
[5]:  0000000000000000000000000000000000000000000000000000000000000060
[6]:  0000000000000000000000000000000000000000000000000000000000000000
[7]:  00000000000000000000000000000000000000000000000000038d7ea4c68000 – amount in
[8]:  0000000000000000000000000000000000000000000000000000000000000002 - количество элементов steps
[9]:  0000000000000000000000000000000000000000000000000000000000000040
[10]: 0000000000000000000000000000000000000000000000000000000000000180
[11]: 0000000000000000000000001a32a715b4ebef211bbf4baa414f563b25cc50c9 – ZK/WETH-A (SyncSwap Aqua LP)
[12]: 00000000000000000000000000000000000000000000000000000000000000a0
[13]: 0000000000000000000000000000000000000000000000000000000000000000
[14]: 0000000000000000000000000000000000000000000000000000000000000120
[15]: 0000000000000000000000000000000000000000000000000000000000000000
[16]: 0000000000000000000000000000000000000000000000000000000000000060
[17]: 0000000000000000000000005aea5775959fbc2557cc8789bc1bf90a239d9a91 – WETH
[18]: 00000000000000000000000040b768de8b2e4ed83d982804cb2fcc53d2529be9 – USDC.e/ZK-A (SyncSwap Aqua LP)
[19]: 0000000000000000000000000000000000000000000000000000000000000002
[20]: 0000000000000000000000000000000000000000000000000000000000000000
[21]: 00000000000000000000000040b768de8b2e4ed83d982804cb2fcc53d2529be9 – USDC.e/ZK-A (SyncSwap Aqua LP)
[22]: 00000000000000000000000000000000000000000000000000000000000000a0
[23]: 0000000000000000000000000000000000000000000000000000000000000000
[24]: 0000000000000000000000000000000000000000000000000000000000000120
[25]: 0000000000000000000000000000000000000000000000000000000000000000
[26]: 0000000000000000000000000000000000000000000000000000000000000060
[27]: 0000000000000000000000005a7d6b2f92c77fad6ccabd7ee0624e64907eaf3e – ZK
[28]: 00000000000000000000000036f302d18dcede1ab1174f47726e62212d1ccead – wallet address
[29]: 0000000000000000000000000000000000000000000000000000000000000002
[30]: 0000000000000000000000000000000000000000000000000000000000000000

[00] 0000000000000000000000000000000000000000000000000000000000000060 +
[01] 0000000000000000000000000000000000000000000000000000000000005c36 + 
[02] 00000000000000000000000000000000000000000000000000000000671c0f3a + 
[03] 0000000000000000000000000000000000000000000000000000000000000001 +
[04] 0000000000000000000000000000000000000000000000000000000000000020 + 
[05] 0000000000000000000000000000000000000000000000000000000000000060 +
[06] 0000000000000000000000000000000000000000000000000000000000000000 +
[07] 000000000000000000000000000000000000000000000000000009184e72a000 +
[08] 0000000000000000000000000000000000000000000000000000000000000002 +
[09] 0000000000000000000000000000000000000000000000000000000000000040 + 
[10] 0000000000000000000000000000000000000000000000000000000000000140 ?
[11] 0000000000000000000000001a32a715b4ebef211bbf4baa414f563b25cc50c9 +
[12] 0000000000000000000000000000000000000000000000000000000000000080 ?
[13] 0000000000000000000000000000000000000000000000000000000000000000 +
[14] 0000000000000000000000000000000000000000000000000000000000000120 +
[15] 0000000000000000000000000000000000000000000000000000000000000080
[16] 0000000000000000000000000000000000000000000000000000000000011111
[17] 0000000000000000000000000000000000000000000000000000000000000123
[18] 0000000000000000000000000000000000000000000000000000000000000124
[19] 0000000000000000000000000000000000000000000000000000000000000126
[20] 0000000000000000000000000000000000000000000000000000000000000040
[21] 0000000000000000000000000000000000000000000000000000000000000000
[22] 0000000000000000000000000000000000000000000000000002222222222222
[23] 0000000000000000000000001a32a715b4ebef211bbf4baa414f563b25cc50c9
[24] 0000000000000000000000000000000000000000000000000000000000000080
[25] 00000000000000000000000040b768de8b2e4ed83d982804cb2fcc53d2529be9
[26] 00000000000000000000000000000000000000000000000000000000000000c0
[27] 0000000000000000000000000000000000000000000000000000000000000020
[28] 0000000000000000000000000000000000000000000000000000000000033333
[29] 0000000000000000000000000000000000000000000000000000000000000020
[30] 0000000000000000000000000000000000000000000000000000000000044444
    
    '''

    tx_args = TxArgs(
        paths=[
            TxArgs(
                steps=[
                    TxArgs(
                        pool=Tokens.ZK_WETH_LP,
                        data=f'0x'
                             f'{Tokens.WETH[2:].zfill(64)}'
                             f'{Tokens.USDC_E_ZK_LP[2:].zfill(64)}'
                             f'{"2".zfill(64)}',
                        callback=Tokens.ZERO,
                        callbackData='0x',
                        useVault=False
                    ).tuple(),
                    TxArgs(
                        pool=Tokens.USDC_E_ZK_LP,
                        data=f'0x'
                             f'{Tokens.ZK[2:].zfill(64)}'
                             f'{client.account.address[2:].zfill(64)}'
                             f'{"2".zfill(64)}',
                        callback=Tokens.ZERO,
                        callbackData='0x',
                        useVault=True
                    ).tuple(),
                ],
                tokenIn=Tokens.ZERO,
                amountIn=from_token_amount.Wei
            ).tuple()
        ],
        amountOutMin=amount_out_min.Wei,
        deadline=int(time.time()) + 1200
    )

    data = router_contract.encodeABI('swap', args=tx_args.tuple())
    print(data)

    print(data[:10])
    data = data[10:]
    i = 0
    while data:
        print(f'[{str(i).zfill(2)}] {data[:64]}')
        data = data[64:]
        i += 1

    tx_hash = await client.send_transaction(
        to=router_address,
        data=router_contract.encodeABI('swap', args=tx_args.tuple()),
        value=from_token_amount.Wei,
        max_priority_fee_per_gas=client.max_priority_fee()
    )

    if tx_hash:
        try:
            await client.verif_tx(tx_hash=tx_hash)
            print(f'Transaction success ({from_token_amount.Ether} ETH -> {amount_out_min.Ether} {to_token_symbol})!! '
                  f'tx_hash: {tx_hash.hex()}')
            # Transaction success (0.001 ETH -> 2.28988 USDC)!! tx_hash: 0x5e97aaaa972dc2aca2bdb8b6241fe6dd5bb9eaeb238d0dcd941c31c46198b51e
        except Exception as err:
            print(f'Transaction error!! tx_hash: {tx_hash.hex()}; error: {err}')
    else:
        print(f'Transaction error!!')


if __name__ == '__main__':
    amount = TokenAmount(0.00001)
    asyncio.run(main(from_token_amount=amount))
