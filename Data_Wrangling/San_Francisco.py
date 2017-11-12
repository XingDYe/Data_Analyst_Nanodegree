#! /user/bin/env python
#-*- coding: utf-8 -*-

## Create the database and import data into database.

import sqlite3
import csv


# connected to database
conn = sqlite3.connect('project.db')
conn.text_factory = str
cur = conn.cursor()

with open('ways_tags.csv','r') as file:
	dr = csv.DictReader(file)
	db0 = [(e['id'],e['key'],e['type'],e['value']) for e in dr]
cur.executemany("INSERT INTO ways_tags(id,key,type,value) VALUES(?,?,?,?)",db0)

with open('nodes_tags.csv','r') as file:
	dr1 = csv.DictReader(file)
	db1 = [(e['id'],e['key'],e['type'],e['value']) for e in dr1]
cur.executemany("INSERT INTO nodes_tags(id, key, type, value) VALUES(?,?,?,?)",db1)

with open('ways_nodes.csv','r') as f2:
	dr2 = csv.DictReader(f2)
	db2 = [(e['id'],e['node_id'], e['position']) for e in dr2]
cur.executemany("INSERT INTO ways_nodes(id, node_id, position) VALUES(?,?,?)",db2)

with open('nodes.csv','r') as f3:
	dr3 = csv.DictReader(f3)
	db3 = [(e['id'],e['uid'],e['user'],e['changeset'],e['lat'], e['lon'], e['timestamp']) for e in dr3]
cur.executemany("INSERT INTO nodes(id, uid, user, changeset, lat, lon,'timestamp') VALUES(?,?,?,?,?,?,?)",db3)

with open('ways.csv','r') as f4:
	dr4 = csv.DictReader(f4)
	db4 = [(e['id'], e['uid'], e['user'], e['changeset'], e['timestamp']) for e in dr4]
cur.executemany("INSERT INTO ways(id, uid, user, changeset,'timestamp') VALUES(?,?,?,?,?)",db4)	

conn.commit()
conn.close()
