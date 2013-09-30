#!/usr/bin/env python
""" Very basic web viewer of a mongo database
"""
from flask import Flask, render_template
import pymongo
from bson.objectid import ObjectId

APP = Flask(__name__)
DATABASE_HOST="localhost"   
DATABASE_PORT=27017
connection = pymongo.Connection( DATABASE_HOST, DATABASE_PORT)

#------------------------------------------------------------------------------
@APP.route('/')
def list_database():
    """ list all databases from the connection
    """
    db_list = connection.database_names()
    return render_template('base.html', db_list=db_list)

#------------------------------------------------------------------------------
@APP.route('/db/<database>/')
def list_collections(database):
    """ list all connections from the connection, database
    """
    col_list = ""
    for col in connection[database].collection_names():
        col_list += "<a href='/db/" + database + "/" + col + "/'>" + col +  " </a><br />"
    return "<h1>Database: %s</h1>%s" % ( database,  col_list  )

#------------------------------------------------------------------------------
@APP.route('/db/<database>/<collection>/')
def list_documents(database,collection):
    """ list all documents from the connection, database, collection
    """
    doc_list = ""
    cur = connection[database][collection].find({}, fields=['_id'])
    for doc in cur:
        doc_list += "<a href='/db/%s/%s/%s/'>%s</a><br />" % ( database, collection,doc['_id'],doc["_id"] )
    return "<h1>Database: <a href='/%s/'>%s</a></h1><h2>collection: <a href='/db/%s/%s/'>%s</a></h2>%s" % ( database, database, database, collection, collection,  doc_list  )

#------------------------------------------------------------------------------
@APP.route('/db/<database>/<collection>/<_id>/')
def single_record(database,collection,_id):
    """ list all keys,values from the connection, database, collection, record
    """
    doc_list = ""
    cur = connection[database][collection].find_one( {'_id': ObjectId(_id)} )
    for doc in cur:
        doc_list += "<strong>%s:</strong> %s<br />" % ( doc, cur[doc] )
    message = "<br /><a href=\"/db/%s/%s/%s/remove\">Remove this document</a>" % ( database, collection, _id )
    return "<h1>Database: %s</h1><h2>collection: %s</h2><h3>record: %s</h3>%s%s" % ( database, collection, _id,  doc_list, message  )

#------------------------------------------------------------------------------
@APP.route('/db/<database>/<collection>/<_id>/remove')
def remove_record(database,collection,_id):
    """ Removes a record from the collection. Useful for deleting bad records.
    """
    doc_list = ""
    cur = connection[database][collection].find_and_modify( {'_id': ObjectId(_id)}, remove=True )
    for doc in cur:
        doc_list += "<strong>%s:</strong> %s<br />" % ( doc, cur[doc] )
    message = "<br /><strong>Document has been removed</strong>"
    message += "<br /><a href=\"/db/%s/%s/\">Return to Collection" % ( database, collection )
    return "<h1>Database: %s</h1><h2>collection: %s</h2><h3>record: %s</h3>%s%s" % ( database, collection, _id,  doc_list, message  )

#------------------------------------------------------------------------------
if __name__ == '__main__':
    """ start the APPlication
    """
    APP.debug = True
    APP.run()
