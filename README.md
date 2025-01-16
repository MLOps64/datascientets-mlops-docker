# EXAMEN DOCKER SPRINT1 (13/01/2025)
## PRESENTATION
```tex
Dans notre scénario, une équipe a créé une application qui permet d'utiliser un algorithme de sentiment analysis: il permet de prédire si une phrase (en anglais) a plutôt un caractère positif ou négatif. Cette API va être déployée dans un container dont l'image est pour l'instant datascientest/fastapi:1.0.0.
```
```test
Regardons les points d'entrée de notre API:
```
```test
/status renvoie 1 si l'API fonctionne
/permissions renvoie les permissions d'un utilisateur
/v1/sentiment renvoie l'analyse de sentiment en utilisant un vieux modèle
/v2/sentiment renvoie l'analyse de sentiment en utilisant un nouveau modèle
```
```tex
Le point d'entrée /status permet simplement de vérifier que l'API fonctionne bien. 
Le point d'entrée /permissions permet à quelqu'un, identifié par un username et un password de voir à quelle version du modèle il a accès. 
Enfin les deux derniers prennent une phrase en entrée, vérifie que l'utilisateur est bien identifiée, vérifie que l'utilisateur a bien le droit d'utiliser ce modèle et si c'est le cas, renvoie le score de sentiment: -1 est négatif; +1 est positif.
```
## STRUCTURE DU PROJET

