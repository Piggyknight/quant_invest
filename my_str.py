# -*- coding:utf-8 -*-


def IsBlank(input_str: str) -> bool:
    return not (input_str and input_str.strip())


def IsNotBlank(input_str: str) -> bool:
    return bool(input_str and input_str.strip())
