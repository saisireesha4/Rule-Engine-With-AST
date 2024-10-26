from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:saisi123@localhost/rules_db'
db = SQLAlchemy(app)

class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    conditions = db.Column(db.JSON, nullable=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/evaluate', methods=['POST'])
def evaluate():
    age = int(request.form['age'])
    income = int(request.form['income'])
    department = request.form['department']

    user_data = {"age": age, "income": income, "department": department}

    result = {}
    rules = Rule.query.all()
    for rule in rules:
        conditions = rule.conditions
        is_eligible = evaluate_rule(user_data, conditions)
        result[rule.name] = {
            "description": rule.description,
            "is_eligible": is_eligible
        }

    return render_template('result.html', result=result)

def evaluate_rule(user_data, conditions):
    for key, condition in conditions.items():
        if key == 'age' and user_data['age'] < condition.get('min', 0):
            return False
        elif key == 'income' and user_data['income'] < condition.get('min', 0):
            return False
        elif key == 'department' and user_data['department'] != condition:
            return False
    return True

if __name__ == '__main__':
    db.create_all()  # Creates the tables if they don't exist
    app.run(debug=True)
