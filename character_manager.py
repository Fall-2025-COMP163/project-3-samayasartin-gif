"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: Samaya Sartin

AI Usage: Microsoft Copilot
- Debugging 
- Elaborating on subjects like dictionaries and lists

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)


# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):
    """
    Create a new character with stats based on class

    Valid classes: Warrior, Mage, Rogue, Cleric

    Returns: Dictionary with character data including:
            - name, class, level, health, max_health, strength, magic
            - experience, gold, inventory, active_quests, completed_quests

    Raises: InvalidCharacterClassError if class is not valid
    """
    valid_classes = ["Warrior", "Mage", "Rogue", "Cleric"]
    if character_class not in valid_classes:
        raise InvalidCharacterClassError(f"{character_class} is not valid.")

    if character_class == "Warrior":
        health = 120
        strength = 15
        magic = 5
    elif character_class == "Mage":
        health = 80
        strength = 8
        magic = 20
    elif character_class == "Rogue":
        health = 90
        strength = 12
        magic = 10
    elif character_class == "Cleric":
        health = 100
        strength = 10
        magic = 15
    return {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": health,
        "max_health": health,
        "strength": strength,
        "magic": magic,
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": []
    }

    # Validate character_class first
    # Example base stats:
    # Warrior: health=120, strength=15, magic=5
    # Mage: health=80, strength=8, magic=20
    # Rogue: health=90, strength=12, magic=10
    # Cleric: health=100, strength=10, magic=15

    # All characters start with:
    # - level=1, experience=0, gold=100
    # - inventory=[], active_quests=[], completed_quests=[]

    # Raise InvalidCharacterClassError if class not in valid list

def save_character(character, save_directory="data/save_games"):
    """
    Save character to file

    Filename format: {character_name}_save.txt

    File format:
    NAME: character_name
    CLASS: class_name
    LEVEL: 1
    HEALTH: 120
    MAX_HEALTH: 120
    STRENGTH: 15
    MAGIC: 5
    EXPERIENCE: 0
    GOLD: 100
    INVENTORY: item1,item2,item3
    ACTIVE_QUESTS: quest1,quest2
    COMPLETED_QUESTS: quest1,quest2

    Returns: True if successful
    Raises: PermissionError, IOError (let them propagate or handle)
    """
    if not os.path.exists(save_directory): #Checksif pathway exist in files
        os.makedirs(save_directory) # if not creates one
    filename = f"{character['name']}_save.txt"
    filepath = os.path.join(save_directory, filename) #joins saved directory with file name so that it actually saves
    with open(filepath, "w") as file:
        file.write(f"NAME: {character['name']}\n")
        file.write(f"CLASS: {character['class']}\n")
        file.write(f"LEVEL: {character['level']}\n")
        file.write(f"HEALTH: {character['health']}\n")
        file.write(f"MAX HEALTH: {character['max_health']}\n")
        file.write(f"STRENGTH: {character['strength']}\n")
        file.write(f"MAGIC: {character['magic']}\n")
        file.write(f"EXPERIENCE: {character['experience']}\n")
        file.write(f"GOLD: {character['gold']}\n")
        file.write(f"INVENTORY: {','.join(character['inventory'])}\n")
        file.write(f"ACTIVE QUESTS: {','.join(character['active_quests'])}\n") #lists of active quests is seperated by commas like needed
        file.write(f"COMPLETED QUESTS: {','.join(character['completed_quests'])}\n")

    return True


