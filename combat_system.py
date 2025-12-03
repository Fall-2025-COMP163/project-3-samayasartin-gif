"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: Samaya Sartin

AI Usage: Microsoft Copilot
- Typo checks
- Explaining how to use different methods with other methods without inheritance

Handles combat mechanics
"""

import character_manager
import random
from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    """
    Create an enemy based on type

    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100

    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
    enemies = ["Goblin","goblin", "Orc", "orc", "Dragon", "dragon"]
    if enemy_type not in enemies:
        raise InvalidTargetError(f"{enemy_type} is not valid.")
    enemy_type = enemy_type.lower()
    if enemy_type == "goblin":
        return {"name": "Goblin", "health": 50, "max_health": 50,
                "strength": 8, "magic": 2, "xp_reward": 25, "gold_reward": 10}
    elif enemy_type == "orc":
        return {"name": "Orc", "health": 80, "max_health": 80,
                "strength": 12, "magic": 5, "xp_reward": 50, "gold_reward": 25}
    elif enemy_type == "dragon":
        return {"name": "Dragon", "health": 200, "max_health": 200,
                "strength": 25, "magic": 15, "xp_reward": 200, "gold_reward": 100}
    else:
        raise InvalidTargetError(f"{enemy_type} is not valid.")


def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level

    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons

    Returns: Enemy dictionary
    """
    if character_level < 3:
        return create_enemy("goblin")
    elif character_level < 6:
        return create_enemy("orc")
    elif character_level >= 6:
        return create_enemy("dragon")


# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system

    Manages combat between character and enemy
    """

    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        self.character = character
        self.enemy = enemy
        self.combat_active = True
        self.turn = 1

    def start_battle(self):
        """
        Start the combat loop

        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}

        Raises: CharacterDeadError if character is already dead
        """
        if self.character["health"] <= 0:
            raise CharacterDeadError(f"{self.character['name']} is already dead.")

        self.combat_active = True

        while self.character["health"] > 0 and self.enemy["health"] > 0 and self.combat_active:

            self.player_turn()
            display_combat_stats(self.character,self.enemy)
            if self.enemy["health"] <= 0 or self.combat_active == False:
                break

            self.enemy_turn()
            display_combat_stats(self.character, self.enemy)
            if self.character["health"] <= 0 or self.combat_active == False:
                break
                
        if self.combat_active == False:
            return {"winner": "escape", "xp_gained": 0, "gold_gained": 0}
        elif self.character["health"] > 0:
            xp = self.enemy["xp_reward"]
            gold = self.enemy["gold_reward"]
            character_manager.gain_experience(self.character, xp)
            character_manager.add_gold(self.character, gold)
            return {"winner": "player", "xp_gained": xp, "gold_gained": gold}
        else:
            return {"winner": "enemy", "xp_gained": 0, "gold_gained": 0}

    def player_turn(self):
        """
        Handle player's turn

        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run

        Raises: CombatNotActiveError if called outside of battle
        """
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active.")
        print(f"1. Basic Attack\n2. Special Ability\n3. Try to Run")
        combat_choice = input("What is your move?(1, 2, or 3): ")
        if combat_choice == "1":
            damage = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, damage)
        elif combat_choice == "2":
            use_special_ability(self.character, self.enemy)
        elif combat_choice == "3":
            self.attempt_escape()

    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI

        Enemy always attacks

        Raises: CombatNotActiveError if called outside of battle
        """
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active.")
        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)


    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack

        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1

        Returns: Integer damage amount
        """
        damage = attacker["strength"] - (defender["strength"] // 4)
        if damage < 1:
            damage = 1
        display_battle_log(f"{attacker['name']} has hit {defender['name']} for {damage} damage!")
        return damage

    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy

        Reduces health, prevents negative health
        """
        target["health"] -= damage
        if target["health"] <= 0:
            target["health"] = 0

    def check_battle_end(self):
        """
        Check if battle is over

        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        if self.character["health"] <= 0:
            print(f"{self.character['name']} is dead.\n Battle is over.")
        elif self.enemy["health"] <= 0:
            print(f"{self.character['name']} is dead.\n Battle is over.")
        else:
            None

    def attempt_escape(self):
        """
        Try to escape from battle

        50% success chance

        Returns: True if escaped, False if failed
        """
        escape = random.randint(1,2)
        if escape == 1:
            display_battle_log("Your escape plan was successful! PONK.")
            self.combat_active = False
        elif escape == 2:
            display_battle_log("Your escape plan was unsuccessful! Keep fighting!")
            self.combat_active = True
        # Use random number or simple calculation
        # If successful, set combat_active to False


# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability

    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)

    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
    if character["class"] == "Warrior":
        warrior_power_strike(character, enemy)
    elif character["class"] == "Mage":
        mage_fireball(character, enemy)
    elif character["class"] == "Rogue":
        rogue_critical_strike(character, enemy)
    elif character["class"] == "Cleric":
        cleric_heal(character)

    # Track cooldowns (optional advanced feature)



def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    power_strike = character["strength"] * 2
    enemy["health"] -= power_strike
    display_battle_log(f"{character['name']} has used Power Strike on enemy, taking {power_strike} damage.")


def mage_fireball(character, enemy):
    """Mage special ability"""
    fireball = character["magic"] * 2
    enemy["health"] -= fireball
    display_battle_log(f"{character['name']} has used Fireball on enemy, taking {fireball} damage.")


def rogue_critical_strike(character, enemy):
    """Rogue special ability"""

    chance = random.randint(1,2)
    if chance == 1:
        critical_strike = character["strength"] * 2
    elif chance == 2:
        critical_strike = character["strength"] * 3
    enemy["health"] -= critical_strike
    display_battle_log(f"{character['name']} has used Critical Strike on enemy, taking {critical_strike} damage.")


def cleric_heal(character):
    """Cleric special ability"""
    character["health"] += 30
    if character["health"] < character["max_health"]:
        character["health"] = character["max_health"]
    display_battle_log(f"{character['name']} has healed themselves.")


# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Check if character is in condition to fight

    Returns: True if health > 0 and not in battle
    """
    if character["health"] <= 0:
        return False
    else:
        return True


def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy

    Returns: Dictionary with 'xp' and 'gold'
    """
    return{
        "xp": enemy["xp_reward"],
        "gold": enemy["gold_reward"]
    }


def display_combat_stats(character, enemy):
    """
    Display current combat status

    Shows both character and enemy health/stats
    """
    print(f"{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}\n")


def display_battle_log(message):
    """
    Display a formatted battle message
    """
    print(f">>> {message}")


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")

    # Test enemy creation
    try:
        goblin = create_enemy("goblin")
        print(f"Created {goblin['name']}")
    except InvalidTargetError as e:
         print(f"Invalid enemy: {e}")

    # Test battle
    test_char = {
         'name': 'Hero',
         'class': 'Warrior',
         'health': 120,
         'max_health': 120,
         'strength': 15,
         'magic': 5
     }

    battle = SimpleBattle(test_char, goblin)
    try:
        result = battle.start_battle()
        print(f"Battle result: {result}")
    except CharacterDeadError:
        print("Character is dead!")

