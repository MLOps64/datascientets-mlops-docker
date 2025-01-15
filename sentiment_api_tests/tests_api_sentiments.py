import os
import requests
import json
import datetime

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

# GLOBAL Variable
#file_log = '/home/ubuntu/workspace/sprint1/docker/exam_PAPET/log/api_test.log'
file_log = None
default_log_path = '/home/ubuntu/workspace/sprint1/docker/exam_PAPET/api_test.log'
api_address = 'localhost'
api_port = 8000

# Write message ito log file
def write_log(message):
    try:
        #if os.environ.get('LOG') == 1:
        with open(file_log, 'a') as file:
            file.write(message)
    except  Exception as ex:
        print("Error write_log Exception: {} ".format(ex))
        raise e
    
# generic function for perform request
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
    
# Authentification Test Function
def test_authentification(action,test_params):
    test_status = 'SUCCESS'
    try:
        res = perform_request('GET','http',api_address,api_port,action,test_params)
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

==>  HTTP status {test_status}:{status_code}

'''.format(status_code=status_code,test_status=test_status,username=test_params['username'], password=test_params['password'],action=action)
    return output

# Authorisation Test Function
def test_authorization(action,test_params):
    test_status = 'SUCCESS'
    test_auth = 'Authorise'
    score = None
    #print(test_params)
    try:
        res = perform_request('GET','http',api_address,api_port,action,test_params)
    except Exception as e:
        raise e
    #
    #print(json.loads(res.content)['score'])
    try:
        score = json.loads(res.content)['score']
    except Exception as e :
        score = 'Not Authorize'
    #
    status_code = res.status_code
    #
    if not status_code == int(test_params['code_expected']):
        test_status = 'FAILURE'
        test_auth = 'Not Authorize'
    output = '''
============================
    Authorization test
============================

request done at {action}
| username = {username}
| password = {password}
| sentence = {sentence}
| score    = {score}


expected result = {code_expected}
actual restult = {status_code}

==>  HTTP Status : {test_status}:{status_code} / Authorisation : {test_auth}
'''.format(status_code=status_code,test_status=test_status,username=test_params['username'], password=test_params['password'],sentence=test_params['sentence'],test_auth=test_auth,code_expected=test_params['code_expected'],action=action,score=score)
    return output
    
# Content Test Function
def test_content(action,test_params):
    test_status = 'SUCCESS'
    test_auth = 'Authorise'
    score = None
    test_score = 'FAILURE'
    #print(test_params)
    try:
        res = perform_request('GET','http',api_address,api_port,action,test_params)
    except Exception as e:
        raise e
    #
    #print(json.loads(res.content)['score'])
    try:
        score = json.loads(res.content)['score']
    except Exception as e :
        pass
    #
    status_code = res.status_code
    #
    if (score is not None and test_params['test_score'] == '>' and score > 0) or (score is not None and test_params['test_score'] == '<' and score < 0):
        test_score = 'SUCCESS'

    #
    if not status_code == int(test_params['code_expected']):
        test_status = 'FAILURE'
        test_auth = 'Not Authorize'
    output = '''
============================
    Content test
============================

request done at {action}
| username      = {username}
| password      = {password}
| sentence      = {sentence}
| score         = {score}
| test score    = {test_score}


expected result = {code_expected}
actual restult = {status_code}

==>  HTTP Status : {test_status}:{status_code} / Authorisation : {test_auth}

