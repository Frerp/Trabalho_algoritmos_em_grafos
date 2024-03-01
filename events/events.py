import random

def handle_event(event_type):
    if event_type == 'inimigo':
        return 'Você encontrou um inimigo!'
    elif event_type == 'arma':
        return 'Você encontrou uma arma!'
    elif event_type == 'cura':
        return 'Você encontrou uma cura!'
    elif event_type == 'tesouro':
        return 'Você encontrou um tesouro!'
    else:
        return 'Evento desconhecido!'

def generate_random_event():
    return random.choice(['inimigo', 'arma', 'cura', 'tesouro'])
