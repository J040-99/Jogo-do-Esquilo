from flask import Flask, render_template, request, session
import random
import os

app = Flask(__name__)
app.template_folder = 'templates'
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    session['difficulty'] = session.get('difficulty', 5)  # Define initial difficulty if not in session
    if 'number' not in session:
        session['number'] = random.randint(1, session['difficulty'])
        session['attempts'] = 5  # Initialize attempts only once

    difficulty = session['difficulty']
    if difficulty == 5:
        level = 'Fácil'
    elif difficulty == 10:
        level = 'Médio'
    elif difficulty == 15:
        level = 'Difícil'
    elif 20 <= difficulty <= 40:
        level = 'Impossível'
    elif difficulty >= 45:
        level = 'Deus'
    else:
        level = 'Fácil'

    print(f'Nivel: {level}\nNumero: {session["number"]}')
    return render_template('index.html', level=level, message='Teste a sua sorte.', attempts=session.get('attempts', 5), difficulty=difficulty)

@app.route('/guess', methods=['POST'])
def guess():
    guess = int(request.form['guess'])
    number = session.get('number')
    attempts = session.get('attempts', 5) - 1
    session['attempts'] = attempts  # Update attempts in session

    difficulty = session.get('difficulty')
    if difficulty == 5:
        level = 'Fácil'
    elif difficulty == 10:
        level = 'Médio'
    elif difficulty == 15:
        level = 'Difícil'
    elif 20 <= difficulty <= 40:
        level = 'Impossível'
    elif difficulty >= 45:
        level = 'Deus'
    else:
        level = 'Fácil'

    if guess == number:
        session['difficulty'] += 5  # Increase difficulty
        session.pop('number')  # Remove number to start a new game
        return render_template('win.html', message="Parabéns! Você venceu!")
    elif attempts == 0:
        session['difficulty'] = 5
        session.pop('number')  # Remove number to start a new game
        return render_template('lose.html', message='Game Over! Perdeste tudo.', number=number)
    else:
        if guess < number:
            message = "O número é maior."
            number -= 1
        else:
            message = "O número é menor."
            number += 1

        session['number'] = number  # Update number in session
        print(f'Nivel: {level}\nNumero: {session["number"]}')
        return render_template('index.html', level=level, message=message, attempts=attempts, difficulty=difficulty)

@app.route('/win')
def win():
    return render_template('win.html')

@app.route('/lose')
def lose():
    return render_template('lose.html')

if __name__ == '__main__':
    app.run()
