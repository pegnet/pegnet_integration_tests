
import unittest
import json
import configparser
from factom_keys.fct import FactoidPrivateKey, FactoidAddress
from helpers.cli_methods import send_command_to_cli_and_receive_text
from helpers.currency import get_all_currency

class PegnetBalanceTests(unittest.TestCase):

    _balance_ = "pegnetd balances "
    _newcvt_ = "pegnetd newcvt "
    _newtx_ = "pegnetd newtx "

    def setUp(self):
        self.config = configparser.ConfigParser()
        self.config.read("../test_data/pegnet_config.ini")
        self.private_key = FactoidPrivateKey(key_string=self.config['data']['fct_private_key_3'])
        self.address = self.private_key.get_factoid_address()
        self.private_key_2 = FactoidPrivateKey(key_string=self.config['data']['fct_private_key_1'])
        self.address_2 = self.private_key_2.get_factoid_address()
        self.ec_address =  self.config['data']['ec_public_address']


    def test_balance(self):
        print(self.address.to_string())
        print(send_command_to_cli_and_receive_text(self._balance_ + self.address.to_string()))


    def test_all_currency_conversions(self):
        currency = get_all_currency()
        funds_to_transfer = "0.00001"
        for i in currency:
            for j in currency:
                if i != j:
                    result = send_command_to_cli_and_receive_text(self._newcvt_ + self.ec_address + " " +  self.address.to_string() +
                                                     " " + i + " " + funds_to_transfer + " " + j)
                    print(result)
                    self.assertTrue("conversion sent" in result, "Testcase failed")

    def test_all_currency_transactions(self):
        currency = get_all_currency()
        funds_to_transfer = "0.000001"

        for i in currency:
            print(f"{self._newtx_} {self.ec_address} {self.address.to_string()} {i}  {funds_to_transfer} {self.address_2.to_string()}")
            result = send_command_to_cli_and_receive_text(self._newtx_ + self.ec_address + " " + self.address.to_string() +
                      " " + i + " " +  funds_to_transfer + " " + self.address_2.to_string())
            print(result)
            self.assertTrue("transaction sent" in result, "Testcase failed")

    def test_single_currency_conversions(self):
        from_currency = "PEG"
        to_currency = "pXAU"
        funds_to_transfer = "0.00001"

        before_PEG = self.check_balance(from_currency)
        before_pXAU = self.check_balance(to_currency)
        result = send_command_to_cli_and_receive_text(self._newcvt_ + self.ec_address + " " +  self.address.to_string() + " " + from_currency + " " + funds_to_transfer + " " + to_currency)
        print(result)

        after_PEG = self.check_balance(from_currency)
        after_pXAU = self.check_balance(to_currency)

        self.assertEqual(before_PEG,after_PEG,"PEGs are not matching. Testcase Failed")
        self.assertEqual(before_pXAU,after_pXAU, "pXAU are not matching. Testcase Failed")


    def test_single_currency_transaction(self):
        currency = "pXAU"
        funds_to_transfer = "0.0001"
        before_balance = self.check_balance(currency)

        print(f"address : {self.address.to_string()} balance of pXBT before transaction is {before_balance}")
        print(f"{self._newcvt_} {self.ec_address} {self.address.to_string()} {currency}  {funds_to_transfer} {self.address_2.to_string()}")
        result = send_command_to_cli_and_receive_text(self._newtx_ + self.ec_address + " " + self.address.to_string() + " " + currency + " " + funds_to_transfer + " " + self.address_2.to_string())
        print(result + "\n")
        after_balance = self.check_balance(currency)
        print(f"address : {self.address.to_string()} balance of {currency} after transaction is {after_balance}")
        self.assertEqual(before_balance, after_balance, "%s are not matching. Testcase Failed" % currency)


    def check_balance(self, currency):
        all_balance = json.loads(send_command_to_cli_and_receive_text(self._balance_ + self.address.to_string()))
        balance = all_balance[currency]
        print(f"balance of {currency}  is {balance}")
        return balance