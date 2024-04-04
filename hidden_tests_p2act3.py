def sol_guessing_game(num):
    while True:
        x = input("Guess the number: ")
        try:
            x = int(x)
        except:
            print("You must type an integer between 1 and 20! Please try again.")
            continue
        if x<1 or x>20:
            print("You must type an integer between 1 and 20! Please try again.")
            continue
        if x == num:
            print("You got it!")
            break
        elif x > num:
            print("Your guess is too high.")
        else:
            print("Your guess is too low.")
    return

def simulate_binary_search(num, min_num=0, max_num=20):
    guesses = []
    next_guess = 10
    lower_bound = min_num
    upper_bound = max_num
    while True:
        guesses.append(next_guess)
        if next_guess == num:
            break
        elif next_guess > num:
            upper_bound = next_guess
        else:
            lower_bound = next_guess
        if upper_bound - lower_bound == 1 and next_guess == lower_bound:
            next_guess = upper_bound
        else:
            next_guess = int((upper_bound+lower_bound)/2)
    return [str(i) for i in guesses]


def input_guessing_game(num_tests = 25):
    input_values = []
    seeds = []
    sol_args = []
    seed_value_pairs = {3: 7930248, 4: 139692022, 6: 604187583, 2: 1278024465, 9: 625745961, 17: 684947168, 8:1394704656,
                        10: 1017146387, 11: 2069729668, 19: 1006415970, 1: 1252004018, 14: 52374068, 12:424273413,
                        16: 1117544251, 13: 1812609522, 20: 625179369, 5: 1899653659, 18: 1030404755, 7:525181308,
                        15: 803083387}
    for num, seed_value in seed_value_pairs.items():
        sol_args.append({"num":num})
        seeds.append(seed_value)
        input_values.append([str(i) for i in simulate_binary_search(num)])
    args = [{} for i in range(20)]
    ### add data validation tests:
    from random import choice, choices
    test_results = choices([1, 5, 10, 15, 20], k =5)
#     for item in choices([1, 5, 10, 15, 20], k=5):
#         sol_args.append({"num":item})
    seeds += [seed_value_pairs[i] for i in test_results]
    bad_options = ["one", "-45", "5eh3", "stop"]
    for res in test_results:
        sol_args.append({"num":res})
        input_values.append(["3", choice(bad_options), str(res)])
        args.append({})
    return sol_args, seeds, input_values, args

def sol_cube_game(num_cubes, human_turn):
#     num_cubes = generate_random_number(min_num=10, max_num=15)
    print(f"The game starts with {num_cubes} cubes.")
#     human_turn = generate_random_number(min_num=1, max_num=10) > 5
    if human_turn:
        print("You start!")
    else:
        print("I start!")
    ### BEGIN SOLUTION
    while True:
        if human_turn: 
            print(f"There are {num_cubes} cubes left.")
            while True: 
                player_cubes = input("How many cubes do you want to take? ")
                if player_cubes != "1" and player_cubes != "2":
                    print("You must take either 1 or 2 cubes. Please try again.")
                    continue
                break
            num_cubes -= int(player_cubes)
            human_turn = False
        else:
            human_turn = True
            if num_cubes%3 == 2:
                print("I take 2 cubes.")
                num_cubes -= 2
            else:
                print("I take 1 cube.")
                num_cubes -= 1
        if num_cubes <= 0:
            break
    if human_turn:
        print("You lose!")
    else:
        print("You win!")
    return


