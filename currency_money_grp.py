# -*- coding:utf-8 -*-
from currency_money_enum import *


class E_MONEY_GRP(Enum):
    none = 0
    eur_usd = 1
    usd_jpy = 2
    gold = 3


def GetMoneyGrp(grp_str: str) -> E_MONEY_GRP:
    if "eurusd" == grp_str :
        return E_MONEY_GRP.eur_usd
    elif "jpyusd" == grp_str:
        return E_MONEY_GRP.usd_jpy
    elif "gold" == grp_str:
        return E_MONEY_GRP.gold


def GetSrcMoney(grp: E_MONEY_GRP) -> E_MONEY_TYPE:
    if grp == E_MONEY_GRP.eur_usd:
        return E_MONEY_TYPE.usd
    elif grp == E_MONEY_GRP.usd_jpy:
        return E_MONEY_TYPE.jpy
    elif grp == E_MONEY_GRP.gold:
        return E_MONEY_TYPE.usd


def GetTargetMoney(grp: E_MONEY_GRP) -> E_MONEY_TYPE:
    if grp == E_MONEY_GRP.eur_usd:
        return E_MONEY_TYPE.eur
    elif grp == E_MONEY_GRP.usd_jpy:
        return E_MONEY_TYPE.usd
    elif grp == E_MONEY_GRP.gold:
        return E_MONEY_TYPE.gold


def GetPointFactor(grp: E_MONEY_GRP)-> float:
    if grp == E_MONEY_GRP.eur_usd:
        return 0.00001
    elif grp == E_MONEY_GRP.usd_jpy:
        return 0.001
    elif grp == E_MONEY_GRP.gold:
        return 0.1
