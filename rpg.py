import random

# =====================================
# KLASSER
# =====================================

class Item:
    def __init__(self, name, strength_bonus):
        self.name = name
        self.strength_bonus = strength_bonus

# Kommentar:
# Klassen Item representerar ett föremål som spelaren kan ha i sin ryggsäck.
# Varje Item har ett namn och en styrkebonus som påverkar spelarens STR i strider.

class Player:
    def __init__(self, name, strength=5, hp=10, level=1):
        self.name = name
        self.strength = strength
        self.hp = hp
        self.level = level
        self.inventory = []

    # Beräknar spelarens totala styrka, inklusive bonusar från items
    def get_total_strength(self):
        return self.strength + sum(item.strength_bonus for item in self.inventory)

    # Lägger till ett item i inventoryt, hanterar full ryggsäck
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

    # Byter ut ett item i inventoryt
    def replace_item(self, index, new_item):
        if 0 <= index < len(self.inventory):
            old = self.inventory[index]
            self.inventory[index] = new_item
            print(f"\nDu byter ut '{old.name}' mot '{new_item.name}'!")

    # Skriver ut spelarens egenskaper med separationslinjer och mellanrum
    def print_stats(self):
        print("\n====================================")
        print("          DINA EGENSKAPER           ")
        print("====================================")
        print(f"HP     : {self.hp}")
        print(f"STR    : {self.strength} (+{self.get_total_strength() - self.strength} från items)")
        print(f"LEVEL  : {self.level}")
        print("====================================\n")

    # Skriver ut spelarens inventory med snygga rubriker och separationslinjer
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
# Player-klassen innehåller allt som behövs för att representera spelaren:
# - Grundläggande egenskaper: HP, STR, LEVEL
# - Inventory: en lista med Item-objekt
# - Funktioner för att lägga till/ersätta items
# - Funktioner för att skriva ut stats och inventory

# =====================================
# FUNKTIONER FÖR ATT SKAPA ITEMS OCH SCENER
# =====================================

# Skapar ett slumpmässigt item med namn och STR-bonus
def create_random_item():
    names = ["Glödande Dolk", "Månring", "Eldstav", "Skuggkappa", "Järnsandal"]
    name = random.choice(names)
    bonus = random.randint(1, 4)
    return Item(name, bonus)

# Kommentar:
# Denna funktion används när spelaren hittar en kista.
# Ett nytt Item skapas slumpmässigt med styrkebonus 1-4.

# Slumpar fram vilken scen spelaren hamnar i
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
# generate_scene väljer slumpmässigt en av flera scener och kör den.
# Detta ger variation i äventyret och gör att spelaren inte vet vad som väntar.

# =====================================
# SCENER / MÖTEN
# =====================================

def scene_fork_road(player):
    print("\n------------------------------------")
    print("        VÄGSKÄL I SKOGEN")
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
# En typisk scen där spelaren får flera val.
# Valen påverkar vad som händer: monster, fälla eller kista.
# Om spelaren anger ogiltig input får hen ändå en konsekvens (monster).

def scene_ambush_monster(player):
    print("\n------------------------------------")
    print("           MONSTERAMBUSH")
    print("------------------------------------")
    print("\nEtt monster hoppar fram ur buskarna och stirrar hotfullt på dig!\n")
    encounter_monster(player)

# Kommentar:
# Enkel scen som alltid leder till ett monster-möte.

def scene_trap_pit(player):
    print("\n------------------------------------")
    print("               FALLFÄLLA")
    print("------------------------------------")
    print("\nMarken ser stabil ut, men plötsligt sjunker den under dina fötter...\n")
    encounter_trap_interactive(player)

# Kommentar:
# Tidigare var detta en enkel HP-reducering, nu är det ett interaktivt möte
# där spelaren får tre val för att försöka undvika fällan.

def scene_mysterious_old_man(player):
    print("\n------------------------------------")
    print("           GAMMAL MANNEN")
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
# Detta är en interaktiv scen med flera val som påverkar styrka, inventory eller träff av fälla.
# Den visar hur story-element kan kombineras med strids-/fälllogik.

