import random

# =====================================
# KLASSER

class Item:
    def __init__(self, name, strength_bonus):
        self.name = name
        self.strength_bonus = strength_bonus

# Kommentar:
# Item-klassen representerar ett föremål som spelaren kan ha i sin ryggsäck.
# Varje Item har:
# - name: Namnet på föremålet (t.ex. "Glödande Dolk")
# - strength_bonus: En bonus som läggs till spelarens STR i strider


class Player:
    def __init__(self, name, strength=5, hp=10, level=1):
        self.name = name
        self.strength = strength
        self.hp = hp
        self.level = level
        self.inventory = []

    def get_total_strength(self):
        return self.strength + sum(item.strength_bonus for item in self.inventory)

    # Kommentar:
    # Beräknar spelarens totala STR inklusive bonusar från items i inventory.
    # Exempel: Om STR=5 och två items med 2+1 bonus → total STR = 8

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

    # Kommentar:
    # Lägg till ett item i ryggsäcken.
    # Om inventory är fullt får spelaren möjlighet att byta ut ett item.

    def replace_item(self, index, new_item):
        if 0 <= index < len(self.inventory):
            old = self.inventory[index]
            self.inventory[index] = new_item
            print(f"\nDu byter ut '{old.name}' mot '{new_item.name}'!")

    # Kommentar:
    # Byter ut ett item på angivet index med ett nytt item.

    def print_stats(self):
        print("\n====================================")
        print("          DINA EGENSKAPER           ")
        print("====================================")
        print(f"HP     : {self.hp}")
        print(f"STR    : {self.strength} (+{self.get_total_strength() - self.strength} från items)")
        print(f"LEVEL  : {self.level}")
        print("====================================\n")

    # Kommentar:
    # Skriver ut spelarens stats på ett snyggt format.
    # Visar HP, STR och LEVEL samt bonus från items.

    def print_inventory(self):
        print("\n====================================")
        print("             DIN RYGGSÄCK           ")
        print("====================================")
        if not self.inventory:
            print("Din ryggsäck är tom!")
        else:
            for i, item in enumerate(self.inventory):
                print(f"{i+1}. {item.name} (+{item.strength_bonus} STR)")
        print("====================================\n")

    # Kommentar:
    # Skriver ut innehållet i inventory på ett snyggt format.
    # Om inget finns visas meddelandet att ryggsäcken är tom.


# =====================================
# FUNKTIONER FÖR ITEMS OCH SCENER

def create_random_item():
    names = ["Glödande Dolk", "Månring", "Eldstav", "Skuggkappa", "Järnsandal"]
    name = random.choice(names)
    bonus = random.randint(1, 4)
    return Item(name, bonus)

# Kommentar:
# Skapar ett slumpmässigt Item med namn och styrkebonus.
# Används i kistor och andra belöningar.


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

# Kommentar:
# Slumpar fram vilken scen spelaren hamnar i.
# Varje scen är en funktion som tar player som argument.
# Detta ger variation i äventyret.


# =====================================
# SCENER / MÖTEN

def scene_fork_road(player):
    print("\n------------------------------------")
    print("         VÄGSKÄL I SKOGEN")
    print("------------------------------------")
    print("\nDu kommer till ett vägskäl. Tre vägar leder vidare genom skogen.\n")
    print("1) Gå in i dimman där inget kan ses på längre än några meter")
    print("2) Följ den steniga vägen som ser trygg men lång ut")
    print("3) Gå mot ljudet av vatten som porlar längre fram")
    choice = input("> ")

    if choice == "1":
        encounter_monster(player)
    elif choice == "2":
        encounter_chest_interactive(player)
    elif choice == "3":
        encounter_trap_interactive(player)
    else:
        print("Du tvekar… men ett monster hittar dig!")
        encounter_monster(player)

# Kommentar:
# En typisk scen med flera val som leder till olika interaktiva encounters:
# - Monster, kista eller fälla beroende på spelarens val.
# Ogiltigt val får konsekvens (monster attack).

def scene_ambush_monster(player):
    print("\n------------------------------------")
    print("           MONSTERAMBUSH")
    print("------------------------------------")
    print("\nEtt monster hoppar fram ur buskarna och stirrar hotfullt på dig!\n")
    encounter_monster(player)

# Kommentar:
# En enkel scen som alltid leder till ett monstermöte.

def scene_trap_pit(player):
    print("\n------------------------------------")
    print("             FALLFÄLLA")
    print("------------------------------------")
    print("\nMarken ser stabil ut, men plötsligt sjunker den under dina fötter...\n")
    encounter_trap_interactive(player)

# Kommentar:
# Tidigare var detta en snabb HP-förlust, nu är det en interaktiv fälla.
# Spelaren får flera alternativ att undvika skada.

