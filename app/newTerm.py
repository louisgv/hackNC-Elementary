from allImports import *
from switch import *
@app.route("/newTerm", methods=["POST"])
def newterm():
  page        = request.path  
  username    = authUser(request.environ)
  admin       = User.get(User.username == username)
  try: 
    if admin.isAdmin:
      #BASIC DATA
      data            = request.form
      info_key        = int(data['keyValue'])
      term_year       = data['year']
      same_year       = [11]
      semester_name   = cfg['termInfo'][info_key]   #USE THE VALUE OF THE POST TO GET THE NAME
      term_name       = semester_name + " " + term_year
      #LOOK AT CONFIG.YAML ANY KEY THAT REQUIRES THE SAME YEAR FOR THE TERM CODE PLACE INSIDE THE same_year LIST
      for x in same_year:
        if info_key == x:
          term_code = term_year + str(info_key)
        else:
          term_code = str(int(term_year)-1) + str(info_key)
      
      
      #STOP DUPLICATES#
      #I NEED TO ENSURE THAT THE TERM CODE DOES NOT ALREADY EXSIST IN THE DATABASE
      
      
      newTerm = Term(termCode=int(term_code), name=term_name, semester=semester_name, year=int(term_year), editable = True)
      newTerm.save(force_insert=True)
      
      
  except Exception as e:
    log.writer("ERROR","newTerm",e)
  message = "Term: Term {} has been created".format(data['year'])
  log.writer("INFO", page, message)
  flash("Term successfully created")
  return redirect(url_for("systemManagement"))