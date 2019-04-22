# Mutraff - A TWM traffic controller

Mutraff enables dynamic traffic control using TWM (traffic weighted maps).
It uses a distributed architectrue based on AMQP protocol (using python Pika).

Components:
* Controller - The distributed controller for all the components.
* MessageCounter - A distributed message generator.
* Ruleset - A Ruleset engine for creating event-driven controls.
* TrafficCenter - The Traffic Control Unit
* Vehicle - A Vehicle abstraction.