$${\color{red}PS:\space  Modifier \space la \space variable \space ROOT\_PATH \space dans \space docker/script/setup.sh \space avec \space votre \space PATH  \space ou \space vous\space  avez \space  décompressé \space l'archive.}$$

```bash
ROOT_PATH=~/workspace/sprint1/docker/exam_PAPET
```
- Organisation des repertoires
```tex
~/workspace/sprint1/docker/exam_PAPET$ ls -ila
total 40
512332 drwxrwxr-x 5 ubuntu ubuntu 4096 Jan 16 15:46 .
512331 drwxrwxr-x 3 ubuntu ubuntu 4096 Jan 13 17:13 ..
512345 drwxrwxr-x 8 ubuntu ubuntu 4096 Jan 15 18:32 .git
512374 -rw-rw-r-- 1 ubuntu ubuntu  542 Jan 14 11:49 .gitignore
512333 -rw-rw-r-- 1 ubuntu ubuntu 6407 Jan 16 18:42 README.md
574338 drwxrwxr-x 4 ubuntu ubuntu 4096 Jan 16 18:09 docker
574089 -rw-rw-r-- 1 ubuntu ubuntu   89 Jan 13 22:32 requirements.txt
572027 drwxrwxr-x 6 ubuntu ubuntu 4096 Jan 13 22:18 sentiment_api_tests
```
- le repertoire sentiment_api_tests contient le projet python
```tex
~/workspace/sprint1/docker/exam_PAPET$ ls -ila sentiment_api_tests/
total 40
572027 drwxrwxr-x 6 ubuntu ubuntu  4096 Jan 13 22:18 .
512332 drwxrwxr-x 5 ubuntu ubuntu  4096 Jan 16 18:44 ..
572043 drwxrwxr-x 2 ubuntu ubuntu  4096 Jan 13 22:30 bin
572028 drwxrwxr-x 2 ubuntu ubuntu  4096 Jan 13 18:07 include
572039 drwxrwxr-x 3 ubuntu ubuntu  4096 Jan 13 22:18 lib
572042 lrwxrwxrwx 1 ubuntu ubuntu     3 Jan 13 22:18 lib64 -> lib
572044 -rw-rw-r-- 1 ubuntu ubuntu    70 Jan 13 22:18 pyvenv.cfg
572047 drwxrwxr-x 3 ubuntu ubuntu  4096 Jan 13 22:18 share
512387 -rw-rw-r-- 1 ubuntu ubuntu 11992 Jan 16 15:46 tests_api_sentiments.py
```
- le repertoire docker contient le projet docker avec un sous repertoire phyton qui contient les fichiers de construction de l'image et un sous repertoire scripts.

```tex
~/workspace/sprint1/docker/exam_PAPET$ ls -ila docker
total 36
574338 drwxrwxr-x 4 ubuntu ubuntu 4096 Jan 16 18:45 .
512332 drwxrwxr-x 5 ubuntu ubuntu 4096 Jan 16 18:44 ..
574566 -rw-rw-r-- 1 ubuntu ubuntu   73 Jan 16 13:50 .env
574339 -rw-rw-r-- 1 ubuntu ubuntu  295 Jan 16 16:54 Dockerfile
571996 -rw-r--r-- 1 root   root   3761 Jan 16 17:54 api_test.log.2025-01-16_17:52:56
574343 -rw-rw-r-- 1 ubuntu ubuntu 1988 Jan 16 16:53 docker-compose.yml
574278 -rw-rw-r-- 1 ubuntu ubuntu  995 Jan 16 18:07 log.txt
574653 drwxrwxr-x 2 ubuntu ubuntu 4096 Jan 16 12:36 python
517983 drwxrwxr-x 2 ubuntu ubuntu 4096 Jan 16 12:38 scripts
```

- Le fichier .env contient les variable pour le docker-compose.yml
```tex
FILE_LOG=/app/log/api_test.log
LOG=1
HOST=service_api_analysis
PORT=8000
```



## CREATION DEPOT GITHUB
[https://github.com/MLOps64/datascientets-mlops-docker.git]
- Sur la VM de DataScienTest
```bash
echo "EXAMEN DOCKER SPRINT1 (13/01/2025)" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/MLOps64/datascientets-mlops-docker.git
git push -u origin main
```
## MISE EN PLACE ENVIRONEMENT PROJET
- Virtual env Python
```bash
python3 -m venv sentiment_api_tests
source ./sentiment_api_tests/bin/activate
cd  ./sentiment_api_tests/
python -m pip install requests==2.32.3
python freeze > requirements.txt
```
- deactivate virtual env
```bash
deactivate
```
- Git commint and push
```bash
touch .gitignore
git add *
git commit -m 'First Commit'
git push -u origin main
```
- Test CURL PI sentiments
```bash
docker container run -p 8000:8000 datascientest/fastapi:1.0.0
netstat -tupln | grep 8000
statut=$(curl http://localhost:8000/status)
echo $statut
1
```
- Si la variable d'environement LOG == 1 alors on test, en début d'execution du script, si le fichier existe on le supprime pour initialiser l'execution.
```bash
if log is not None and log == '1':
        try:
            os.remove(file_log)
            print("LOG -> {}, remove {}".format(log,file_log))
        except  OSError as e:
            print("Remove {} Error: {}".format(file_log,e))
    else:
        log='0'
```
- Test Authentification : Attention à la variable d'environnement "LOG"sa valeur est une chaine de carratères et pas un "int".
```bash
 # TEST 1.1
    try:
        output = test_authentification(test_params_alice_auth_ok)
        if int(log) == 1:
            write_log(output)
    except Exception as e:
```
- On utilise les variables d'environnement:
    - "LOG" pour activer l'écriture des logs
    - "ROUTING_TEST' pour separer les tests
    - "FILE_LOG" pour la localisation du fichier de log
        - LOG=1 => activation
        - ROUTING_TEST=AUTHENTIFICATION => execute les tests authentification
        - ROUTING_TEST=AUTHORIZATION    => execute les tests authorisation
        - ROUTING_TEST=CONTENT          => execute les tests content
        - ROUTING_TEST=ALL or None      => execute tous les tests
```bash
export ROUTING_TEST=AUTHENTIFICATION
python3 sentiment_api_tests/tests_api_sentiments.py
    LOG => 1, ROUTING_TEST => AUTHENTIFICATION
    Lancement du test d'authentification ...
```
```bash
export ROUTING_TEST=AUTHORIZATION
python3 sentiment_api_tests/tests_api_sentiments.py
    LOG => 1, ROUTING_TEST => AUTHORIZATION
    Lancement du test d'authorization ...
```
```bash
export ROUTING_TEST=CONTENT
python3 sentiment_api_tests/tests_api_sentiments.py
LOG => 1, ROUTING_TEST => CONTENT
Lancement du test Content ...
```
```bash
export  ROUTING_TEST=ALL # or not initialized (None)
python3 sentiment_api_tests/tests_api_sentiments.py
    LOG => 1, ROUTING_TEST => ALL
    Lancement du test d'authentification ...
    Lancement du test d'authorization ...
    Lancement du test Content ...
```
- Pour la variable d'environnement "LOG", on l'initialise dans le shell qui lance le python
```bash
(sentiment_api_tests) ubuntu@ip-172-31-37-170:~$ export LOG=1
(sentiment_api_tests) ubuntu@ip-172-31-37-170:~$ /usr/bin/python3 /home/ubuntu/workspace/sprint1/docker/exam_PAPET/sentiment_api_tests/tests_api_sentiments.py
```
## DOCKER
- installation de docker-compose
```bash
sudo apt update
sudo apt install docker-compose
# aprés reconnexion au shell
docker-compose -version
docker-compose version 1.28.2, build 67630359
```
- creation de l'image à partir du Dockerfile
```bash
ubuntu@ip-172-31-37-170:~/workspace/sprint1/docker/exam_PAPET/docker$ docker build . -t e.papet/test_sentiments_analysis:1.0.0
ubuntu@ip-172-31-37-170:~/workspace/sprint1/docker/exam_PAPET/docker$ docker images -a | grep e.papet/test_sentiments_analysis
    e.papet/test_sentiments_analysis   1.0.0     ec4ef5d8197c   23 minutes ago   453MB
```
### DOCKERFILE
- Creation des repertoires /app (WORKDIR), /app/python (SRC python), /app/ (LOG)
- On auriat pu lancer le scrip python avec un autre USER que root, il aurai falu vers un chown sur les repertoires créés.

### DOCKER-COMPOSE
- Il créé l'ensemble des networks et le volume data partagé par les 3 containers de test
- Il ordonance l'execution des 3 tests par l'option depand_on:
```bash
    depends_on:
      - api_service
      - test_authentification
```
- Creation de 2 network pour la segrégation des reseaux
```bash
networks:
  client_analysis:
    driver: bridge
    ipam:
      driver: default
      config:
        - subnet: 172.22.0.0/16
  service_analysis:
    driver: bridge
    ipam:
      driver: default
      config:
        - subnet: 172.21.0.0/16
```

- L'image est la même pour les 3 containers de test.
- La variable d'environement ROUTING_TEST permet au containers d'executer les bons test.
```tex
    environment:
      LOG: $LOG
      ROUTING_TEST: AUTHORIZATION
      FILE_LOG: $FILE_LOG
      HOST: $HOST
      PORT: $PORT
```
- les valeurs de la variable ROUTING_TEST :
    - AUTHENTIFICATION permet d'executer les tests Authentification 
    - AUTHORIZATION permet d'executer les tests Authorization 
    - CONTENT permet d'executer les tests CONTENT
    - ALL permet d'executer l'ensemble des tests 

## INSTALLATION
- Avant de lancer le script docker/scripts/setup.sh il faut éditer le script et modifier la variable ROOT_PATH
```bash
# PATH TO Docker repository [modified with your path]
ROOT_PATH=~/workspace/sprint1/docker/exam_PAPET
```
- Le script docker/scripts/setup.sh supprime tous les containers, volumes, images, network
```bash
# Remove all containers images volumes network for copy new sources
docker-compose -f $ROOT_PATH/docker/docker-compose.yml down >>$FILE_LOG 2>&1
docker system prune --volumes -f >>$FILE_LOG 2>&1
```
- Il construit l'image
```bash
# option --no-cache force to recreate all layer's image
cd $ROOT_PATH/docker && docker build --no-cache=true . -t e.papet/test_sentiments_analysis:1.0.0 >>$FILE_LOG 2>&1

```
- En fin d'execution il copie le fichier log qui se trouve dans le repertoire partagé dans le repertoire docker avec la date d'execution du test.
```bash
# Verify Volume
volume=$(docker volume inspect --format '{{ .Mountpoint }}' docker_volume_data)
sudo ls -ilarth $volume/log >>$FILE_LOG 2>&1
# cp api_test.log to ROOT_PATH
sudo cp $volume/log/api_test.log $ROOT_PATH/docker/api_test.log.${CURRENTDATE} >>$FILE_LOG 2>&1
sudo chmod 644 $ROOT_PATH/docker/api_test.log.${CURRENTDATE}
echo "File log test is located on $ROOT_PATH/docker/api_test.log.${CURRENTDATE}"

```

