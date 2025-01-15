# EXAMEN DOCKER SPRINT1 (13/01/2025)
## STRUCTURE DU PROJET
```bash
~/workspace/sprint1/docker/exam_PAPET
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
(sentiment_api_tests) ubuntu@ip-172-31-37-170:~$export LOG=1
(sentiment_api_tests) ubuntu@ip-172-31-37-170:~$ /usr/bin/python3 /home/ubuntu/workspace/sprint1/docker/exam_PAPET/sentiment_api_tests/tests_api_sentiments.py
```