def scene_mysterious_old_man(player):
    print("\n------------------------------------")
    print("           GAMMLA MANNEN")
    print("------------------------------------")
    print("\nEn gammal man stoppar dig och ler mystiskt.\n")
    print("1) Be om råd eller hjälp från den gamle mannen")
    print("2) Försök ge bort ett föremål från din ryggsäck för att få hans förtroende")
    print("3) Ignorera mannen och fortsätt utan att stanna")
    choice = input("> ")

    if choice == "1":
        gain = random.randint(1, 3)
        player.strength += gain
        print(f"\nDen gamle mannen ger dig en energikick. Du får +{gain} STR!")
    elif choice == "2":
        if not player.inventory:
            print("Du har inga föremål att ge bort.")
        else:
            player.print_inventory()
            idx = int(input("Vilket föremål vill du ge bort? (1-n): ")) - 1
            if 0 <= idx < len(player.inventory):
                removed = player.inventory.pop(idx)
                print(f"Du gav bort {removed.name}.")
    else:
        print("Du går vidare utan att lyssna… men marken börjar skaka under dig.")
        encounter_trap_interactive(player)

# Kommentar:
# Interaktiv scen där spelaren kan påverka:
# - styrka (+STR)
# - ge bort items
# - eller råka ut för fälla

def scene_dark_cave(player):
    print("\n------------------------------------")
    print("            MÖRK GROTTA")
    print("------------------------------------")
    print("\nDu går in i en mörk grotta med eko som studsar mellan väggarna.\n")
    print("1) Tänd en fackla och utforska långsamt")
    print("2) Smyg tyst genom grottan och försök undvika faror")
    print("3) Skapa ett högt ljud för att skrämma eventuella fiender")
    choice = input("> ")

    if choice == "1":
        encounter_monster(player)
    elif choice == "2":
        if random.random() < 0.5:
            print("Du smyger förbi faran och hittar en kista med något intressant.")
            encounter_chest_interactive(player)
        else:
            encounter_monster(player)
    else:
        print("Stenar faller från taket och du måste agera snabbt!")
        encounter_trap_interactive(player)

# Kommentar:
# Grotta-scenen erbjuder olika val med slumpade konsekvenser.
# Kan leda till monster, kista eller fälla.

def scene_find_chest(player):
    print("\n------------------------------------")
    print("           GAMMAL KISTA")
    print("------------------------------------")
    print("\nDu hittar en gammal kista som glimmar till i skenet från solen eller facklan.\n")
    encounter_chest_interactive(player)

# Kommentar:
# Enkel scen som leder till ett interaktivt kistmöte.


# =====================================
# INTERAKTIVA ENCOUNTERS

def encounter_trap_interactive(player):
    print("\n------------------------------------")
    print("               FALLFÄLLA")
    print("------------------------------------")
    steps = 0

    while steps < 3 and player.hp > 0:
        print("\nVad vill du göra?")
        print("1) Hoppa bakåt för att undvika att falla")
        print("2) Kasta ett föremål på marken för att utlösa eventuella fällor")
        print("3) Spring rakt fram och hoppas på det bästa")
        choice = input("> ")

        if choice == "1":
            if random.random() < 0.5:
                print("Du lyckas hoppa bakåt och undviker fällan.")
                return
            else:
                dmg = random.randint(1, 2)
                print(f"Du halkar och tar {dmg} skada.")
                player.hp -= dmg
        elif choice == "2":
            if player.inventory:
                print("Fällan aktiveras på ditt föremål istället och du undviker skada.")
                return
            else:
                print("Du har inget att kasta! Fällan aktiveras på dig.")
                dmg = random.randint(1, 2)
                player.hp -= dmg
        else:
            dmg = random.randint(1, 3)
            print(f"Du rusar fram och träffas av en mekanism i fällan! -{dmg} HP")
            player.hp -= dmg

        steps += 1

    print("Du tar dig till slut bort från fällan.")
    check_game_over(player)

# Kommentar:
# Fällor har flera steg, varje val kan ge skada eller undvikande.
# Spelaren kan försöka tre gånger innan fällan slutar.

def encounter_chest_interactive(player):
    print("\n------------------------------------")
    steps = 0

    while steps < 3:
        print("\nVad vill du göra?")
        print("1) Öppna kistan försiktigt")
        print("2) Slå sönder kistan för att snabbt komma åt innehållet")
        print("3) Ignorera kistan och gå vidare")
        choice = input("> ")

        if choice == "1":
            if random.random() < 0.6:
                item = create_random_item()
                print(f"Du öppnar kistan och hittar '{item.name}' som du tar med dig.")
                player.add_item(item)
                return
            else:
                print("Kistan var boobytrapped! Du tar 1 skada.")
                player.hp -= 1
        elif choice == "2":
            if random.random() < 0.4:
                item = create_random_item()
                print(f"Du krossar kistan och hittar '{item.name}'! Du tar med dig det.")
                player.add_item(item)
                return
            else:
                print("Kistan exploderar lätt och du tar 2 skada.")
                player.hp -= 2
        else:
            print("Du går vidare utan att öppna kistan.")
            return

        steps += 1

    check_game_over(player)

