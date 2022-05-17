import keyword
import os
import logging
import pathlib
import json
import sqlite3
from fastapi import FastAPI, Form, HTTPException
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
        cur.execute(f'''{schema}''')
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
    cur.execute('''SELECT name, category FROM items''')
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
    cur.execute('''SELECT name, category FROM items WHERE name LIKE (?)''', (f"%{keyword}%", ))
    items = cur.fetchall()
    item_list = [dict(item) for item in items]
    items_json = {"items": item_list}
    conn.close()
    logger.info(f"Get items with name containing {keyword}")
    return items_json

@app.post("/items")
def add_item(name: str = Form(...), category: str = Form(...)):
    conn = sqlite3.connect(DATABASE_NAME)
    cur = conn.cursor()
    cur.execute('''INSERT INTO items(name, category) VALUES (?, ?)''', (name, category))
    conn.commit()
    conn.close()
    logger.info(f"Receive item: {name}")
    return {"message": f"item received: {name}"}

@app.get("/image/{image_filename}")
async def get_image(image_filename):
    # Create image path
    image = images / image_filename

    if not image_filename.endswith(".jpg"):
        raise HTTPException(status_code=400, detail="Image path does not end with .jpg")

    if not image.exists():
        logger.debug(f"Image not found: {image}")
        image = images / "default.jpg"

    return FileResponse(image)

