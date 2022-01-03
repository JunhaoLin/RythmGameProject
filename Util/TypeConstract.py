# This page is copied directly from 
# https://github.ccs.neu.edu/CS4500-F21/shoshone/blob/master/Trains/Other/func_utils.py
# which is co-authored by me and others

"""A collection of utility functions for modifying the behavior of functions and methods."""

from functools import lru_cache
from typing import Any, Callable, Iterable, Set, TypeVar

TypeValidator = Callable[[Any], bool]
"""Represents a function that validates a given type is of a certain type by returning a boolean."""


def memoize(func: Callable):
    """Decorate a function with this annotation to memoize (cache) arguments without bound.

    Note: all arguments in a decorated function must be hashable."""
    @lru_cache(maxsize=None)
    def func_wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return func_wrapper


T = TypeVar("T")


def flatten_set(double_set: Iterable[Set[T]]) -> Set[T]:
    """Flattten the given iterable of sets of items to one set of items."""
    return {item for set in double_set for item in set}


def type_contract(value: Any, type_validator: TypeValidator) -> None:
    """Determines whether a given value conforms to a type given a type validator. If the check
    does not pass, this function will throw a TypeError.

    In practice, this function simply asserts that calling the given value on the function returns True.

    Use built-in module type validators for working with built-in types. This improves readability
    and confidence in correctness.

    Examples: ::

        type_contract(4, lambda x: isinstance(x, int)) # -> type_validator returns true, type check passes
        type_contract("hello", lambda x: isinstance(x, int)) # -> throws TypeError
        type_contract(4, bool) # -> BAD, improper use
    """
    if not is_function(type_validator):
        raise TypeError(
            f"type_contract received an invalid type validator. It cannot be called.")

    is_valid = type_validator(value)
    if not is_bool(is_valid):
        raise TypeError(
            f"type_contract received an invalid type validator. It does not return a boolean.")

    if not is_valid:
        raise TypeError(
            f"Value {value} does not pass {type_validator.__name__} type validation.")


def is_int(maybe_int: Any) -> bool:
    """A type validator for integers.

    Note: this will reject boolean literals as `ints`.

    Examples: ::

        type_contract(4, is_int) # -> passes
        type_contract(True, is_int) # -> errors"""
    # Python booleans inherit from integers for legacy reasons
    # Thus we need to seperately check that the given value is not a boolean literal.
    return isinstance(maybe_int, int) and type(maybe_int) is not bool


def is_float(maybe_float: Any) -> bool:
    """A type validator for floats.

    Examples: ::

        type_contract(4.5, is_float) # -> passes"""
    return isinstance(maybe_float, float)


def is_str(maybe_str: Any) -> bool:
    """A type validator for strings.

    Examples: ::

        type_contract("hello", is_str) # -> passes"""
    return isinstance(maybe_str, str)


def is_bool(maybe_bool: Any) -> bool:
    """A type validator for booleans.

    Examples: ::

        type_contract(True, is_bool) # -> passes"""
    return isinstance(maybe_bool, bool)


def is_none(maybe_none: Any) -> bool:
    """A type validator for None.

    Examples: ::

        type_contract(None, is_none) # -> passes"""
    return maybe_none is None


def is_any(_: Any) -> bool:
    """A type validator for any value.

    AVOID USING UNLESS COMPLETELY NECESSARY.

    Examples: ::

        type_contract("hello", is_any) # -> passes
        type_contract(5, is_any) # -> passes"""
    return True


def is_function(maybe_function: Any) -> bool:
    """A type validator for functions.

    Note: a value is a function if it is callable.
    Therefore, objects implementing `__call__()` are functions.

    Examples: ::

        type_contract(lambda x: x, is_function) # -> passes"""
    return callable(maybe_function)


def is_instance_of(t: type) -> TypeValidator:
    """Returns a type validator for a checking if a value is an instance of the given type.

    Examples: ::

        type_contract(Posn(10,5), is_instance_of(Posn)) # -> passes"""
    type_contract(t, lambda x: isinstance(x, type))

    def instance_checker(maybe_instance: Any) -> bool:
        """A type validator for an instance of a class."""
        return isinstance(maybe_instance, t)
    return instance_checker


def is_one_of(*type_validators: TypeValidator) -> TypeValidator:
    """Returns a type validator for a checking if a value is one the given type validators.

    Examples: ::

        type_contract("hello", is_one_of(is_str, is_int)) # -> passes
        type_contract(10, is_one_of(is_str, is_int)) # -> passes
        type_contract(True, is_one_of(is_str, is_int)) # -> errors"""
    type_contract(type_validators, lambda maybe_validators: all(
        is_function(maybe_validator) for maybe_validator in maybe_validators))

    def one_of_checker(maybe_value: Any) -> bool:
        return any(type_validator(maybe_value) for type_validator in type_validators)
    return one_of_checker


