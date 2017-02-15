# First you need to start mongo database
# Go to c:\users\r1702898\downloads\mongo and type
# cd C:/Program Files/MongoDB/Server/3.2/bin/
# mongod --dbpath=C:/users/r1702898/documents/modelagem/meusmodelos/mongorepository/

import pymongo as mongo

client1 = mongo.MongoClient()
db = client1.dsdb
people = db.people
person1 = {'name': 'John', 'dob' : '1957-12-24'}
person2 = {"_id" : "XVT162", "empname" : "Jane Doe", "dob" : "1964-05-16"}
persons = [{"empname" : "Abe Lincoln", "dob" : "1809-02-12"}, {"empname" : "Anon I. Muss"}]

print("1")
result = people.insert_many(persons)
print(result)
person_id1 = people.insert_one(person1).inserted_id
print(person_id1)
print(people)
print(person1)
print(person2)
print(persons)
client1.close()
print("5")