def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file

    Args:
        character_name: Name of character to load
        save_directory: Directory containing save files

    Returns: Character dictionary
    Raises:
        CharacterNotFoundError if save file doesn't exist
        SaveFileCorruptedError if file exists but can't be read
        InvalidSaveDataError if data format is wrong
    """
    # Check if file exists → CharacterNotFoundError
    filename = os.path.join(save_directory, f"{character_name}_save.txt")
    if not os.path.isfile(filename):
        raise CharacterNotFoundError(f"{character_name} is not a valid save file.")
    # Try to read file → SaveFileCorruptedError
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
    except:
        raise SaveFileCorruptedError(f"Could not read {character_name}'s save file (Corrupted File)")
    # Validate data format → InvalidSaveDataError
    character = {}
    try:
        for line in lines:
            if ":" not in line:
                raise InvalidSaveDataError("Bad line format")
            key, value = line.strip().split(":", 1)
            key = key.strip().upper()
            value = value.strip()

            if key in ["LEVEL", "HEALTH", "MAX_HEALTH", "STRENGTH", "MAGIC", "EXPERIENCE", "GOLD"]:
                character[key.lower()] = int(value)
            elif key in ["INVENTORY", "ACTIVE_QUESTS", "COMPLETED_QUESTS"]:
                character[key.lower()] = value.split(",") if value else []
            elif key in ["NAME", "CLASS"]:
                character[key.lower()] = value
            else:
                raise InvalidSaveDataError(f"Unexpected field: {key}")
    except Exception as e:
        raise InvalidSaveDataError(f"Invalid save data format: {e}")
    return character


def list_saved_characters(save_directory="data/save_games"):
    """
    Get list of all saved character names

    Returns: List of character names (without _save.txt extension)
    """
    if not os.path.exists(save_directory):
        return []

    files = os.listdir(save_directory)
    save_files = [f for f in files if f.endswith("_save.txt")]
    names = [f.replace("_save.txt", "") for f in save_files]

    return names

def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file

    Returns: True if deleted successfully
    Raises: CharacterNotFoundError if character doesn't exist
    """
    filepath = os.path.join(save_directory, f"{character_name}_save.txt")
    if os.path.isfile(filepath):
        os.remove(filepath)
        return True
    else:
        raise CharacterNotFoundError(f"{character_name} is not a valid save file.")
    # Verify file exists before attempting deletion


# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add experience to character and handle level ups

    Level up formula: level_up_xp = current_level * 100
    Example when leveling up:
    - Increase level by 1
    - Increase max_health by 10
    - Increase strength by 2
    - Increase magic by 2
    - Restore health to max_health

    Raises: CharacterDeadError if character health is 0
    """
    # Check if character is dead first
    if character["health"] == 0:
        raise CharacterDeadError(f"{character['name']} is dead")
    character["experience"] += xp_amount
    while character["experience"] >= character["level"] * 100:
        character["experience"] -= character["level"] * 100
        character["level"] += 1
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        character["health"] = character["max_health"]


def add_gold(character, amount):
    """
    Add gold to character's inventory

    Args:
        character: Character dictionary
        amount: Amount of gold to add (can be negative for spending)

    Returns: New gold total
    Raises: ValueError if result would be negative
    """
    new_total = character["gold"] + amount
    if new_total < 0:
        raise ValueError("Gold cannot be negative")
    character["gold"] = new_total
    return character["gold"]


def heal_character(character, amount):
    """
    Heal character by specified amount

    Health cannot exceed max_health

    Returns: Actual amount healed
    """
    if character["health"] <= 0:
        raise CharacterDeadError(f"{character['name']} is dead and cannot be healed.")
    healed = min(amount, character["max_health"] - character["health"])
    character["health"] += healed
    return healed



def is_character_dead(character):
    """
    Check if character's health is 0 or below

    Returns: True if dead, False if alive
    """
    if character["health"] <= 0:
        return True
    else:
        return False


def revive_character(character):
    """
    Revive a dead character with 50% health

    Returns: True if revived
    """
    if character["health"] <= 0:
        character["health"] = character["max_health"] // 2
        return True
    else:
        raise CharacterDeadError("Character is alive and cannot be revived.")


# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Validate that character dictionary has all required fields

    Required fields: name, class, level, health, max_health,
                    strength, magic, experience, gold, inventory,
                    active_quests, completed_quests

    Returns: True if valid
    Raises: InvalidSaveDataError if missing fields or invalid types
    """
    required = ["name", "class", "level", "health", "max_health", "strength", "magic",
                "experience", "gold", "inventory", "active_quests", "completed_quests"]
    for key in required:
        if key not in character:
            raise InvalidSaveDataError(f"Missing field: {key}")
    if not isinstance(character["level"], int):
        raise InvalidSaveDataError("Level must be int")
    if not isinstance(character["inventory"], list):
        raise InvalidSaveDataError("Inventory must be list")
    return True


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")

    # Test character creation
    try:
        char = create_character("TestHero", "Warrior")
        print(f"Created: {char['name']} the {char['class']}")
        print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    except InvalidCharacterClassError as e:
        print(f"Invalid character class: {e}")
    # Test saving
    try:
        save_character(char)
        print(f"Saved: {char['name']} the {char['class']}")
    except Exception as e:
        print(f"Save error: {e}")
    # Test loading
    try:
        loaded = load_character(char)
        print(f"Loaded: {loaded['name']}")
    except CharacterNotFoundError:
        print("Character not found")
    except SaveFileCorruptedError:
        print(f"Save file corrupted")