def input_cube_game(num_tests=15):
    ### args is a list of emppty dictionaries
    ### sol args contains {"num_cubes" and "human_turn" as keys. 
    ### seeds are the seed values. 
    ### input values needs to be a list of lists of strings to type in. 
    seed_value_pairs = {1161384037: (12, False), 884250324: (14, True), 1683279519: (10, False), 1623396223: (14, False),
                        973648171: (11, True), 627050995: (12, True), 1398912615: (15, True), 392286598: (10, True),
                        900069285: (13, False), 1999589752: (13, True)}
    sol_args = []
    seeds = []
    input_values = []
    args = [{}]
    options = ["1", "2"]
    bad_guess = ["one", "dsfa", "3"]
    from random import choice
    for seed, combo in seed_value_pairs.items():
        if combo[0]%3 == 0 and combo[1]:
            ### Machine wins. Choose randomly until they run out. 
            for i in range(3):
                sol_args.append({"num_cubes":combo[0], "human_turn":combo[1]})
                seeds.append(seed)
                args.append({})
                input_values.append([choice(options) for i in range(int(combo[0]/3))])
            ### add a bad guess: 
            sol_args.append({"num_cubes":combo[0], "human_turn":combo[1]})
            seeds.append(seed)
            args.append({})
            l = [choice(options) for i in range(int(combo[0]/3))]
            ind = choice(range(len(l)))
            l = l[:ind] + [choice(bad_guess)] + l[ind:]
            input_values.append(l) 
        elif combo[0]%3==0:
            ### Human wins. Test that the machine takes one cube each time. 
            for i in range(3):
                sol_args.append({"num_cubes":combo[0], "human_turn":combo[1]})
                seeds.append(seed)
                args.append({})
                input_values.append(["2"]*4)
            ### add a bad guess: 
            sol_args.append({"num_cubes":combo[0], "human_turn":combo[1]})
            seeds.append(seed)
            args.append({})
            l = ["2"]*4
            ind = choice(range(len(l)))
            l = l[:ind] + [choice(bad_guess)] + l[ind:]
            input_values.append(l) 
            ### choose randomly to test that the machine is playing perfectly
            for i in range(3):
                sol_args.append({"num_cubes":combo[0], "human_turn":combo[1]})
                seeds.append(seed)
                args.append({})
                input_values.append([choice(options) for i in range(int(combo[0]/3)+2)])
            sol_args.append({"num_cubes":combo[0], "human_turn":combo[1]})
            seeds.append(seed)
            args.append({})
            l = [choice(options) for i in range(int(combo[0]/3)+2)]
            ind = choice(range(len(l)))
            l = l[:ind] + [choice(bad_guess)] + l[ind:]
            input_values.append(l) 
        elif combo[0]%3==1 and combo[1]:
            ### human takes 1 and 2 from then on to win. 
            for i in range(3):
                sol_args.append({"num_cubes":combo[0], "human_turn":combo[1]})
                seeds.append(seed)
                args.append({})
                values = ["1"] + ["2"]*int((combo[0]-1)/3)
                input_values.append(values)
            sol_args.append({"num_cubes":combo[0], "human_turn":combo[1]})
            seeds.append(seed)
            args.append({})
            l = ["1"] + ["2"]*int((combo[0]-1)/3)
            ind = choice(range(len(l)))
            l = l[:ind] + [choice(bad_guess)] + l[ind:]
            input_values.append(l) 
            for i in range(3):
                sol_args.append({"num_cubes":combo[0], "human_turn":combo[1]})
                seeds.append(seed)
                args.append({})
                input_values.append([choice(options) for i in range(int(combo[0]/3+2))])
            sol_args.append({"num_cubes":combo[0], "human_turn":combo[1]})
            seeds.append(seed)
            args.append({})
            l = [choice(options) for i in range(int(combo[0]/3+2))]
            ind = choice(range(len(l)))
            l = l[:ind] + [choice(bad_guess)] + l[ind:]
            input_values.append(l) 
        elif combo[0]%3==1:
            ### Machine wins. Choose randomly. 
            for i in range(3):
                sol_args.append({"num_cubes":combo[0], "human_turn":combo[1]})
                seeds.append(seed)
                args.append({})
                input_values.append([choice(options) for i in range(int(combo[0]/3+2))])
            sol_args.append({"num_cubes":combo[0], "human_turn":combo[1]})
            seeds.append(seed)
            args.append({})
            l = [choice(options) for i in range(int(combo[0]/3+2))]
            ind = choice(range(len(l)))
            l = l[:ind] + [choice(bad_guess)] + l[ind:]
            input_values.append(l) 
        elif combo[0]%3==2 and combo[1]:
            ### human wins if they take 2 at first. 
            for i in range(3):
                sol_args.append({"num_cubes":combo[0], "human_turn":combo[1]})
                seeds.append(seed)
                args.append({})
                input_values.append(["2"]*int(combo[0]/3+2))
            sol_args.append({"num_cubes":combo[0], "human_turn":combo[1]})
            seeds.append(seed)
            args.append({})
            l = ["2"]*int(combo[0]/3+2)
            ind = choice(range(len(l)))
            l = l[:ind] + [choice(bad_guess)] + l[ind:]
            input_values.append(l) 
            for i in range(3):
                sol_args.append({"num_cubes":combo[0], "human_turn":combo[1]})
                seeds.append(seed)
                args.append({})
                input_values.append([choice(options) for i in range(int(combo[0]/3+2))])
            sol_args.append({"num_cubes":combo[0], "human_turn":combo[1]})
            seeds.append(seed)
            args.append({})
            l = [choice(options) for i in range(int(combo[0]/3+2))]
            ind = choice(range(len(l)))
            l = l[:ind] + [choice(bad_guess)] + l[ind:]
            input_values.append(l) 
        else:
            ### machine wins. Choose randomly.
            for i in range(3):
                sol_args.append({"num_cubes":combo[0], "human_turn":combo[1]})
                seeds.append(seed)
                args.append({})
                input_values.append([choice(options) for i in range(int(combo[0]/3+2))])
            sol_args.append({"num_cubes":combo[0], "human_turn":combo[1]})
            seeds.append(seed)
            args.append({})
            l = [choice(options) for i in range(int(combo[0]/3+2))]
            ind = choice(range(len(l)))
            l = l[:ind] + [choice(bad_guess)] + l[ind:]
            input_values.append(l) 
            
    return sol_args, seeds, input_values, args
