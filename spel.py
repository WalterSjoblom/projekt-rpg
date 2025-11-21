<<<<<<< HEAD
=======
import random


# Kod på spelets funktoner
class Item:
    def __init__(self, name, strength_bonus):
        self.name = name
        self.strength_bonus = strength_bonus


class Player:
    def __init__(self, hp, strength):
        self.hp = hp
        self.strength = strength
        self.level = 1
        self.inventory = []

    def get_total_strength(self):
        return self.strength + sum(item.strength_bonus for item in self.inventory)

    def add_item(self, item):
        if len(self.inventory) < 5:
            self.inventory.append(item)
        else:
            print("Inventory fullt! Du måste byta ut ett föremål.")
    
    def replace_item(self, index, new_item):
        if 0 <= index < len(self.inventory):
            self.inventory[index] = new_item

    def print_stats(self):
        print(f"HP: {self.hp}")
        print(f"STR: {self.strength}")
        print(f"LVL: {self.level}")

    def print_inventory(self):
        print("\n--- Inventory ---")
        if not self.inventory:
            print("Tomt.")
        for i, item in enumerate(self.inventory):
            print(f"{i+1}. {item.name} (+{item.strength_bonus} STR)")
        print("-----------------\n")


def main():
    player = Player(hp=10, strength=5)
    game_loop(player)
>>>>>>> 2385268721bf29286c33e6b7ca57721eced144b3
