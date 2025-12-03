"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: Samaya Sartin

AI Usage: [Document any AI assistance used]

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20


# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    """
    Add an item to character's inventory

    Args:
        character: Character dictionary
        item_id: Unique item identifier

    Returns: True if added successfully
    Raises: InventoryFullError if inventory is at max capacity
    """
    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError()
    else:
        character["inventory"].append(item_id)
    return True


def remove_item_from_inventory(character, item_id):
    """
    Remove an item from character's inventory

    Args:
        character: Character dictionary
        item_id: Item to remove

    Returns: True if removed successfully
    Raises: ItemNotFoundError if item not in inventory
    """
    if item_id in character["inventory"]:
        character["inventory"].remove(item_id)
    else:
        raise ItemNotFoundError("Item not in inventory")


def has_item(character, item_id):
    """
    Check if character has a specific item

    Returns: True if item in inventory, False otherwise
    """
    if item_id in character["inventory"]:
        return True
    else:
        return False

def count_item(character, item_id):
    """
    Count how many of a specific item the character has

    Returns: Integer count of item
    """
    items = list.count(character["inventory"], item_id)
    return items


def get_inventory_space_remaining(character):
    """
    Calculate how many more items can fit in inventory

    Returns: Integer representing available slots
    """
    space_left = MAX_INVENTORY_SIZE- list.count(character["inventory"])
    return space_left


def clear_inventory(character):
    """
    Remove all items from inventory

    Returns: List of removed items
    """
    removed_items = list(character["inventory"])
    character["inventory"] = []
    return removed_items



# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    """
    Use a consumable item from inventory

    Args:
        character: Character dictionary
        item_id: Item to use
        item_data: Item information dictionary from game_data

    Item types and effects:
    - consumable: Apply effect and remove from inventory
    - weapon/armor: Cannot be "used", only equipped

    Returns: String describing what happened
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'consumable'
    """
    if item_id not in character["inventory"]:
        raise ItemNotFoundError("Item not in inventory")
    elif item_id in character["inventory"]:
        if item_data["type"] != "consumable":
            raise InvalidItemTypeError("Item type is not consumable")
        elif item_data["type"] == "consumable":
            broken = parse_item_effect(item_data["effect"])
            apply_stat_effect(character, broken[0], broken[1])
        return f"{item_data["item_id"]} was use increasing {broken[0]} by {broken[1]}"


def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon

    Args:
        character: Character dictionary
        item_id: Weapon to equip
        item_data: Item information dictionary

    Weapon effect format: "strength:5" (adds 5 to strength)

    If character already has weapon equipped:
    - Unequip current weapon (remove bonus)
    - Add old weapon back to inventory

    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'weapon'
    """
    if item_id not in character["inventory"]:
        raise ItemNotFoundError("Item not in inventory")
    if item_data["type"] != "weapon":
        raise InvalidItemTypeError("Item cannot be equipped because it is not a weapon.")

    if "equipped_weapon" in character and character["equipped_weapon"]:
        old_item_id = character["equipped_weapon"]
        character["inventory"].append(old_item_id)
    stat, value = parse_item_effect(item_data["effect"])
    character[stat] = character.get(stat, 0) + value

    character["equipped_weapon"] = item_id

    # Remove from inventory
    character["inventory"].remove(item_id)

    return f"Equipped {item_id}."


def equip_armor(character, item_id, item_data):
    """
    Equip armor

    Args:
        character: Character dictionary
        item_id: Armor to equip
        item_data: Item information dictionary

    Armor effect format: "max_health:10" (adds 10 to max_health)

    If character already has armor equipped:
    - Unequip current armor (remove bonus)
    - Add old armor back to inventory

    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'armor'
    """
    if item_id not in character["inventory"]:
        raise ItemNotFoundError("Item not in inventory")

    if item_data["type"] != "armor":
        raise InvalidItemTypeError("Item can not be equipped because it is not a weapon.")

    if "equipped_armor" in character and character["equipped_weapon"]:
        old_armor = character["equipped_armor"]
        old_effect = old_armor["effect"]
        broken = parse_item_effect(old_effect)
        stats = broken[0]
        value = int(broken[1])
        character[stats] -= value
        character["inventory"].append(old_armor["item_id"])

    if item_data["type"] == "armor":
        effects = item_data["effect"]
        broken = parse_item_effect(effects)
        stats = broken[0]
        value = int(broken[1])
        if stats in character:
            character[stats] += int(value)
        else:
            character[stats] = int(value)
    character["inventory"].remove(item_id)


