/ ** DESCRIPTION DU CONTENU DU FICHIER README ** /

* A quoi sert la lib. 
* Comment l’installer.
* Un exempe concret d’utilisation.
* La licence d’utilisation.
* Un lien vers la doc si elle existe.

CENTREON BOT Lib - afficher le status des hosts et services et faire aussi des aquitement sur centreon
============================================================================================

Ce module centreon_bot_telegram permet de connaitre le status et de faire le aquitements 
des services et les hosts present sur la plate forme de supervision centreon
----------------------------------------------------------------------------------------------------
    Information a renseigner avant l'utilisation du bot telegram
    ============================================================
    
* BOT_TOKEN : le token qui delivre telegram apres creation du bot sur telegram (BotFather)
* URL_CENTREON : le a votre plateforme centreon (http://adresse-server-centreon/centreon/api/index.php)
* AUTH_URL : l'url pour recuperé le token que fournir centreon en ajoutant le surfixe (URL_CENTREON + '?action=authenticate')
* USERNAME_CENTREON :  nom d'utilisation de centreon
* PASSWORD_CENTREON : mot de passe de centreon

    Instalation du packeges
    =======================
    pip install -r requirements.txt
    python setup.py install
    
    
Exemple d'utilisation : 
    
    >>> from centreon_bot_telegram import starter
    >>> starter.starters()
    
Ce code est sous la licence WTFPL

GNU GPL: 
   * La liberté d'exécuter le logiciel, pour n'importe quel usage ;
   * La liberté d'étudier le fonctionnement d'un programme et de l'adapter à ses besoins, ce qui passe par l'accès aux codes sources ;
   * La liberté de redistribuer des copies ;
   * L'obligation de faire bénéficier à la communauté des versions modifiées.
    