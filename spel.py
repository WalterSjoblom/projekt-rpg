
import random

# -----------------------------
# Item Class
# -----------------------------
class Item:
    def __init__(self, name, strength_bonus):
        self.name = name
        self.strength_bonus = strength_bonus


# -----------------------------
# Player Class
# -----------------------------
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


# -----------------------------
# Random Item Generator
# -----------------------------
def create_random_item():
    names = ["Glödande Dolk", "Månring", "Trollkarlens Sten", "Skuggkappa", "Järnsandal"]
    name = random.choice(names)
    bonus = random.randint(1, 4)
    return Item(name, bonus)


# -----------------------------------------------------
# STORY SCENE ENGINE
# -----------------------------------------------------
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