def unequip_weapon(character):
    """
    Remove equipped weapon and return it to inventory

    Returns: Item ID that was unequipped, or None if no weapon equipped
    Raises: InventoryFullError if inventory is full
    """
    if "equipped_weapon" in character and character["equipped_weapon"]:
        weapon_id = character["equipped_weapon"]
        weapon_data = item_data_dict[weapon_id]  # look up the weapon’s data
        stat, value = parse_item_effect(weapon_data["effect"])
        character[stat] -= value

        if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
            raise InventoryFullError("Inventory full")

        character["inventory"].append(weapon_id)
        character["equipped_weapon"] = None

        return weapon_id
    return None


def unequip_armor(character):
    """
    Remove equipped armor and return it to inventory

    Returns: Item ID that was unequipped, or None if no armor equipped
    Raises: InventoryFullError if inventory is full
    """
    if "equipped_armor" in character and character["equipped_armor"]:
        armor = character["equipped_armor"]
        effect = armor["effect"]
        broken = parse_item_effect(effect)
        stats = broken[0]
        value = int(broken[1])
        character[stats] -= value
        if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
            raise InventoryFullError("Inventory full")

        character["inventory"].append(armor["item_id"])
        character["equipped_armor"] = None

        return f"{armor["item_id"]} was unequipped."
    return None


# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    """
    Purchase an item from a shop

    Args:
        character: Character dictionary
        item_id: Item to purchase
        item_data: Item information with 'cost' field

    Returns: True if purchased successfully
    Raises:
        InsufficientResourcesError if not enough gold
        InventoryFullError if inventory is full
    """
    if character["gold"] < item_data["cost"]:
        raise InsufficientResourcesError("Not enough gold to purchase.")
    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory full")
    character["gold"] -= item_data["cost"]
    character["inventory"].append(item_id)
    return True


def sell_item(character, item_id, item_data):
    """
    Sell an item for half its purchase cost

    Args:
        character: Character dictionary
        item_id: Item to sell
        item_data: Item information with 'cost' field

    Returns: Amount of gold received
    Raises: ItemNotFoundError if item not in inventory
    """
    if item_id not in character["inventory"]:
        raise ItemNotFoundError("Item not in inventory")
    price = item_data["cost"] // 2
    character["inventory"].remove(item_id)
    character["gold"] += price
    return price


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    """
    Parse item effect string into stat name and value

    Args:
        effect_string: String in format "stat_name:value"

    Returns: Tuple of (stat_name, value)
    Example: "health:20" → ("health", 20)
    """
    broken = effect_string.split(":", 1)
    return (broken[0], int(broken[1]))


def apply_stat_effect(character, stat_name, value):
    """
    Apply a stat modification to character

    Valid stats: health, max_health, strength, magic

    Note: health cannot exceed max_health
    """
    if stat_name == "health":
        if (character["health"] + value) > character["max_health"]:
            character["health"] = character["max_health"]
    else:
        character[stat_name] += value



def display_inventory(character, item_data_dict):
    """
    Display character's inventory in formatted way

    Args:
        character: Character dictionary
        item_data_dict: Dictionary of all item data

    Shows item names, types, and quantities
    """
    if character["inventory"] == []:
        print(f"Inventory is empty")
    inventory = character["inventory"]
    counts = {}
    for item in inventory:
        counts[item] = counts.get(item, 0) + 1

    print("Inventory:")
    for item_id, qty in counts.items():
        if item_id in item_data_dict:
            name = item_data_dict[item_id]["name"]
            item_type = item_data_dict[item_id]["type"]
            print(f"- {name} ({item_type}) x{qty}")
        else:
            print(f"- {item_id} (unknown) x{qty}")



# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")

    # Test adding items
    test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}

    try:
        add_item_to_inventory(test_char, "health_potion")
        print(f"Inventory: {test_char['inventory']}")
    except InventoryFullError:
        print("Inventory is full!")

    # Test using items
    test_item = {
        'item_id': 'health_potion',
        'type': 'consumable',
        'effect': 'health:20'
     }

    try:
        result = use_item(test_char, "health_potion", test_item)
        print(result)
    except ItemNotFoundError:
        print("Item not found")
