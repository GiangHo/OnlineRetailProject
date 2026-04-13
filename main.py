from src.extract import OnlineRetailRaw
from src.load import OnlineRetailPushing
from src.transform import OnlineRetailFormater


def run_etl():
    retail_extract = OnlineRetailRaw()
    df = retail_extract.extract_data()

    retail_formatter = OnlineRetailFormater()
    df_clean = retail_formatter.transform_data(df)

    retail_load = OnlineRetailPushing()
    retail_load.load_data(df_clean)

if __name__ == "__main__":
    run_etl()
