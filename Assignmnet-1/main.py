from fastapi import FastAPI, Query
app = FastAPI()

# ── Temporary data — acting as our database for now ──────────
products = [
    {'id': 1, 'name': 'Wireless Mouse',      'price': 499,
        'category': 'Electronics', 'in_stock': True},
    {'id': 2, 'name': 'Notebook',            'price':  99,
        'category': 'Stationery',  'in_stock': True},
    {'id': 3, 'name': 'USB Hub',             'price': 799,
        'category': 'Electronics', 'in_stock': False},
    # ── Endpoint 0 — Home ────────────────────────────────────────
    {'id': 4, 'name': 'Pen Set',             'price':  49,
        'category': 'Stationery',  'in_stock': True},
    {'id': 5, 'name': 'Color Pencils',             'price':  200,
        'category': 'Stationery',  'in_stock': True},
    {'id': 6, 'name': 'Sketch Book',             'price':  250,
        'category': 'Stationery',  'in_stock': False},
    {'id': 7, 'name': 'Wireless earphones',             'price':  699, 'category': 'Electronics',  'in_stock': True},]


@app.get('/')
def home():
    return {'message': 'Welcome to our E-commerce API'}

# ── Endpoint 1 — Return all products ──────────────────────────


@app.get('/products')
def get_all_products():
    return {'products': products, 'total': len(products)}


@app.get('/products/filter')
def filter_products(
    category:  str = Query(None, description='Electronics or Stationery'),
    max_price: int = Query(None, description='Maximum price'),
    in_stock:  bool = Query(None, description='True = in stock only')
):
    result = products          # start with all products

    if category:
        result = [p for p in result if p['category'] == category]

    if max_price:
        result = [p for p in result if p['price'] <= max_price]

    if in_stock is not None:
        result = [p for p in result if p['in_stock'] == in_stock]

    return {'filtered_products': result, 'count': len(result)}

# ── Endpoint 2 — Return one product by its ID ──────────────────


@app.get('/products/{product_id}')
def get_product(product_id: int):
    for product in products:
        if product['id'] == product_id:
            return {'product': product}
    return {'error': 'Product not found'}


@app.get("/products/category/{category_name}")
def get_by_category(category_name: str):
    result = [p for p in products if p["category"] == category_name]
    if not result:
        return {"error": "No products found in this category"}
    return {"category": category_name, "products": result, "total": len(result)}


@app.get("/instock")
def get_instock():
    available = [p for p in products if p["in_stock"] == True]
    return {"in_stock_products": available, "count": len(available)}


@app.get("/summary")
def get_summary():
    available = [p for p in products if p["in_stock"] == True]
    not_available = [p for p in products if p["in_stock"] == False]
    result = []
    for p in products:
        if p["category"] not in result:
            result.append(p["category"])

    return {"store_name": "My E-commerce Store", "total_products": len(products), "in_stock": len(available), "out_of_stock": len(not_available), "categories": result}


@app.get("/products/search/{keyword}")
def get_by_keyword(keyword: str):
    result = [product for product in products if keyword.lower()
              in product["name"].lower()]
    if not result:
        return {"message": "No products matched your search"}
    return {"keyword": keyword, 'product': result, 'count': len(result)}


@app.get("/deals")
def get_deals():
    best_deal = min(products, key=lambda p: p["price"])
    premium_pick = max(products, key=lambda p: p["price"])
    return {"best_deal": best_deal, "premium_pick": premium_pick}
