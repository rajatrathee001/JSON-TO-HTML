from flask import Flask,render_template, request
import os
import logging
from datetime import datetime
import json

app = Flask(__name__)

BASE_PATH = os.getcwd()
UPLOAD_PATH = os.path.join(BASE_PATH,'static/upload/')
OUTPUT_PATH = os.path.join(BASE_PATH,'static/output/')

@app.errorhandler(404)
def error404(error):
    message = "ERROR 404 : Page Not Found !!! ,Please go to the home page and try again "
    return render_template("error.html",message=message)

@app.errorhandler(405)
def error405(error):
    message = "ERROR 405 : Method Not Found !!!"
    return render_template("error.html",message=message)

@app.errorhandler(500)
def error500(error):
    message = 'INTERNAL ERROR 500 : Error occurs in the program !!!'
    return render_template("error.html",message=message)

def current_datetime():
    # datetime object containing current date and time
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string

# def validateJSON(jsonData):
#     try:
#         json.loads(jsonData)
#     except ValueError as err:
#         return False
#     return True

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == "POST":
        upload_file = request.files['file_name']
        filename = upload_file.filename
        print("The filename that has been uploaded = ",filename)
        # Know the extension of filename
        # only .json format
        ext = filename.split('.')[-1]
        print('The extension of the filename = ',ext)
        if ext.lower() in ['json']:
            #saveing the file
            path_save = os.path.join(UPLOAD_PATH,filename)
            upload_file.save(path_save)
            print('File save successfully')
            try:
                with open(path_save) as json_file:
                    data = json.load(json_file)
                    # isvalid =  validateJSON(data)
                    # if (isvalid == True):
                    #     # Print the type of data variable
                    print("Type:", type(data))
                    # Print the data of dictionary
                    print("\n",data)
                    return render_template('index.html',fileupload=True,extension=False,not_validate=False,data=data,file_filename=filename)
                # else:
                    #     error = "The file is not json valid"
                    #     f = open("error_log.txt", "a")
                    #     f.write('\n')
                        
                    #     f.write(str(current_datetime()))

                    #     # writing in the file0
                    #     f.write(str(error))
                    #     # closing the file
                    #     f.close()
                    #     return render_template('index.html',fileupload=False,extension=False,not_validate=True,data=data,file_filename=filename)
            except Exception as Argument:
                logging.exception("\t Error!!, This is not a valid path.\n")
                # creating/opening a file
                f = open("error_log.txt", "a")
                f.write('\n')

                f.write(str(current_datetime()))

                # writing in the file
                f.write(str(Argument))
                # closing the file
                f.close()

                return render_template('index.html',fileupload=False,extension=False,error=Argument,got_error=True)

        else:
            print('use only the extension with .json file')
            return render_template('index.html',extension=True,fileupload=False)
        
    return render_template('index.html',fileupload=False,extension=False,got_error=False,not_validate=False)
    
    
if __name__ == '__main__':
      app.run(debug=True,)