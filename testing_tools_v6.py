def get_function(act_name, func_name):
    text = "from hidden_tests_" + act_name + " import sol_" + func_name
    import importlib
    module = importlib.import_module("hidden_tests_"+act_name)
    return getattr(module, "sol_"+func_name)

def get_input(act_name, func_name):
    text = "from hidden_tests_" + act_name + " import input_" + func_name
    import importlib
    module = importlib.import_module("hidden_tests_"+act_name)
    return getattr(module, "input_"+func_name)()

def get_seed_value_pairs(**args):
    return {3: 7930248, 6: 604187583, 2: 1278024465, 9: 625745961, 17: 684947168, 8: 1394704656,
            10: 1017146387, 11: 2069729668, 19: 1006415970, 1: 1252004018, 14: 52374068, 12: 424273413, 
            16: 1117544251, 13: 1812609522, 20: 625179369, 5: 1899653659, 18: 1030404755, 7: 525181308,
            15: 803083387}


### For interactive functions: 
from contextlib import redirect_stdout
from io import StringIO
import builtins
import sys

class PatchedInput:
    def __init__(self, input_values):
        self.input_values = input_values
        self.input_copy = input_values.copy()
        self.original_input = builtins.input
        self.original_output = sys.stdout
        self.captured_lines = []
        self.captured_io = StringIO()
        self.input_lines = []
        self.output_lines = []
        self.failed_to_end = False
        self.ended_soon = False

    def __enter__(self):
        builtins.input = self.custom_input
        sys.stdout = self.captured_io

    def __exit__(self, exc_type, exc_value, traceback):
        if self.input_values:
            print("FUNCTION SHOULD HAVE CONTINUED, BUT INSTEAD ENDED.")
            self.ended_soon = True
        builtins.input = self.original_input
        sys.stdout = self.original_output
        self.clean_up()
    
    def custom_input(self, prompt):
        self.input_lines.append(prompt)
        self.captured_lines.append(prompt)
        print(prompt, end='\n')
        if self.input_values:
            return self.input_values.pop(0)
        else:
            print("THE FUNCTION SHOULD HAVE ENDED HERE, BUT INSTEAD CONTINUED.")
            self.failed_to_end = True
            self.__exit__

    def clean_up(self):
        self.captured_lines = self.captured_io.getvalue().splitlines()
        if self.failed_to_end:
            self.captured_lines = self.captured_lines[0:self.captured_lines.index("THE FUNCTION SHOULD HAVE ENDED BUT INSTEAD CONTINUED")+1]
        i = 0
        for input_line in self.input_lines:
            try:
                self.captured_lines[self.captured_lines.index(input_line)] = input_line + self.input_copy[i]
            except:
                pass
            i += 1
          

def simulate_interaction(input_values, function, args={}):
    """Function that automatically interacts with an interactive function in Python given a pre-selected
        list of input values. It returns a PatchedInput instance (pi) with pi.captured_lines showing the
        full interaction, pi.failed_to_end =True in case the function did not end with the provided arguments
        and pi.ended_soon=True in case the function ended without using all provided input arguments. 
    
        Parameters:
            input_values (list[str]): The list of pre-selected input values to test the function. 
            function (func): The interactive function which takes the input values. 
            args (dict{str:any}, Optional, default:None): arguments required by the function. 

        """
    patched_input = PatchedInput(input_values)
    with patched_input:
        try:
            function(**args)
        except:
            return patched_input
            pass
    return patched_input

def compare_interactive_randomized_function(act_name, func_name, global_vars, num_pairs=20):
    """Function that compares the output of an interactive function to the expected output. It prints out
    an error message if the outputs don't match exactly.
    
    Parameters:
        act_name (str): The activity name
        func_name (str): The name of the tested function

    Returns:
        None

    Notes:
    Assumes there is a function called sol_[func_name] in the appropriate module
    Assumes there is a function called input_[func_name] in the appropriate module which generates a tuple:
        (list of input values (for the input function), list of parameters (list of dictionaries))
    """
#     seed_value_pairs = get_seed_value_pairs(rand_func, num_pairs, global_vars)
#     seed_value_pairs = get_seed_value_pairs()
    sol_args, seed_values, test_inputs, args = get_input(act_name, func_name)
    sol_func = get_function(act_name, func_name)
    func = global_vars[func_name]
    for input_args, seed_value, input_values, arg in zip(sol_args, seed_values, test_inputs, args):
        ### Run the simulation to obtain expected values. 
        exp_pi = simulate_interaction(input_values.copy(), sol_func, args={**input_args})
        global_vars['seed'] = seed_value
        seed = seed_value
        real_pi = simulate_interaction(input_values.copy(), func, arg)
        message = ""
        if real_pi.failed_to_end:
            message = "Your function continued after it should have ended. \n"
        if real_pi.ended_soon:
            message = "Your function ended when it shouldn't have. \n"
        exp_interaction = "\n".join(exp_pi.captured_lines)
        real_interaction = "\n".join(real_pi.captured_lines)
        assert exp_interaction == real_interaction, message + "Your function returned: \n" + real_interaction + "\n\nExpected:\n" + exp_interaction
    return
