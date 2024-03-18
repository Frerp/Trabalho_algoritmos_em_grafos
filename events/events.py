import random

def handle_event(event_type):
    if event_type == 'inimigo':
        return 'Você encontrou um inimigo!'
    elif event_type == 'arma':
        return 'Você encontrou uma arma!'
    elif event_type == 'cura':
        return 'Você encontrou uma cura!'
    elif event_type == 'deslizamento_pedra':
        return 'Você encontrou um deslizamento de pedra!'
    elif event_type == 'areia_movedica':
        return 'Você encontrou areia movediça!'
    elif event_type == 'rio_traicoeiro':
        return 'Você encontrou um rio traiçoeiro!'
    elif event_type == 'checkpoint':
        return 'Você encontrou um checkpoint!'
    else:
        return 'Evento desconhecido!'

def generate_random_event():
    return random.choice(['inimigo', 'arma', 'cura', 'deslizamento_pedra', 'areia_movedica', 'rio_traicoeiro'])