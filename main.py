import random
import numpy as np
# by default, involves the operations: + - / * ** (exponential) % (modulo) and grouping symbols: ()
def generate_no_latex(operations:list=["+", "-", "/", "*", "**", "%"], grouping:list=["()"], num_length_limit:int=8, num_magnitude_limit:int=500): # chose a random default maximum, since you need some max
    equation = np.random.randint(0, num_magnitude_limit, size=num_length_limit).tolist() # tolist bc I need it to be mutable
    # [int(num) for num in str(random.randint(0, 10**length_limit-1))] # ex. if the length of all of the numbers combined can be 10, the largest number is 10 1s times 9
    
    # insert operators between each number
    for i in range(len(equation)-1, 0, -1): # going backwards to avoid index shifting issues
        equation.insert(i, operations[random.randint(0, len(operations)-1)])
    
    # insert grouping symbols; note that I use start and end here but they may be reversed later on
    number_indices = [i for i in range(len(equation)) if i % 2 == 0] # all even indices
    start_grouping_potential_indices = np.array([num_index + 1 for num_index in number_indices if num_index > -1 and num_index < len(equation)]) # should start after an operator; + (
    end_grouping_potential_indices = np.array([num_index - 1 for num_index in number_indices if num_index > -1 and num_index < len(equation)]) # should end before an operator; ) +

    max_pairs = min((len(start_grouping_potential_indices), len(end_grouping_potential_indices)))
    num_grouping_pairs = np.random.randint(0, max_pairs) if max_pairs > 0 else 0

    pairs = []
    for i in range(num_grouping_pairs): 
        pair = [random.choice(number_indices), random.choice(number_indices)]
        first_index, second_index = sorted(pair)
        if first_index == second_index: 
            continue
        opening = first_index
        closing = second_index+1
        # no full duplication
        if (closing, opening) in pairs: 
            continue
        pairs.append((closing, opening))

    inserted = [] # keeps track of how much offset I need to add to each
    for closing, opening in sorted(pairs): # reverse so that indices don't shift each other
        grouping_symbol = random.choice(grouping)
        print(f"opening: {opening}, closing: {closing}, equation length: {len(equation)}")
        equation.insert(opening + len([index for index in inserted if index <= opening]), grouping_symbol[0])
        equation.insert(closing + len([index for index in inserted if index <= closing]) + 1, grouping_symbol[1])
        inserted.append(opening)
        inserted.append(closing)

    # convert each item to string so that it can all be turned into 1 big string
    equation = [str(num) for num in equation]
    print(equation)

    final_string = ' '.join(equation)
    final_string += f' = {eval(final_string)}'
    return final_string

print(generate_no_latex())