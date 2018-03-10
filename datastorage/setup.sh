#!/bin/bash
sleep 10
MONGODB1=`ping -c 1 mongoprimary | head -1  | cut -d "(" -f 2 | cut -d ")" -f 1`
MONGODB2=`ping -c 1 mongosecondary | head -1  | cut -d "(" -f 2 | cut -d ")" -f 1`
MONGODB3=`ping -c 1 mongoarbitre | head -1  | cut -d "(" -f 2 | cut -d ")" -f 1`

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
                  {_id: 0, host: "mongoprimary"},
                  {_id: 1, host: "mongosecondary"},
                  {_id: 2, host: "mongoarbitre", "arbiterOnly" : true}
                ]
     }
 )
EOF
