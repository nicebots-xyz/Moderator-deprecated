from googleapiclient import discovery
# Import perspective_api_key from the config.py file
from config import perspective_api_key, toxicity_names, toxicity_definitions
# Import the re module to use regular expressions
import re

# Create an instance of the API client
client = discovery.build("commentanalyzer",
                            "v1alpha1",
                            developerKey=perspective_api_key,
                            discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
                            static_discovery=False,
                        )

analyze_request = {
    'comment': {'text': ''},
    'requestedAttributes': {'TOXICITY': {}, 'SEVERE_TOXICITY': {}, 'IDENTITY_ATTACK': {}, 'INSULT': {}, 'PROFANITY': {}, 'THREAT': {}, 'SEXUALLY_EXPLICIT': {}, 'FLIRTATION': {}, 'OBSCENE': {}, 'SPAM': {}},
    'languages': [],
    'doNotStore': 'true' 
}
analyze_request_not_en = {
    'comment': {'text': ''}, 
    'requestedAttributes': {'TOXICITY': {}, 'SEVERE_TOXICITY': {}, 'IDENTITY_ATTACK': {}, 'INSULT': {}, 'PROFANITY': {}, 'THREAT': {}},
    'languages': [],
    'doNotStore': 'true'  
} 
def get_toxicity(message: str):
    #we first remove all kind of markdown from the message to avoid exploits
    message = re.sub(r'\*([^*]+)\*', r'\1', message)
    message = re.sub(r'\_([^_]+)\_', r'\1', message)
    message = re.sub(r'\*\*([^*]+)\*\*', r'\1', message)
    message = re.sub(r'\_\_([^_]+)\_\_', r'\1', message)
    message = re.sub(r'\|\|([^|]+)\|\|', r'\1', message)
    message = re.sub(r'\~([^~]+)\~', r'\1', message)
    message = re.sub(r'\~\~([^~]+)\~\~', r'\1', message)
    message = re.sub(r'\`([^`]+)\`', r'\1', message)
    message = re.sub(r'\`\`\`([^`]+)\`\`\`', r'\1', message) 
    message = re.sub(r'\:([^:]+)\:', r'\1', message)
    
    #we try doing the request in english, but if we get 'errorType': 'LANGUAGE_NOT_SUPPORTED_BY_ATTRIBUTE' we try again with the analyze_request_not_en
    try:
        analyze_request['comment']['text'] = message
        response = client.comments().analyze(body=analyze_request).execute()
    except:
        analyze_request_not_en['comment']['text'] = message
        response = client.comments().analyze(body=analyze_request_not_en).execute()
    try: return [float(response['attributeScores']['TOXICITY']['summaryScore']['value']), float(response['attributeScores']['SEVERE_TOXICITY']['summaryScore']['value']), float(response['attributeScores']['IDENTITY_ATTACK']['summaryScore']['value']), float(response['attributeScores']['INSULT']['summaryScore']['value']), float(response['attributeScores']['PROFANITY']['summaryScore']['value']), float(response['attributeScores']['THREAT']['summaryScore']['value']), float(response['attributeScores']['SEXUALLY_EXPLICIT']['summaryScore']['value']), float(response['attributeScores']['FLIRTATION']['summaryScore']['value']), float(response['attributeScores']['OBSCENE']['summaryScore']['value']), float(response['attributeScores']['SPAM']['summaryScore']['value'])]
    except: return [float(response['attributeScores']['TOXICITY']['summaryScore']['value']), float(response['attributeScores']['SEVERE_TOXICITY']['summaryScore']['value']), float(response['attributeScores']['IDENTITY_ATTACK']['summaryScore']['value']), float(response['attributeScores']['INSULT']['summaryScore']['value']), float(response['attributeScores']['PROFANITY']['summaryScore']['value']), float(response['attributeScores']['THREAT']['summaryScore']['value'])]

#test part
def test():
    print("Testing toxicity.py...")
    print("Hello world:")
    result = get_toxicity('Hello world')
    try: print(f"TOXICITY: {result[0]}; SEVERE_TOXICITY: {result[1]}; IDENTITY ATTACK: {result[2]}; INSULT: {result[3]}; PROFANITY: {result[4]}; THREAT: {result[5]}; SEXUALLY EXPLICIT: {result[6]}; FLIRTATION: {result[7]}; OBSCENE: {result[8]}; SPAM: {result[9]}")
    except: print(f"TOXICITY: {result[0]}; SEVERE_TOXICITY: {result[1]}; IDENTITY ATTACK: {result[2]}; INSULT: {result[3]}; PROFANITY: {result[4]}; THREAT: {result[5]}")
    print("HELLO WORLD GET ABSOLUTELY BUY MY NEW MERCH OMGGGGGGG:")
    result = get_toxicity('HELLO WORLD GET ABSOLUTELY BUY MY NEW MERCH OMGGGGGGG')
    try: print(f"TOXICITY: {result[0]}; SEVERE_TOXICITY: {result[1]}; IDENTITY ATTACK: {result[2]}; INSULT: {result[3]}; PROFANITY: {result[4]}; THREAT: {result[5]}; SEXUALLY EXPLICIT: {result[6]}; FLIRTATION: {result[7]}; OBSCENE: {result[8]}; SPAM: {result[9]}")
    except: print(f"TOXICITY: {result[0]}; SEVERE_TOXICITY: {result[1]}; IDENTITY ATTACK: {result[2]}; INSULT: {result[3]}; PROFANITY: {result[4]}; THREAT: {result[5]}")
#uncomment the following line to test the code
#test()