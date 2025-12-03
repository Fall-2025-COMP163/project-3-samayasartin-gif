"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: Samaya Sartin

AI Usage: Microsoft Copilot 
- Exception Usage
- Typos
- Debugging

This module handles quest management, dependencies, and completion.
"""
from character_manager import gain_experience, add_gold
from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)


# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    """
    Accept a new quest

    Args:
        character: Character dictionary
        quest_id: Quest to accept
        quest_data_dict: Dictionary of all quest data

    Requirements to accept quest:
    - Character level >= quest required_level
    - Prerequisite quest completed (if any)
    - Quest not already completed
    - Quest not already active

    Returns: True if quest accepted
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        InsufficientLevelError if character level too low
        QuestRequirementsNotMetError if prerequisite not completed
        QuestAlreadyCompletedError if quest already done
    """
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"{quest_id} does not exist.")
    quest_info = quest_data_dict[quest_id]
    if character["level"] < quest_info["required_level"]:
        raise InsufficientLevelError("Character's level is too low.")
    if quest_info["prerequisite"] != "NONE":
        if quest_info["prerequisite"] not in character["completed_quests"]:
            raise QuestRequirementsNotMetError("Character is not ready for this quest.")
    if quest_id in character["completed_quests"]:
        raise QuestAlreadyCompletedError(f"{quest_id} has already been completed.")
    if quest_id in character["active_quests"]:
        return False
    else:
        character["active_quests"].append(quest_id)
        return True


def complete_quest(character, quest_id, quest_data_dict):
    """
    Complete an active quest and grant rewards

    Args:
        character: Character dictionary
        quest_id: Quest to complete
        quest_data_dict: Dictionary of all quest data

    Rewards:
    - Experience points (reward_xp)
    - Gold (reward_gold)

    Returns: Dictionary with reward information
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        QuestNotActiveError if quest not in active_quests
    """
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"{quest_id} does not exist.")
    quest_info = quest_data_dict[quest_id]
    if quest_id not in character["active_quests"]:
        raise QuestNotActiveError(f"{quest_id} is not active.")
    character["active_quests"].remove(quest_id)
    character["completed_quests"].append(quest_id)
    gain_experience(character, quest_info["reward_xp"])
    add_gold(character, quest_info["reward_gold"])
    return {
        "quest": quest_id,
        "message": f"{quest_id.upper()} COMPLETED!",
        "reward_gold": quest_info["reward_gold"],
        "reward_xp": quest_info["reward_xp"]
    }

def abandon_quest(character, quest_id):
    """
    Remove a quest from active quests without completing it

    Returns: True if abandoned
    Raises: QuestNotActiveError if quest not active
    """
    if quest_id not in character["active_quests"]:
        raise QuestNotActiveError(f"{quest_id} is not active.")
    character["active_quests"].remove(quest_id)
    return True



def get_active_quests(character, quest_data_dict):
    """
    Get full data for all active quests

    Returns: List of quest dictionaries for active quests
    """
    active_quests = character["active_quests"]
    result = []
    for quest_id in active_quests:
        if quest_id in quest_data_dict:
            result.append(quest_data_dict[quest_id])
        else:
            raise QuestNotFoundError(f"{quest_id} does not exist.")
    return result


def get_completed_quests(character, quest_data_dict):
    """
    Get full data for all completed quests

    Returns: List of quest dictionaries for completed quests
    """
    complete_quests = character["completed_guests"]
    result = []
    for quest_id in complete_quests:
        if quest_id in quest_data_dict:
            result.append(quest_data_dict[quest_id])
        else:
            raise QuestNotFoundError(f"{quest_id} does not exist.")
    return result


def get_available_quests(character, quest_data_dict):
    """
    Get quests that character can currently accept

    Available = meets level req + prerequisite done + not completed + not active

    Returns: List of quest dictionaries
    """
    available_quests = []
    for quest_id in quest_data_dict:
        quest_info = quest_data_dict[quest_id]
        if character["level"] <  quest_info["required_level"]:
            continue
        if quest_info["prerequisite"] not in character["completed_quests"] and quest_info["prerequisite"] != "NONE":
            continue
        if quest_id in character["completed_quests"]:
            continue
        if quest_id in character["active_quests"]:
            continue
        available_quests.append(quest_info)
    return available_quests


# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    """
    Check if a specific quest has been completed

    Returns: True if completed, False otherwise
    """
    if quest_id in character["completed_quests"]:
        return True
    else:
        return False


def is_quest_active(character, quest_id):
    """
    Check if a specific quest is currently active

    Returns: True if active, False otherwise
    """
    if quest_id in character["active_quests"]:
        return True
    else:
        return False


def can_accept_quest(character, quest_id, quest_data_dict):
    """
    Check if character meets all requirements to accept quest

    Returns: True if can accept, False otherwise
    Does NOT raise exceptions - just returns boolean
    """
    quest_info = quest_data_dict[quest_id]
    if character["level"] < quest_info["required_level"]:
        return False
    elif quest_info["prerequisite"] not in character["completed_quests"] and quest_info["prerequisite"] != "NONE":
        return False
    elif quest_id in character["completed_quests"]:
        return False
    elif quest_id in character["active_quests"]:
        return False
    else:
        return True


def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    """
    Get the full chain of prerequisites for a quest

    Returns: List of quest IDs in order [earliest_prereq, ..., quest_id]
    Example: If Quest C requires Quest B, which requires Quest A:
             Returns ["quest_a", "quest_b", "quest_c"]

    Raises: QuestNotFoundError if quest doesn't exist
    """
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"{quest_id} does not exist.")

    prereq_chain = []
    current_id = quest_id

    while True:
        if current_id not in quest_data_dict:
            raise QuestNotFoundError(f"{current_id} does not exist.")
        quest_info = quest_data_dict[current_id]
        prereq = quest_info["prerequisite"]
        if prereq == "NONE":
            break
        if prereq not in quest_data_dict:
            raise QuestNotFoundError(f"Prerequisite {prereq} does not exist.")
        prereq_chain.append(prereq)
        current_id = prereq

    prereq_chain.reverse()
    prereq_chain.append(quest_id)
    return prereq_chain



# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    """
    Calculate what percentage of all quests have been completed

    Returns: Float between 0 and 100
    """

    total_quests = len(quest_data_dict)
    completed_quests = len(character['completed_quests'])
    percentage = (completed_quests / total_quests) * 100
    return percentage


def get_total_quest_rewards_earned(character, quest_data_dict):
    """
    Calculate total XP and gold earned from completed quests

    Returns: Dictionary with 'total_xp' and 'total_gold'
    """
    completed_quests = character["completed_quests"]
    total_xp = 0
    total_gold = 0
    for quest_id in completed_quests:
        quest_info = quest_data_dict[quest_id]
        total_xp += quest_info["reward_xp"]
        total_gold += quest_info["reward_gold"]
    return {"total_xp": total_xp, "total_gold": total_gold}

def get_quests_by_level(quest_data_dict, min_level, max_level):
    """
    Get all quests within a level range

    Returns: List of quest dictionaries
    """
    quest_range = []
    for quest_id in quest_data_dict:
        quest_info = quest_data_dict[quest_id]
        required_level = quest_info["required_level"]
        if min_level <= required_level <= max_level:
            quest_range.append(quest_info)
    return quest_range


# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    """
    Display formatted quest information

    Shows: Title, Description, Rewards, Requirements
    """
    print(f"\n=== {quest_data['title']} ===")
    print(f"Description: {quest_data['description']}")
    print(f"Rewards: {quest_data['reward_gold']} gold and {quest_data['reward_xp']} XP")
    print(f"Requirements: {quest_data['required_level']} XP")


def display_quest_list(quest_list):
    """
    Display a list of quests in summary format

    Shows: Title, Required Level, Rewards
    """
    if not quest_list:
        print("No quests available.")
        return None
    for quest in quest_list:
        print(f"- {quest['title']} (Level {quest['required_level']})")
        print(f"  Rewards: {quest['reward_gold']} gold, {quest['reward_xp']} XP")


def display_character_quest_progress(character, quest_data_dict):
    """
    Display character's quest statistics and progress

    Shows:
    - Active quests count
    - Completed quests count
    - Completion percentage
    - Total rewards earned
    """
    active_count = len(character["active_quests"])
    completed_count = len(character["completed_quests"])
    total_quests = len(quest_data_dict)
    completion_percentage = (completed_count / total_quests * 100) if total_quests > 0 else 0
    total_xp = 0
    total_gold = 0
    for quest_id in character["completed_quests"]:
        if quest_id in quest_data_dict:
            quest_info = quest_data_dict[quest_id]
            total_xp += quest_info["reward_xp"]
            total_gold += quest_info["reward_gold"]
    print("\n=== Quest Progress ===")
    print(f"Active Quests: {active_count}")
    print(f"Completed Quests: {completed_count}")
    print(f"Completion: {completion_percentage:.1f}%")
    print(f"Total Rewards Earned: {total_gold} gold, {total_xp} XP")

# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    """
    Validate that all quest prerequisites exist

    Checks that every prerequisite (that's not "NONE") refers to a real quest

    Returns: True if all valid
    Raises: QuestNotFoundError if invalid prerequisite found
    """
    for quest_id, quest_info in quest_data_dict.items():
        prereq = quest_info["prerequisite"]
        if prereq != "NONE" and prereq not in quest_data_dict:
            raise QuestNotFoundError(
                f"Quest '{quest_id}' has invalid prerequisite '{prereq}'."
            )
    return True


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")

    # Test data
    test_char = {
        'level': 1,
        'active_quests': [],
        'completed_quests': [],
        'experience': 0,
        'gold': 100
    }

    test_quests = {
        'first_quest': {
            'quest_id': 'first_quest',
            'title': 'First Steps',
            'description': 'Complete your first quest',
            'reward_xp': 50,
            'reward_gold': 25,
            'required_level': 1,
            'prerequisite': 'NONE'
        }
    }

    try:
        accept_quest(test_char, 'first_quest', test_quests)
        print("Quest accepted!")
    except QuestRequirementsNotMetError as e:
        print(f"Cannot accept: {e}")

