from flask import Flask,request, jsonify
from structured_out import call_model
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
    
if __name__ == '__main__':
    app.run(debug=True)
