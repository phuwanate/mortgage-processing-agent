import json
import boto3
import uuid
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    
    try:
        # Initialize Bedrock Agent Runtime client
        bedrock_agent_client = boto3.client(
            'bedrock-agent-runtime',
            region_name=os.getenv('AGENT_REGION')  # Replace with your actual region that agent is deployed in
        )
        
        # Extract parameters from event
        agent_id = os.getenv('AGENT_ID')
        agent_alias_id = os.getenv('AGENT_ALIAS_ID')  # Replace with your actual alias ID
        input_text = event.get('inputText', 'Hi')
        session_id = event.get('sessionId', str(uuid.uuid4()))
        
        # Validate required parameters
        if not agent_id or not input_text:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Missing required parameters: agentId and inputText'
                })
            }
        
        # Invoke the agent
        response = bedrock_agent_client.invoke_agent(
            agentId=agent_id,
            agentAliasId=agent_alias_id,
            sessionId=session_id,
            inputText=input_text
        )
        
        # Process the streaming response
        agent_response = ""
        for event_chunk in response['completion']:
            if 'chunk' in event_chunk:
                chunk_data = event_chunk['chunk']
                if 'bytes' in chunk_data:
                    agent_response += chunk_data['bytes'].decode('utf-8')
        
        return {
            'statusCode': 200,
            'body': agent_response
        }
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f'AWS Error ({error_code}): {error_message}'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f'Unexpected error: {str(e)}'
            })
        }


# Alternative function for batch processing or complex workflows
def invoke_agent_with_context(agent_id, agent_alias_id, input_text, session_id=None, enable_trace=False):
    """
    More advanced agent invocation with additional options
    """
    
    bedrock_agent_client = boto3.client('bedrock-agent-runtime')
    
    if not session_id:
        session_id = str(uuid.uuid4())
    
    params = {
        'agentId': agent_id,
        'agentAliasId': agent_alias_id,
        'sessionId': session_id,
        'inputText': input_text
    }
    
    # Enable trace for debugging (optional)
    if enable_trace:
        params['enableTrace'] = True
    
    try:
        response = bedrock_agent_client.invoke_agent(**params)
        
        # Collect all response chunks
        full_response = ""
        trace_data = []
        
        for event in response['completion']:
            if 'chunk' in event:
                chunk = event['chunk']
                if 'bytes' in chunk:
                    full_response += chunk['bytes'].decode('utf-8')
            
            # Collect trace information if enabled
            if 'trace' in event and enable_trace:
                trace_data.append(event['trace'])
        
        result = {
            'response': full_response,
            'sessionId': session_id
        }
        
        if enable_trace:
            result['trace'] = trace_data
            
        return result
        
    except Exception as e:
        raise Exception(f"Failed to invoke agent: {str(e)}")
