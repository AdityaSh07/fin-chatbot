from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Literal

# {
#   "rawInput": "Lunch at McDonalds for ₹250"
# }

load_dotenv()


def call_model(query):


    model = ChatGoogleGenerativeAI(model= 'gemini-1.5-flash')



    class Classify(BaseModel):
        amount: int = Field(description='Fetch how much amount spent is mentioned.')
        category: Literal['Food', 'Transport', 'Shopping', 'Bills', 'Entertainment', 'Health', 'Other'] = Field(description='Which category the expense belong to?')
        description: str = Field(description='Give description about the event. Use words only as per the query.')
        merchant: str = Field(description='Which merchant/company is mentioned where the money is used', default='Not Mentioned')


    structured_model = model.with_structured_output(Classify)

    result = structured_model.invoke(query)

    return result





