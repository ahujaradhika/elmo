from __future__ import print_function
import json, uuid
from ibm_watson import AssistantV2

ASSISTANT_IAM_APIKEY = 

def load_credential(authfile = None):
    if authfile == None:
        authfile = 'ibm-credentials.env'

    with open(authfile) as f:
        cred = {}
        for line in f:
            parts = line.strip('\r').strip('\n').split("=")
            
            if len(parts) == 2:
                cred[parts[0]] = parts[1]
        return cred;

    return None

def create_elmo(credential):
    # If service instance provides API key authentication
    return AssistantV2(
               version='2018-09-20',
               # url is optional, and defaults to the URL below. Use the correct URL for your region.
               url='https://gateway.watsonplatform.net/assistant/api',
               iam_apikey=credential['ASSISTANT_IAM_APIKEY'])

#########################
# Sessions
#########################
def create_session(assistant, ass_id):
    session = assistant.create_session(ass_id).get_result()
    print(json.dumps(session, indent=2))
    return session

def delete_session(assistant, ass_id, sess_id):
    return assistant.delete_session(ass_id, sess_id).get_result()

#########################
# Message
#########################
def send_message(assistant, ass_id, sess_id, msg):
    message = assistant.message(
        ass_id,
        sess_id,
        input={'text': msg}, #'What\'s the weather like?'},
        context={
            'metadata': {
                'deployment': 'myDeployment'
            }
        }).get_result()
    #print(json.dumps(message, indent=2))
    return message['output']['generic'][0]['text']

if __name__ == '__main__':
    credential = load_credential()

    if not credential:
        pass

    elmo = create_elmo(credential)
    ass_id = "70f87349-4762-41fb-a263-5dfc9626ad53"
    sess_id = create_session(elmo, ass_id)["session_id"]

    dialog = "hello"
    msg = ""
    while not "bye" in msg.lower() and not "see you" in msg.lower():
        msg = send_message(elmo, ass_id, sess_id, dialog)
        dialog = input("Elmo: %s\nMe: " %(msg.strip('\r').strip('\n')))

    delete_session(elmo, ass_id, sess_id)
