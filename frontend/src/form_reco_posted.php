<?php

//nom de domaine <=> penser à le changer si activé sécruté d'acces
#$hostName = '172.24.0.1';
//securité d'acces : si pas bon nom de page et pas bon host alors arret. cela permet de limiter certianes attaques liées au post mais pas bon pour les moteurs
//if ($hostName != gethostbyname($_SERVER['REMOTE_ADDR'])) die(header("Location: http://www.perdu.com"));

//NOM DU FICHIER
$urlPageForm = "form_reco_posted.php";


//vérifie que le user pour qui se fait la recherche existe
#$user   = (isset($_POST['nameUser'])) ?  $_POST['nameUser'] : '';
$user   = (isset($_POST['worker_login'])) ?  $_POST['worker_login'] : '';
//vérifie que le mot a chercher existe et a plus de 1 caractère
//gestion des erreurs
$error = 0;
if ($user=='') $error++;
//on passe la rq pour le traitement si on a aucune erreur
//ici : action = 2
if ($error ==0) {//query pour la recommandation
  $query_reco = 'MATCH (tom:dev {nom:"'.$user.'"})-[:travail]->(p)<-[:travail]-(coworker)-[:travail]->(autresProjets) RETURN autresProjets.nom as projets';
  $result = $client->run($query_reco);
  $countRepo = 0;
  $resultQuery = 'PAS DE RESULTAT';
  $resultQueryTmp = '';
  foreach ($result->getRecords() as $record) {
      $lename  = sprintf($record->value('projets'));
      $countRepo++;
      $resultQueryTmp.=$countRepo.'. : '.$lename.'<br>';
    }
  $resultQuery = ($countRepo > 0) ? $resultQueryTmp : $resultQuery;
  // AFFICHAGE
  $returnForm="<hr><h4>Nos conseils pour le login:'$user'</h4>";
  $returnForm.='<hr>Les repos ('.$query_reco.')<br>'.$resultQuery;
  #$returnForm.='<hr>Les repos ('.$query_friend.')<br>'.$resultQuery2;
}
####################################### EOF #######################################
