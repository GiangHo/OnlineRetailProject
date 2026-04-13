import pandas as pd

class OnlineRetailFormater(object):
    def __init__(self):
        pass

    def remove_nan(self, df):
        df.dropna(inplace=True)
        return df

    def clean_quantity(self, df):
        df = df[df['Quantity'] > 0]
        return df

    def clean_price(self, df):
        df = df[df['Price'] != 0]
        return df

    def clean_invoice(self, df):
        df['Invoice'] = df['Invoice'].astype(str)
        df = df[~df["Invoice"].str.contains("C", na=False)]
        return df

    def rename_columns(self, df):
        df = df.rename(columns={
            'Invoice': 'invoice',
            'StockCode': 'stock_code',
            'Description': 'description',
            'Country': 'country_name',
            'Customer ID': 'customer_id',
            'Quantity': 'quantity',
            'Price': 'unit_price',
        })
        return df

    def convert_date(self, df):
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
        # sua full date
        df['full_date'] = df['InvoiceDate'].dt.strftime('%d/%m/%Y')
        df['month'] = df['InvoiceDate'].dt.strftime('%m')
        df['day'] = df['InvoiceDate'].dt.strftime('%d')
        df['year'] = df['InvoiceDate'].dt.strftime('%Y')
        df['day_of_week'] = df['InvoiceDate'].dt.strftime('%A')
        df['hour'] = df['InvoiceDate'].dt.strftime('%H')
        return df

    def transform_data(self, df):
        # remove Nan row
        df = self.remove_nan(df)

        df = self.clean_quantity(df)
        df = self.clean_price(df)
        df= self.clean_invoice(df)
        df = self.convert_date(df)

        df['total_amount'] = df["Quantity"] * df["Price"]

        return df