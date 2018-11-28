# Dialogflow Integration with Snatchbot using Python

[Snatchbot](https://snatchbot.me/) is a one of the popular chatbot development platform where user can easily create chatbot for their purpose and integrate on multiple channels.

To take advantage of powerful NLP provided by [Dialogflow](https://dialogflow.com/) this script is created to provide bridge between Dialogflow and Snatchbot responses.

It is a Flask based script in Python which uses Dialogflow SDK. It accepts request from Snatchbot, passes on to Dialogflow, get response from Dialogflow and pass it back to Snatchbot with Snatchbot compatible JSON.

## Steps for integration
1. Get your **Agent Project Id** from Dialogflow console.

![Project ID](https://raw.githubusercontent.com/pragnakalp/dialogflow-connector-for-snatchbot-using-python/master/images/project_id.png)

2. Download **Service Account Credential file** from GCP.

![Service Account](https://raw.githubusercontent.com/pragnakalp/dialogflow-connector-for-snatchbot-using-python/master/images/service_account.png)

3. Enter the file path downloaded above in the app.py file on line number 16.

4. Run your code using Ngrok if you are using this integrator from local machine and copy the Ngrok url.

![Run Ngrok](https://raw.githubusercontent.com/pragnakalp/dialogflow-connector-for-snatchbot-using-python/master/images/run_ngrok.png)

![Ngrok](https://raw.githubusercontent.com/pragnakalp/dialogflow-connector-for-snatchbot-using-python/master/images/ngrok.png)

5. Go to your snatchbot account and create a new bot or select existing bot. 

6. In the bot create new interaction of JSON API type. 
![Select JSON API interaction](https://raw.githubusercontent.com/pragnakalp/dialogflow-connector-for-snatchbot-using-python/master/images/select-json-api-interaction.png)

7. In the JSON API interaction set the **API Address** of ngrok obtained in 4th step. Also, set the **Error Message** so that if snatchbot is not able to connect to your API URL then it will display this error message.
![Set API URL](https://raw.githubusercontent.com/pragnakalp/dialogflow-connector-for-snatchbot-using-python/master/images/set-api-url.png)

8. You're done! Now, when this JSON API interaction is called in your chat flow, it will make request to Dialogflow and fetch response from there.

#### This script is still work in progress and more features will be added in future. You are welcome to fork it and add more changes.

> Developed by [Pragnakalp Solutions - Chatbots Development(Dialogflow, Snatchbot, Chatfuel), Python Development](https://pragnakalp.com/)

