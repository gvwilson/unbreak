import polars as pl

orders = pl.DataFrame({
    "order_id": [1, 2, 3, 4],
    "customer_id": [10, 20, 30, 99],
    "amount": [50.0, 75.0, 30.0, 20.0],
})

customers = pl.DataFrame({
    "customer_id": [10, 20, 30],
    "name": ["Alice", "Bob", "Carol"],
})

# BUG: the default join is inner, so order 4 (customer_id=99) is silently dropped
# BUG: because there is no matching customer; use how="left" to retain all orders
result = orders.join(customers, on="customer_id")
print(f"orders in input : {len(orders)}")
print(f"rows after join : {len(result)}")
print(result)
