import logging
import time
import os
from slack_sdk.web import WebClient
from slack_sdk.rtm_v2 import RTMClient
from flask import Flask, request, make_response
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.document_loaders import PyPDFLoader
from langchain.chains.question_answering import load_qa_chain

from gen_ai_hub.proxy.langchain.init_models import init_llm

app = Flask(__name__)

# Create a logger object
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)

# Create a file handler
handler = logging.FileHandler('app.log')
handler.setLevel(logging.DEBUG)

logger.addHandler(handler)

# Initialize event_counter
event_counter = 0

processed_event_ids = set()

docs = [
    "testData/kubernetes.pdf",
    "testData/argo.pdf",
    "testData/flux.pdf",
    "testData/opentelemetry.pdf",
]

slack_token = os.getenv('SLACK_TOKEN')
rtm_client = RTMClient(token=slack_token)
web_client = WebClient(token=slack_token)


# Your function which takes question, answers from QA model
def model(question):

    loaders = [ PyPDFLoader(doc) for doc in docs]
    documents = []
    for loader in loaders:
        documents.extend(loader.load())
    # documents population from the loaded PDFs - remains the same
    chainpdf = load_qa_chain(llm=init_llm('gpt-4', max_tokens=100), chain_type="stuff")
    answer = chainpdf.run(input_documents=documents, question=question)
    # Call your model function here and get the response
    # return the answer 

    return answer

# The address Slack will use to send event data
@app.route("/slack/events", methods=["POST"])
def slack_events():
    global event_counter
    received_time = time.time()
    data = request.get_json()
    event_id = data.get('event_id')
    logger.info('Event ID: %s', event_id)

      # Output the entire request data to the log
    logger.debug('Received request data: %s' % data)

    # Increment the event counter
    event_counter += 1
    logger.info('Event count: %s' % event_counter)

    if "challenge" in data:
        return make_response(data.get("challenge"), 200, {"content_type": "application/json"})
    if 'event' in data: 
        event_data = data['event']
         # avoid bot's own message
        if event_data.get("subtype") != "bot_message" and event_id not in processed_event_ids:
            processed_event_ids.add(event_id)
            if 'text' in event_data:
                question = event_data['text']
                channel_id = event_data['channel']
                
                answer = model(question)  # replace with your implementation
                web_client.chat_postMessage(channel=channel_id, text=answer)

    response = make_response("data processed", 200,)
    response_time = time.time() - received_time
    logger.info('Time taken to process the request: %s seconds' % response_time)
    return response

@app.after_request
def after_request(response):
    header_info = response.headers  # This is a dictionary with headers info.
    logger.debug('Response Header: %s' % header_info)
    return response

if __name__ == "__main__":
    app.run(port=3000)