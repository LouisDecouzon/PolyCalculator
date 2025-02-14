# PolyCalculator
Readme pour la partie Application
On a deux fichiers pythons : un back(API) pour réceptionner les demandes de calcul de la part du front qui se compose exclusivement d'une page html contenant la calculatrice, un peu de css ainsi qu'un fichier javascript pour envoyer les demandes de calcul à l'API; et récupérer le résultat des calculs via redis qui ont été mis là précédemment par le consumer (le deuxième fichier python) qui lui a eu accès aux calculs dans un premier temps grâce à l'API par rabbitMQ.
Donc pour résumer, le chemin suivi par le calcul est le suivant :
-Demande du calcul sur la page html
-Réception par l'API et mise en file d'attente dans rabbitMQ
-Le consumer récupère le calul, le traite et stocke le résultat dans une liste redis, c'est ici que j'ai dévié des instructions du sujet en n'utilisant pas de système d'ID pour les calculs. J'ai eu cependant un problème de délai dans l'affichage des résultats puisque c'est le résultat de l'opération n-1 qui est renvoyé lorsque c'est la n qui est demandé.
-L'API prend le calcul de redis et l'envoie à la page html. Ici, j'ai un problème de tranmission et/ou d'affichage puisque le je ne parviens pas à afficher le resultat dans le champ prévu à cet effet.
