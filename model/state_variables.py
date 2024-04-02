from radcad.types import StateVariables


initial_state: StateVariables = {
    'staked_balance': 0.0, # количество застейканных токенов, млн. USDe
    'unstaked_balance': 0.0, # количество токенов в обращении, млн. USDe
    'TVL': 0.0, # Общее количество токенов, staked_balance + unstaked_balance, млн. USDe
    'promised_staked_balance': 0.0, # долг перед вкладчиками (стейкерами), млн. USDe
    'curr_time': 0.0, # Текущее время, год
    'prev_time': 0.0, # Время на предыдущем шаге, год
    'epoch_index': None, # Индекс текущей эпохи; в рамках эпохи параметры постоянны
    'epoch_start': 0.0, # Начало текущей эпохи
    'epoch_promised_init_investment': 0.0, # Инвестиции на начало текущей эпохи исходя из обещанной ставки
    'mod_rp': 0.0, # My small experiment
}