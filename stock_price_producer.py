from confluent_kafka import Producer
import fetch_stock_prices as fsp
import constants

import json
import time
import logging
logging.basicConfig(level = logging.INFO)

class StockPriceProducer:
    def __init__(self, host, port, topic):
        self.config = {
            'bootstrap.servers': f'{host}:{port}',
            'acks': 'all'
        }
        self.producer = Producer(self.config)
        self.topic = topic

    
    def delivery_callback(self, err, msg):
        if err:
            logging.info(f"Message failed delivery: {err}")
        else:
            logging.info(
                f"producer event to topic = {msg.topic()} : key = {msg.key().decode('utf-8')} : partition = {msg.partition()} : value = {msg.value().decode('utf-8'):12}")
    
    def run(self):
        my_stock_prices = fsp.FetchStockPrices(constants.portfolio).fetch_stock_price()

        while True:
            n = 0
            for stock in my_stock_prices:
                self.producer.produce(self.topic, key=stock, value=json.dumps(my_stock_prices[stock]), callback=self.delivery_callback)
                n+=1
            self.producer.poll(n)
            self.producer.flush()
            time.sleep(60)


if __name__=="__main__":
    stock_producer = StockPriceProducer('localhost', '9092', 'demo')
    stock_producer.run()
