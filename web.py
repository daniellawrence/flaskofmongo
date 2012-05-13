#!/usr/local/bin/python
from flask import Flask
import pymongo
from bson.objectid import ObjectId
app = Flask(__name__)
DATABASE_HOST="localhost"   
DATABASE_PORT=27017
connection = pymongo.Connection( DATABASE_HOST, DATABASE_PORT)

#------------------------------------------------------------------------------
@app.route('/')
def list_database():
	db_list = ""
	for db in connection.database_names():
		db_list += "<a href='/" + db + "/'>" + db +  " </a><br />"
	return "%s" %  db_list

#------------------------------------------------------------------------------
@app.route('/<database>/')
def list_collections(database):
	col_list = ""
	for col in connection[database].collection_names():
		col_list += "<a href='/" + database + "/" + col + "/'>" + col +  " </a><br />"
	return "<h1>Database: %s</h1>%s" % ( database,  col_list  )

#------------------------------------------------------------------------------
@app.route('/<database>/<collection>/')
def list_documents(database,collection):
	doc_list = ""
	cur = connection[database][collection].find({}, fields=['_id'])
	for doc in cur:
		doc_list += "<a href='/%s/%s/%s/'>%s</a><br />" % ( database, collection,doc['_id'],doc["_id"] )
	return "<h1>Database: <a href='/%s/'>%s</a></h1><h2>collection: <a href='/%s/%s/'>%s</a></h2>%s" % ( database, database, database, collection, collection,  doc_list  )

#------------------------------------------------------------------------------
@app.route('/<database>/<collection>/<_id>/')
def single_record(database,collection,_id):
	doc_list = ""
	cur = connection[database][collection].find_one( {'_id': ObjectId(_id)} )
	for doc in cur:
		doc_list += "<strong>%s:</strong> %s<br />" % ( doc, cur[doc] )
	return "<h1>Database: %s</h1><h2>collection: %s</h2><h3>record: %s</h3>%s" % ( database, collection, _id,  doc_list  )

#------------------------------------------------------------------------------
if __name__ == '__main__':
	app.debug = True
	app.run()
