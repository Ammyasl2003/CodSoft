from flask import Flask, render_template, request, redirect, url_for
import random
import string
from datetime import datetime
import os
app = Flask(__name__)

# In-memory storage for tasks (in a real app, use a database)
tasks = []

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Calculator route
@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    result = None
    if request.method == 'POST':
        try:
            num1 = float(request.form['num1'])
            num2 = float(request.form['num2'])
            operation = request.form['operation']
            
            if operation == 'add':
                result = num1 + num2
            elif operation == 'subtract':
                result = num1 - num2
            elif operation == 'multiply':
                result = num1 * num2
            elif operation == 'divide':
                if num2 == 0:
                    result = "Error: Cannot divide by zero!"
                else:
                    result = num1 / num2
        except ValueError:
            result = "Error: Please enter valid numbers!"
    
    return render_template('calculator.html', result=result)

# Password Generator route
@app.route('/password', methods=['GET', 'POST'])
def password_generator():
    password = None
    if request.method == 'POST':
        try:
            length = int(request.form['length'])
            if length < 4:
                password = "Password length must be at least 4 characters"
            else:
                # Define character sets
                lowercase = string.ascii_lowercase
                uppercase = string.ascii_uppercase
                digits = string.digits
                symbols = string.punctuation
                
                # Ensure at least one character from each set
                all_chars = []
                all_chars.append(random.choice(lowercase))
                all_chars.append(random.choice(uppercase))
                all_chars.append(random.choice(digits))
                all_chars.append(random.choice(symbols))
                
                # Fill the rest with random choices from all sets
                remaining_length = length - 4
                if remaining_length > 0:
                    all_chars.extend(random.choices(
                        lowercase + uppercase + digits + symbols,
                        k=remaining_length
                    ))
                
                # Shuffle the characters
                random.shuffle(all_chars)
                password = ''.join(all_chars)
        except ValueError:
            password = "Please enter a valid number for length"
    
    return render_template('password.html', password=password)

# To-Do List routes
@app.route('/todo', methods=['GET', 'POST'])
def todo_list():
    if request.method == 'POST':
        task_content = request.form['content']
        if task_content.strip():
            new_task = {
                'id': len(tasks) + 1,
                'content': task_content,
                'date_created': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'completed': False
            }
            tasks.append(new_task)
        return redirect(url_for('todo_list'))
    
    return render_template('todo.html', tasks=tasks)

@app.route('/todo/delete/<int:task_id>')
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return redirect(url_for('todo_list'))

@app.route('/todo/complete/<int:task_id>')
def complete_task(task_id):
    global tasks
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = not task['completed']
            break
    return redirect(url_for('todo_list'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
