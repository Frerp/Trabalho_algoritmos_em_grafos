import random
from characters.enemy import Enemy
from characters.weapon import Weapon
from characters.terreno import Terreno
from characters.heal import Heal

def generate_random_event():
    evento = random.choice(['inimigo', 'arma', 'cura', 'terreno'])
    if evento == 'inimigo':
        nomeInimigo = random.choice(['Pantera Mística', 'Leão de Nemeia', 'Formigas Quimera', 'Cobra Gigante'])
        if(nomeInimigo == 'Pantera Mística'):
            image_path = 'Assets/pantera.jpeg'
            attack = 15
            health = 50
        elif (nomeInimigo == 'Leão de Nemeia'):
            image_path = 'Assets/leao.jpeg'
            attack = 12
            health = 60
        elif (nomeInimigo == 'Formigas Quimera'):
            image_path = 'Assets/formiga.jpeg'
            attack = 30
            health = 70
        elif (nomeInimigo == 'Cobra Gigante'):
            image_path = 'Assets/cobra.jpeg'
            attack = 20
            health = 65
        objeto = Enemy('inimigo', nomeInimigo, attack, health, image_path)
    elif evento == 'arma':
        damage = random.randint(10, 30)
        objeto = Weapon('arma', damage, 3)
    elif evento == 'cura':
        healing_points = random.randint(15, 30)
        objeto = Heal('cura', healing_points)
    elif evento == 'terreno':
        name = random.choice(['deslizamento_pedra', 'areia_movedica', 'rio_traicoeiros'])
        damage = random.randint(10, 20)
        objeto = Terreno('terreno', name, damage)
    return objeto