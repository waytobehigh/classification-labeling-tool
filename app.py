import streamlit
import os
from typing import List, Tuple

from omegaconf import DictConfig
from pathlib import Path

from utils.handlers import *
from utils.hydra import read_config
from utils.streamlit import rerun


@streamlit.cache(allow_output_mutation=True)
def init() -> Tuple[DictConfig, List, List]:
    cfg = read_config('./config.yaml')

    if not os.path.isdir(cfg.input_path):
        raise NotADirectoryError

    for label in cfg.labels:
        os.makedirs(os.path.join(cfg.output_path, label), exist_ok=True)

    paths = list(Path(cfg.input_path).glob(cfg.input_pattern))
    cache = []

    return cfg, paths, cache


if __name__ == '__main__':
    cfg, paths, cache = init()

    streamlit.title('Classification labeling tool')

    if not paths:
        streamlit.markdown('There are no files to label :(')
    else:
        file = paths[-1]
        globals()[cfg.handler](file)

        for label in cfg.labels:
            if streamlit.button(label):
                paths.pop(-1)
                cache.append((file, label))
                rerun()

    streamlit.markdown(f'{len(paths)} images left')
    streamlit.markdown('Commit the changes if you are sure')
    if streamlit.button('COMMIT'):
        for file, label in cache:
            os.rename(file, os.path.join(cfg.output_path, label, file.stem))
        streamlit.caching.clear_cache()
        rerun()

    streamlit.write([(str(file), tag) for file, tag in cache])
