def s_update_curr_time(params, substep, state_history, previous_state, policy_input):
    new_curr_time = policy_input['new_curr_time']
    return "curr_time", new_curr_time

def s_update_prev_time(params, substep, state_history, previous_state, policy_input):
    new_prev_time = policy_input['new_prev_time']
    return "prev_time", new_prev_time

def s_update_staked_balance(params, substep, state_history, previous_state, policy_input):
    new_staked_balance = policy_input['new_staked_balance']
    return "staked_balance", new_staked_balance

def s_update_unstaked_balance(params, substep, state_history, previous_state, policy_input):
    new_unstaked_balance = policy_input['new_unstaked_balance']
    return "unstaked_balance", new_unstaked_balance

def s_update_TVL(params, substep, state_history, previous_state, policy_input):
    new_TVL = policy_input['new_TVL']
    return "TVL", new_TVL

def s_update_promised_staked_balance(params, substep, state_history, previous_state, policy_input):
    new_promised_staked_balance = policy_input['new_promised_staked_balance']
    return "promised_staked_balance", new_promised_staked_balance

def s_update_epoch_index(params, substep, state_history, previous_state, policy_input):
    new_epoch_index = policy_input['new_epoch_index']
    return "epoch_index", new_epoch_index

def s_update_epoch_start(params, substep, state_history, previous_state, policy_input):
    new_epoch_start = policy_input['new_epoch_start']
    return "epoch_start", new_epoch_start

def s_update_epoch_promised_init_investment(params, substep, state_history, previous_state, policy_input):
    new_epoch_promised_init_investment = policy_input['new_epoch_promised_init_investment']
    return "epoch_promised_init_investment", new_epoch_promised_init_investment

def s_update_mod_rp(params, substep, state_history, previous_state, policy_input):
    new_mod_rp = policy_input['new_mod_rp']
    return "mod_rp", new_mod_rp

