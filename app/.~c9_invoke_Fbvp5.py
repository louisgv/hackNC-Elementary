from allImports import *

@app.route("/redirect", methods=["GET"])
def redirectCourses():
   username = user.
   user = User.get(User.username == username)
   
   if user.program != 0 and user.program is not None:
      program = user.program
   else:
      program = Program.get()
      
   print program.pID
   
   return "hello"
