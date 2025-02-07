from confluent_kafka import Producer
import logging


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
                f"producer event to topic {msg.topic()}: key = {msg.key().decode('utf-8'):12} calue = {msg.value().decode('utf-8'):12}")
    
    def run(self):
        for i in range(10000):
            self.producer.produce(self.topic, f"This is message number {i}", callback=self.delivery_callback)
        
        self.producer.poll(1000)
        self.producer.flush()


if __name__=="__main__":
    stock_producer = StockPriceProducer('localhost', '9092', 'demo')
    stock_producer.run()
