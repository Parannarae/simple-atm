import unittest
from unittest import mock
from unittest.mock import patch

from app.atm import ATM
from data.card import Card
from device_interface.bank_system import BankSystem


class TestATM(unittest.TestCase):
    @patch('device_interface.bank_system.BankSystem')
    @patch('device_interface.card_reader.CardReader')
    @patch('device_interface.display.Display')
    @patch('device_interface.keypad.KeyPad')
    @patch('device_interface.cash_bin.CashBin')
    def setUp(self, cash_bin_mock, keypad_mock, display_mock, card_reader_mock, bank_system_mock):
        self.bank_system_mock = bank_system_mock
        self.card_reader_mock = card_reader_mock
        self.display_mock = display_mock
        self.keypad_mock = keypad_mock
        self.cash_bin_mock = cash_bin_mock
        self.atm = ATM(bank_system=bank_system_mock,
                       card_reader=card_reader_mock,
                       display=display_mock,
                       keypad=keypad_mock,
                       cash_bin=cash_bin_mock)

        # mute all display method
        display_mock.display_str = mock.MagicMock()

    def test_read_card(self):
        # no card is presented in the reader
        self.card_reader_mock.read_card = mock.MagicMock(return_value=None)
        self.assertFalse(self.atm.read_card())

        # card is presented in the reader
        card_number = '1234567890'
        self.card_reader_mock.read_card = mock.MagicMock(return_value=Card(card_number))
        self.assertTrue(self.atm.read_card())

    def test_read_and_validate_pin(self):
        def is_correct_pin_mock(correct_pin: int) -> bool:
            return lambda x : x == correct_pin

        correct_pin = 1234
        wrong_pin = 5678
        self.bank_system_mock.is_correct_pin = is_correct_pin_mock(correct_pin)
        self.keypad_mock.read = mock.MagicMock(return_value=correct_pin)
        self.assertTrue(self.atm.read_and_validate_pin())
        self.assertEqual(self.keypad_mock.read.call_count, 1)

        self.keypad_mock.read = mock.MagicMock(return_value=wrong_pin)
        self.assertFalse(self.atm.read_and_validate_pin())
        self.assertEqual(self.keypad_mock.read.call_count, ATM.MAX_RETRY_PIN)

    def test_select_account(self):
        account_numbers = ['123456789', '234567890']
        self.bank_system_mock.get_accounts = mock.MagicMock(return_value=account_numbers)

        selected_number = 0
        self.keypad_mock.read = mock.MagicMock(return_value=selected_number)
        self.atm.select_account()
        self.assertEqual(self.atm.current_account_num, account_numbers[selected_number])

        # reset account_number
        self.atm._clear_information()
        selected_number = 1
        self.keypad_mock.read = mock.MagicMock(return_value=selected_number)
        self.atm.select_account()
        self.assertEqual(self.atm.current_account_num, account_numbers[selected_number])

    def test_get_operation_menu(self):
        input_val = 1
        self.keypad_mock.read = mock.MagicMock(return_value=input_val)
        self.assertEqual(self.atm.get_operation_menu(), ATM.OpType(input_val))

        input_val = 2
        self.keypad_mock.read = mock.MagicMock(return_value=input_val)
        self.assertEqual(self.atm.get_operation_menu(), ATM.OpType(input_val))

        input_val = 3
        self.keypad_mock.read = mock.MagicMock(return_value=input_val)
        self.assertEqual(self.atm.get_operation_menu(), ATM.OpType(input_val))

        input_val = 4
        self.keypad_mock.read = mock.MagicMock(return_value=input_val)
        self.assertEqual(self.atm.get_operation_menu(), None)
        self.assertEqual(self.keypad_mock.read.call_count, ATM.MAX_RETRY_MENU)

if __name__ == '__main__':
    unittest.main()