from typing import List, Tuple, Set, Dict, Union, Optional

def print_person_info(name:str, height: Optional[Union[int , float]] = None):
    print(f"name:{name}, height:{height}")

print_person_info("xiaoming")

# def test_type(list_arg:List[str], tuple_arg: Tuple[int, bool], set_arg: Set[int]):
#     print(type(list_arg), list_arg)
#     print(type(tuple_arg), tuple_arg)
#     print(type(set_arg), set_arg)

# test_type(["xiaoming"], tuple_arg=(44, False), set_arg=set([1,1,2,2]))

# def test_type_dict(dict_arg: Dict[str, int]):
#     print(type(dict_arg), dict_arg)

# test_type_dict({"age": 18})
