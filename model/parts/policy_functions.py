import numpy as np
from model.utils import is_shock, runge_kutta4, runge_kutta4_system

RP_HIGH, RP_LOW = 0.262, 0.095
RP_TAU = 100.

def p_update_time(params, substep, state_history, previous_state):
    dtime = params['timestep']

    timestep = previous_state['timestep']
    curr_time = previous_state['curr_time']

    if previous_state['timestep'] == 0:
        np.random.seed(seed=previous_state['simulation']+previous_state['run']+previous_state['subset'])  

    if timestep == 0:
        new_curr_time = 0.
        new_prev_time = 0.
    else:
        new_curr_time = curr_time + dtime
        new_prev_time = curr_time

    return {
        'new_curr_time': new_curr_time,
        'new_prev_time': new_prev_time,
    }

def p_update_fund(params, substep, state_history, previous_state):
    timestep = params['timestep']
    shock_times = params['shock_times']
    rn_list = params['actual_profit_rate']
    rp_list = params['promised_profit_rate']
    rw_list = params['withdraw_rate']
    ri_list = params['investment_rate']
    s0_list = params['deposits_density']
    investment_list = params['investors_investments']
    manager_fund_list = params['manager_investments']
    alpha_list = params['alpha']
    beta_list = params['beta']
    gamma_list = params['gamma']
    invest_std = params['invest_std']
    withdraw_std = params['withdraw_std']
    fb_enable = params['feedback_enable']

    curr_time = previous_state['curr_time']
    prev_time = previous_state['prev_time']
    epoch_index = previous_state['epoch_index']
    epoch_start = previous_state['epoch_start']
    epoch_promised_init_investment = previous_state['epoch_promised_init_investment']
    staked_balance = previous_state['staked_balance']
    promised_staked_balance = previous_state['promised_staked_balance']
    unstaked_balance = previous_state['unstaked_balance']
    mod_rp = previous_state['mod_rp']

    new_epoch_index = epoch_index
    new_epoch_start = epoch_start
    new_epoch_promised_init_investment = epoch_promised_init_investment

    shock_flag = is_shock(curr_time, prev_time, shock_times)
    if shock_flag:
        if epoch_index is None:
            new_epoch_index = 0

            new_promised_staked_balance = investment_list[new_epoch_index]
            new_epoch_promised_init_investment = new_promised_staked_balance
            new_staked_balance = investment_list[new_epoch_index] + manager_fund_list[new_epoch_index]
            mod_rp = RP_HIGH
        else:
            rp = rp_list[epoch_index]
            alpha = alpha_list[epoch_index]
            beta = beta_list[epoch_index]
            gamma = gamma_list[epoch_index]
            s0 = s0_list[epoch_index]
            ri = ri_list[epoch_index]
            rw = rw_list[epoch_index]
            rn = rn_list[epoch_index]

            if fb_enable:
                rp = mod_rp

            def s_old(t):
                return s0 * np.exp(ri * (t - epoch_start)) + np.random.normal(scale=invest_std)
            
            def w_old(t):
                dt = t - epoch_start
                try:
                    return rw * np.exp((rp - rw) * dt) * \
                        (epoch_promised_init_investment + alpha * s0 * (np.exp((rw + ri - rp) * dt) - 1) / (rw + ri - rp)) + \
                        np.random.normal(scale=withdraw_std)
                except ZeroDivisionError:
                    return rw * np.exp((rp - rw) * dt) * \
                        (epoch_promised_init_investment + alpha * s0 * dt) + \
                        np.random.normal(scale=withdraw_std)

            def old_promised_staked_func(x, t):
                return rp * x + alpha * s_old(t) - w_old(t)
            
            def old_unstaked_func(state, t):
                x, _ = state
                return -1 * gamma * x + (1 - alpha) * s_old(t) + (1 - beta) * w_old(t)

            def old_staked_func(state, t):
                x, y = state
                return rn * y + alpha * s_old(t) - w_old(t) + rn * (x + abs(x)) / 2
            
            new_promised_staked_balance = runge_kutta4(promised_staked_balance, curr_time, timestep, old_promised_staked_func)            

            state = [unstaked_balance, staked_balance]
            old_funcs = [old_unstaked_func, old_staked_func]     
            new_unstaked_balance, new_staked_balance = runge_kutta4_system(state, curr_time, timestep, old_funcs)

            new_epoch_index += 1
            new_promised_staked_balance += investment_list[new_epoch_index]
            new_epoch_promised_init_investment = new_promised_staked_balance
            new_staked_balance += investment_list[new_epoch_index] + manager_fund_list[new_epoch_index]

            tmp = min(staked_balance - promised_staked_balance, 0)
            mod_rp = RP_LOW + (RP_HIGH - RP_LOW) * np.exp(tmp / RP_TAU)

        new_epoch_start = curr_time

    if not shock_flag or epoch_index is None:
        rn = rn_list[new_epoch_index]
        rp = rp_list[new_epoch_index]
        rw = rw_list[new_epoch_index]
        ri = ri_list[new_epoch_index]
        s0 = s0_list[new_epoch_index]
        alpha = alpha_list[new_epoch_index]
        beta = beta_list[new_epoch_index]
        gamma = gamma_list[new_epoch_index]

        if fb_enable:
            rp = mod_rp

        def s(t):
            return s0 * np.exp(ri * (t - new_epoch_start)) + np.random.normal(scale=invest_std)
    
        def w(t):
            dt = t - new_epoch_start
            try:
                return rw * np.exp((rp - rw) * dt) * \
                    (new_epoch_promised_init_investment + alpha * s0 * (np.exp((rw + ri - rp) * dt) - 1) / (rw + ri - rp)) + \
                    np.random.normal(scale=withdraw_std)
            except ZeroDivisionError:
                return rw * np.exp((rp - rw) * dt) * \
                    (new_epoch_promised_init_investment + alpha * s0 * dt) + \
                    np.random.normal(scale=withdraw_std)

        def unstaked_func(state, t):
            x, _ = state
            return -1 * gamma * x + (1 - alpha) * s(t) + (1 - beta) * w(t)

        def staked_func(state, t):
            x, y = state
            return rn * y + alpha * s(t) - w(t) + rn * (x + abs(x)) / 2
        
        def promised_staked_func(x, t):
            return rp * x + alpha * s(t) - w(t)
    
        state = [unstaked_balance, staked_balance]
        funcs = [unstaked_func, staked_func]     
        new_unstaked_balance, new_staked_balance = runge_kutta4_system(state, curr_time, timestep, funcs)
        new_promised_staked_balance = runge_kutta4(promised_staked_balance, curr_time, timestep, promised_staked_func)

    if not fb_enable:
        mod_rp = rp

    new_TVL = new_staked_balance + new_unstaked_balance

    return {
        'new_staked_balance': new_staked_balance,
        'new_promised_staked_balance': new_promised_staked_balance,
        'new_unstaked_balance': new_unstaked_balance,
        'new_TVL': new_TVL,
        'new_epoch_index': new_epoch_index,
        'new_epoch_start': new_epoch_start,
        'new_epoch_promised_init_investment': new_epoch_promised_init_investment,
        'new_mod_rp': mod_rp,
    }