def scene_dark_cave(player):
    print("\n------------------------------------")
    print("              MÖRK GROTTA")
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

def scene_find_chest(player):
    print("\n------------------------------------")
    print("               GAMMAL KISTA")
    print("------------------------------------")
    print("\nDu hittar en gammal kista som glimmar till i skenet från solen eller facklan.\n")
    encounter_chest_interactive(player)

# Kommentar:
# Alla scener använder nu interaktiva encounters istället för snabba HP-förändringar.
# Valen är längre beskrivningar för bättre storykänsla.

# =====================================
# INTERAKTIVA ENCOUNTERS
# =====================================

def encounter_trap_interactive(player):
    print("\n------------------------------------")
    print("               FALLFÄLLA")
    print("------------------------------------")
    print("\nDu märker att marken under dig är instabil och farlig.\n")
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
# Trappan/fällan är nu interaktiv med flera steg.
# Spelaren får 3 val på varje steg, och slumpmässiga konsekvenser avgör om hen skadas eller inte.

def encounter_chest_interactive(player):
    print("\n------------------------------------")
    print("               MYSTISK KISTA")
    print("------------------------------------")
    print("\nDu närmar dig en gammal kista och funderar på vad som kan finnas inuti.\n")
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
# Kistan har nu flera steg där spelaren får välja mellan olika sätt att interagera.
# Utfallet påverkas av slump + inventory, och spelaren kan skadas eller få ett item.

# =====================================
# MONSTER ENCOUNTERS
# =====================================

def encounter_monster(player):
    monsters = ["Sfinx", "Varg", "Ogre", "Skuggvandrare", "Drakling"]
    monster = random.choice(monsters)
    monster_hp = random.randint(2, 4)
    monster_str = random.randint(3, 6)

    print("\n------------------------------------")
    print(f"           DU MÖTER EN {monster.upper()}")
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
                print("Du lyckas! Monstret tar skada.")
                monster_hp -= 1
            else:
                print("Misslyckat! Monstret attackerar dig.")
                dmg = random.randint(1, 3)
                player.hp -= dmg
                print(f"-{dmg} HP")
        elif choice == "2":
            if random.random() < 0.4:
                print("Du hittar en svag punkt! Monstret tar skada.")
                monster_hp -= 1
            else:
                print("Misslyckas med att hitta en svag punkt! Monstret attackerar.")
                dmg = random.randint(1, 3)
                player.hp -= dmg
                print(f"-{dmg} HP")
        else:
            if player.get_total_strength() > monster_str:
                print("Du träffar hårt! Monstret tar skada.")
                monster_hp -= 2
            else:
                print("Monstret är för starkt! Du tar skada istället.")
                dmg = random.randint(1, 3)
                player.hp -= dmg
                print(f"-{dmg} HP")

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
# Monster-encounters är flerstegs-interaktiva med tre val per steg.
# Spelaren kan attackera, distrahera eller smyga.
# Resultatet avgörs av slump och spelarens totala styrka.
# Max 4 steg per encounter. Monster eller spelare kan dö.

# =====================================
# HUVUDLOOP OCH CHECK
# =====================================

def check_game_over(player):
    if player.hp <= 0:
        print("\nDU DOG! SPELET ÄR ÖVER.")
        exit()
    if player.level >= 10:
        print("\nDU NÅDDE LEVEL 10! DU VANN SPELET!")
        exit()
    return False

# Kommentar:
# Kontrollera om spelaren har dött eller vunnit spelet.
# Används efter alla encounters.

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
# Huvudloopen som kör spelet tills spelaren vinner eller dör.
# Spelaren kan kolla stats, inventory eller gå vidare till nästa scen.

# =====================================
# MAIN
# =====================================

def main():
    print("====================================")
    print("       VÄLKOMMEN TILL ÄVENTYRSSPELET")
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
# main() startar spelet, frågar spelaren om hen vill anta utmaningen.
# Skapar spelaren och startar game_loop.
# Detta är ingångspunkten för programmet.

# =====================================
# STARTA SPELET
# =====================================

if __name__ == "__main__":
    main()

# Kommentar:
# Detta säkerställer att spelet startar endast när filen körs direkt.
