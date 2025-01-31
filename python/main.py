import keyword
import os
import logging
import pathlib
import json
import sqlite3
import hashlib
from fastapi import FastAPI, File, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware


DATABASE_NAME = "../db/mercari.sqlite3"

app = FastAPI()
logger = logging.getLogger("uvicorn")
logger.level = logging.INFO
images = pathlib.Path(__file__).parent.resolve() / "image"
origins = [ os.environ.get('FRONT_URL', 'http://localhost:3000') ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET","POST","PUT","DELETE"],
    allow_headers=["*"],
)

@app.on_event("startup")
def database_connect():
    conn = sqlite3.connect(DATABASE_NAME)
    cur = conn.cursor()
    with open('../db/items.db') as schema_file:
        schema = schema_file.read()
        cur.executescript(f'''{schema}''')
        conn.commit()
        logger.info("Database initialization successful!")
        conn.close()


@app.get("/")
def root():
    return {"message": "Hello, world!"}

@app.get("/items")
def get_items():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('''SELECT items.name, category.name as category, items.image FROM items INNER JOIN category ON category.id = items.category_id''')
    items = cur.fetchall()
    item_list = [dict(item) for item in items]
    items_json = {"items": item_list}
    conn.close()
    logger.info("Items get successfully!")
    return items_json

@app.get("/search")
def search_items(keyword: str):
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('''SELECT items.name, category.name as category, items.image FROM items INNER JOIN category ON category.id = items.category_id WHERE items.name LIKE (?)''', (f"%{keyword}%", ))
    items = cur.fetchall()
    item_list = [dict(item) for item in items]
    items_json = {"items": item_list}
    conn.close()
    logger.info(f"Get items with name containing {keyword}")
    return items_json

@app.get("/items/{item_id}")
def get_item(item_id):
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('''SELECT items.name, category.name as category, items.image FROM items INNER JOIN category ON category.id = items.category_id WHERE items.id = (?)''', (item_id, ))
    conn.commit()
    #conn.close()
    logger.info(f"Item fetch successful from item id")
    return cur.fetchone()
    

@app.post("/items")
def add_item(name: bytes = File(...), category: bytes = File(...), image: bytes = File(...)):
    conn = sqlite3.connect(DATABASE_NAME)
    cur = conn.cursor()

    # decode file to string
    name_str = name.decode('utf-8')
    category_str = category.decode('utf-8')

    # encode uploaded image
    hash = encoded_image(image)
    cur.execute('''INSERT OR IGNORE INTO category
                (name) VALUES (?)''', (category_str, ))
    cur.execute('''SELECT id FROM category WHERE name = (?)''', (category_str, ))
    category_id = cur.fetchone()[0]
    cur.execute('''INSERT INTO items
                (name, category_id, image) VALUES (?,?,?)''', (name_str, category_id, hash))
    conn.commit()
    conn.close()

    logger.info(f"item received: {name_str}, {category_str}, {hash}")
    open
    return {"message": f"item received: {name_str}, {category_str}, {hash}"}

@app.get("/image/{image_filename}")
async def get_image(image_filename):
    # Create image path
    image = images / image_filename

    if not image_filename.endswith(".jpg"):
        raise HTTPException(status_code=400, detail="Image path does not end with .jpg")

    if not image.exists():
        logger.info(f"Image not found: {image}")
        image = images / "default.jpg"

    return FileResponse(image)

def encoded_image(image):
    hash_image = hashlib.sha256(image).hexdigest() + ".jpg"

    with open("images/" + hash_image, "wb") as file:
        file.write(image)
    return hash_image