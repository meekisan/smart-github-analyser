<?php
/**
############################## GESTION FORMULAIRE POST ##############################
####################################### START #######################################
**/
//pour les erreurs
ini_set('display_errors', 1);


######### VARIABLES NON LIEES AU POST
//nom de ma page
$urlPage     = 'index.php'; //http://localhost/index.php
//nb de star minimale à prendre en compte
$nbStar     = 3;
//texte par defaut du formulaire
$txtSearchDefault = "Cliquez ici pour saisir votre recherche d'au moins 1 caractère";
$search = $txtSearchDefault;

$sizeLangue         = 5;//nb de langue par defaut visible dans le menu
$sizeLangueMax      = 30;//nb de langue max visible dans le menu


//pour neo4j
//les lib
require_once 'vendor/autoload.php';
//ClientBuilder
use GraphAware\Neo4j\Client\ClientBuilder;
//connexion à neo4j
$client = ClientBuilder::create()
    ->addConnection('default', 'http://neo4j:neo@recommandation:7474')
    ->build();

//action liées au post
$returnForm         = '';
$optionStar         = '';
$optionLangues      = '';
$optionLanguesAutre = '';
$optionUsers        = '';
$user               = '';
$langue             = '';
$star               = 0;

//actions liées au POST
if ($_POST) {
  $action = (isset($_POST['action'])) ? ((preg_replace('[^0-9]','',$_POST['action']) > 0) ? preg_replace('[^0-9]','',$_POST['action']) : 0) : 0;
  if ($action==1) include("form_search_posted.php");
  elseif($action==2) include("form_reco_posted.php");
  }

//  MATCH (n:Repo)-[r]-(m) RETURN DISTINCT type(r) AS laRelation
//  control-center/serviced


//query pour obtenir les users
/*$query = 'MATCH (n:User) WHERE n.name <> "papy" RETURN n.name as name, n.login as login';
$result = $client->run($query);
foreach ($result->getRecords() as $record) {
    $lename  = sprintf($record->value('name'));
    $lelogin = sprintf($record->value('login'));
    $selected = ($lelogin==$user) ? ' checked="checked"' : '';
    $optionUsers.='<input type="radio" name="nameUser" value="'.$lelogin.'" style="width:10px;"'.$selected.' /><label style="margin-right:30px;">'.$lename.'</label> ';
  }
  */
//AFFICHER LES RELATIONS POSSIBLES
//query pour obtenir les users
$query = 'MATCH (n:Repo)-[r]-(m) RETURN DISTINCT type(r) AS laRelation;';
$result = $client->run($query);
$num = 0;
$laRelation = '';
foreach ($result->getRecords() as $record) {
    $num++;
    $laRelation.= ($num==1) ? ':'.sprintf($record->value('laRelation')) : '|:'.sprintf($record->value('laRelation'));

    //$optionUsers.='<input type="radio" name="nameUser" value="'.$lelogin.'" style="width:10px;"'.$selected.' /><label style="margin-right:30px;">'.$lename.'</label> ';
  }
  //echo 'Les relations des repo sont <=> '.$laRelation.'<hr>';
//  MATCH (u:User{login:"Gracianne"})-[:LIKE|:WORK|:FOLLOW|:OWN]->(r:Repo) RETURN DISTINCT r.name



//query pour obtenir les langues
$query = 'MATCH (n:Languages) WHERE (toInt(n.size) > 1) AND n.language <> "null" RETURN n.language as language, n.size as size ORDER BY toInt(n.size) DESC';
$result = $client->run($query);
$nbLanges = 0;
$autresLangues = '';
foreach ($result->getRecords() as $record) {
    $nbLanges++;
    $lename = sprintf($record->value('language'));
    $lasize = sprintf($record->value('size'));
    $selected = (strpos(','.$langue,','.$lename)!==false) ? ' selected="$selected"' : '';
    $sizeLangue = ($selected != '') ? 30 : $sizeLangue;
    //pour avoir les 50 premières langues
    if ($nbLanges <=50) $optionLangues.= '<option value="'.$lename.'"'.$selected.'>'.(($lename=='null') ? 'Aucune langue' : $lename).' ('.number_format($lasize,0, ',', '.').' files)</option>';
    //pour avoir toutes les langues
    $autresLangues[$lename]= $lasize;
  }
