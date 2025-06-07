import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Store Information
STORE_INFO = {
    "name": "Rome-Restaurants - Orders Made Easy",
    "owner": "Marco Bellini",
    "founded": 2015,
    "history": "Founded in 2015 by Marco Bellini, Rome-Restaurants started as a small online platform connecting local Roman restaurants with food enthusiasts. Over the years, we've expanded to offer a wide range of authentic Italian food products and kitchenware shipped worldwide.",
    "mission": "To bring authentic Roman culinary experiences to your home",
    "products": [
        "Authentic Roman pasta (Bucatini, Tonnarelli, Spaghetti)",
        "Roman-style pizza kits",
        "Artisanal olive oils from Lazio region",
        "Traditional Roman cheese (Pecorino Romano)",
        "Italian kitchenware (pasta makers, pizza stones)",
        "Gourmet Roman sauce collection",
        "Italian wine selection",
        "Roman coffee blends",
        "Gift baskets with Roman specialties"
    ],
    "customer_support": {
        "email": "rome.provider@gmail.com",
        "phone": "+1 (555) 123-4567",
        "working_hours": "Monday-Friday: 9AM-6PM (EST), Saturday: 10AM-4PM (EST)",
        "live_chat": "Available during working hours on our website"
    }
}

# Load the FAQ dataset
def load_faq_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data['questions']

# Initialize the Gemini model
def initialize_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Please set your GEMINI_API_KEY in the .env file")
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=api_key,
        temperature=0.1
    )
    return llm

# Create a prompt template with store information
def create_prompt_template(faq_data):
    # Prepare the FAQ context
    faq_context = "\n".join([
        f"Q: {item['question']}\nA: {item['answer']}" 
        for item in faq_data
    ])
    
    # Prepare store information
    store_info = f"""
    Store Name: {STORE_INFO['name']}
    Owner: {STORE_INFO['owner']}
    Founded: {STORE_INFO['founded']}
    History: {STORE_INFO['history']}
    Mission: {STORE_INFO['mission']}
    
    Products Offered:
    {', '.join(STORE_INFO['products'])}
    
    Customer Support:
    Email: {STORE_INFO['customer_support']['email']}
    Phone: {STORE_INFO['customer_support']['phone']}
    Working Hours: {STORE_INFO['customer_support']['working_hours']}
    Live Chat: {STORE_INFO['customer_support']['live_chat']}
    """
    
    template = """You are a helpful customer support assistant for {store_name}. 
    Use the following store information and FAQ to answer questions. 
    If you don't know the answer, just respond with this exact message - 'Please contact our customer support team for further assistance.'.
    Use simple text only - simple formatting and no markdown. Show lists properly with orderer lists but with proper plain text formatting.

    Store Information:
    {store_info}

    FAQ Information:
    {faq_context}

    Customer Question: {question}
    Helpful Answer:"""
    
    return PromptTemplate(
        template=template,
        input_variables=["question"],
        partial_variables={
            "store_info": store_info,
            "faq_context": faq_context,
            "store_name": STORE_INFO['name']
        }
    )

# Main chatbot function
def run_chatbot():
    print(f"Welcome to {STORE_INFO['name']} Support Chatbot!")
    print("Type 'quit' to exit at any time.\n")
    print("About our store:")
    print(f"- Founded in {STORE_INFO['founded']} by {STORE_INFO['owner']}")
    print(f"- {STORE_INFO['mission']}")
    print("\nHow can I help you today?\n")
    
    # Load data and initialize model
    faq_data = load_faq_data("Ecommerce_FAQ_Chatbot_dataset.json")
    llm = initialize_model()
    prompt_template = create_prompt_template(faq_data)
    
    # Create the chain using the new recommended approach
    chatbot_chain = (
        RunnablePassthrough.assign(faq_context=lambda x: faq_data)
        | prompt_template
        | llm
    )
    
    # Chat loop
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            print("Goodbye! Grazie for visiting Rome-Restaurants!")
            break
        
        try:
            response = chatbot_chain.invoke({"question": user_input})
            print("\nAssistant:", response.content, "\n")
        except Exception as e:
            print("\nSorry, I encountered an error. Please try again or contact support.\n")
            print(f"Error: {str(e)}\n")

if __name__ == "__main__":
    run_chatbot()