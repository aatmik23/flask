from flask import Flask, request, render_template, url_for, redirect, flash, session
app=Flask(__name__)
app.secret_key="mysecretkey"
@app.route("/",methods=["POST","GET"])
def form():
    if request.method == "POST":
      name=request.form.get("name")
      if not name:
         flash('name cannot be empty')
         return redirect(url_for("form"))
      flash(f"thanks {name} your form is submitted")   
      return redirect(url_for('thankyou'))
    return render_template('form.html')
@app.route("/thankyou")
def thankyou():
   return render_template('thankyou.html')
   
      
    # @app.route("/feedback", methods=["POST","GET"])
# def feedback():
#     if request.method=="POST":
#         name=request.form.get("username")
#         message=request.form.get("message")
#         return render_template("thankyou.html",name=name,message=message)
    
    
#     return render_template('feedback.html')
