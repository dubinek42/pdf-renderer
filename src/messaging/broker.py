from dramatiq.brokers.rabbitmq import RabbitmqBroker

from ..settings import RabbitConfig

broker = RabbitmqBroker(url=RabbitConfig().get_rabbit_url())
