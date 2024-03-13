from model.parts.policy_functions import *
from model.parts.state_update_functions import *


partial_state_update_blocks = [
    # Обновление времени + задание seed'а в начале симуляции
    {
        'policies': {
            'update_time': p_update_time,
        },
        'variables': {
            'curr_time': s_update_curr_time,
            'prev_time': s_update_prev_time,
        }
    }, 

    # Обновление баланса фонда
    {
        'policies': {
            'update_fund': p_update_fund,
        },
        'variables': {
            'staked_balance': s_update_staked_balance,
            'unstaked_balance': s_update_unstaked_balance,
            'TVL': s_update_TVL,
            'promised_staked_balance': s_update_promised_staked_balance,
            'epoch_index': s_update_epoch_index,
            'epoch_start': s_update_epoch_start,
            'epoch_promised_init_investment': s_update_epoch_promised_init_investment,
        }
    }, 
]