from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime

Base = declarative_base()

# ===================== DIMENSIONS =====================

class DimDate(Base):
    __tablename__ = "dim_date"
    __table_args__ = {"schema": "dwh"}

    date_id = Column(Integer, primary_key=True, autoincrement=True)
    full_date = Column(DateTime, unique=True)
    day = Column(Integer)
    month = Column(Integer)
    year = Column(Integer)
    hour = Column(Integer)
    day_of_week = Column(String)


class DimCustomer(Base):
    __tablename__ = "dim_customer"
    __table_args__ = {"schema": "dwh"}

    customer_key = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer)
    country_id = Column(Integer)


class DimProduct(Base):
    __tablename__ = "dim_product"
    __table_args__ = {"schema": "dwh"}

    product_key = Column(Integer, primary_key=True, autoincrement=True)
    stock_code = Column(String)
    description = Column(String)


class DimCountry(Base):
    __tablename__ = "dim_country"
    __table_args__ = {"schema": "dwh"}

    country_id = Column(Integer, primary_key=True, autoincrement=True)
    country_name = Column(String, unique=True)


# ===================== FACT =====================

class FactSales(Base):
    __tablename__ = "fact_sales"
    __table_args__ = {"schema": "dwh"}

    sales_key = Column(Integer, primary_key=True, autoincrement=True)
    invoice_no = Column(String)

    date_id = Column(Integer, ForeignKey("dwh.dim_date.date_id"))
    customer_key = Column(Integer, ForeignKey("dwh.dim_customer.customer_key"))
    product_key = Column(Integer, ForeignKey("dwh.dim_product.product_key"))
    country_id = Column(Integer, ForeignKey("dwh.dim_country.country_id"))

    quantity = Column(Integer)
    unit_price = Column(Numeric)
    total_amount = Column(Numeric)
