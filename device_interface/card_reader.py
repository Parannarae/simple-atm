from typing import Optional

from data.card import Card

class CardReader:
    def __init__(self):
        # card reader connection code
        self.reader_system = None

    def read_card(self) -> Optional[Card]:
        """Read a card information.

        Returns:
            None if no card is in the reader
        """
        raise NotImplementedError