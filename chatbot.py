from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

def call_chatbot(query, expense = ''):

    model = ChatGoogleGenerativeAI(model='gemini-2.5-flash')

    chat_history = []
    with open('history.txt') as f:
        chat_history.extend(f.readlines())

    template = PromptTemplate(
        template='''
    You are a helpful financial advisor chatbot.
    Your job is to analyze the user’s expenses and provide intelligent advice on how to save money and optimize spending. Given expense data with details such as amount, category, description, merchant, and date, examine spending patterns and suggest practical ways the user can reduce expenses or avoid unnecessary spending. Provide clear, actionable recommendations related to each expense or overall categories. Be friendly, concise, and personalized.
    If no expenses are provided just give advices as per the question.
    ''', input_variables=['expense']
    )

    template = ChatPromptTemplate([
        ('system', '''
    You are a helpful financial advisor chatbot.
    Your job is to analyze the user’s expenses and provide intelligent advice on how to save money and optimize spending. Given expense data in Indian Rupees with details such as amount, category, description, merchant, and date, examine spending patterns and suggest practical ways the user can reduce expenses or avoid unnecessary spending. Provide clear, actionable recommendations related to each expense or overall categories. Be friendly, concise, and personalized.
    If no expenses are provided just give advices as per the question.
        '''),
        MessagesPlaceholder(variable_name='chat_history'),
        ('human', '{query} {expense}')
    ])

    chat_history.append(HumanMessage(f'{query} {expense}'))

    prompt = template.invoke({
        'expense': expense,
        'chat_history': chat_history,
        'query': query
    })

    result = model.invoke(prompt)
    chat_history.append(AIMessage(result.content))

    file_name = "history.txt"

    with open(file_name, 'a') as file:
        for message in chat_history:
            if isinstance(message, HumanMessage):
                file.write(f"Human: {message.content}\n")
            elif isinstance(message, AIMessage):
                file.write(f"AI: {message.content}\n")

    return result