# Kommentar:
# Kistmöte har flera steg med val.
# Spelaren kan få ett item eller skada.

def encounter_monster(player):
    monsters = ["Sfinx", "Varg", "Ogre", "Skuggvandrare", "Drakling"]
    monster = random.choice(monsters)
    monster_hp = random.randint(2, 4)
    monster_str = random.randint(3, 6)

    print("\n------------------------------------")
    print(f"     DU MÖTER EN {monster.upper()}")
    print("------------------------------------\n")

    steps = 0
    while monster_hp > 0 and player.hp > 0 and steps < 4:
        print("\nVad gör du?")
        if monster == "Sfinx":
            print("1) Försök lösa en gåta som sfinxen ställer")
            print("2) Försök smyga förbi försiktigt utan att väcka uppmärksamhet")
            print("3) Anfall direkt med dina vapen och styrka")
        else:
            print("1) Distrahera monstret med en oväntad handling")
            print("2) Leta efter en svag punkt att attackera")
            print("3) Attackera direkt med all kraft du har")

        choice = input("> ")

        if choice == "1":
            if random.random() < 0.5:
                monster_hp -= 1
                print("Du lyckas! Monstret tar skada.")
            else:
                dmg = random.randint(1, 3)
                print(f"Misslyckat! Monstret attackerar dig. -{dmg} HP")
                player.hp -= dmg
        elif choice == "2":
            if random.random() < 0.4:
                monster_hp -= 1
                print("Du hittar en svag punkt! Monstret tar skada.")
            else:
                dmg = random.randint(1, 3)
                print(f"Misslyckas med att hitta en svag punkt! Monstret attackerar. -{dmg} HP")
                player.hp -= dmg
        else:
            if player.get_total_strength() > monster_str:
                monster_hp -= 2
                print("Du träffar hårt! Monstret tar skada.")
            else:
                dmg = random.randint(1, 3)
                print(f"Monstret är för starkt! Du tar skada istället. -{dmg} HP")
                player.hp -= dmg

        steps += 1

    if monster_hp <= 0:
        print(f"\nDu besegrar {monster}!")
        player.level += 1
        check_game_over(player)
    else:
        print(f"\n{monster} besegrar dig…")
        player.hp = 0
        check_game_over(player)

# Kommentar:
# Monster-encounter med max 4 steg.
# Spelaren kan attackera, smyga eller lösa gåta (för Sfinx).
# Skador och monster-HP bestäms slumpmässigt och med spelarens STR.

# =====================================
# HUVUDLOOP OCH CHECK

def check_game_over(player):
    if player.hp <= 0:
        print("\nDU DOG! SPELET ÄR ÖVER.")
        exit()
    if player.level >= 10:
        print("\nDU NÅDDE LEVEL 10! DU VANN SPELET!")
        exit()
    return False

# Kommentar:
# Kontrollerar om spelaren vunnit eller dött efter varje encounter.

def game_loop(player):
    while True:
        print("\n------------------------------------")
        print(f"LEVEL: {player.level} | HP: {player.hp} | STR: {player.strength}")
        print("------------------------------------\n")

        print("Vad vill du göra?")
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

# Kommentar:
# Huvudloopen körs tills spelaren dör eller vinner.
# Spelaren kan kolla stats, inventory eller gå vidare i äventyret.

# =====================================
# MAIN

def main():
    print("====================================")
    print("    VÄLKOMMEN TILL ÄVENTYRSSPELET")
    print("====================================\n")
    print("ANTAR DU UTMANINGEN? SKRIV 'JA' FÖR ATT BÖRJA.\n")
    choice = input("> ").strip().lower()

    if choice != "ja":
        print("Du valde att inte anta utmaningen... spelet avslutas.")
        return

    print("\nModigt val! Ditt äventyr börjar nu...\n")
    name = input("Vad heter du, äventyrare? ")

    # Skapa spelare
    player = Player(name)

    print(f"\n{name}, dina startvärden är:\n")
    player.print_stats()
    print("Din ryggsäck är tom.\n")

    # Starta spelet
    game_loop(player)

# Kommentar:
# main() är startpunkten.
# Frågar spelaren om hen vill börja, skapar spelare och startar huvudloop.

if __name__ == "__main__":
    main()

# Kommentar:
# Skriptet startar bara spelet om filen körs direkt.
