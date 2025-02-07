import yfinance as yf


class FetchStockPrices:
    def __init__(self, portfolio: str)->None:
        self.portfolio = portfolio
    
    def fetch_stock_price(self)->dict:
        current_price_portfolio = {}
        for stock_name in self.portfolio:
            stock_data = yf.Ticker(self.portfolio[stock_name])
            price = stock_data.info.get('currentPrice')
            current_price_portfolio[stock_name] = {
                'ticker': self.portfolio[stock_name],
                'price': price
            }
        return current_price_portfolio


if __name__=="__main__":
    portfolio = {
        'netflix': 'NFLX',
    }
    my_stock_prices = FetchStockPrices(portfolio).fetch_stock_price()
    print(my_stock_prices)
