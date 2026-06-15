import random
import numpy as np
# NOTE: sometimes this will return an expression where grouping symbols are only around a single number
# by default, involves the operations: + - / * ** (exponential) % (modulo) and grouping symbols: ()
def generate_no_latex(num_length_limit:int=8, num_magnitude_limit:int=500, grouping:list=["()"], operations:list=["+", "-", "/", "*", "**", "%"]): # chose a random default maximum, since you need some max
    equation = np.random.randint(0, num_magnitude_limit, size=num_length_limit).tolist() # tolist bc I need it to be mutable
    
    # insert operators between each number
    if operations: 
        for i in range(len(equation)-1, 0, -1): # going backwards to avoid index shifting issues
            equation.insert(i, operations[random.randint(0, len(operations)-1)])
    
    # checking for division by 0, and if so replacing all 0s with random numbers between 1 and num_magnitude_limit
    for i in range(len(equation)): 
        if equation[i-1] == "/" and str(equation[i]) == "0": 
            equation[i] = np.random.randint(0, num_magnitude_limit)
    
    # insert grouping symbols
    if grouping: 
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
            equation.insert(opening + len([index for index in inserted if index <= opening]), grouping_symbol[0])
            equation.insert(closing + len([index for index in inserted if index <= closing]) + 1, grouping_symbol[1])
            inserted.append(opening)
            inserted.append(closing)

    # convert each item to string so that it can all be turned into 1 big string
    equation = [str(num) for num in equation]
    # print(equation)

    final_string = ' '.join(equation)
    try: 
        final_string += f' = {eval(final_string)}'
    except ValueError: 
        if (operators is None or len(operators) = 0) and num_length_limit == 1: 
            print(f"You cannot create an equation with multiple numbers without an operator. Either add at least one operator or restrict the equation to one number only")
    return final_string

if __name__ == "__main__": # prevents from running if running a unittest
    print(generate_no_latex())