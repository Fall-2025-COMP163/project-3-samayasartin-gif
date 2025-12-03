"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: Samaya Sartin

AI Usage: Microsoft Copilot

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False


# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display main menu and get player choice

    Options:
    1. New Game
    2. Load Game
    3. Exit

    Returns: Integer choice (1-3)
    """
    print("Options:\n1. New Game\n2. Load Game\n3. Exit")
    while True:
        try:
            user_choice = int(input("Enter your choice: "))
            if user_choice in (1, 2, 3):
                return user_choice
            else:
                print("Invalid choice, choose from 1-3.")
        except ValueError:
            print("Please enter a number (1-3).")


def new_game():
    """
    Start a new game

    Prompts for:
    - Character name
    - Character class

    Creates character and starts game loop
    """
    global current_character

    user_name = input("Enter your character name: ")
    user_class = input("Enter your character class: ")
    try:
        current_character = character_manager.create_character(user_name, user_class)
    except InvalidCharacterClassError:
        print("Invalid character class.")
        return None
    character_manager.save_character(current_character)
    print(f"\nHello, {user_name} the {user_class}!")
    game_loop()

def load_game():
    """
    Load an existing saved game

    Shows list of saved characters
    Prompts user to select one
    """
    global current_character

    try:
        saved_characters = character_manager.list_saved_characters()
        if not saved_characters:
            print("No saved characters found.")
            return None

        print("Saved Characters:")
        for i, name in enumerate(saved_characters, 1):
            print(f"{i}. {name}")

        choice = int(input("Choose a character to load: "))
        if 1 <= choice <= len(saved_characters):
            current_character = character_manager.load_character(saved_characters[choice - 1])
            print(f"Loaded {current_character}!")
            game_loop()
        else:
            print("Invalid choice.")
    except CharacterNotFoundError:
        print("Character not found.")
    except SaveFileCorruptedError:
        print("Save file corrupted.")


# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character

    game_running = True

    while game_running:
        choice = game_menu()
        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print("Game saved. Exiting...")
            game_running = False


def game_menu():
    """
    Display game menu and get player choice

    Options:
    1. View Character Stats
    2. View Inventory
    3. Quest Menu
    4. Explore (Find Battles)
    5. Shop
    6. Save and Quit

    Returns: Integer choice (1-6)
    """
    print("\n=== Game Menu ===")
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore (Find Battles)")
    print("5. Shop")
    print("6. Save and Quit")
    while True:
        try:
            choice = int(input("Enter your choice: "))
            if choice in (1, 2, 3, 4, 5, 6):
                return choice
            else:
                print("Invalid choice, choose 1-6.")
        except ValueError:
            print("Please enter a number (1-6).")



# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character
    character = current_character
    print("\n=== View Character Stats ===\n"
          f"Name: {character['name']}\n"
          f"Class: {character['class']}\n"
          f"Level: {character['level']}\n"
          f"Health: {character['health']}\n"
          f"Max Health: {character['max_health']}\n"
          f"Strength: {character['strength']}\n"
          f"Magic: {character['magic']}\n"
          f"Experience: {character['experience']}\n"
          f"Gold: {character['gold']}\n")
    quest_handler.display_character_quest_progress(character, all_quests)


def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    inventory_system.display_inventory(current_character, all_items)
    inventory_choice= input("\nWould you like to:\n"
                            "1) Use an item\n"
                            "2) Equip weapons\n"
                            "3) Drop item\n"
                            "Your choice:")
    if inventory_choice == "1":
        item_choice = input("\nWhat item do you want to use:")
        try:
            inventory_system.use_item(current_character, item_choice, all_items)
        except Exception as e:
            print(f"Error using item: {e}")
    elif inventory_choice == "2":
        item_choice = input("\nWhat weapon do you want to equip:")
        try:
            inventory_system.equip_weapon(current_character, item_choice, all_items)
        except Exception as e:
            print(f"Error equipping weapon: {e}")
    elif inventory_choice == "3":
        item_choice = input("\nWhat item do you want to drop:")
        try:
            inventory_system.remove_item_from_inventory(current_character, item_choice)
        except Exception as e:
            print(f"Error dropping item: {e}")


def quest_menu():
    """Quest management menu"""
    global current_character, all_quests

    while True:
        print("\n=== Quest Menu ===")
        print("1. View Active Quests")
        print("2. View Available Quests")
        print("3. View Completed Quests")
        print("4. Accept Quest")
        print("5. Abandon Quest")
        print("6. Complete Quest (for testing)")
        print("7. Back")
        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                quest_handler.display_quest_list(quest_handler.get_active_quests(current_character, all_quests))
            elif choice == "2":
                quest_handler.display_quest_list(quest_handler.get_available_quests(current_character, all_quests))
            elif choice == "3":
                quest_handler.display_quest_list(quest_handler.get_completed_quests(current_character, all_quests))
            elif choice == "4":
                quest_id = input("Enter quest ID to accept: ")
                quest_handler.accept_quest(current_character, quest_id, all_quests)
            elif choice == "5":
                quest_id = input("Enter quest ID to abandon: ")
                quest_handler.abandon_quest(current_character, quest_id)
            elif choice == "6":
                quest_id = input("Enter quest ID to complete (testing): ")
                quest_handler.complete_quest(current_character, quest_id, all_quests)
            elif choice == "7":
                print("Returning to game menu...")
                break
            else:
                print("Invalid choice. Please select 1-7.")

        except QuestNotFoundError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


def explore():
    """Find and fight random enemies"""
    global current_character
    try:
        enemy = combat_system.get_random_enemy_for_level(current_character["level"])
        print(f"\nA wild {enemy['name']} appears!")
        battle = combat_system.SimpleBattle(current_character, enemy)
        result = battle.start_battle()

        if result["winner"] == "player":
            print(f"You defeated the {enemy['name']}!")
            print(f"Gained {result['xp_gained']} XP and {result['gold_gained']} gold.")
        elif result["winner"] == "enemy":
            print("You were defeated...")
            handle_character_death()
        elif result["winner"] == "escape":
            print("You escaped safely.")
    except Exception as e:
        print(f"Error during exploration: {e}")

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items

    while True:
        print("\n=== Shop Menu ===")
        print(f"Your Gold: {current_character['gold']}")
        print("Available Items:")
        for item_id, data in all_items.items():
            print(f"- {data['name']} ({data['type']}) : {data['cost']} gold")

        print("\nOptions:\n1. Buy Item\n2. Sell Item\n3. Back")
        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                item_id = input("Enter item ID to buy: ")
                if item_id in all_items:
                    inventory_system.purchase_item(current_character, item_id, all_items[item_id])
                    print(f"Purchased {all_items[item_id]['name']}!")
                else:
                    print("Invalid item ID.")
            elif choice == "2":
                item_id = input("Enter item ID to sell: ")
                if item_id in all_items:
                    msg = inventory_system.sell_item(current_character, item_id, all_items[item_id])
                    print(msg)
                else:
                    print("Invalid item ID.")
            elif choice == "3":
                break
            else:
                print("Invalid choice.")
        except Exception as e:
            print(f"Error: {e}")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character

    try:
        character_manager.save_character(current_character)
        print(f"Game saved successfully for {current_character['name']}!")
    except FileNotFoundError:
        print("Error: Save file not found.")
    except IOError as e:
        print(f"File I/O error while saving: {e}")
    except Exception as e:
        print(f"Unexpected error while saving game: {e}")


def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items

    try:
        # Try to load quests and items
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
        print("Game data loaded successfully!")

    except MissingDataFileError:
        print("Missing data files. Creating default data...")
        game_data.create_default_data_files()
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
        print("Default data created and loaded.")

    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check your data files for formatting issues.")
        # Re-raise so main() can decide whether to exit
        raise

    except Exception as e:
        print(f"Unexpected error while loading game data: {e}")
        raise

def handle_character_death():
    """Handle character death"""
    global current_character, game_running

    print("\n=== You have fallen in battle! ===")
    print("Your character has died...")

    while True:
        choice = input("Would you like to:\n"
                       "1) Revive (costs 50 gold)\n"
                       "2) Quit Game\n"
                       "Enter your choice: ")

        if choice == "1":
            try:
                if current_character['gold'] >= 50:
                    character_manager.revive_character(current_character)
                    current_character['gold'] -= 50
                    print("You have been revived! Be careful out there...")
                else:
                    print("You don't have enough gold to revive. Game over.")
                    game_running = False
                return
            except InsufficientResourcesError:
                print("You don't have enough gold to revive. Game over.")
                game_running = False
                return
            except Exception as e:
                print(f"Unexpected error during revival: {e}")
                game_running = False
                return

        elif choice == "2":
            print("Game over. Thanks for playing!")
            game_running = False
            return

        else:
            print("Invalid choice. Please select 1 or 2.")


def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""

    # Display welcome message
    display_welcome()

    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return

    # Main menu loop
    while True:
        choice = main_menu()

        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")


if __name__ == "__main__":
    main()

