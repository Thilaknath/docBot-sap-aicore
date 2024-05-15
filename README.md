# Infra Bot based on LLM

This bot leverages SAP AI Core specifically the Generative AI Hub in AI Core to parse and understand PDF documents, replying to Slack messages with answers extracted from the documents or using Transformer-based Language Models when it doesn't have a specific answer.

## Useful Links
| Topic  | Link  |
| --------- | --------- |
| SAP AI Core Help   | https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/   |
| Post Configuration  & Create Deployment |  https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/create-deployment-for-generative-ai-model-in-sap-ai-core  |


## Prerequisites
**Note:** *This project requires python3 and pip, The installation steps for the same and setup of virtualenv for running this project are not within the scope of this documentation. This is a POC to tryout Enhancing LLMs with RAG and Generative AI Hub SDK*

1) Enable the entitlement SAP AI Core from control centre for your global account
2) Assign the entitlement towards the sub account where you want the SAP AI Core service instane created.
3) Create a service instance followed by a service key and download the service key to a file 
4) Clone the repository
4) Initiate a virtual env with in the project directory, I used visual studio code and executed this through the UI. This could also be done using `virtualenv` 
5) Install the sap-llm-commons. Follow the steps from the SAP LLM proxy wiki linked above.

## Concept
The idea of the app is to respond to everyday infra related questions which the developers would otherwise refer to the internal wiki pages for our project. 

## Running the App 
**Note:** *This app is not production ready. Since this is a POC it is only encouraged to run this app in your local and check how it works. The app also requires a slack application which will respond to your questions. The setup of slack app is not covered here*

1. Make sure you are within your virtual environment with the correct python kernel loaded (This was tested locally using python 3.11.4)
2. Install the dependencies for the project using `pip install -r requirements.txt`
3. Start the app using `python slackApp.py` . The app will start in port `3000`
4. You need to have ngrok installed to have a temporary route to your application which you can configure in slack
5. Upon ngrol step start ngrok to listen in port `3000` using `ngrok http http://localhost:3000`
6. Configure in your slack app -> Event Subscriptions -> Request URL -> URL_FROM_NGROK/slack/events -> A challenge will be sent to your app upon which it should work
