# WARNING: NOT FOR USE IN PRODUCTION AFTER REAL DATA EXISTS!!!!!!!!!!!!!!!!!!!!!!
'''
This script creates the database tables in the SQLite file. 
Update this file as you update your database.
'''
import os, sys
import importlib
import datetime

# Don't forget to import your own models!
from app.models import *

conf = load_config('app/config.yaml')

sqlite_dbs  = [ conf['databases']['dev']
                # add more here if multiple DBs
              ]

# Remove DBs
for fname in sqlite_dbs:
  try:
    print ("Removing {0}.".format(fname))
    os.remove(fname)
  except OSError:
    pass

# Creates DBs
for fname in sqlite_dbs:
  if os.path.isfile(fname):
    print ("Database {0} should not exist at this point!".format(fname))
  print ("Creating empty SQLite file: {0}.".format(fname))
  open(fname, 'a').close()
  

def class_from_name (module_name, class_name):
  # load the module, will raise ImportError if module cannot be loaded
  # m = __import__(module_name, globals(), locals(), class_name)
  # get the class, will raise AttributeError if class cannot be found
  c = getattr(module_name, class_name)
  return c
    
"""This file creates the database and fills it with some dummy run it after you have made changes to the models pages."""
def get_classes (db):
  classes = []
  for str in conf['models'][db]:
    print ("\tCreating model for '{0}'".format(str))
    c = class_from_name(sys.modules[__name__], str)
    classes.append(c)
  return classes

  
mainDB.create_tables(get_classes('mainDB'))

# Adding dummy data
users = User(  firstName = "Scott",
                lastName  = "Heggen",
                username  = "heggens",
                email     = "heggens@berea.edu",
                isAdmin   = 1,
                program   = 1
             ).save(force_insert=True)

users = User(  firstName = "Matt",
                lastName  = "Jadud",
                username  = "jadudm",
                email     = "jadudm@berea.edu",
                isAdmin   = 0,
                program   = 2
             ).save(force_insert=True)

division = Division(  name = "Division I"
              ).save()

division = Division(  name = "Division II"
              ).save()

program  = Program( name = "Computer Science",
                    division = 2,
                    prefix   = "CSC"
              ).save()
              
program  = Program( name = "Mathematics",
                    division = 1,
                    prefix   = "MAT"
              ).save()
             
subject = Subject(  prefix  = "CSC",
                    pid     = 1,
                    webname = "cs.berea.edu"
                    ).save(force_insert=True)
                    
subject = Subject(  prefix  = "MAT",
                    pid     = 2,
                    webname = "math.berea.edu"
                  ).save(force_insert=True)

banner = BannerSchedule(  letter        = "Standard A",
                          days          = "MWF",
                          startTime     = datetime.time(8, 0, 0),
                          endTime       = datetime.time(9, 10, 0),
                          sid           = "A",
                          order         = 1
                        ).save()

banner = BannerSchedule(  letter        = "Standard B",
                          days          = "MWF",
                          startTime     = datetime.time(9, 20, 0),
                          endTime       = datetime.time(10, 30, 0),
                          sid           = "B",
                          order         = 2
                        ).save()

bannercourse =  BannerCourses(  subject       = "CSC",
                                number        = 236,
                                ctitle        = "Data Structures"
                              ).save()

bannercourse =  BannerCourses(  subject       = "MAT",
                                number        = 135,
                                ctitle        = "Calculus I"
                              ).save()

term = Term(  name              = "Fall 2016",
              termCode          = 201611,
              editable          = 0
            ).save()
            
term = Term(  name              = "Spring 2017",
              termCode          = 201612,
              editable          = 0
            ).save()            

course = Course(  bannerRef         = 1,
                  prefix            = "CSC",
                  term              = 201611,
                  schedule          = 1,
                  capacity          = 20,
                  roomPref          = "Preference1"
                ).save()
                
course = Course(  bannerRef         = 2,
                  prefix            = "MAT",
                  term              = 201612,
                  schedule          = 2,
                  capacity          = 20,
                  roomPref          = "Preference2"
                ).save()                

course = Course(  bannerRef         = 1,
                  prefix            = "CSC",
                  term              = 201612,
                  schedule          = 1,
                  capacity          = 20,
                  roomPref          = "Preference1"
                  ).save()
                  
pchair = ProgramChair(  username  = "heggens",
                        pid       = 1
                    ).save()
                    
pchair = ProgramChair(  username  = "jadudm",
                        pid       = 2
                    ).save()

dchair = DivisionChair( username  = "heggens",
                        did       = 1
                      ).save()
                    
dchair = DivisionChair(  username  = "jadudm",
                        did       = 2
                      ).save()

instructor = InstructorCourse(  username = "heggens",
                                course   = 1
                              ).save()
                              
instructor = InstructorCourse(  username = "jadudm",
                                course   = 2
                              ).save()                              