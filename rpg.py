import random

class Item:
    def __init__(self, name, strength_bonus):
        self.name = name
        self.strength_bonus = strength_bonus



class Player:
    def __init__(self, strength=5, hp=10, level=1):
        self.strength = strength
        self.hp = hp
        self.level = level
        self.inventory = []

    def get_total_strength(self):
        return self.strength + sum(item.strength_bonus for item in self.inventory)

    def add_item(self, item):
        if len(self.inventory) < 5:
            self.inventory.append(item)
            print(f"\nDu lägger '{item.name}' i din ryggsäck! (+{item.strength_bonus} STR)")
        else:
            print("\nDin ryggsäck är full!")
            self.print_inventory()
            choice = input("Vill du byta ut ett föremål i ryggsäcken? (j/n): ").lower()
            if choice == "j":
                index = int(input("Vilket föremål vill du byta ut? (1-5): ")) - 1
                self.replace_item(index, item)
            else:
                print("Du lämnar föremålet...")

    def replace_item(self, index, new_item):
        if 0 <= index < len(self.inventory):
            old = self.inventory[index]
            self.inventory[index] = new_item
            print(f"\nDu byter ut '{old.name}' mot '{new_item.name}'!")

    def print_stats(self):
        print(f"\n--- DINA EGENSKAPER ---")
        print(f"HP: {self.hp}")
        print(f"STR: {self.strength} (+{self.get_total_strength() - self.strength} från items)")
        print(f"LEVEL: {self.level}\n")

    def print_inventory(self):
        print("\n--- INVENTORY ---")
        if not self.inventory:
            print("Tomt!")
        else:
            for i, item in enumerate(self.inventory):
                print(f"{i+1}. {item.name} (+{item.strength_bonus} STR)")
        print("----------------------\n")


def create_random_item():
    names = ["Glödande Dolk", "Månring", "Trollkarlens Sten", "Skuggkappa", "Järnsandal"]
    name = random.choice(names)
    bonus = random.randint(1, 4)
    return Item(name, bonus)



def generate_scene(player):
    scenes = [
        scene_fork_road,
        scene_ambush_monster,
        scene_trap_pit,
        scene_mysterious_old_man,
        scene_dark_cave,
        scene_find_chest
    ]
    scene = random.choice(scenes)
    scene(player)



def scene_fork_road(player):
    print("\nDu kommer till ett vägskäl. Tre vägar leder vidare genom skogen.")
    print("1) Ta den dimmiga stigen")
    print("2) Följ den steniga vägen")
    print("3) Gå mot ljudet av vatten")

    choice = input("> ")

    if choice == "1":
        print("Den dimmiga stigen leder dig till... ett monster!")
        encounter_monster(player)
    elif choice == "2":
        print("Du hittar en gammal staty. Den öppnar sig och avslöjar en kista!")
        encounter_chest(player)
    elif choice == "3":
        print("Du glider på en hal sten och faller i en ström!")
        encounter_trap(player)
    else:
        print("Ogiltigt val, du snubblar omkring... och möter ett monster ändå!")
        encounter_monster(player)

def scene_ambush_monster(player):
    print("\nEtt monster hoppar fram ur buskarna!")
    encounter_monster(player)


def scene_trap_pit(player):
    print("\nDu trampar på lös mark och faller ner i en grop!")
    encounter_trap(player)


def scene_mysterious_old_man(player):
    print("\nEn mystisk gammal man stoppar dig.")
    print("'Jag kan hjälpa dig... eller kanske inte.'")
    print("1) Be honom om styrka")
    print("2) Ge honom ett av dina föremål")
    print("3) Ignorera honom")

    choice = input("> ")
