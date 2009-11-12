#!/usr/bin/python
import sys, os
sys.path.append(os.getcwd()[:os.getcwd().find('src')])

import sqlobject as s
import src.model as m

databasename = "pictureresource.db"
connectionString = 'sqlite:%s/%s' % (os.getcwd(), databasename)
connection = s.connectionForURI(connectionString)
s.sqlhub.processConnection = connection

picts = m.Painting.select(m.Painting.q.filepath <> None)
print picts
print list(picts)
