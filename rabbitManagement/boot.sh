#!/bin/bash

service rabbitmq-server start 

#Exchange
/usr/local/bin/rabbitmqadmin declare exchange  name=github_archive type=topic durable=true 
/usr/local/bin/rabbitmqadmin declare exchange  name=simulator type=topic durable=true 

#Queue
/usr/local/bin/rabbitmqadmin declare queue  name=archives durable=true 
/usr/local/bin/rabbitmqadmin declare queue  name=commits durable=true 
/usr/local/bin/rabbitmqadmin declare queue  name=files durable=true 

# binding queue
/usr/local/bin/rabbitmqadmin declare binding source=github_archive destination_type=queue destination=archives routing_key=*.* 
/usr/local/bin/rabbitmqadmin declare binding source=simulator destination_type=queue destination=commits routing_key=commit.* 
/usr/local/bin/rabbitmqadmin declare binding source=simulator destination_type=queue destination=files routing_key=file.* 

#create user rabbit
rabbitmqctl add_user rabbit m0bR4b1tt
rabbitmqctl set_permissions -p / rabbit ".*" ".*" ".*"
rabbitmqctl set_user_tags rabbit administrator

# restart rabbit
service rabbitmq-server stop 
rabbitmq-server
