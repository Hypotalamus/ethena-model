from dataclasses import dataclass
from typing import List
from radcad.utils import default
import math

# SCENARIO == 1 - четыре варианта с двумя наборами параметров;
# SCENARIO == 2 - автоматически регулируемая процентная ставка
# SCENARIO == 3 - безусловное помесячное снижение процентной ставки в первый год

SCENARIO = 2

if SCENARIO == 1:
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
        investment_rate: List[List[float]]=default([[0.], [7.187, 0.], [7.187, 0.], [7.187, 0.]])
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
        # включить обратную связь
        feedback_enable: List[bool]=default([False])

elif SCENARIO == 2:
    N = 5 # number of years

    @dataclass
    class Parameters:
        # длительность одного шага, год
        timestep: List[float]=default([1.e-3])
        # моменты изменения параметров модели, год
        shock_times: List[List[float]]=default([[float(x) / 12. for x in range(1, 12 * N + 1)]])
        # C инвестиции менеджера, млн. USD
        manager_investments: List[List[float]]=default([(12 * N + 1) * [0.]])
        # K инвестиции инвесторов, млн. USD 
        investors_investments: List[List[float]]=default([(12 * N + 1) * [0.]])
        # s0 плотность депозитов в начале периодов, млн. USD / год  
        deposits_density: List[List[float]]=default([[100. * math.exp(7.187 * float(x)/12.) for x in range(12)] + (12 * (N - 1) + 1) * [1600.]])
        # ri скорость инвестиций, 1 / год 
        investment_rate: List[List[float]]=default([12 * [7.187] + (12 * (N - 1) + 1) * [0.]])    
        # rw скорость оттока средств, 1 / год 
        withdraw_rate: List[List[float]]=default([(12 * N + 1) * [1.47]])
        # rp обещанная скорость прироста средств, 1 / год
        promised_profit_rate: List[List[float]]=default([[0.501 - (0.501 - 0.095) * float(x) / 12. for x in range(12)] + (12 * (N - 1) + 1) * [0.095]])         
        # promised_profit_rate: List[List[float]]=default([(12 * N + 1) * [0.501]])
        # rn действительная скорость прироста средств, 1 / год 
        actual_profit_rate: List[List[float]]=default([(12 * N + 1) * [0.104]])
        # Доля наминченных токенов, идущих в стейк (в каждый момент времени)    
        alpha: List[List[float]]=default([12 * [0.9] + (12 * (N - 1) + 1) * [0.3]])
        # Доля погашаемых токенов при выходе из стейка (в каждый момент времени)
        beta: List[List[float]]=default([(12 * N + 1) * [0.9]])
        # Коэффициент погашения токенов, находящихся в обращении (в каждый момент времени)
        gamma: List[List[float]]=default([12 * [1.0] + (12 * (N - 1) + 1) * [0.4]])
        # Стандартное отклонение для инвестиций на каждом шаге
        invest_std: List[float]=default([0.])
        # стандартное отклонение для оттока средств
        withdraw_std: List[float]=default([0.])
        # включить обратную связь
        feedback_enable: List[bool]=default([True])

elif SCENARIO == 3:
    N = 5

    @dataclass
    class Parameters:
        # длительность одного шага, год
        timestep: List[float]=default([1.e-3])
        # моменты изменения параметров модели, год
        shock_times: List[List[float]]=default([[float(x) / 12. for x in range(1, 12 * N + 1)]])
        # C инвестиции менеджера, млн. USD
        manager_investments: List[List[float]]=default([(12 * N + 1) * [0.]])
        # K инвестиции инвесторов, млн. USD 
        investors_investments: List[List[float]]=default([(12 * N + 1) * [0.]])
        # s0 плотность депозитов в начале периодов, млн. USD / год  
        deposits_density: List[List[float]]=default([[100. * math.exp(7.187 * float(x)/12.) for x in range(12)] + (12 * (N - 1) + 1) * [600.]])
        # ri скорость инвестиций, 1 / год 
        investment_rate: List[List[float]]=default([12 * [7.187] + (12 * (N - 1) + 1) * [0.]])    
        # rw скорость оттока средств, 1 / год 
        withdraw_rate: List[List[float]]=default([(12 * N + 1) * [1.47]])
        # rp обещанная скорость прироста средств, 1 / год
        promised_profit_rate: List[List[float]]=default([[0.501 - (0.501 - 0.095) * float(x) / 12. for x in range(12)] + (12 * (N - 1) + 1) * [0.095]])
        # rn действительная скорость прироста средств, 1 / год 
        actual_profit_rate: List[List[float]]=default([(12 * N + 1) * [0.104]])
        # Доля наминченных токенов, идущих в стейк (в каждый момент времени)    
        alpha: List[List[float]]=default([12 * [0.9] + (12 * (N - 1) + 1) * [0.3]])
        # Доля погашаемых токенов при выходе из стейка (в каждый момент времени)
        beta: List[List[float]]=default([(12 * N + 1) * [0.9]])
        # Коэффициент погашения токенов, находящихся в обращении (в каждый момент времени)
        gamma: List[List[float]]=default([12 * [1.0] + (12 * (N - 1) + 1) * [0.4]])
        # Стандартное отклонение для инвестиций на каждом шаге
        invest_std: List[float]=default([0.])
        # стандартное отклонение для оттока средств
        withdraw_std: List[float]=default([0.])
        # включить обратную связь
        feedback_enable: List[bool]=default([False]) 

parameters = Parameters().__dict__