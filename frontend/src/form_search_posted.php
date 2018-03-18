<?php

//nom de domaine <=> penser à le changer si activé sécruté d'acces
#$hostName = '172.24.0.1';
//securité d'acces : si pas bon nom de page et pas bon host alors arret. cela permet de limiter certianes attaques liées au post mais pas bon pour les moteurs
//if ($hostName != gethostbyname($_SERVER['REMOTE_ADDR'])) die(header("Location: http://www.perdu.com"));

//NOM DU FICHIER
$urlPageForm = "form_search_posted.php";
//vérifie l'action a mener
$action = (isset($_POST['action'])) ? ((preg_replace('[^0-9]','',$_POST['action']) > 0) ? preg_replace('[^0-9]','',$_POST['action']) : 0) : 0;
//vérifie que le user pour qui se fait la recherche existe
$user   = (isset($_POST['worker_login'])) ?  $_POST['worker_login'] : '';
//vérifie que le mot a chercher existe et a plus de 1 caractère
$search = (isset($_POST['nameSearch'])) ? ((strlen($_POST['nameSearch']) > 1) ? $_POST['nameSearch'] : '') : '';
//implode les langues demandées car choix multiples
$langue = (isset($_POST['language'])) ? $_POST['language']: '';
//nombre de star à reprendre
//cas où on laisse un champ libre
$star = (isset($_POST['star'])) ? $_POST['star'] : '';
$relationType = $_POST['type'];
//cas où on a un menu
//$star   = (isset($_POST['star'])) ? ((preg_replace('[^0-9]','',$_POST['star']) > 0) ? preg_replace('[^0-9]','',$_POST['nameStar']) : 0) :0;


//gestion des erreurs
$error = 0;
//if ($search=='') $error++;

//on passe la rq pour le traitement si on a aucune erreur
//ici : action = 1
if (($action ==1) && ($error ==0)) {
  //retourner les données saisies
  $txtSearchDefault = $search;
  $where = '';
  if($star != ''){
    if(empty($where))
      $where .= 'WHERE ';
    $where .= ' autresProjets.stars >'.$star;
  }
  if($langue !=''){
    if(empty($where))
        $where .= ' WHERE ';
    else
      $where .= ' AND ';
    $where .=' filter(langue IN autresProjets.language WHERE langue= "'.$langue.'")';
  }
  $query = 'MATCH (a:Actor {login:"'.$user.'"})-[:'.$relationType.']->(p)<-[:'.$relationType.']-(coActor)-[:'.$relationType.']->(otherRepos) '.$where.' RETURN otherRepos.repo_name AS repos';
  //query pour obtenir les users
  $result = $client->run($query);
  $countRepo = 0;
  $resultQuery = 'PAS DE RESULTAT';
  $resultQueryTmp = '';
  foreach ($result->getRecords() as $record) {
      $lename  = sprintf($record->value('repos'));
      $countRepo++;
      $resultQueryTmp.=$countRepo.'. : <a href="https://github.com/'.$lename.'" target="_blank" class="none">'.$lename.'</a><br>';
    }
  $resultQuery = ($countRepo > 0) ? $resultQueryTmp : $resultQuery;
  // AFFICHAGE
  $returnForm="<hr><h4>le résultat de ma demande ci dessous</h4>";
  $returnForm.='$user = ['.$user.']';
  $returnForm.='<hr>$search = ['.$search.']';
  $returnForm.='<hr>$langue = ['.$langue.']';
  $returnForm.='<hr>$star = ['.$star.']';
  $returnForm.='<hr>$resultQuery = <br>'.$resultQuery;


}

####################################### EOF #######################################