def is_optional(type_validator: TypeValidator) -> TypeValidator:
    """Returns a type validator for an optional type. The given argument is a type validator
    for the underlying type.

    Examples: ::

        type_contract("hello", is_optional(is_str)) # -> passes
        type_contract(None, is_optional(is_str)) # -> passes
        type_contract(-10, is_optional(is_str)) # -> errors"""
    type_contract(type_validator, is_function)

    def optional_checker(maybe_optional: Any) -> bool:
        return maybe_optional is None or type_validator(maybe_optional)
    return optional_checker


def is_list_of(item_type_validator: TypeValidator) -> TypeValidator:
    """Returns a type validator for a list. The given argument is a type validator for elements of the list.

    Examples: ::

        type_contract(["hello", "dog"], is_list_of(is_str)) # -> passes
        type_contract([], is_list_of(is_int)) # -> passes
        type_contract(["hi", 123], is_list_of(is_str)) # -> errors"""
    type_contract(item_type_validator, is_function)

    def list_checker(maybe_list: Any) -> bool:
        return isinstance(maybe_list, list) and all(item_type_validator(item) for item in maybe_list)
    return list_checker


def is_set_of(item_type_validator: TypeValidator) -> TypeValidator:
    """Returns a type validator for a set. The given argument is a type validator for elements of the set.

    Examples: ::

        type_contract({1,2,3}, is_set_of(is_int)) # -> passes
        type_contract(set(), is_set_of(is_str)) # -> passes
        type_contract({1,2, "hello"}, is_set_of(is_int)) # -> errors"""
    type_contract(item_type_validator, is_function)

    def set_checker(maybe_set: Any) -> bool:
        return isinstance(maybe_set, set) and all(item_type_validator(item) for item in maybe_set)
    return set_checker


def is_tuple_of(*type_validators: TypeValidator) -> TypeValidator:
    """Returns a type validator for a tuple. The given arguments are type validators,
    in order, for the elements of the tuple. If a tuple is supposed to be empty, pass no arguments.

    Examples: ::

        type_contract((1,2,3), is_tuple_of(is_int, is_int, is_int)) # -> passes
        type_contract(tuple(), is_tuple_of()) # -> passes
        type_contract(("hello", "world"), is_tuple_of(is_str)) # -> errors
        type_contract(("hello", "world"), is_tuple_of(is_str, is_str, is_str)) # -> errors"""
    type_contract(type_validators, lambda maybe_validators: all(
        is_function(maybe_validator) for maybe_validator in maybe_validators))

    def tuple_checker(maybe_tuple: Any) -> bool:
        if not isinstance(maybe_tuple, tuple):
            return False
        # enforce that tuple lengths are the same
        if len(maybe_tuple) != len(type_validators):
            return False
        return all(item_validator(item) for item_validator, item in zip(type_validators, maybe_tuple))
    return tuple_checker


def is_iterable_of(item_type_validator: TypeValidator) -> TypeValidator:
    """Returns a type validator for an iterable. The given argument is a type validator for elements of the iterable.

    Examples: ::

        type_contract(["hello", "dog"], is_iterable_of(is_str)) # -> passes
        type_contract(set(), is_iterable_of(is_int)) # -> passes
        type_contract(["hi", 123], is_iterable_of(is_str)) # -> errors"""
    type_contract(item_type_validator, is_function)

    def iterable_checker(maybe_iterable: Any) -> bool:
        return isinstance(maybe_iterable, Iterable) and all(item_type_validator(item) for item in maybe_iterable)
    return iterable_checker


def is_dict_of(key_type_validator: TypeValidator, value_type_validator: TypeValidator) -> TypeValidator:
    """Returns a type validator for a dictionary. The first argument is a type
    validator for the keys of the dictionary, and the second argument is a type
    validator for the values of the dictionary.

    Examples: ::

        type_contract({1: "hello", 2: "world"}, is_dict_of(is_int, is_str)) # -> passes
        type_contract({"hello": None, "world": None}, is_dict_of(is_str, is_none)) # -> passes
        type_contract({"hello": None, "world": 5}, is_dict_of(is_str, is_int)) # -> errors"""
    type_contract(key_type_validator, is_function)
    type_contract(value_type_validator, is_function)

    def dict_checker(maybe_dict: Any) -> bool:
        return isinstance(maybe_dict, dict) and all(key_type_validator(key) and value_type_validator(value) for key, value in maybe_dict.items())
    return dict_checker
