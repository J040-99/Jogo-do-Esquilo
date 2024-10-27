from flask import Flask, render_template, request, session
import random
import os

app = Flask(__name__)
app.template_folder = 'templates'
secret_key = os.urandom(24)
print(f'Secret Key: {secret_key}')


@app.route('/')
def index():
    session['difficulty'] = session.get('difficulty', 5)  # Define a dificuldade inicial se não estiver na sessão
    difficulty = session['difficulty']
    if 'number' not in session:
        session['number'] = random.randint(1, session['difficulty'])
        session['attempts'] = 5  # Inicializa as tentativas apenas uma vez
        difficulty = session['difficulty']
    if difficulty == 5:
        level = 'Fácil'
    elif difficulty == 10:
        level = 'Médio'
    elif difficulty == 15:
        level = 'Difícil'
    elif difficulty >= 20 and difficulty <=40:
        level = 'Impossivel' 
    elif difficulty >= 50:
        leve = 'Deus'
    else:
        level = 'Fácil'
    print(f'Nivel: {level}\nNumero: {session['number']}')
    return render_template('index.html', level=level, message='Teste a sua sorte.', attempts=session.get('attempts', 5), difficulty=session.get('difficulty', 5))

@app.route('/guess', methods=['POST'])
def guess():
    guess = int(request.form['guess'])
    number = session.get('number')
    attempts = session.get('attempts', 5) - 1
    session['attempts'] = attempts  # Atualiza o número de tentativas na sessão
    difficulty = session.get('difficulty')
    if difficulty == 5:
        level = 'Fácil'
    elif difficulty == 10:
        level = 'Médio'
    elif difficulty == 15:
        level = 'Difícil'
    elif difficulty >= 20 and difficulty <=40:
        level = 'Impossivel' 
    elif difficulty >= 50:
        leve = 'Deus'
    else:
        level = 'Fácil'

    if guess == number:
        # Jogo ganho
        session['difficulty'] += 5  # Aumenta a dificuldade
        session.pop('number')  # Remove o número da sessão para iniciar um novo jogo
        return render_template('win.html', message="Parabéns! Você venceu!")
    elif attempts == 0:
        # Jogo perdido
        session['difficulty'] = 5
        session.pop('number')  # Remove o número da sessão para iniciar um novo jogo
        return render_template('lose.html', message='Game Over! Perdeste tudo.', number = number)
    else:
        # Chute incorreto
        if guess < number:
            message = "O número é maior."
            number -= 1
        elif guess > number:
            message = "O número é menor."
            number += 1
        session['number'] = number  # Atualiza o número na sessão
        print(f'Nivel: {level}\nNumero: {session['number']}')
        return render_template('index.html', level=level, message=message, attempts=session.get('attempts', 5), difficulty=session.get('difficulty', 5))

@app.route('/win')
def win():
    return render_template('win.html')

@app.route('/lose')
def lose():
    return render_template('lose.html')

if __name__ == '__main__':
    app.run(debug=True)
