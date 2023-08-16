from itertools import product
import re



# PARSE INPUT

def parse_switch(switch_str):
    if switch_str == 'None' or switch_str == '' or switch_str == ' ' or switch_str == '\n':
        return None

    # Parse operator, value with regex
    matches = re.search(r'(\+|-|\*|¢|/)', switch_str)

    if matches is None:        
        raise Exception(f'Invalid operator: {switch_str}')
    
    operator = matches.group(0)
    matches = re.search(r'(\d+)', switch_str)

    if matches is None:
        raise Exception(f'Invalid value: {switch_str}')
    
    value = int(matches.group(0)) 
    return {
        'operator': operator,
        'value': value
    }

def parse_input(input_str):
    lines = input_str.split('\n')
    initial_voltages = [int(lines[0]), int(lines[0])]
    expected_voltages = [int(v) for v in lines[1:3]]

    switches = []
    # Loop in 2 steps
    for i in range(3, len(lines), 2):        
        left_swtich = parse_switch(lines[i])
        right_switch = parse_switch(lines[i+1])

        switches.append([left_swtich, right_switch])
            

    return initial_voltages, expected_voltages, switches



switches = [
    [
        {
            'operator': '/',
            'value': 2
        },
        {
            'operator': '+',
            'value': 100
        }
    ],
    [
        {
            'operator': '+',
            'value': 100
        },
        {
            'operator': '-',
            'value': 40
        }
    ],
    [
        None,
        {
            'operator': '/',
            'value': 2
        }
    ],
    [
        None,
        {
            'operator': '+',
            'value': 10
        }
    ],
    [
        {
            'operator': '+',
            'value': 60
        },
        None
    ],
    [
        {
            'operator': '*',
            'value': 2
        },
        {
            'operator': '/',
            'value': 2
        }
    ],
    [
        {
            'operator': '+',
            'value': 60
        },
        {
            'operator': '*',
            'value': 2
        }
    ],
    [
        None,
        {
            'operator': '*',
            'value': 2
        }
    ],
]



def parse_operation(switch):
    if switch is None:
        return lambda x: x
    
    operator = switch['operator']
    value = switch['value']

    if operator in ['+', '¢']:
        return lambda x: x + value
    elif operator == '-':
        return lambda x: x - value
    elif operator == '*':
        return lambda x: x * value
    elif operator == '/':
        return lambda x: x / value
    else:
        raise Exception('Invalid operator')


def try_combination(voltages, combination, switches):
    for i, switch in enumerate(switches):
        if not combination[i]:
            continue
        
        for i, value in enumerate(voltages):
            voltages[i] = switch[i](value)

    return voltages
            

        

def solve_lock(initial_voltages, expected_voltages, switches):

    switches = [
        [
            parse_operation(parse_switch(s)) for s in row
        ]
        for row in switches
    ]

    combinations = product([False, True], repeat=len(switches))

    for combination in combinations:
        voltages = initial_voltages.copy()
        voltages = try_combination(voltages, combination, switches)

        if voltages == expected_voltages:
            return combination

    return None   
    


    


# solve_lock(initial_voltages, expected_voltages, switches)

parsed_switches = [
    [
        parse_operation(s) for s in row
    ]
    for row in switches
]

