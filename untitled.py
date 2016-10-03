from pymongo import MongoClient

client = MongoClient('localhost', 27017)
if 'test' in client.database_names():
    print "test found in the database names!"
db = client.test
if 'restraunts' in db.collection_names():
    print "restraunts collection exist in database!"
doc = db.restraunts.find_one({'_id': 'the'})
print doc
l = doc['postings']
print len(l)
le = [('d', 1), ('q', 2)]
# updating the posing list
db.restraunts.update(
    {'_id': 'the'},
    {'postings': le})
print "Printing updated details\n"
doc = db.restraunts.find_one({'_id': 'the'})
print doc['postings']
