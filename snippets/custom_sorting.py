"""
1. sort a list of alphanumeric string like:
    ["2D", "1D", "2W", "3Y", "1W", "3M", "1Y", "6M"]
    where D, W, M and Y represent, respectively, days, weeks, months, years.

    first by letter (in implied chronological order) and then numbers, e.g.

    desired result = ["1D", "2D", "1W, "2W", "3M", "6M", "1Y", "3Y"]

2. Get the sorted indices of the list in 1. above to sort another related list (e.g. associated zero rates)
"""

import random
import re

desired_result = ["1D", "2D", "1W", "2W", "3M", "6M", "18M", "1Y", "3Y"]
print(f"original list:\n{desired_result}")

# permutate the list for testing
random.shuffle(desired_result)
print(f"reshuffled list:\n{desired_result}")

print()

# 1. get the ordered list back
print("Point 1.: order the list")
def custom_sort(x):
    num, letter = re.findall(r"[^\W\d_]+|\d+", x)
    return ["DWMY".index(c) for c in letter], int(num)


ordered_list = sorted(desired_result, key=lambda x: custom_sort(x))
print(f"ordered_list:\n{ordered_list}")

"""
string_to_replace = ["1S", "2S", "3S", "1W", "2W", "3M", "6M", "1Y", "3Y"]
print(f"string_to_replace: {string_to_replace}")
string_replaced = [w.replace("S", "D") for w in string_to_replace]
print(f"string_replaced: {string_replaced}")
"""
print()

# 2. get sorted indices
print("Point 2.: order the indices")
ordered_list_index = sorted(range(len(desired_result)), key=lambda x: custom_sort(desired_result[x]))
print(f"ordered_list_index: {ordered_list_index}")

#   ################## ##################
print(f"the desired_result is still shuffled: {desired_result}")
# ordered_list_from_indices = np.array(desired_result)[ordered_list_index]

ordered_list_from_indices_using_map = list(map(desired_result.__getitem__, ordered_list_index))
print(f"the ordered_list_from_indices using map: {ordered_list_from_indices_using_map}")

#   ################## easier (same speed or sloghtly faster)
print()
print(f"the desired_result is still shuffled: {desired_result}")

ordered_list_from_indices = [desired_result[i] for i in ordered_list_index]
print(f"the ordered_list_from_indices: {ordered_list_from_indices}")
