import ast


def str_to_list(string):
    if isinstance(string, str):
        return ast.literal_eval(string)
    return string
