class Enemy:
    def __init__(self, type, name, attack, health, image_path):
        self.type = type
        self.name = name
        self.health = health
        self.attack = attack
        self.image_path = image_path