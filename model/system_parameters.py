from dataclasses import dataclass
from typing import List
from radcad.utils import default


@dataclass
class Parameters:

    # длительность одного шага, год
    timestep: List[float]=default([1.e-3])
    # моменты изменения параметров модели, год
    shock_times: List[List[float]]=default([[], [0.5], [1.0], [0.5]])
    # C инвестиции менеджера, млн. USD
    manager_investments: List[List[float]]=default([[0.], [0., 0.]])
    # K инвестиции инвесторов, млн. USD 
    investors_investments: List[List[float]]=default([[0.], [0., 0.]])
    # s0 плотность депозитов в начале периодов, млн. USD / год  
    deposits_density: List[List[float]]=default([[20.], [100., 400.], [100., 800.], [100., 400.]])
    # ri скорость инвестиций, 1 / год 
    investment_rate: List[List[float]]=default([[0.], [7.187, 0.], [7.187, 0.], [7.187, 0.3]])
    # rw скорость оттока средств, 1 / год 
    withdraw_rate: List[List[float]]=default([[0.05], [1.47, 1.47]])
    # rp обещанная скорость прироста средств, 1 / год 
    promised_profit_rate: List[List[float]]=default([[0.095], [0.501, 0.501], [0.501, 0.501], [0.501, 0.095]])
    # rn действительная скорость прироста средств, 1 / год 
    actual_profit_rate: List[List[float]]=default([[0.104], [0.104, 0.104]])
    # Доля наминченных токенов, идущих в стейк (в каждый момент времени)    
    alpha: List[List[float]]=default([[0.6], [0.9, 0.3]])
    # Доля погашаемых токенов при выходе из стейка (в каждый момент времени)
    beta: List[List[float]]=default([[0.9], [0.9, 0.9]])
    # Коэффициент погашения токенов, находящихся в обращении (в каждый момент времени)
    gamma: List[List[float]]=default([[1.0], [1.0, 0.4]])
    # Стандартное отклонение для инвестиций на каждом шаге
    invest_std: List[float]=default([0.])
    # стандартное отклонение для оттока средств
    withdraw_std: List[float]=default([0.]) 

parameters = Parameters().__dict__