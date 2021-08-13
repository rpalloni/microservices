Project setup:
* product microservice (Django Rest Framework)
CRUD ops via Postman:
- create
- list/retrieve
- update
- destroy

* catalog microservice (Django Rest Framework)
Create catalog
Add product data to catalog


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


create/update/destroy => publish() message queue (producer.py) => add to catalog (consumer.py)

>> command: python manage.py consumer
custom django command to run consumer.py within the framework context

