import sys

import streamlit
from hydra.core.global_hydra import GlobalHydra
from hydra.experimental import compose, initialize


@streamlit.cache(allow_output_mutation=True)
def read_config(path: str):
    GlobalHydra.instance().clear()
    initialize(config_path='..')
    return compose(path, overrides=sys.argv[1:])
