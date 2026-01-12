import random

class Item:
    def __init__(self, name, strength_bonus):
        self.name = name
        self.strength_bonus = strength_bonus

class Player:
    def __init__(self, name, strength=5, hp=10, level=1):
        self.name = name
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
        print("\n--- DINA EGENSKAPER ---")
        print(f"HP: {self.hp}")
        print(f"STR: {self.strength} (+{self.get_total_strength() - self.strength} från items)")
        print(f"LEVEL: {self.level}")
        print("-------------------------\n")

    def print_inventory(self):
        print("\n--- INVENTORY ---")
        if not self.inventory:
            print("Din ryggsäck är tom!")
        else:
            for i, item in enumerate(self.inventory):
                print(f"{i+1}. {item.name} (+{item.strength_bonus} STR)")
        print("----------------------\n")


def create_random_item():
    names = ["Glödande Dolk", "Månring", "Eldstav", "Skuggkappa", "Järnsandal"]
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
    random.choice(scenes)(player)


def scene_fork_road(player):
    print("\nDu kommer till ett vägskäl. Tre vägar leder vidare genom skogen.")
    print("1) Gå in i dimman")
    print("2) Följ den steniga vägen")
    print("3) Gå mot ljudet av vatten")
    choice = input("> ")

    if choice == "1":
        encounter_monster(player)
    elif choice == "2":
        encounter_chest(player)
    elif choice == "3":
        encounter_trap(player)
    else:
        print("Du tvekar… men ett monster hittar dig!")
        encounter_monster(player)


def scene_ambush_monster(player):
    print("\nEtt monster hoppar fram ur buskarna!")
    encounter_monster(player)


def scene_trap_pit(player):
    print("\nDu faller ner i en fälla!")
    encounter_trap(player)


def scene_mysterious_old_man(player):
    print("\nEn gammal man stoppar dig.")
    print("1) Be om hjälp")
    print("2) Ge bort ett item")
    print("3) Ignorera honom")
    choice = input("> ")

    if choice == "1":
        gain = random.randint(1, 3)
        player.strength += gain
        print(f"\nDen gamle mannen blåser på dig. Du får +{gain} STR!")
    elif choice == "2":
        if not player.inventory:
            print("Du har inga items att ge!")
        else:
            player.print_inventory()
            idx = int(input("Vilket item vill du ge bort? (1-n): ")) - 1
            if 0 <= idx < len(player.inventory):
                removed = player.inventory.pop(idx)
                print(f"Du gav bort {removed.name}.")
    else:
        print("Du går vidare… en fälla aktiveras!")
        encounter_trap(player)


def scene_dark_cave(player):
    print("\nDu går in i en mörk grotta…")
    print("1) Tänd en fackla")
    print("2) Smyg")
    print("3) Skapa ett högt ljud")
    choice = input("> ")

    if choice == "1":
        encounter_monster(player)
    elif choice == "2":
        if random.random() < 0.5:
            print("Du smyger förbi… och hittar en kista!")
            encounter_chest(player)
        else:
            encounter_monster(player)
    else:
        print("Stenar faller från taket!")
        damage = random.randint(1, 2)
        player.hp -= damage
        print(f"Du tar {damage} skada!")
        if check_game_over(player):
            return


def scene_find_chest(player):
    print("\nDu hittar en skimrande kista!")
    encounter_chest(player)



def encounter_trap(player):
    damage = random.randint(1, 3)
    print(f"\nEn fälla aktiveras! Du tar {damage} skada!")
    player.hp -= damage
    check_game_over(player)


def encounter_monster(player):
    monsters = ["Sfinx", "Varg", "Ogre", "Skuggvandrare", "Drakling"]
    monster = random.choice(monsters)
    monster_hp = random.randint(2, 4)
    monster_str = random.randint(3, 6)

    print(f"\n*** DU MÖTER EN {monster.upper()}! ***")
    steps = 0

    while monster_hp > 0 and player.hp > 0 and steps < 4:

        print("\nVad gör du?")

        if monster == "Sfinx":
            print("1) Svara på en gåta")
            print("2) Smyga förbi")
            print("3) Attackera")
        else:
            print("1) Distrahera")
            print("2) Leta svag punkt")
            print("3) Attackera")

        choice = input("> ")

        if choice == "1":
            if random.random() < 0.5:
                print("Du lyckas! Monstret tar skada.")
                monster_hp -= 1
            else:
                print("Miss! Monstret attackerar!")
                dmg = random.randint(1, 3)
                player.hp -= dmg
                print(f"-{dmg} HP")
        elif choice == "2":
            if random.random() < 0.4:
                print("Du hittar en chans att skada monstret!")
                monster_hp -= 1
            else:
                print("Du misslyckas!")
                dmg = random.randint(1, 3)
                player.hp -= dmg
                print(f"-{dmg} HP")
        else:
            if player.get_total_strength() > monster_str:
                print("Du träffar hårt!")
                monster_hp -= 2
            else:
                print("Monstret är för starkt!")
                dmg = random.randint(1, 3)
                player.hp -= dmg
                print(f"-{dmg} HP")

        steps += 1

    if monster_hp <= 0:
        print(f"\n*** Du besegrar {monster}! ***")
        player.level += 1
        check_game_over(player)
    else:
        print(f"\n{monster} besegrar dig…")
        player.hp = 0
        check_game_over(player)


def encounter_chest(player):
    item = create_random_item()
    print(f"\nKistan innehåller '{item.name}' (+{item.strength_bonus} STR)!")
    player.add_item(item)



def check_game_over(player):
    if player.hp <= 0:
        print("\n💀 DU DOG! SPELET ÄR ÖVER.")
        exit()
    if player.level >= 10:
        print("\n🏆 DU NÅDDE LEVEL 10! DU VANN SPELET!")
        exit()
    return False


def game_loop(player):
    while True:
        print("\n------------------------------------")
        print(f"LEVEL: {player.level} | HP: {player.hp} | STR: {player.strength}")
        print("------------------------------------")

        print("\nVad vill du göra?")
        print("1. Ge dig vidare i äventyret")
        print("2. Kolla dina stats")
        print("3. Kolla din ryggsäck")

        choice = input("> ").strip()

        if choice == "1":
            generate_scene(player)
        elif choice == "2":
            player.print_stats()
        elif choice == "3":
            player.print_inventory()
        else:
            print("Ogiltigt val!")



def main():
    print("====================================")
    print(" VÄLKOMMEN TILL ÄVENTYRSSPELET! ")
    print("====================================")
    print("ANTAR DU UTMANINGEN? SKRIV 'JA' FÖR ATT BÖRJA.")
    choice = input("> ").strip().lower()

    if choice != "ja":
        print("Du valde att inte anta utmaningen... spelet avslutas.")
        return

    print("\nModigt val! Ditt äventyr börjar nu...")
    name = input("Vad heter du, äventyrare? ")

    # Skapa spelare
    player = Player(name)

    print(f"\n{name}, dina startvärden är:")
    player.print_stats()
    player.print_inventory()

    # Starta spelet
    game_loop(player)


# Starta spelet
if __name__ == "__main__":
    main()
