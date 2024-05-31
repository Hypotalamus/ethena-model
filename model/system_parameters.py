from dataclasses import dataclass
from typing import List
from radcad.utils import default
import math

# SCENARIO == 1 - четыре варианта с двумя наборами параметров;
# SCENARIO == 2 - автоматически регулируемая процентная ставка
# SCENARIO == 3 - безусловное помесячное снижение процентной ставки в первый год
# SCENARIO == 4 - стресс-тест автоматически регулируемой процентной ставки:
#   rn также меняется после одного года: 11% -> 11%, 8%, 4%, 0%, -2%, -50%
#   rn: 0.104, 0.077, 0.039, 0., -0.02, -0.693
# SCENARIO == 5 - стресс-тест автоматически регулируемой процентной ставки:
#   alpha меняется после одного года: 0.3 -> 0.3, 0.6, 0.9, 1.0
#   gamma меняется после одного года: 0.4 -> 0.4, 0.75, 1.0, 1.25
# SCENARIO == 6 - параметрический резонанс
SCENARIO = 6

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
        deposits_density: List[List[float]]=default([[20.], [100., 680.], [100., 800.], [100., 400.]])
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

elif SCENARIO == 4:
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
        actual_profit_rate: List[List[float]]=default([12 * [0.104] + (12 * (N - 1) + 1) * [0.104]
                                                      ,12 * [0.104] + (12 * (N - 1) + 1) * [0.077]
                                                      ,12 * [0.104] + (12 * (N - 1) + 1) * [0.039]
                                                      ,12 * [0.104] + (12 * (N - 1) + 1) * [0.]
                                                      ,12 * [0.104] + (12 * (N - 1) + 1) * [-0.02]
                                                      ,12 * [0.104] + (12 * (N - 1) + 1) * [-0.693]
                                                       ])
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

elif SCENARIO == 5:
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
        actual_profit_rate: List[List[float]]=default([12 * [0.104] + (12 * (N - 1) + 1) * [0.104]])
        # Доля наминченных токенов, идущих в стейк (в каждый момент времени)    
        alpha: List[List[float]]=default([12 * [0.9] + (12 * (N - 1) + 1) * [0.3]
                                         ,12 * [0.9] + (12 * (N - 1) + 1) * [0.6]
                                         ,12 * [0.9] + (12 * (N - 1) + 1) * [0.9]
                                         ,12 * [0.9] + (12 * (N - 1) + 1) * [1.0]
                                         ])
        # Доля погашаемых токенов при выходе из стейка (в каждый момент времени)
        beta: List[List[float]]=default([(12 * N + 1) * [0.9]])
        # Коэффициент погашения токенов, находящихся в обращении (в каждый момент времени)
        gamma: List[List[float]]=default([12 * [1.0] + (12 * (N - 1) + 1) * [0.4]
                                         ,12 * [1.0] + (12 * (N - 1) + 1) * [0.75]
                                         ,12 * [1.0] + (12 * (N - 1) + 1) * [1.0]
                                         ,12 * [1.0] + (12 * (N - 1) + 1) * [12.5]
                                          ])
        # Стандартное отклонение для инвестиций на каждом шаге
        invest_std: List[float]=default([0.])
        # стандартное отклонение для оттока средств
        withdraw_std: List[float]=default([0.])
        # включить обратную связь
        feedback_enable: List[bool]=default([True])

elif SCENARIO == 6:
    N = 2
    T = 1. / 2.
    sh_nums = 365 * N
    sh_t = [1./365 * x for x in range(sh_nums)]
    ampl = 0.2

    @dataclass
    class Parameters:
        # длительность одного шага, год
        timestep: List[float]=default([1.e-4])
        # моменты изменения параметров модели, год
        shock_times: List[List[float]]=default([sh_t])
        # C инвестиции менеджера, млн. USD
        manager_investments: List[List[float]]=default([[0.] * sh_nums])
        # K инвестиции инвесторов, млн. USD 
        investors_investments: List[List[float]]=default([[0.] * sh_nums])
        # s0 плотность депозитов в начале периодов, млн. USD / год  
        deposits_density: List[List[float]]=default([[200. * (1 + ampl * math.cos(2 * math.pi * t / T)) for t in sh_t]]) # []
        # ri скорость инвестиций, 1 / год 
        investment_rate: List[List[float]]=default([[0.] * sh_nums])
        # rw скорость оттока средств, 1 / год 
        withdraw_rate: List[List[float]]=default([[0.6] * sh_nums])
        # rp обещанная скорость прироста средств, 1 / год 
        promised_profit_rate: List[List[float]]=default([[0.095] * sh_nums])
        # rn действительная скорость прироста средств, 1 / год 
        actual_profit_rate: List[List[float]]=default([[0.104] * sh_nums])
        # Доля наминченных токенов, идущих в стейк (в каждый момент времени)    
        alpha: List[List[float]]=default([[0.6] * sh_nums])
        # Доля погашаемых токенов при выходе из стейка (в каждый момент времени)
        beta: List[List[float]]=default([[0.9] * sh_nums])
        # Коэффициент погашения токенов, находящихся в обращении (в каждый момент времени)
        gamma: List[List[float]]=default([[1.0] * sh_nums])
        # Стандартное отклонение для инвестиций на каждом шаге
        invest_std: List[float]=default([0.])
        # стандартное отклонение для оттока средств
        withdraw_std: List[float]=default([0.])
        # включить обратную связь
        feedback_enable: List[bool]=default([True])

parameters = Parameters().__dict__