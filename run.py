from flask import Flask,request, jsonify
from structured_out import call_model
from chatbot import call_chatbot
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

# {
#   "rawInput": "Lunch at X for ₹250"
# }

@app.route('/parse-expense', methods = ['POST'])
def chatbot():
        if request.method == 'POST':
            data = request.get_json()
            input = data.get("rawInput")

        if not data:
            return jsonify({
                 'success': False
            })
    
        result = call_model(query=input)

        return jsonify({
            'success': True,
            "data": {
                "amount": result.amount,
                "category": result.category,
                "description": result.description,
                "merchant": result.merchant
            }

        })
# amount=1500 category='Clothes' description='Spent on X' merchant='X'



# {
#   "query": "How can I save more money on food?",
#   "expenses": [
#     {
#       "amount": 1200,
#       "category": "Food",
#       "description": "Weekly groceries",
#       "date": "2025-09-15T10:30:00Z"
#     },
#     {
#       "amount": 500,
#       "category": "Food",
#       "description": "Dinner at restaurant",
#       "date": "2025-09-14T20:15:00Z"
#     },
#     {
#       "amount": 3000,
#       "category": "Shopping",
#       "description": "New clothes",
#       "date": "2025-09-10T14:00:00Z"
#     }
#   ]
# }

@app.route('/get-advice', methods = ['POST'])
def interact_chatbot():
        if request.method == 'POST':
            data = request.get_json()
            query = data.get("query")
            expenses = data.get("expenses")

        if expenses:
            formatted_expenses = ", ".join([
                f"{exp['category']}: {exp['amount']} ({exp['description']})" for exp in expenses])
            result = call_chatbot(query, formatted_expenses)
        else:
            result = call_chatbot(query)

        if not data:
            return jsonify({
                 'success': False
            })
    
        

        return jsonify({
            "success": True,
            "message": result.content
        })



    
if __name__ == '__main__':
    app.run(debug=True)
