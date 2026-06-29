import random
import numpy as np

def calc_full_equation(num_length_limit:int=8, num_magnitude_limit:int=500, grouping:list=["()"], operations:list=["+", "-", "/", "*", "**", "%"], num_reruns:int=10): 
    if num_length_limit == 0: 
        return "" # need to return here, so eval isn't called
    equation = get_equation(num_length_limit, num_magnitude_limit, grouping, operations)
    # convert each item to string so that it can all be turned into 1 big string
    equation_ints = [str(int(num)) if isinstance(num, float) else num for num in equation]
    equation_floats = [str(num) for num in equation]
    all_ints = ' '.join(equation_ints)
    all_floats = ' '.join(equation_floats)

    try: 
        all_ints += f' = {eval(all_floats)}'
    except SyntaxError: 
        if (operations is None or len(operations) == 0) and num_length_limit > 1: 
            raise SyntaxError(f"You cannot create an equation with multiple numbers without an operator. Either add at least one operator or restrict the equation to one number only")
    except (OverflowError, ZeroDivisionError, TypeError) as error: # sometimes I'm ending up with a complex number, so catching type error. https://docs.python.org/3/tutorial/errors.html
        found_no_error_equation = False
        condition = False # specific to the error type
        i = 0
        while not condition and not found_no_error_equation: # a lot of duplication here
            equation = get_equation(num_length_limit, num_magnitude_limit, grouping, operations)
            equation_ints = [str(int(num)) if isinstance(num, float) else num for num in equation]
            equation_floats = [str(num) for num in equation]
            all_ints = ' '.join(equation_ints)
            all_floats = ' '.join(equation_floats)
            
            try: 
                all_ints += f' = {eval(all_floats)}'
                found_no_error_equation = True
                break # if valid final string was found
            except (OverflowError, ZeroDivisionError, TypeError): 
                i += 1
                if isinstance(error, OverflowError): condition = i >= num_reruns # should happen after i increment
                continue
        if not found_no_error_equation: raise OverflowError(f"After attempting {num_reruns} reruns, we were unable to generate an equation which didn't overflow python's float limit. Please either decrease the num length and/or num magnitude limit or remove ** from the operations list (if you want to keep the same num length limit and/or num magnitude limit the same). You can also increase your number of retries, but doing so will increase computation time and, at a certain equation size, will no longer work")
    return all_ints


# NOTE: sometimes this will return an expression where grouping symbols are only around a single number
# by default, involves the operations: + - / * ** (exponential) % (modulo) and grouping symbols: ()
# num length limit refers to the maximum number of numbers in the equation
def get_equation(num_length_limit:int=8, num_magnitude_limit:int=500, grouping:list=["()"], operations:list=["+", "-", "/", "*", "**", "%"], num_reruns:int=5): # chose a random default maximum, since you need some max
    equation = np.random.randint(0, num_magnitude_limit, size=num_length_limit).tolist() # tolist bc I need it to be mutable
    # convert items to float, so that overflow error thrown rather than computer dying
    equation = [float(i) for i in equation]
    # insert operators between each number
    if operations: 
        for i in range(len(equation)-1, 0, -1): # going backwards to avoid index shifting issues
            equation.insert(i, operations[random.randint(0, len(operations)-1)])
    
    # checking for division or mod by 0, and if so replacing all 0s with random numbers between 1 and num_magnitude_limit
    for i in range(1, len(equation)):
        if (equation[i-1] == "%" or equation[i-1] == "/") and equation[i] == 0.0: 
            equation[i] = float(np.random.randint(1, num_magnitude_limit))
    
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
            if second_index - first_index < 2: # don't want parantheses just around a number without an operation
                continue
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
    
    return equation
