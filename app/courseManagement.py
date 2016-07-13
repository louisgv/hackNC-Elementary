# ADD ANY IMPORTS HERE
from allImports import *
from updateCourse import DataUpdate
from app.logic.databaseInterface import createInstructorDict
from app.logic.functions import doesConflict
conflicts = load_config(os.path.join(here, 'conflicts.yaml'))
import pprint

#CROSS LISTED COURSES#

@app.route("/courseManagement/crossListed/", defaults={'tid':0}, methods=["GET", "POST"])
@app.route("/courseManagement/crossListed/<tid>", methods = ["GET","POST"])
def crossListed(tid):
    # DATA FOR THE NAVBAR AND SIDE BAR
    terms = Term.select().order_by(-Term.termCode)
    if tid == 0:
        counter = 0
        for term in terms:
            if counter == 0:
                tid = term.termCode
            counter += 1
    page = "crossListed"
    username = authUser(request.environ)
    admin = User.get(User.username == username)
    ##DATA FOR THE CROSS LISTED COURSE TABLE##
    crossListedCourses = Course.select().where(Course.crossListed == 1).where(
        Course.term == tid).order_by(+Course.schedule).order_by(+Course.rid)
        
    instructors = createInstructorDict(crossListedCourses)
    
    ##DATA FOR THE ADD COURSE FORM##
    courseInfo = BannerCourses.select().order_by(
        BannerCourses.number).order_by(
        BannerCourses.subject)
    users = User.select(User.username, User.firstName, User.lastName)
    schedules = BannerSchedule.select()
    rooms = Rooms.select()
    return render_template("crossListed.html",

                           cfg=cfg,
                           isAdmin=admin.isAdmin,
                           allTerms=terms,
                           page=page,
                           currentTerm=int(tid),
                           courses=crossListedCourses,
                           instructors=instructors,
                           courseInfo=courseInfo,
                           users=users,
                           schedules=schedules,
                           rooms=rooms
                           )
#############################
#SCHEDULE AND ROOM CONFLICTS#
#############################


@app.route("/courseManagement/conflicts/<tid>", methods=["GET"])

def conflictsListed(tid):
    #DATA FOR THE NAVEBAR AND SIDEBAR#
    page = "conflicts"
    terms = Term.select().order_by(-Term.termCode)
    username = authUser(request.environ)
    admin = User.get(User.username == username)
    #DATA FOR THE ROOM AND SCHEDULING CONFLICTS#
    #CREATE A CONFLICT DICTIONARY TO HOLD ALL OF THE CONFLICTS
    conflict_dict = dict()  
    #THE KEY WILL BE BUILDING NAMES
    #THE VALUE WILL BE A LIST OF COURSE OBJECTS THAT CONFLICT
    #STORE THE DICT KEYS SO WE CAN EASILY LOOP THROUGH THEM ON THE VIEW
    dict_keys = []          
    # GRAB ALL OF THE DISTINCT BUILDING NAMES
    buildings = Rooms.select(Rooms.building).distinct()               
    # LOOP THROUGH ELEMENTS IN THE QUERY
    for element in buildings:
      # RESET THE BUIDLING CONFLICTS
      buildingConflicts = []                                          
      # GET ALL OF THE ROOMS FOR THAT BUILDING
      rooms = Rooms.select().where(Rooms.building==element.building)  
      for room in rooms:
          #WE NEED TO CREATE A LIST SO THAT WE CAN SORT OUT THE 'ZZZ' SCHEDULE AND SO THAT WE CAN POP() FROM THE LIST      
          courseList = [] 
          courses = Course.select().where(room.rID == Course.rid, Course.term == tid).order_by(Course.rid) 
          if courses:           
              for course in courses:
                  #DON'T ADD 'ZZZ' TO COURSE LIST BECAUSE ITS NOT PRESENT IN CONFLICTS.YAML 
                  if course.schedule != "ZZZ":         
                      #APPEND THE COURSE OBJECT TO THE COURSELIST FOR SCHEDULE CHECKING
                      courseList.append(course)        
                  #THEN WE GO AHEAD AND APPEND THE COURSE OBJECT FOR 'ZZZ' SCHEDULES TO CONFLICTS
                  else:                                
                      #BECAUSE THEY HAVE SPECIAL TIME ENTRIES THAT NEEED TO BE CHECKED MANUALLY
                      buildingConflicts.append(course) 
              while courseList != []: 
                  current_course = courseList.pop()
                  #CHECK TO SEE IF NOW EMPTY ==> NEEDED TO PREVENT SEG FAULT
                  if courseList != []:                 
                    for course in courseList:
                      if course.schedule is not None and current_course.schedule is not None:
                        #ACCESS THE SID THROUGH THE COURSE OBJECT
                        if doesConflict(current_course.schedule.sid, course.schedule.sid):
                          #APPEND BOTH COURSE OBJECTS TO THE CONFLICTS LIST
                          buildingConflicts.append(current_course) 
                          buildingConflicts.append(course)         
      if buildingConflicts != []:
        #REMOVE DUPLICATE COURSE OBJECTS FROM THE CONFLICTS LIST
        seen = set()
        seen_add = seen.add
        buildingConflicts = [x for x in buildingConflicts if not (x in seen or seen_add(x))]
        #ADD THE KEY TO THE LIST
        dict_keys.append(element.building)                      
        #SET THE KEY(building name) TO THE VALUE(list of course objects)
        conflict_dict[element.building] = buildingConflicts     
        #DATA FOR THE CONFLICTS TABLE
        instructors = createInstructorDict(buildingConflicts)
    return render_template("conflicts.html",
                           cfg=cfg,
                           isAdmin=admin.isAdmin,
                           allTerms=terms,
                           page=page,
                           currentTerm=int(tid),
                           conflicts_dict=conflict_dict,
                           dict_keys=dict_keys,
                           instructors=instructors
                           )
