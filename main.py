from constants import *
import copy
import random
import math

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
            # print(k + ": " + str(temp_metadata["character_stats"][k]) + " (+1)")
        else:
            # print(k + ": " + str(temp_metadata["character_stats"][k]))
            pass
    
    if character_metadata["has_rng_safety"] and num_stats_leveled < 2:
        # print("\nRerolling level " + str(character_metadata["current_level"] + 1))
        return simulate_level_up(copy.deepcopy(character_metadata), current_class_growths) 
    
    temp_metadata["current_level"] += 1
    return temp_metadata  

def level_up_stats_with_classes(character_metadata):
    if character_metadata["current_level"] >= 30:
        return simulate_level_up(character_metadata, character_metadata["master_class_growths"])  
    elif character_metadata["current_level"] >= 20:
        return simulate_level_up(character_metadata, character_metadata["advanced_class_growths"])  
    elif character_metadata["current_level"] >= 10:
        return simulate_level_up(character_metadata, character_metadata["intermediate_class_growths"])    
    elif character_metadata["current_level"] >= 5:
        return simulate_level_up(character_metadata, character_metadata["beginner_class_growths"])    
    else:
        return simulate_level_up(character_metadata, character_metadata["starting_class_growths"])    

def level_to_target(character_metadata, target_level):
    for _ in range(target_level - character_metadata["current_level"]):
        # print(character_metadata["name"] + ": Level " + str(character_metadata["current_level"] + 1))
        character_metadata = level_up_stats_with_classes(character_metadata) 
        # print("\n")
    return character_metadata

def simulate_one_hundred_iterations(blank_template, character_metadata, target_level):
    temp_level_metadata = copy.deepcopy(character_metadata)

    for _ in range (100):
        for k in character_metadata["character_stats"].keys():
            leveled_metadata = level_to_target(temp_level_metadata, target_level)
            blank_template[k] += leveled_metadata["character_stats"][k]

    # print(character_metadata["name"] + ": Level " + str(target_level) + " Average")

    for k in character_metadata["character_stats"].keys():
        blank_template[k] = math.ceil(blank_template[k] / 100)
        # print(k + ": " + str(blank_template[k]))
    
    return blank_template

def simulate_recruitment_stats(blank_template, character_metadata, target_level):
    ret_stats = {}
    ret_stats[1] = character_metadata["character_stats"]
    reset_blank_template = copy.deepcopy(blank_template)

    for level in range(2, target_level + 1):
        ret_stats[level] = simulate_one_hundred_iterations(reset_blank_template, character_metadata, level)
        reset_blank_template = copy.deepcopy(blank_template)
    
    print(ret_stats)
    return ret_stats


if __name__ == "__main__":
    character_metadata = IRIS_METADATA
    blank_template = BLANK_STARTING_STATS

    # level_to_target(character_metadata, 40)

    # simulate_one_hundred_iterations(blank_template, character_metadata, 40)

    simulate_recruitment_stats(blank_template, character_metadata, 40)

    
