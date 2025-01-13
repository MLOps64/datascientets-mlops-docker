import os
import requests
"""
    Objet  : Script python de test de l'API sentiment : datascientest/fastapi:1.0.0
    Auteur : <e.papet64@gmail.com>
    Date   : 13/01/2025
    ENPOINTS :
     ./status 
     ./permissions
     ./vi/sentiment
     ./v2/sentiment
"""

file_log = './api_test.log'
api_address = 'localhost'
api_port = 8000

def write_log(message):
    try:
        #if os.environ.get('LOG') == 1:
        with open(file_log, 'a') as file:
            file.write(message)
    except  Exception as ex:
        print("Error write_log Exception: {} ".format(ex))
        raise e

def perform_request(method,protocol,address,port,action,test_params):
    try:
        req = requests.request(method, "{}://{}:{}{}".format(protocol,address,port,action),params=test_params)
        return req
    except requests.RequestException as rex:
        print("Error RequestExcetion: {} ".format(rex))
        raise rex
    except Exception as ex:
        print("Error Excetion: {} ".format(ex))
        raise ex
    

        

def test_authentification(test_params):
    test_status = 'SUCCESS'
    print("Lancement du test d'authentification ...")
    try:
        res = perform_request('GET','http',api_address,api_port,"/permissions",test_params)
    except Exception as e:
        raise e
    #
    status_code = res.status_code
    if not status_code == 200:
        test_status = 'FAILURE'
    output = '''
============================
    Authentication test
============================

request done at {action}
| username={username}
| password={password}

expected result = 200
actual restult = {status_code}

==>  {test_status}

'''.format(status_code=status_code,test_status=test_status,username=test_params['username'], password=test_params['password'],action='/permission')
    return output

def test_authorzaition():
    print("Lancement du test d'authorization ...")

def test_content():
    print("Lancement du test de content ...")

# main
if __name__ == "__main__":  
    # test environement
    #for key, value in os.environ.items():
        #print('{}: {}'.format(key, value))

    # attention les valeurs des varibales d'environement sont des STRING
    log = os.environ.get('LOG')

    # New test if exit file ./api_test.log delete it after.
    if log is not None and log == '1':
        try:
            os.remove(file_log)
            print("LOG -> {}, remove {}".format(log,file_log))
        except  OSError as e:
            print("Remove {} Error: {}".format(file_log,e))
    else:
        log='0'
        
    # Crendential
    test_params_alice_auth_ok =  {
        'username': 'alice',
        'password': 'wonderland'
    }
    # 
    test_params_bob_auth_ok =  {
        'username': 'bob',
        'password': 'builder'
    }
    #
    test_params_auth_ko =  {
        'username': 'alice',
        'password': 'clementine'
    }
    # TEST 1.1
    try:
        output = test_authentification(test_params_alice_auth_ok)
        if int(log) == 1:
            write_log(output)
    except Exception as e:
        print(" Error authentification: {}".format(e))
    # TEST 1.2
    try:
        output = test_authentification(test_params_bob_auth_ok)
        if int(log) == 1:
            write_log(output)
    except Exception as e:
        print(" Error authentification: {}".format(e))
    # TEST 1.3
    try:
        output = test_authentification(test_params_auth_ko)
        if int(log) == 1:
            write_log(output)
    except Exception as e:
        print(" Error authentification: {}".format(e))