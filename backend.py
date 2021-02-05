from fastapi import FastAPI
from pydantic import BaseModel	
import pymongo
import sqlite3

app = FastAPI()
class Meme(BaseModel):
	_id : str
	name : str
	url : str
	caption : str

@app.get('/memes')
def get_all_memes():
	with sqlite3.connect('memes.db') as con:
		cursorObj = con.cursor()
		cursorObj.execute("CREATE TABLE IF NOT EXISTS meme(id integer PRIMARY KEY, name text, url text, caption text)")
		data = (cursorObj.execute("SELECT * FROM meme")).fetchall()
		return data

@app.get('/memes/{_id}')
def get_by_id(_id:str):
	with sqlite3.connect('memes.db') as con:
		cursorObj = con.cursor()
		cursorObj.execute("CREATE TABLE IF NOT EXISTS meme(id integer PRIMARY KEY, name text, url text, caption text)")
		data = (cursorObj.execute("SELECT * FROM meme WHERE id=?", (_id,))).fetchall()
		# con.close()
		return data

@app.post('/memes')
def create_meme(name : str,url: str, caption: str):	
	with sqlite3.connect('memes.db') as con:
		cursorObj = con.cursor()
		cursorObj.execute("CREATE TABLE IF NOT EXISTS meme(id integer PRIMARY KEY, name text, url text, caption text)")
		cursorObj.execute("insert into meme(name,url,caption) values(?,?,?)",(name, url, caption))
		con.commit()
		return 1


