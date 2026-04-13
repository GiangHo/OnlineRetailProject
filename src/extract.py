import pandas as pd

from config.system_config import ONLINE_RETAIL_FILE


class OnlineRetailRaw(object):
    def __init__(self):
        self.file_path = ONLINE_RETAIL_FILE

    def extract_data(self):
        df = pd.read_csv(self.file_path)
        return df
