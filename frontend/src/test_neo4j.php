<?php
ini_set('display_errors', 1);

require_once 'vendor/autoload.php';

use GraphAware\Neo4j\Client\ClientBuilder;

$client = ClientBuilder::create()
    ->addConnection('default', 'http://neo4j:rabbit8497@recommandation:7474')
    ->build();

$option = '';
$query = 'MATCH (n) WHERE EXISTS(n.name) RETURN DISTINCT "node" as entity, n.name AS name LIMIT 25 UNION ALL MATCH ()-[r]-() WHERE EXISTS(r.name) RETURN DISTINCT "relationship" AS entity, r.name AS name';
$result = $client->run($query);
foreach ($result->getRecords() as $record) {
    $lename= sprintf($record->value('name'));
    $option.='<option value="'.$lename.'>'.$lename.'</option>';
  }
echo '<select>'.$option.'</select>';
/*

require_once 'vendor/autoload.php';

use GraphAware\Neo4j\Client\ClientBuilder;

echo "<hr>Yes<hr>";

$client = ClientBuilder::create()
    ->addConnection('default', 'http://toto:toto@recommandation') // Example for HTTP connection configuration (port is optional)
    ->build();

foreach ($result->getRecords() as $record) {
    echo sprintf('Person name is : %s and has %d number of friends', $record->value('name'), count($record->value('friends')));
}
*/
