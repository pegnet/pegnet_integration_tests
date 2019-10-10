import configparser
import unittest
import time

import fat_py.fat2 as fat2
import fat_py.fat2.consts as consts
from factom_keys.fct import FactoidPrivateKey, FactoidAddress
from fat_py import FATd
from helpers.currency import get_all_currency

class PegnetTransactionTests(unittest.TestCase):

    def setUp(self):
        self.fatd = FATd()
        config = configparser.ConfigParser()
        config.read("../test_data/pegnet_config.ini")
        self.private_key = FactoidPrivateKey(key_string=config['data']['fct_private_key_1'])
        self.address = self.private_key.get_factoid_address()

        self.output_addresses = [
            FactoidAddress(address_string=config['data']['output_address1']),
            FactoidAddress(address_string=config['data']['output_address2']),
        ]

    def test_pegnet_default_balance(self):
        balances = self.fatd.get_pegnet_balances(self.address)
        print(balances)


    def test_send_transaction(self):
        tx = fat2.Transaction()
        tx.set_input(self.address, "PEG", 1000)
        tx.add_transfer(self.output_addresses[0], 500)
        tx.add_transfer(self.output_addresses[1], 500)

        tx_batch = fat2.TransactionBatch()
        tx_batch.add_transaction(tx)
        tx_batch.add_signer(self.private_key)
        ext_ids, content = tx_batch.sign()

        print(content.decode())
        print(self.fatd.send_transaction(consts.TRANSACTIONS_CHAIN_ID, ext_ids, content))

    def test_get_sync_status(self):
        sync_status = self.fatd.get_sync_status()
        print(sync_status)
        while(sync_status['syncheight'] != sync_status['factomheight']):
            print("pegnet not yet synched")
            time.sleep(5)

    def test_pegnet_issuance(self):
        print(self.fatd.get_pegnet_issuance())


    def test_currency_is_not_zero(self):
        sync_status = self.fatd.get_sync_status()
        print(sync_status['syncheight'])
        for i in range(sync_status['syncheight'],0,-1):
            rates = self.fatd.get_pegnet_rates(i)
            if rates != None:
                for key in rates.keys():
                    if rates[key] == 0:
                        print(f"rate should not be 0 but it is for {key} at the height : {i}")