################
#CHANGE TRACKER#
################


@app.route("/courseManagement/tracker/<tid>", methods=["GET"])
def trackerListed(tid):
    # DATA FOR THE NAVBAR AND SIDE BAR
    page = "tracker"
    terms = Term.select().order_by(-Term.termCode)
    username = authUser(request.environ)
    admin = User.get(User.username == username)
    # DATA FOR THE CHANGE TRACKER PAGE
    # ALL OF THIS CAME FROMT HE COURSECHANGE.PY
    if (request.method == "GET"):
        username = authUser(request.environ)
        admin = User.get(User.username == username)
        if admin.isAdmin:
            courses = CourseChange.select().where(CourseChange.verified == False)
            pprint.pprint(courses)
            classDict = dict()
            instructorsDict = dict()
            for course in courses:
                instructorsDict[course.cId] = InstructorCourseChange.select().where(
                    InstructorCourseChange.course == course.cId)
                tdClass = course.tdcolors
                tdClassList = tdClass.split(",")
                classDict[course.cId] = tdClassList
        '''
      DATA STRUCTURES
      NOTE: The keys for both dictionaries the course identification number
        classDict[cId] = [className,className,className,className,className]
        *Then it will return a list of classnames that can be accessed through an index

        instructorsDict[cid] = intructorCourseChange peewee object
      '''
        return render_template("tracker.html",
                               cfg=cfg,
                               isAdmin=admin.isAdmin,
                               allTerms=terms,
                               page=page,
                               currentTerm=int(tid),
                               courses=courses,
                               instructorsDict=instructorsDict,
                               classDict=classDict
                               )
    else:
        return render_template("404.html", cfg=cfg)


@app.route("/courseManagement/tracker/<tid>/verified", methods=["POST"])
def verifyChange(tid):
    if (request.method == "POST"):
        page = "/" + request.url.split("/")[-1]
        username = authUser(request.environ)
        admin = User.get(User.username == username)
        if admin.isAdmin:
            data = request.form
            verify = DataUpdate()
            verify.verifyCourseChange(data)
            message = "Course Change: {0} has been verified".format(data['id'])
            log.writer("INFO", page, message)
            flash("Your course has been marked verified")
            return url_for("/courseManagement/tracker/<tid>")
