import alpaca_trade_api as tradeapi


class Martingale(object):
    def __init__(self) -> None:
        # API authentication keys can be taken from the Alpaca dashboard.
        # https://app.alpaca.markets/paper/dashboard/overview
        self.key_id = 'PKCRN5I3D0P320QYDRJ8'
        self.secret_key = '0kzmDATHro5NTAczu2HgPHXlTy0zPgpOcmvmTjCj'
        self.base_url = 'https://paper-api.alpaca.markets'

        # The symbol we will be trading
        self.symbol = 'IVV'

        # When this variable is not None, we have an order open
        self.current_order = None

        # The closing price of the last aggregate we saw
        self.last_price = 1

        # The connection to the Alpaca API
        self.api = tradeapi.REST(
            self.key_id,
            self.secret_key,
            self.base_url
        )

        # Get our starting position, in case we already have one open
        try:
            self.position = int(self.api.get_position(self.symbol).qty)
        except:
            # No position exists
            self.position = 0

    def send_order(self, target_qty):
        # We don't want to have two orders open at once
        if self.current_order is not None:
            self.api.cancel_order(self.current_order.id)

        delta = target_qty - self.position
        if delta == 0:
            return
        print(f'Processing the order for {target_qty} shares')

        try:
            if delta > 0:
                buy_qty = delta
                if self.position < 0:
                    buy_qty = min(abs(self.position), buy_qty)
                print(f'Buying {buy_qty} shares')
                self.current_order = self.api.submit_order(
                    self.symbol, buy_qty, 'buy', 'limit', 'day', self.last_price)

            elif delta < 0:
                sell_qty = abs(delta)
                if self.position > 0:
                    sell_qty = min(abs(self.position), sell_qty)
                print(f'Selling {sell_qty} shares')
                self.current_order = self.api.submit_order(
                    self.symbol, sell_qty, 'sell', 'limit', 'day', self.last_price)

        except Exception as e:
            print(e)


if __name__ == "__main__":
    t = Martingale()
    t.send_order(3)
