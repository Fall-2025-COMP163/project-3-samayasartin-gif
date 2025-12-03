"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: Samaya Sartin

AI Usage: Microsoft Copilot
- Debugging
- Typos


This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)


# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file

    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)

    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    if not os.path.isfile(filename):
        raise MissingDataFileError(f"Quest data file {filename} not found")
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
    except:
        raise CorruptedDataError(f"Could not read {filename} (Corrupted File)")

    quests = {}
    block = []
    for line in lines:
        line = line.strip()
        if line == "":
            if block:
                quest = parse_quest_block(block)
                quests[quest["quest_id"]] = quest
                block = []
        else:
            block.append(line)

    if block:
        quest = parse_quest_block(block)
        quests[quest["quest_id"]] = quest

    return quests

def load_items(filename="data/items.txt"):
    """
    Load item data from file

    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description

    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    if not os.path.isfile(filename):
        raise MissingDataFileError(f"Item data file {filename} not found")
    try:
        file = open(filename, "r")
        contents = file.readlines()
    except:
        raise CorruptedDataError(f"Could not read {filename} save file")
    items = {}
    item_data = {}
    item_id = None
    for line in contents:
        line = line.strip()
        if not line:
            if item_id:
                items[item_id] = item_data
                items_data = {}
                item_id = None
                continue
        if ":" not in line:
            raise InvalidDataFormatError(f"Bad line format: {line}")
        key, value = line.strip().split(":", 1)
        key = key.strip().upper()
        value = value.strip()

        if key == "ITEM_ID":
            item_id = value
        elif key in ["NAME", "TYPE", "DESCRIPTION", "EFFECT"]:
            item_data[key.lower()] = value
        elif key in ["COST"]:
            try:
                item_data[key.lower()] = int(value)
            except ValueError:
                raise InvalidDataFormatError(f"Expected integer for {key}, got {value}")
        else:
            raise InvalidDataFormatError(f"Unexpected key: {key}")
    if item_id:
        items[item_id] = item_data
    return item_data


def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields

    Required fields: quest_id, title, description, reward_xp,
                    reward_gold, required_level, prerequisite

    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    required_fields = ["quest_id", "title", "description", "reward_xp",
                       "reward_gold", "required_level", "prerequisite"]
    for field in required_fields:
        if field not in quest_dict:
            raise InvalidDataFormatError(f"Missing required field: {field}")
    for numeric_field in ["reward_xp", "reward_gold", "required_level"]:
        if not isinstance(quest_dict[numeric_field], int):
            raise InvalidDataFormatError(f"{numeric_field} must be an integer")
    return True


def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields

    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable

    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    required_fields = ["item_id", "name", "type", "effect", "cost", "description"]
    for field in required_fields:
        if field not in item_dict:
            raise InvalidDataFormatError(f"Missing required field: {field}")
    if not isinstance(item_dict["cost"], int):
        raise InvalidDataFormatError("Cost must be an integer")
    if item_dict["type"] not in ["weapon", "armor", "consumable"]:
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}")
    return True

def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    data_dir = "data"
    try:
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    except OSError as e:
        raise CorruptedDataError(f"Could not create data directory: {e}")
    quest_file = os.path.join(data_dir, "quests.txt")
    if not os.path.isfile(quest_file):
        try:
            with open(quest_file, "w") as f:
                f.write(
                    "QUEST_ID: first_steps\n"
                    "TITLE: First Steps\n"
                    "DESCRIPTION: Begin your adventure by defeating your first enemy\n"
                    "REWARD_XP: 50\n"
                    "REWARD_GOLD: 25\n"
                    "REQUIRED_LEVEL: 1\n"
                    "PREREQUISITE: NONE\n\n"
                    "QUEST_ID: goblin_hunter\n"
                    "TITLE: Goblin Hunter\n"
                    "DESCRIPTION: The village is being terrorized by goblins. Defeat 3 goblins to protect the townsfolk.\n"
                    "REWARD_XP: 100\n"
                    "REWARD_GOLD: 75\n"
                    "REQUIRED_LEVEL: 2\n"
                    "PREREQUISITE: first_steps\n\n"
                    "QUEST_ID: equipment_upgrade\n"
                    "TITLE: Better Equipment\n"
                    "DESCRIPTION: Visit the shop and purchase your first weapon or armor\n"
                    "REWARD_XP: 75\n"
                    "REWARD_GOLD: 50\n"
                    "REQUIRED_LEVEL: 2\n"
                    "PREREQUISITE: first_steps\n\n"
                    "QUEST_ID: orc_menace\n"
                    "TITLE: The Orc Menace\n"
                    "DESCRIPTION: A band of orcs has been spotted near the forest. Defeat them to earn the village's gratitude.\n"
                    "REWARD_XP: 200\n"
                    "REWARD_GOLD: 150\n"
                    "REQUIRED_LEVEL: 3\n"
                    "PREREQUISITE: goblin_hunter\n\n"
                    "QUEST_ID: dragon_slayer\n"
                    "TITLE: Dragon Slayer\n"
                    "DESCRIPTION: A fearsome dragon threatens the kingdom. Only the bravest heroes dare face this challenge.\n"
                    "REWARD_XP: 500\n"
                    "REWARD_GOLD: 500\n"
                    "REQUIRED_LEVEL: 6\n"
                    "PREREQUISITE: orc_menace\n\n"
                    "QUEST_ID: treasure_hunter\n"
                    "TITLE: Treasure Hunter\n"
                    "DESCRIPTION: Explore and collect 5 different items for your collection\n"
                    "REWARD_XP: 150\n"
                    "REWARD_GOLD: 100\n"
                    "REQUIRED_LEVEL: 3\n"
                    "PREREQUISITE: equipment_upgrade\n\n"
                    "QUEST_ID: master_adventurer\n"
                    "TITLE: Master Adventurer\n"
                    "DESCRIPTION: Reach level 10 to prove yourself as a true adventurer\n"
                    "REWARD_XP: 1000\n"
                    "REWARD_GOLD: 1000\n"
                    "REQUIRED_LEVEL: 10\n"
                    "PREREQUISITE: dragon_slayer\n"
                )

        except Exception as e:
            raise CorruptedDataError(f"Could not create quests.txt: {e}")
    items_file = os.path.join(data_dir, "items.txt")
    if not os.path.isfile(items_file):
        try:
            with open(items_file, "w") as f:
                f.write(
                    "ITEM_ID: health_potion\n"
                    "NAME: Health Potion\n"
                    "TYPE: consumable\n"
                    "EFFECT: health:20\n"
                    "COST: 25\n"
                    "DESCRIPTION: Restores 20 health points\n\n"
                    "ITEM_ID: super_health_potion\n"
                    "NAME: Super Health Potion\n"
                    "TYPE: consumable\n"
                    "EFFECT: health:50\n"
                    "COST: 75\n"
                    "DESCRIPTION: Restores 50 health points\n\n"
                    "ITEM_ID: iron_sword\n"
                    "NAME: Iron Sword\n"
                    "TYPE: weapon\n"
                    "EFFECT: strength:5\n"
                    "COST: 100\n"
                    "DESCRIPTION: A sturdy iron sword that increases strength\n\n"
                    "ITEM_ID: steel_sword\n"
                    "NAME: Steel Sword\n"
                    "TYPE: weapon\n"
                    "EFFECT: strength:10\n"
                    "COST: 250\n"
                    "DESCRIPTION: A masterwork steel sword for experienced warriors\n\n"
                    "ITEM_ID: fire_staff\n"
                    "NAME: Fire Staff\n"
                    "TYPE: weapon\n"
                    "EFFECT: magic:8\n"
                    "COST: 200\n"
                    "DESCRIPTION: A magical staff imbued with fire magic\n\n"
                    "ITEM_ID: leather_armor\n"
                    "NAME: Leather Armor\n"
                    "TYPE: armor\n"
                    "EFFECT: max_health:10\n"
                    "COST: 75\n"
                    "DESCRIPTION: Light armor that increases maximum health\n\n"
                    "ITEM_ID: steel_armor\n"
                    "NAME: Steel Armor\n"
                    "TYPE: armor\n"
                    "EFFECT: max_health:25\n"
                    "COST: 200\n"
                    "DESCRIPTION: Heavy armor providing excellent protection\n\n"
                    "ITEM_ID: magic_robe\n"
                    "NAME: Magic Robe\n"
                    "TYPE: armor\n"
                    "EFFECT: magic:5\n"
                    "COST: 150\n"
                    "DESCRIPTION: Enchanted robes that enhance magical power\n\n"
                    "ITEM_ID: strength_elixir\n"
                    "NAME: Strength Elixir\n"
                    "TYPE: consumable\n"
                    "EFFECT: strength:3\n"
                    "COST: 50\n"
                    "DESCRIPTION: Permanently increases strength by 3\n\n"
                    "ITEM_ID: wisdom_elixir\n"
                    "NAME: Wisdom Elixir\n"
                    "TYPE: consumable\n"
                    "EFFECT: magic:3\n"
                    "COST: 50\n"
                    "DESCRIPTION: Permanently increases magic by 3\n"
                )
        except Exception as e:
            raise CorruptedDataError(f"Could not create quests.txt: {e}")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary

    Args:
        lines: List of strings representing one quest

    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
    quest_data = {}
    quest_id = None

    for line in lines:
        if ": " not in line:
            raise InvalidDataFormatError(f"Bad line format: {line}")
        key, value = line.strip().split(": ", 1)
        key = key.strip().upper()
        value = value.strip()

        if key == "QUEST_ID":
            quest_id = value
        elif key in ["TITLE", "DESCRIPTION", "PREREQUISITE"]:
            quest_data[key.lower()] = value
        elif key in ["REWARD_XP", "REWARD_GOLD", "REQUIRED_LEVEL"]:
            try:
                quest_data[key.lower()] = int(value)
            except ValueError:
                raise InvalidDataFormatError(f"Expected integer for {key}, got {value}")
        else:
            raise InvalidDataFormatError(f"Unexpected key: {key}")

    if not quest_id:
        raise InvalidDataFormatError("Missing QUEST_ID field")

    quest_data["quest_id"] = quest_id
    return quest_data


def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary

    Args:
        lines: List of strings representing one item

    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    item_data = {}
    item_id = None

    for line in lines:
        if ": " not in line:
            raise InvalidDataFormatError(f"Bad line format: {line}")

        key, value = line.strip().split(": ", 1)
        key = key.strip().upper()
        value = value.strip()

        if key == "ITEM_ID":
            item_id = value
        elif key in ["NAME", "TYPE", "DESCRIPTION", "EFFECT"]:
            item_data[key.lower()] = value
        elif key == "COST":
            try:
                item_data[key.lower()] = int(value)
            except ValueError:
                raise InvalidDataFormatError(f"Expected integer for COST, got {value}")
        else:
            raise InvalidDataFormatError(f"Unexpected key: {key}")

    if not item_id:
        raise InvalidDataFormatError("Missing ITEM_ID field")

    # Attach item_id as part of the dictionary
    item_data["item_id"] = item_id

    return item_data


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")

    # Test creating default files
    create_default_data_files()

    # Test loading quests
    try:
        quests = load_quests()
        print(f"Loaded {len(quests)} quests")
    except MissingDataFileError:
        print("Quest file not found")
    except InvalidDataFormatError as e:
        print(f"Invalid quest format: {e}")

    # Test loading items
    try:
        items = load_items()
        print(f"Loaded {len(items)} items")
    except MissingDataFileError:
        print("Item file not found")
    except InvalidDataFormatError as e:
        print(f"Invalid item format: {e}")
