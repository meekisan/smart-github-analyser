<?php
################### IMPORT DATA ##############################
###################### START #################################

//pour les erreurs
ini_set('display_errors', 1);


######### VARIABLES NON LIEES AU POST
//nom de ma page
$urlPage     = 'import_data.php';
//variable autre
$nodeCreate ='';

//pour neo4j
//les lib
require_once 'vendor/autoload.php';
//ClientBuilder
use GraphAware\Neo4j\Client\ClientBuilder;
//connexion à neo4j
$client = ClientBuilder::create()
    ->addConnection('default', 'http://neo4j:rabbit8497@recommandation:7474')
    ->build();

 /**
 Create REPO
**/
//ON SUPPRIME LE NOEUD A CREER AU CAS OU

//on créé le noed
$nodeShema =
  array(//repoName,Structure du CSV,fileName.csv (est dans le dossier \neo4j\import ),INDEX,AUTRE
    array('Repo',' {repo_name: row.repo_name}', 'repository.csv','repo_name','')
    ,array('Languages', ' {language: row.name, size:row.size}', 'language_list.csv','language','')
    ,array('Licences', ' {repo_name: row.repo_name, licence:row.licence}', 'licences.csv','licence','')
    ,array('LanguesRepo', ' {repo_name: row.repo_name, languages:split(row.language,",")}', 'languages.csv','repo_name','')
);


//nb node à créer
$nbNode = count($nodeShema);
for ($i=0; $i<$nbNode; $i++) {
  $node   = $nodeShema[$i][0];
  $schema = $nodeShema[$i][1];
  $file   = $nodeShema[$i][2];
  $index  = $nodeShema[$i][3];
  //on supprime le node en question
  $query = 'MATCH (n:'.$node.') DETACH DELETE n';
  $result = $client->run($query);
  //si pas supprimé alors arret
  if (!$result) die("pas possible pour $query");
  //on load les données depuis le csv selon le schéma en question
  $query = 'USING PERIODIC COMMIT LOAD CSV WITH HEADERS FROM "file:///'.$file.'" AS row CREATE (:'.$node.$schema.');';

  $result = $client->run($query);
  //on index ensuite la clé souhaité
  $query = 'CREATE INDEX ON :'.$node.'('.$index.');';
  $result = $client->run($query);
  if ($result) $nodeCreate.='<li>'.$node.' depuis '.$file.'</li>';
  flush();
  }
//pour les RELATIONS
$linkCreate = '';
$linkShema =
  array(//repoName1,key1,repoName2,key2,relation,type de relation
    array('Repo','repo_name', 'Licences','repo_name','LICENCE',1,'nodeC','keyc','keyA1','keyB1','keyC1')
    ,array('Repo','repo_name', 'LanguesRepo','repo_name','LANGUES',1,'nodeC','keyc','keyA1','keyB1','keyC1')
    ,array('Languages','language', 'LanguesRepo','repo_name','SPEAK',2,'Repo','repo_name','keyA1','languages','keyC1')
);
$nbLink = count($linkShema);
for ($i=0; $i<$nbLink; $i++) {
  $nodeA = $linkShema[$i][0];
  $keyA  = $linkShema[$i][1];
  $nodeB = $linkShema[$i][2];
  $keyB  = $linkShema[$i][3];
  $relat = $linkShema[$i][4];
  $type  = $linkShema[$i][5];
  $nodeC = $linkShema[$i][6];
  $keyC  = $linkShema[$i][7];
  $keyA1  = $linkShema[$i][8];
  $keyB1  = $linkShema[$i][9];
  $keyC1  = $linkShema[$i][10];


  //on supprime la relation en question
  $query = 'MATCH ()-[r:'.$relat.']-() DETACH DELETE r';
  $result = $client->run($query);
  //si pas supprimé alors arret
  if (!$result) die("pas possible pour $query");
  //on load les données depuis le csv selon le schéma en question
  $query = 'MATCH (a:'.$nodeA.') MATCH (b:'.$nodeB.') WHERE (a.'.$keyA.' = b.'.$keyB.') AND a<>b MERGE (a)-[:'.$relat.']->(b);';
  if ($type==2) $query = 'MATCH (b:'.$nodeB.') UNWIND b.'.$keyB1.' AS eleB MATCH (a:'.$nodeA.') MATCH (c:'.$nodeC.') WHERE split(split(eleB,":")[1],\'"\')[1] = a.'.$keyA.' AND c.'.$keyC.' = b.'.$keyB.' CREATE (a)-[:'.$relat.']->(c)';
  //if ($type==2) die($query);
  $result = $client->run($query);
  if ($result) $linkCreate.='<li>('.$nodeA.':'.$keyA.')-[:'.$relat.']->('.$nodeB.':'.$keyB.') ['.$query.']</li>';
  flush();
  }
  echo "<ol>$nodeCreate.</ol><ol>$linkCreate</ol>";
  die("FAIT");


/*
MATCH (b:LanguesRepo) UNWIND b.languages AS lang
MATCH (a:Languages)
MATCH (r:Repo)
WHERE split(split(lang,':')[1],'"')[1] = a.language AND r.repo_name = b.repo_name
CREATE (r)-[:SPEAK]->(a)
RETURN split(lang,':')[1], a.language, r.repo_name LIMIT 50
*/




############################## EOF #############################
