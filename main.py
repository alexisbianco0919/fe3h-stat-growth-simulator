from constants import *
import copy
import random

def did_stat_level(base_growth, class_growth):
    growth_percentage = base_growth + class_growth
    rand_num = random.randint(0, 100)
    if rand_num <= growth_percentage:
        return True
    else:
        return False
    
def simulate_level_up(character_metadata, current_class_growths):
    temp_metadata = copy.deepcopy(character_metadata)
    num_stats_leveled = 0

    for k in character_metadata["character_stats"].keys():
        if did_stat_level(character_metadata["base_growths"][k], current_class_growths[k]):
            temp_metadata["character_stats"][k] += 1
            num_stats_leveled += 1
            print(k + ": " + str(temp_metadata["character_stats"][k]) + " (+1)")
        else:
            print(k + ": " + str(temp_metadata["character_stats"][k]))
    
    if character_metadata["has_rng_safety"] and num_stats_leveled < 2:
        print("\nRerolling level " + str(character_metadata["current_level"] + 1))
        return simulate_level_up(copy.deepcopy(character_metadata), current_class_growths)  # Ensure reroll starts fresh
    
    temp_metadata["current_level"] += 1
    return temp_metadata  # Return the updated character

def level_up_stats_with_classes(character_metadata):
    if character_metadata["current_level"] >= 10:
        return simulate_level_up(character_metadata, character_metadata["intermediate_class_growths"])    
    elif character_metadata["current_level"] >= 5:
        return simulate_level_up(character_metadata, character_metadata["beginner_class_growths"])    
    else:
        return simulate_level_up(character_metadata, character_metadata["starting_class_growths"])    

def level_to_target(character_metadata, target_level):
    for _ in range(target_level - character_metadata["current_level"]):
        print(character_metadata["name"] + ": Level " + str(character_metadata["current_level"] + 1))
        character_metadata = level_up_stats_with_classes(character_metadata)  # Update character data
        print("\n")

def one_hundred_iterations(character_metadata):
    pass

if __name__ == "__main__":
    character_metadata = IRIS_METADATA
    level_to_target(character_metadata, 40)
    
