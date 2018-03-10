#!/bin/bash
sleep 10
MONGODB1=`ping -c 1 datastorage-primary | head -1  | cut -d "(" -f 2 | cut -d ")" -f 1`
MONGODB2=`ping -c 1 datastorage-secondary | head -1  | cut -d "(" -f 2 | cut -d ")" -f 1`
MONGODB3=`ping -c 1 datastorage-arbitre | head -1  | cut -d "(" -f 2 | cut -d ")" -f 1`

echo "Waiting for startup.."
until curl http://${MONGODB1}:28017/serverStatus\?text\=1 2>&1 | grep uptime | head -1; do
  echo "."
  sleep 5
done

echo curl http://${MONGODB1}:28017/serverStatus\?text\=1 2>&1 | grep uptime | head -1
echo "Started.."


echo SETUP.sh time now: `date +"%T" `
sleep 5
mongo --host ${MONGODB1}:27017 <<EOF
rs.initiate ({
       _id: "rsProjet",
       members: [
                  {_id: 0, host: "smartgithubanalyser_datastorage-primary_1"},
                  {_id: 1, host: "smartgithubanalyser_datastorage-secondary_1"},
                  {_id: 2, host: "smartgithubanalyser_datastorage-arbitre_1", "arbiterOnly" : true}
                ]
     }
 )
EOF