'''.format(status_code=status_code,test_status=test_status,username=test_params['username'], password=test_params['password'],sentence=test_params['sentence'],test_auth=test_auth,code_expected=test_params['code_expected'],test_score=test_score,action=action,score=score)
    return output

# main Function
if __name__ == "__main__":  
    # test environement
    #for key, value in os.environ.items():
        #print('{}: {}'.format(key, value))

    # Type of environement variable is STRING

    # if ROUTING_TEST == ['AUTHENTIFICATION' or 'AUTHORIZATION' or 'CONTENT' or 'ALL' ]
    routing_test = os.environ.get('ROUTING_TEST')
    # secure execution
    if routing_test is None or routing_test not in ('AUTHENTIFICATION', 'AUTHORIZATION', 'CONTENT', 'ALL'):
        routing_test = 'ALL'
    
    # if LOG = 1 trace is write into api_test.log
    log = os.environ.get('LOG')
    file_log = os.environ.get('FILE_LOG')
    # New test if exit file ./api_test.log delete it after.
    if log is not None and log == '1':
        if file_log is None:
            file_log = default_log_path
        try:
            if os.path.isfile(file_log):
                os.remove(file_log)
            os.mknod(file_log)
            write_log(str(datetime.datetime.now()),)
        except  OSError as e:
            print("=> Remove {} Error: {}".format(file_log,e))
    else:
        log='0'

    # print OS variable
    print("=> LOG: {} / FILE_LOG: {} / ROUTING_TEST: {}".format(log,file_log,routing_test))    

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

    # AUTHENTIFICATION TEST
    if routing_test in ('AUTHENTIFICATION', 'ALL'):
        print("Lancement des tests d'authentification ...")
        # TEST 1.1
        try:
            output = test_authentification('/permissions',test_params_alice_auth_ok)
            if int(log) == 1:
                write_log(output)
        except Exception as e:
            print(" Error authentification: {}".format(e))
        # TEST 1.2
        try:
            output = test_authentification('/permissions',test_params_bob_auth_ok)
            if int(log) == 1:
                write_log(output)
        except Exception as e:
            print(" Error authentification: {}".format(e))
        # TEST 1.3
        try:
            output = test_authentification('/permissions',test_params_auth_ko)
            if int(log) == 1:
                write_log(output)
        except Exception as e:
            print(" Error authentification: {}".format(e))

    # AUTHORIZATION TEST
    if routing_test in ('AUTHORIZATION', 'ALL'):
        print("Lancement des tests d'authorization ...")
        # TEST 2.1
        try:
            test_params_alice_auth_ok['sentence'] = 'life is beautiful'
            test_params_alice_auth_ok['code_expected'] = 200
            output = test_authorization('/v1/sentiment',test_params_alice_auth_ok)
            if int(log) == 1:
                write_log(output)
        except Exception as e:
            print(" Error authentification: {}".format(e))

        # TEST 2.2
        try:
            test_params_alice_auth_ok['sentence'] = 'life is beautiful'
            test_params_alice_auth_ok['code_expected'] = 200
            output = test_authorization('/v2/sentiment',test_params_alice_auth_ok)
            if int(log) == 1:
                write_log(output)
        except Exception as e:
            print(" Error authentification: {}".format(e))

        # TEST 2.3
        try:
            test_params_bob_auth_ok['sentence'] = 'life is beautiful'
            test_params_bob_auth_ok['code_expected'] = 200
            output = test_authorization('/v1/sentiment',test_params_bob_auth_ok)
            if int(log) == 1:
                write_log(output)
        except Exception as e:
            print(" Error authentification: {}".format(e))

        # TEST 2.4
        try:
            test_params_bob_auth_ok['sentence'] = 'life is beautiful'
            test_params_bob_auth_ok['code_expected'] = 200
            output = test_authorization('/v2/sentiment',test_params_bob_auth_ok)
            if int(log) == 1:
                write_log(output)
        except Exception as e:
            print(" Error authentification: {}".format(e))

    # CONTENT TEST
    if routing_test in ('CONTENT', 'ALL'):
        print("Lancement des tests de content ...")
        # TEST 3.1
        try:
            test_params_bob_auth_ok['sentence'] = 'life is beautiful'
            test_params_bob_auth_ok['code_expected'] = 200
            test_params_bob_auth_ok['test_score'] = '>'
            output = test_content('/v1/sentiment',test_params_bob_auth_ok)
            if int(log) == 1:
                write_log(output)
        except Exception as e:
            print(" Error authentification: {}".format(e))

        # TEST 3.2
        try:
            test_params_bob_auth_ok['sentence'] = 'that sucks'
            test_params_bob_auth_ok['code_expected'] = 200
            test_params_bob_auth_ok['test_score'] = '<'
            output = test_content('/v1/sentiment',test_params_bob_auth_ok)
            if int(log) == 1:
                write_log(output)
        except Exception as e:
            print(" Error authentification: {}".format(e))

