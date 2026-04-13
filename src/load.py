import pandas as pd
from sqlalchemy import create_engine, text
from config.db_config import DB_URI

class OnlineRetailPushing(object):
    def __init__(self):
        self.engine = create_engine(DB_URI)

    def load_dim_date(self, df):
        dim_date = df[["InvoiceDate", 'day', 'month', 'year', 'hour', 'day_of_week']].drop_duplicates()
        dim_date = dim_date.rename(columns={'InvoiceDate': 'full_date'})

        dim_date.to_sql("dim_date", self.engine, schema="dwh", if_exists="append", index=False)

    def load_dim_country(self, df):
        dim_country = df[["Country"]].drop_duplicates()
        dim_country.columns = ["country_name"]

        existing_countries = pd.read_sql("SELECT country_name FROM dwh.dim_country", self.engine)
        dim_new_countries = dim_country[~dim_country['country_name'].isin(existing_countries['country_name'])]

        dim_new_countries.to_sql("dim_country", self.engine, schema="dwh", if_exists="append", index=False)


    def load_dim_product(self, df):
        dim_product = df[["StockCode", "Description"]].drop_duplicates()
        dim_product.columns = ["stock_code", "description"]

        dim_product.to_sql("dim_product", self.engine, schema="dwh", if_exists="append", index=False)

    def load_dim_customer(self, df):
        dim_customer = df[["Customer ID", "Country"]].drop_duplicates()
        dim_country_db = pd.read_sql("SELECT * FROM dwh.dim_country", self.engine)
        dim_customer = dim_customer.merge(dim_country_db,
                                left_on="Country",
                                right_on="country_name",
                                how="left")
        print(dim_customer.columns)
        dim_customer = dim_customer[["Customer ID", "country_id"]]
        dim_customer.columns = ["customer_id", "country_id"]

        dim_customer.to_sql("dim_customer", self.engine, schema="dwh", if_exists="append", index=False)

    def load_fact_sales(self):
        with self.engine.connect() as conn:
            conn.execute(text(""" 
                    INSERT INTO dwh.fact_sales(
                        invoice_no,
                        date_id,
                        customer_key,
                        product_key,
                        country_id,
                        quantity,
                        unit_price,
                        total_amount
                    )
                    SELECT
                    s."Invoice",
                    d.date_id,
                    c.customer_key,
                    p.product_key,
                    co.country_id,
                    s."Quantity",
                    s."Price",
                    s."total_amount"
                    FROM dwh.staging_sales s
                
                    -- map date
                    JOIN dwh.dim_date d
                        ON CAST(s."InvoiceDate" AS TIMESTAMP) = d.full_date
                
                    -- map product
                    JOIN dwh.dim_product p
                        ON s."StockCode" = p.stock_code
                       AND s."Description" = p.description
                
                    -- map customer
                    JOIN dwh.dim_customer c
                        ON s."Customer ID" = c.customer_id
                
                    -- map country
                    JOIN dwh.dim_country co
                        ON s."Country" = co.country_name;
            """))
            conn.commit()

    def load_data(self, df):
        # add to staging table
        df.to_sql(
            "staging_sales",
            self.engine,
            schema="dwh",
            if_exists="replace",
            index=False,
            chunksize=10000,
            method="multi"
        )

        # add dim table
        self.load_dim_date(df)
        print("Done Date")
        self.load_dim_country(df)
        print("Done country")
        self.load_dim_product(df)
        print("Done product")
        self.load_dim_customer(df)
        print("Done customer")

        # add fact tables
        self.load_fact_sales()
        print("Done fact_sales")
