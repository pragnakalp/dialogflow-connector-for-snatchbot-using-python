# flask modules
from flask import Flask, render_template, request, make_response, jsonify
# dialogflow python SDK
import dialogflow_v2 as dialogflow
# requests modulw
import requests
# UUID to generate session ids
import uuid
# JSON
import json
# CSV
import csv
# OS module
import os
# add the credential file to environment variables
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="<Enter SERVICE ACCOUNT JSON path here>"

# Flask app initialization
app = Flask(__name__)

# function to detect intent using text with the help of Dialogflow SDK
# project_id - Id of the Dialogflow Agent
# session_id - Id of the user's session
# language_code - language to be use (default: en)
def detect_intent_texts(project_id, session_id, texts, language_code, user_id, bot_id, module_id):
    
    text = texts[0]

    # create a session client
    session_client = dialogflow.SessionsClient()

    # create a session
    session = session_client.session_path(project_id, session_id)        

    main_response = {}
    
    if text != "":        
        # create the text input object
        text_input = dialogflow.types.TextInput(text=text, language_code=language_code)

        # create query input object
        query_input = dialogflow.types.QueryInput(text=text_input)

        # call detect_intent function to get the response json (DetectIntentResponse object)
        response = session_client.detect_intent(session=session, query_input=query_input, timeout=20)        

        # store all the fulfillment messages into a list
        responses = response.query_result.fulfillment_messages

        # create a copy for future reuse
        df_response = response
        
        # snatchbot response
        messages = {
            "user_id": str(user_id),
            "bot_id": str(bot_id),
            "module_id": str(module_id),
            "message": ""
        }

        # iterate through responses from dialogfow
        for i, response in enumerate(responses):
            # choose FB responses
            if response.platform == 1:
                # if the response is text
                if response.text.text is not None:
                    try:
                        if response.text.text[0] != "":
                            if messages['message'] != "":
                                # ::next:: is used for new Snatchbot Instant text (new chat bubble)
                                messages['message'] += "\n::next::\n" + response.text.text[0]
                            else:
                                messages['message'] = response.text.text[0]
                    except:
                        pass

                # if response is quick reply
                if response.quick_replies is not None:
                    quick_reply_title = response.quick_replies.title
                    quick_reply_data = response.quick_replies.quick_replies

                    quick_replies = []
                    for qr in quick_reply_data:
                        quick_replies.append(qr)

                    messages['suggested_replies'] = quick_replies

        # if the message is empty
        if messages['message'] != "":
            main_response = messages
        else:
            messages["message"] = df_response.query_result.fulfillment_text
            main_response = messages
    else:
        # build an error
        main_response = {
            "message": "Sorry, no input detected !"
        }

    # print(main_response)
    return main_response        

# function to get the response from the dialogflow SDK


def get_dialogflow_response(dialogflow_project_id, message, user_id, bot_id, module_id, session_id):

    session_id = ""
    # create a blank file and add the path below
    sessions_file_path = "<enter sessions.csv file path>"
    # open the file read mode
    csvfile = open(sessions_file_path, 'r')
    # creating a csv reader object
    csvreader = csv.reader(csvfile, delimiter=",")
    # iterate through rows
    for row in csvreader:
        if row[0] == str(user_id):
            session_id = str(row[1])
            break

    # if session available
    if session_id == "":
        session_id = str(uuid.uuid4())
        csvfile.close()
        
        csvfile = open(sessions_file_path, 'a')
        # creating a csv reader object
        csvwriter = csv.writer(csvfile, delimiter=",", lineterminator="\n")
        csvwriter.writerow([str(user_id), session_id])

    # call the detect_intent_texts functions and pass the project ID, session_id, messenger_user_input, 'en-US'
    response = detect_intent_texts(dialogflow_project_id, session_id, [message], 'en-US', user_id, bot_id, module_id)
    
    # return response
    return response

# main flask python route
@app.route('/', methods=['POST', 'GET'])
def index():
    
    dialogflow_project_id = "<ENTER YOUR DIALOGFLOW AGENT ID>"

    # snatchbot parameters
    user_id = request.form.get('user_id')
    bot_id = request.form.get('bot_id')
    module_id = request.form.get('module_id')
    session_id = request.form.get('session_id')
    message = request.form.get('incoming_message')

    # call the get_dialogflow_response, this will return a chatfuel JSON    
    response = get_dialogflow_response(dialogflow_project_id, message, user_id, bot_id, module_id, session_id)

    # return the main chatfuel JSON to
    return make_response(jsonify(response))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
 
