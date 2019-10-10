
import unittest
import configparser
from factom_keys.fct import FactoidPrivateKey, FactoidAddress
from helpers.cli_methods import send_command_to_cli_and_receive_text
from helpers.currency import get_all_currency

class PegnetBalanceTests(unittest.TestCase):

    def setUp(self):
        self.config = configparser.ConfigParser()
        self.config.read("../test_data/pegnet_config.ini")
        self.private_key = FactoidPrivateKey(key_string=self.config['data']['fct_private_key_3'])
        self.address = self.private_key.get_factoid_address()
        self.private_key_2 = FactoidPrivateKey(key_string=self.config['data']['fct_private_key_1'])
        self.address_2 = self.private_key_2.get_factoid_address()


    def test_balance(self):
        print(self.address.to_string())
        print(send_command_to_cli_and_receive_text("pegnetd balances " + self.address.to_string()))


    def test_new_conversions(self):
        currency = get_all_currency()
        for i in currency:
            for j in currency:
                if i != j:
                    print(send_command_to_cli_and_receive_text("pegnetd newcvt " + self.config['data']['ec_public_address'] + " " +  self.address.to_string() +
                                                     " " + i + " 0.0001 " + j))

    def test_new_transactions(self):
        currency = get_all_currency()
        for i in currency:
            for j in currency:
                print(send_command_to_cli_and_receive_text("pegnetd newtx " + self.config['data']['ec_public_address'] + " " + self.address.to_string() +
                      " " + i + " 0.0001 " + self.address_2.to_string()))