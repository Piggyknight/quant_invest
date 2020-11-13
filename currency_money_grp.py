# -*- coding:utf-8 -*-

from enum import Enum

class E_MONEY_GRP(Enum):
    eur_usd = "eurusd"
    usd_jpy = "jpyusd"
    gold = "gold"


_money_grp = { \
              E_MONEY_GRP.eur_usd: E_MONEY_GRP.eur_usd, \
              E_MONEY_GRP.gold: E_MONEY_GRP.gold}

_src_money = {E_MONEY_GRP.eur_usd: E_MONEY_TYPE.usd, \
              E_MONEY_GRP.gold: E_MONEY_TYPE.usd}

_target_money ={ E_MONEY_GRP.eur_usd : E_MONEY_TYPE.eur, \
                 E_MONEY_GRP.gold: E_MONEY_TYPE.gold}

_point_factor = { E_MONEY_GRP.eur_usd: 0.00001, \
                  E_MONEY_GRP.gold: 0.1 \ 
                  E_MONEY_GRP.usd_jpy: 0.001}


def GetMoneyGrp(grp_str: str) -> E_MONEY_GRP:
    return _money_grp[grp_str]

def GetSrcMoney(grp_str: str) -> E_MONEY_TYPE:
   return _src_money[grp_str]

def GetTargetMoney(grp_str: str) -> E_MONEY_TYPE:
    return _target_money[grp_str]

def GetPointFactor(grp_str: str)-> float:
    return _money_grp[grp_str]
