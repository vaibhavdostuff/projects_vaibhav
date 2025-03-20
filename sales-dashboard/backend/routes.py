from fastapi import APIRouter, Depends
from database import conn, cursor
from models import Sale

router = APIRouter()

@router.post("/sales/")
def add_sale(sale: Sale):
    cursor.execute("INSERT INTO sales (product_name, sales_amount, date) VALUES (%s, %s, %s)",
                   (sale.product_name, sale.sales_amount, sale.date))
    conn.commit()
    return {"message": "Sale record added"}

@router.get("/sales/")
def get_sales():
    cursor.execute("SELECT * FROM sales")
    sales = cursor.fetchall()
    return {"sales": sales}
