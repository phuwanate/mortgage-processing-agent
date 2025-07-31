# G.A.I.N AI Solution - AWS Services Price Calculator Chatbot

## 🏆 Hackathon Project Overview

This repository contains the G.A.I.N AI solution developed for the hackathon day - an intelligent chatbot designed to help users calculate and understand AWS services pricing through natural language interactions.

> **Note**: This is an example implementation that requires additional adjustments for production use.

## 🤖 What is G.A.I.N AI?

G.A.I.N AI is an intelligent chatbot solution that leverages Amazon Bedrock agents to provide:
- **AWS Services Price Calculations**: Interactive pricing estimates for various AWS services
- **Natural Language Processing**: Conversational interface for complex pricing queries  
- **Multi-Agent Architecture**: Specialized agents for different aspects of pricing and recommendations

## 🏗️ Architecture

The solution is built using a multi-agent architecture powered by Amazon Bedrock:

### Core Components

- **Supervisor Agent**: Orchestrates interactions between specialized agents
- **Classification Agent**: Categorizes incoming queries for proper routing
- **Policy Specialist Agent**: Handles pricing policies and guidelines
- **Technical Specialist Agent**: Provides technical service details and configurations
- **Mortgage Processing Agent**: Specialized for loan and financial calculations (example domain)

### AWS Services Used

- **Amazon Bedrock**: Foundation models and agent orchestration
- **AWS Lambda**: Serverless compute for agent functions
- **Amazon DynamoDB**: Data storage for property listings and loan information
- **Amazon S3**: Knowledge base storage
- **AWS CloudFormation**: Infrastructure as Code deployment

### N8N Flow Architecture
<img width="1665" height="421" alt="image" src="https://github.com/user-attachments/assets/b6862bee-7d49-4492-83f5-df395602898e" />

#### Flow Node Descriptions:

1. **When chat message received**
   - **Type**: Chat Trigger Node (This will be changed to webhook line OA.)
   - **Purpose**: Entry point for the chatbot workflow
   - **Function**: Listens for incoming chat messages and captures user input
   - **Output**: Provides `sessionId` and `chatInput` data to the next node
   - **Configuration**: Public webhook endpoint for chat interactions

2. **AWS Lambda**
   - **Type**: AWS Lambda Invocation Node
   - **Purpose**: Executes the Bedrock agent through Lambda function
   - **Function**: Calls `lambda-invoke-agent.py` with user input
   - **Payload**: 
     ```json
     {
       "sessionId": "{{ $json.sessionId }}",
       "inputText": "{{ $json.chatInput }}"
     }
     ```
   - **Output**: Returns the agent's response in the Lambda result format

3. **Code Node**
   - **Type**: JavaScript Code Node
   - **Purpose**: Response parsing and formatting
   - **Function**: Extracts the agent response from Lambda result and maps to expected format
   - **Code**: 
     ```javascript
     return [{
         json: {
             text: $input.first().json.result.body
         }
     }];
     ```
   - **Output**: Formatted response with `text` key for chat display

## 📁 Repository Structure

```
gain-ai-solution/
├── api-schema/                    # OpenAPI specifications
│   ├── loan_calculator.json       # Loan affordability calculator API
│   └── mls_lookup.json            # MLS property lookup API
├── cloudformation-templates/      # Infrastructure templates
│   └── create-customer-resources.yml
├── decks/                         # Presentation materials
│   ├── Bedrock-Builders-enablement(17-3-2025).pdf
│   └── Selling-Guide_07-02-25.pdf
├── src/                          # Source code
│   ├── AgentLoanCalculatorFunction.py
│   ├── lambda-invoke-agent.py    # Main agent invocation handler
│   └── MLSLookupFunction.py
└── system-prompt-templates/      # Agent prompt configurations
    ├── intent-classification-agent.txt
    ├── mortgage-processing-agent.txt
    ├── policy-specialist-agent.txt
    ├── supervisor-agent.txt
    └── tech-specialist-agent.txt
```

## 🚀 Quick Start

