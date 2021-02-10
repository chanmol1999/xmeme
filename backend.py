from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel	
import json
import sqlite3

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Meme(BaseModel):
	name : str
	url : str
	caption : str

@app.get('/memes')
def get_all_memes():
	with sqlite3.connect('memes.db') as con:
		cursorObj = con.cursor()
		cursorObj.execute("CREATE TABLE IF NOT EXISTS meme(id integer PRIMARY KEY, name text, url text, caption text)")
		con.commit()
		con.row_factory = sqlite3.Row
		cursorObj = con.cursor()
		data = (cursorObj.execute("SELECT * FROM meme order by id desc limit 100")).fetchall()
		return ( [dict(ix) for ix in data] ) 

@app.get('/memes/{_id}')
def get_by_id(_id:str):
	with sqlite3.connect('memes.db') as con:
		cursorObj = con.cursor()
		cursorObj.execute("CREATE TABLE IF NOT EXISTS meme(id integer PRIMARY KEY, name text, url text, caption text)")
		con.commit()
		con.row_factory = sqlite3.Row
		cursorObj = con.cursor()
		data = (cursorObj.execute("SELECT * FROM meme WHERE id=?", (_id,))).fetchone()
		return data

@app.post('/memes')
def create_meme(meme:Meme):	
	with sqlite3.connect('memes.db') as con:
		cursorObj = con.cursor()
		cursorObj.execute("CREATE TABLE IF NOT EXISTS meme(id integer PRIMARY KEY, name text, url text, caption text)")
		cursorObj.execute("insert into meme(name,url,caption) values(?,?,?)",(meme.name, meme.url, meme.caption))
		con.commit()
		return {"id":str((cursorObj.lastrowid))}