//trier le tableau $autresLangues par ordre alphabétique
/*@ksort($autresLangues);
foreach ($autresLangues as $key => $val) {
    $optionLanguesAutre.= '<option value="'.$key.'">'.$key.' ('.number_format($val,0, ',', '.').' files)</option>';
}

//POUR LES STARS
for ($i = 1; $i <= $nbStar; $i++) {
  $selected = ($i==$star) ? ' selected="selected"' : '';
  $txt = ($i ==1) ? 'Peu : moins de 10' : (($i ==2) ? 'Intermédiaire : entre 11 et 10.000' : (($i ==3) ? 'Populaire : Plus de 10.000' : 'OUPS $star max est 3'));
  $optionStar.='<option value="'.$i.'"'.$selected.' />'.$txt.'</option>';
}*/

/**
SUPER POUR TROUVER LES USER QUI TRAVAIL SUR LES MEMES LANGUAGES

START s=node(Joe)
MATCH s-[:FRIEND]-()-[:FRIEND]-fof, s-[:LIKES]-()-[:LIKES]-fof
WHERE s != fof
RETURN fof

*/


//FORMULAIRE
$menuForm = '<form action="'.$urlPage.'" method="post" name="F1" style="border:1px solid red">
   <input type="hidden" name="action" value="1" />
   <table>
   <tr>
     <td>Recommandation pour<sup style="color:red">*</sup></td>
     <td>:</td>
     <td>
        <input type="text" name="worker_login"><br>
      </td>
   </tr>
   <tr>
     <td>Recommandation type<sup style="color:red">*</sup></td>
     <td>:</td>
     <td><select id="type" name="type">
          <option value="WORK">Work</option>
          <option value="STAR">Star</option>
         </select></td>
     </tr>
   <tr>
     <td>Star</td>
     <td>:</td>
     <td>
      <input type="text" name="star"><br>
     </td>
   </tr>
   <tr>
     <td>Langues</td>
     <td>:</td>
     <td>
     <input type="text" name="language"><br>
     </td>
    </tr>
    <tr>
      <td colspan="2">&nbsp;</td>
      <td><input name="ok" value="recommandation" type="button" onclick="verifUpload1(F1)" class="button" /></td>
    </tr>
  </table>
</form>';

//le moteur de recommandation
$menuForm2 = '<form action="'.$urlPage.'" method="post" name="F2" style="border:1px solid red">
   <input type="hidden" name="action" value="2" />
   <table>
   <tr>
     <td>Recommandation pour<sup style="color:red">*</sup></td>
     <td>:</td>
     <td>
        <input type="text" name="worker_login"><br>
      </td>
   </tr>
   <tr>
     <td colspan="2">&nbsp;</td>
     <td><input name="ok" value="Vas recommander toto" type="button" onclick="verifUpload2(F2)" class="button" /></td>
   </tr>
  </table>
</form>';

//===AFFICHAGE
$searchDefault = "Cliquez ici pour saisir votre recherche d'au moins 1 caractère";
echo '<!doctype html><html itemscope="" itemtype="http://schema.org/WebPage" lang="fr">
<head>
 <title>Moteur de Recommandation</title>
 <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
 <meta http-equiv="Content-Language" content="FR" />
 <link rel="stylesheet" type="text/css" href="css/style.css" />
 <style>
  td {align:justify;valign:top;}
 </style>
 <script language="javascript" type="text/javascript">

 function verifUpload1() {
   var clic=0;
   var message="";
   var vall = document.F1.worker_login.value;
   if (vall == "") message+="Merci de saisir votre login.\n";
   else if (vall == "'.$searchDefault.'") message+="Merci de saisir au moins 1 caractère.\n";
   if (message != "") alert(message);
   else {
     clic++;
     if (clic==1) document.F1.submit();
     else alert("Votre demande est en cours de traitement. Merci de bien vouloir patienter.");
   }
 }
 function verifUpload2 (F2) {
   var clic=0;
   var message="";
   //var vall = document.F2.getElementById("worker_login").checked;
   //if (vall == "false") message+="Merci de sélectionner un user.\n";
   if (message != "") alert(message);
   else {
     clic++;
     if (clic==1) document.F2.submit();
     else alert("Votre demande est en cours de traitement. Merci de bien vouloir patienter.");
   }
  }
 function nettoyer(ele,vall) {
   if (ele=="nameSearch" && vall=="'.$searchDefault.'") return document.F1.nameSearch.value = "";
 }
 function heightPlus(ele,vall) {
    if (ele=="nameLangue" && vall !="") {
      var l = document.getElementById(ele);
      l.setAttribute("size",'.$sizeLangueMax.');
    }
 }
</script>
</head>
<body>
  <h1>Moteur de Recommandation</h1>
  '.$menuForm.'
  '.$returnForm.'
</body>
</html>';



####################################### EOF #######################################
