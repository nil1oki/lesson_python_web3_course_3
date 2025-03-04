from client import Client
from tasks.base import Base
from data.models import Settings, Contracts
from oklink.fundamental_blockchain_data import APIFunctions
from tasks.koi_finance import KoiFinance
from tasks.space_fi import SpaceFi
from tasks.sync_swap import SyncSwap
from tasks.whale_nft import WhaleNft
from tasks.dmail import Dmail


class Controller(Base):
    def __init__(self, client: Client):
        super().__init__(client)
        
        self.space_fi = SpaceFi(client)
        self.koi_finance = KoiFinance(client)
        self.syncswap = SyncSwap(client)
        self.whale_nft = WhaleNft(client)
        self.dmail = Dmail(client)

    async def count_swaps(self, txs_lst: list[dict] | None = None):
        settings = Settings()
        chain = 'zksync'

        result_txs = []

        api_oklink = APIFunctions(url='https://www.oklink.com', key=settings.oklink_api_key)

        if not txs_lst:
            txs_lst = await api_oklink.address.txlist_all(
                address=self.client.account.address,
                chain=chain
            )

        # KoiFinance ETH -> Token
        result_txs += await api_oklink.address.find_txs(
            address=self.client.account.address,
            signature='0x7ff36ab5',
            to=Contracts.KOI_FINANCE_ROUTER.address,
            chain=chain,
            txs_lst=txs_lst
        )

        # SpaceFi ETH -> Token
        result_txs += await api_oklink.address.find_txs(
            address=self.client.account.address,
            signature='0x7ff36ab5',
            to=Contracts.SPACE_FI_ROUTER.address,
            chain=chain,
            txs_lst=txs_lst
        )

        # SpaceFi Token -> ETH
        result_txs += await api_oklink.address.find_txs(
            address=self.client.account.address,
            signature='0x18cbafe5',
            to=Contracts.SPACE_FI_ROUTER.address,
            chain=chain,
            txs_lst=txs_lst
        )

        # SyncSwap Token -> ETH
        result_txs += await api_oklink.address.find_txs(
            address=self.client.account.address,
            signature='0xd7570e45',
            to=Contracts.SYNCSWAP_ROUTER.address,
            chain=chain,
            txs_lst=txs_lst
        )

        return len(result_txs)

    async def count_mints_nft(self, txs_lst: list[dict] | None = None):
        settings = Settings()
        chain = 'zksync'

        result_txs = []

        api_oklink = APIFunctions(url='https://www.oklink.com', key=settings.oklink_api_key)

        if not txs_lst:
            txs_lst = await api_oklink.address.txlist_all(
                address=self.client.account.address,
                chain=chain
            )

        # Whale NFT
        result_txs += await api_oklink.address.find_txs(
            address=self.client.account.address,
            signature='0x1249c58b',
            to=Contracts.WHALE_NFT_ROUTER.address,
            chain=chain,
            txs_lst=txs_lst
        )

        return len(result_txs)

    async def count_dmail(self, txs_lst: list[dict] | None = None):
        settings = Settings()
        chain = 'zksync'

        result_txs = []

        api_oklink = APIFunctions(url='https://www.oklink.com', key=settings.oklink_api_key)

        if not txs_lst:
            txs_lst = await api_oklink.address.txlist_all(
                address=self.client.account.address,
                chain=chain
            )

        # dmail
        result_txs += await api_oklink.address.find_txs(
            address=self.client.account.address,
            signature='0x5b7d7482',
            to=Contracts.DMAIL.address,
            chain=chain,
            txs_lst=txs_lst
        )

        return len(result_txs)
