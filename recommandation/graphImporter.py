from neo4j.v1 import GraphDatabase
from pymongo import MongoClient
import bson
import sys

# connector Neo4j
driver = GraphDatabase.driver("bolt://localhost:7687", auth=('neo4j','neo'))
#connector mongodb
client = MongoClient('localhost',27017)
db = client['github']



def addRepo(tx,repo_name, language):
   if language:
       tx.run("MERGE (a:Repo {repo_name: $repo_name}) ON CREATE SET a.language= $language", repo_name=repo_name, language=language)
   else:
       tx.run("MERGE (a:Repo {repo_name: $repo_name})", repo_name=repo_name)

def addRelationOwner(tx, repo_name, name):
    tx.run("MATCH (u:Actor { login: $name }),(rn:Repo { repo_name: $repo_name }) MERGE (u)-[r:OWNER]->(rn)", name=name, repo_name=repo_name)

def addRelationFollower(tx,repo_name,name):
   tx.run("MATCH (u:Actor { login: $name }),(rn:Repo { repo_name: $repo_name }) MERGE (u)-[r:FOLLOW]->(rn)", name=name, repo_name=repo_name)

def addRelationStar(tx,repo_name,name):
   tx.run("MATCH (u:Actor { login: $name }),(rn:Repo { repo_name: $repo_name }) MERGE (u)-[r:STAR]->(rn)", name=name, repo_name=repo_name)

def addActor(tx, login):
    tx.run("MERGE (u:Actor {login : $login})", login=login)

def addRelationWorker(tx,repo_name,name):
   tx.run("MATCH (u:Actor { login: $name }),(rn:Repo { repo_name: $repo_name }) MERGE (u)-[r:WORK]->(rn)", name=name, repo_name=repo_name)

def addPropertiesStar(tx,repo_name, stars):
    tx.run("MATCH (a:Repo {repo_name: $repo_name}) SET a.stars= $stars", repo_name=repo_name, stars=stars)

with driver.session() as session:

    #get repository
    cursor = db.archives.aggregate_raw_batches([
        #{ '$match': {'repo.name':'Automattic/wp-calypso'}},
        { '$group': { '_id': {'repo':'$repo.name' ,'language':'$payload.pull_request.base.repo.language'} } },
        { '$sample': { 'size': 10}},
        { '$project': {'_id':1}}])
    for batch in cursor:
        repos = bson.decode_all(batch)
    for repo in repos:
        session.write_transaction(addRepo, repo['_id']['repo'], repo['_id']['language'] if len(repo['_id']) > 1 else '')
        #get users
        cursor = db.archives.aggregate_raw_batches([
            {'$match': {'repo.name':repo['_id']['repo']}},
            {'$group': { '_id': {'actor': '$actor.login'}}},
            {'$project': {'_id':1}}])
        for batch in cursor:
            actors = bson.decode_all(batch)
        for actor in actors:
            session.write_transaction(addActor, actor['_id']['actor'])
        #get repository's owners
        #cursor = db.archives.aggregate_raw_batches([
        #    { '$match' : {'type':'CreateEvent', 'repo.name':'Automattic/wp-calypso' }},
        #    { '$group': { '_id': {'actor': '$actor.login', 'repo':'$repo.name'}}},
        #    { '$project' : {'_id':1}}])
        #for batch in cursor:
        #    owners = bson.decode_all(batch)
        # get workers on repository
        cursor = db.archives.aggregate_raw_batches([
            { '$match' : {'type':'PushEvent', 'repo.name':repo['_id']['repo']}},
            { '$group': { '_id': {'actor': '$actor.login', 'repo':'$repo.name'}}},
            { '$project' : {'_id':1}}])
        for batch in cursor:
            workers = bson.decode_all(batch)
        for work in workers:
            session.write_transaction(addRelationWorker, work['_id']['repo'], work['_id']['actor'])

        cursor = db.archives.aggregate_raw_batches([
            { '$match' : {'type':'WatchEvent', 'repo.name':repo['_id']['repo'] }},
            { '$group': { '_id': {'actor': '$actor.login', 'repo':'$repo.name'}}},
            { '$project' : {'_id':1}}])
        for batch in cursor:
            likers = bson.decode_all(batch)
        for like in likers:
            session.write_transaction(addRelationStar, like['_id']['repo'], like['_id']['actor'])
        #get who stars repository
        cursor = db.archives.aggregate_raw_batches([
            { '$match' : {'type':'WatchEvent', 'repo.name':repo['_id']['repo'] }},
            { '$group': { '_id':'$repo.name', 'stars' :{'$sum':1} }},
            { '$project' : {'_id':1,'stars':1}}])
        for batch in cursor:
            stars = bson.decode_all(batch)
        for star in stars:
            session.write_transaction(addPropertiesStar, star['_id'], star['stars'])
        
        #for owner in owners:
        #    session.write_transaction(add_owner, owner['_id']['repo'], owner['_id']['user'])
