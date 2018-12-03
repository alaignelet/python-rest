from flask import Flask, request
import os
import json
import re
import numpy as np

app = Flask(__name__)

#Create a text file with some contents stored in a given path
@app.route("/file", methods=["POST"])
def createfile():
    path = request.form["path"]
    path_new = request.form["path_new"]
    with open(path, 'r') as f:
        file_content = f.read()
    with open(path_new, "w") as write_file:
        json.dump(file_content, write_file)
    return "JSON FILE CREATED"

#Retrieve the contents of a text file under the given path
@app.route("/file", methods=["GET"])
def getfile():
    path = request.args.get('path')
    with open(path, 'r') as f:
        file_content = f.read()
    return 'FILE CONTENT: \n' + file_content

#Replace the contents of a text file
@app.route("/replacecontent", methods=["POST"])
def replacefile():
    path = request.form["path_file"]
    content = request.form["path_content"]
    
    with open(content, 'r') as f_cont:
        file_content = f_cont.read()
    
    with open(path, 'r+') as f:
        f.truncate(0)
        f.write(file_content)
    return "CONTENT REPLACED"

#Delete the resource that is stored under a given path
@app.route("/file", methods=["DELETE"])
def deletefile():
    path = request.form["path"]
    os.remove(path)
    return "FILE DELETED"


@app.route("/statistics", methods=["GET"])
def statistics():
    path = request.args.get('path')
    stat = request.args.get('stat')
    
    if stat == '1': #Total number of files in that folder
        return 'NUMBER OF FILES: \n' + str(len(os.listdir(path)))

    if stat == '2': #Average number of alphanumeric characters per text file (and standard deviation) in that folder
        list_len = []
        for file in os.listdir(path):
            file = path + '/' + file
            with open(file, 'r') as f:
                file_content = f.read()
            file_alpha_num = re.sub(r'[^a-zA-Z]', "", file_content)
            list_len.append(len(file_alpha_num))
            mean = np.mean(list_len)
            standard_dev = np.std(list_len)
        return 'NUMBER OF ALPHANUMERIC CHARACTERS PER TEXT FILE: \n' + 'MEAN: '+ str(round(mean,2)) + '\n' + 'STANDARD DEVIATION: ' + str(round(standard_dev,2))

    if stat == '3': #Average word length (and standard deviation) in that folder
        list_len = []
        for file in os.listdir(path):
            file = path + '/' + file
            with open(file, 'r') as f:
                file_content = f.read()
            file_alpha_num = re.sub(r'([^\s\w]|_)+', '', file_content)
            for x in file_alpha_num.split():
                list_len.append(len(x))
            mean = np.mean(list_len)
            standard_dev = np.std(list_len)
        return 'AVERAGE WORD LENGTH: \n' + 'MEAN: '+ str(round(mean,2)) + '\n' + 'STANDARD DEVIATION: ' + str(round(standard_dev,2))

    if stat == '4': #Total number of bytes stored in that folder
        list_size = []
        for file in os.listdir(path):
            file = path + '/' + file
            list_size.append(os.path.getsize(file))
            mean = np.mean(list_size)
            standard_dev = np.std(list_size)
        return 'TOTAL NUMBER OF BYTES: \n' + 'MEAN: '+ str(round(mean,2)) + '\n' + 'STANDARD DEVIATION: ' + str(round(standard_dev,2))

if __name__ == '__main__':
    app.run()