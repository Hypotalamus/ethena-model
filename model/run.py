from radcad import Model
from radcad import Simulation, Experiment
from radcad.engine import Engine, Backend
import pandas as pd

from model.system_parameters import parameters
from model.state_variables import initial_state
from model.state_update_blocks import partial_state_update_blocks


model = Model(
    params=parameters,
    initial_state=initial_state,
    state_update_blocks=partial_state_update_blocks,
)

simulation = Simulation(model=model, timesteps=5000, runs=1)
experiment = Experiment([simulation])
experiment.engine = Engine(backend=Backend.PATHOS)

raw_result = experiment.run()
df = pd.DataFrame(raw_result)