### Prerequisites

- AWS Account with appropriate permissions
- AWS CLI configured
- Python 3.12+
- Access to Amazon Bedrock models

### Deployment

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd gain-ai-solution
   ```

2. **Deploy infrastructure**
   ```bash
   aws cloudformation create-stack \
     --stack-name gain-ai-solution \
     --template-body file://cloudformation-templates/create-customer-resources.yml \
     --capabilities CAPABILITY_NAMED_IAM
   ```

3. **Configure environment variables**
   ```bash
   export AGENT_ID=<your-bedrock-agent-id>
   export AGENT_ALIAS_ID=<your-agent-alias-id>
   export AGENT_REGION=<your-aws-region>
   ```

4. **Test the agent**
   ```python
   # Use the lambda-invoke-agent.py function
   # Send test queries to validate functionality
   ```

## 💡 Key Features

### 🔧 Loan Affordability Calculator
- Calculate maximum affordable loan amounts
- Consider monthly income, expenses, down payment, and loan terms
- Provide detailed calculation explanations

### 🏠 MLS Property Lookup
- Search property listings by MLS ID
- Retrieve detailed property information
- Integration with DynamoDB for fast lookups

### 🤝 Multi-Agent Coordination
- Intelligent query routing based on intent classification
- Specialized responses from domain experts
- Consistent terminology and policy adherence

## 📊 API Endpoints

### Loan Calculator
```http
POST /loan-affordability-calculator
Content-Type: application/json

{
  "monthlyIncome": 5000,
  "monthlyExpenses": 2000,
  "downPayment": 10000,
  "loanTerm": 5
}
```

### MLS Lookup
```http
GET /mls/{mlsId}/get-property
```

## 🔧 Configuration

### Agent Prompts
The system uses specialized prompts for each agent type:
- **Supervisor Agent**: Coordinates between specialized agents
- **Classification Agent**: Categorizes incoming queries
- **Policy Specialist**: Handles pricing and policy questions
- **Technical Specialist**: Provides technical AWS service details

### Environment Variables
```bash
AGENT_ID=<bedrock-agent-id>
AGENT_ALIAS_ID=<agent-alias-id>
AGENT_REGION=<aws-region>
PROPERTY_TABLE_NAME=<dynamodb-table-name>
LOAN_TABLE_NAME=<loan-table-name>
```

## 🛠️ Development

### Adding New Agents
1. Create prompt template in `system-prompt-templates/`
2. Implement Lambda function in `src/`
3. Define API schema in `api-schema/`
4. Update CloudFormation template for permissions

### Testing
```python
# Example test invocation
from src.lambda_invoke_agent import invoke_agent_with_context

result = invoke_agent_with_context(
    agent_id="your-agent-id",
    agent_alias_id="your-alias-id",
    input_text="Calculate AWS EC2 pricing for t3.medium instance",
    enable_trace=True
)
```

## 🚧 Known Limitations

- This is an example implementation requiring production adjustments
- Limited to specific use cases (loan calculations, property lookup)
- Requires manual configuration of Bedrock agents
- No built-in authentication or rate limiting

## 🔮 Future Enhancements

- **AWS Pricing Integration**: Direct integration with AWS Pricing API
- **Cost Optimization Recommendations**: Intelligent suggestions for cost savings
- **Multi-Region Support**: Pricing calculations across different AWS regions
- **Advanced Analytics**: Usage patterns and cost forecasting
- **Web Interface**: User-friendly frontend for the chatbot

## 🤝 Contributing

This hackathon project welcomes contributions! Areas for improvement:
- Enhanced AWS service coverage
- Better error handling and validation
- Performance optimizations
- Additional agent specializations

## 📄 License

This project is created for hackathon purposes. Please refer to your organization's guidelines for usage and distribution.

## 🏷️ Tags

`#hackathon` `#aws` `#bedrock` `#ai` `#chatbot` `#pricing` `#serverless` `#lambda` `#dynamodb`

---

**Developed for G.A.I.N AI Solution Hackathon Day**
