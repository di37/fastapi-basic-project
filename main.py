from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from models.models import (
    supplier_pydantic,
    supplier_pydanticIn,
    Supplier,
    product_pydantic,
    product_pydanticIn,
    Product,
)

## Adding cors headers
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Adding CORS urls and add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return {"Message": "go to /docs for the API documentation."}


@app.post("/supplier")
async def add_supplier(supplier_info: supplier_pydanticIn):
    """
    Allows to store new supplier's information.
    """
    supplier_obj = await Supplier.create(**supplier_info.dict(exclude_unset=True))
    response = await supplier_pydantic.from_tortoise_orm(supplier_obj)
    return {"status": "ok", "data": response}


@app.get("/supplier")
async def get_all_suppliers():
    """
    Returns all of the suppliers information stored in the database.
    """
    response = await supplier_pydantic.from_queryset(Supplier.all())
    return {"status": "ok", "data": response}


@app.get("/supplier/{supplier_id}")
async def get_specific_supplier(suppier_id: int):
    """
    Gets a specific supplier record.
    """
    response = await supplier_pydantic.from_queryset_single(Supplier.get(id=suppier_id))
    return {"status": "ok", "data": response}


@app.put("/supplier/{supplier_id}")
async def update_supplier(supplier_id: int, update_info: supplier_pydanticIn):
    """
    Updates a record in the database.
    """
    supplier = await Supplier.get(id=supplier_id)
    update_info = update_info.dict(exclude_unset=True)
    supplier.name = update_info["name"]
    supplier.company = update_info["company"]
    supplier.phone = update_info["phone"]
    supplier.email = update_info["email"]
    await supplier.save()
    response = await supplier_pydantic.from_tortoise_orm(supplier)
    return {"status": "ok", "data": response}


@app.delete("/supplier/{supplier_id}")
async def delete_supplier(supplier_id: int):
    """
    Deletes a record of the supplier.
    """
    await Supplier.filter(id=supplier_id).delete()
    return {"status": "ok"}


@app.post("/product/{supplier_id}")
async def add_product(supplier_id: int, products_details: product_pydanticIn):
    """
    Adds a record of the product according to its supplier.
    """
    supplier = await Supplier.get(id=supplier_id)
    products_details = products_details.dict(exclude_unset=True)
    products_details["revenue"] += (
        products_details["quantity_sold"] * products_details["unit_price"]
    )
    product_obj = await Product.create(**products_details, supplied_by=supplier)
    response = await product_pydantic.from_tortoise_orm(product_obj)
    return {"status": "ok", "data": response}


@app.get("/product")
async def all_products():
    """
    Shows all of the products.
    """
    response = await product_pydantic.from_queryset(Product.all())
    return {"status": "ok", "data": response}


@app.get("/product/{id}")
async def specific_product(id: int):
    """
    Returns a specific product as per its id.
    """
    response = await product_pydantic.from_queryset_single(Product.get(id=id))
    return {"status": "ok", "data": response}


@app.put("/product/{id}")
async def update_product(id: int, update_info: product_pydanticIn):
    """
    Allows to update products already existing in the database.
    """
    product = await Product.get(id=id)
    update_info = update_info.dict(exclude_unset=True)
    product.name = update_info["name"]
    product.quantity_in_stock = update_info["quantity_in_stock"]
    product.revenue += (
        update_info["quantity_sold"] * update_info["unit_price"]
    ) + update_info["revenue"]
    product.quantity_sold += update_info["quantity_sold"]
    product.unit_price = update_info["unit_price"]
    await product.save()
    response = await product_pydantic.from_tortoise_orm(product)
    return {"status": "ok", "data": response}


@app.delete("/product/{id}")
async def delete_product(id: int):
    """
    Deletes a product information from the database as per its id.
    """
    await Product.filter(id=id).delete()
    return {"status": "ok"}


register_tortoise(
    app,
    db_url="sqlite://database.sqlite3",
    modules={"models": ["models.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
