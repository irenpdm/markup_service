from itertools import product
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from fastapi.responses import RedirectResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host = "redis-11553.c250.eu-central-1-1.ec2.cloud.redislabs.com",
    port = 11553,
    password = "lRFsB5mwxnZpNmbUfJwHqL1hvmpwcaBN",
    decode_responses = True
)

class Product(HashModel):
    name: str
    price: float
    kind: str
    markup: float | None = None

    class Meta:
        database = redis

@app.get('/products')
def all():
    return [format(pk) for pk in Product.all_pks()]

def format(pk: str):
    product = Product.get(pk)

    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'kind': product.kind,
        'markup': product.markup
    }

@app.post('/products')
def create(product: Product):
    return product.save()

@app.get('/products/{pk}')
def get(pk: str):
    return Product.get(pk)


@app.delete('/products/{pk}')
def delete(pk: str):
    return Product.delete(pk)

@app.put('/products')
def all():
    return [update_item(pk) for pk in Product.all_pks()]

def update_item(pk: str):
    product = Product.get(pk)
    product.price = product.price + product.price * product.markup / 100
    product.markup = 0
    
    return product.save()

@app.delete('/products')
def all():
    return [delete(pk) for pk in Product.all_pks()]

def delete(pk: str):
    return Product.delete(pk)
