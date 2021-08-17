A simple product-catalog application following a microservices architecture composed of two independent and dynamic services
that communicate with each other using AMQP (Advanced Message Queuing Protocol) communication protocol

Project setup:
* product microservice (Django Rest Framework)
CRUD ops via Postman:
- create
- list/retrieve
- update
- destroy

* catalog microservice (Django Rest Framework)
Create catalog
Add products to catalog

* RabbitMQ as AMQP broker

* no shared db: each microservice has its own database instance

~~~
 ______ container _______                       _______ container ________
|   __________________   |                     |    ___________________   |
|  | product microsrv |  |     ____________    |   |  catalog microsrv |  |
|  |      (DRF)       |  |    |            |   |   |      (DRF)        |  |
|  |                  |==|==> |  RabbitMQ  |===|==>|                   |  |
|  |   product ops    |==|==> | msg broker |===|==>|   catalog ops     |  |
|  |   producer(pika) |  |    |____________|   |   |   consumer(pika)  |  |
|  |__________________|  |                     |   |___________________|  |
|  |                  |  |                     |   |                   |  |
|  |  Postgres prdb   |  |                     |   |  Postgres ctdb    |  |
|  |__________________|  |                     |   |___________________|  |
|________________________|                     |__________________________|

~~~

create/update/destroy events => publish() message queue (producer.py) => add/update/remove product in catalog (consumer.py)

--> command: python manage.py consumer
custom django command to run consumer.py within the framework context

