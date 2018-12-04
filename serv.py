from flask import Flask, request
import os
import json
import re
import numpy as np

def nbrecur(pathaccess, number):
    if len(os.listdir(pathaccess)) == 0:
        return number
    else:
        if len(os.listdir(pathaccess)) == len([name for name in os.listdir(pathaccess) if os.path.isfile(pathaccess + '/' + name)]):
            number += len(os.listdir(pathaccess))
            return number
        else:
            for name in os.listdir(pathaccess):
                if os.path.isfile(pathaccess + '/' + name):
                    number += 1
                else:
                    return nbrecur(pathaccess + '/' + name, number)

def bytesrecur(pathaccess, number):
    if len(os.listdir(pathaccess)) == 0:
        return number
    else:
        if len(os.listdir(pathaccess)) == len([name for name in os.listdir(pathaccess) if os.path.isfile(pathaccess + '/' + name)]):
            for name in os.listdir(pathaccess):
                number += os.path.getsize(pathaccess + '/' + name)
            return number
        else:
            for name in os.listdir(pathaccess):
                if os.path.isfile(pathaccess + '/' + name):
                    number += os.path.getsize(pathaccess + '/' + name)
                else:
                    return bytesrecur(pathaccess + '/' + name, number)
     
def listrecur(pathaccess, liststock):
    if len(os.listdir(pathaccess)) == 0:
        return liststock
    else:
        if len(os.listdir(pathaccess)) == len([name for name in os.listdir(pathaccess) if os.path.isfile(pathaccess + '/' + name)]):
            for name in os.listdir(pathaccess):
                with open(pathaccess + '/' + name, 'r') as f:
                    file_content = f.read()
                    file_alpha_num = re.sub(r'[^a-zA-Z]', "", file_content)
                    liststock.append(len(file_alpha_num))
            return liststock
        else:
            for name in os.listdir(pathaccess):
                if os.path.isfile(pathaccess + '/' + name):
                    with open(pathaccess + '/' + name, 'r') as f:
                        file_content = f.read()
                        file_alpha_num = re.sub(r'[^a-zA-Z]', "", file_content)
                        liststock.append(len(file_alpha_num))
                else:
                    return listrecur(pathaccess + '/' + name, liststock)


def listwordrecur(pathaccess, liststock):
    if len(os.listdir(pathaccess)) == 0:
        return liststock
    else:
        if len(os.listdir(pathaccess)) == len([name for name in os.listdir(pathaccess) if os.path.isfile(pathaccess + '/' + name)]):
            for name in os.listdir(pathaccess):
                with open(pathaccess + '/' + name, 'r') as f:
                    file_content = f.read()
                    file_alpha_num = re.sub(r'([^\s\w]|_)+', '', file_content)
                    for x in file_alpha_num.split():
                        liststock.append(len(x))
            return liststock
        else:
            for name in os.listdir(pathaccess):
                if os.path.isfile(pathaccess + '/' + name):
                    with open(pathaccess + '/' + name, 'r') as f:
                        file_content = f.read()
                        file_alpha_num = re.sub(r'([^\s\w]|_)+', '', file_content)
                        for x in file_alpha_num.split():
                            liststock.append(len(x))
                else:
                    return listwordrecur(pathaccess + '/' + name, liststock)


app = Flask(__name__)

#Create a text file with some contents stored in a given path
@app.route('/file', methods=['POST'])
def createfile():
    path = request.form['path']
    name = request.form['name'] 
    with open(path, 'r') as f:
        file_content = f.read()
    with open(name, 'w') as write_file:
        json.dump(file_content, write_file)
    return name + 'CREATED'
 
#Retrieve the contents of a text file under the given path
@app.route('/file', methods=['GET'])
def getfile():
    path = request.args.get('path')
    with open(path, 'r') as f:
        file_content = f.read()
    return file_content

#Replace the contents of a text file
@app.route('/file', methods=['PUT'])
def replacefile():
    path = request.form['path_file']
    content = request.form['path_content']
    
    with open(content, 'r') as f_cont:
        file_content = f_cont.read()
    
    with open(path, 'r+') as f:
        f.truncate(0)
        f.write(file_content)
    return 'CONTENT TAKEN FROM ' + path + ' TO ' + content 

#Delete the resource that is stored under a given path
@app.route('/file', methods=["DELETE"])
def deletefile():
    path = request.form['path']
    os.remove(path)
    return path + 'DELETED'


@app.route('/statistics', methods=['GET'])
def statistics():
    path = request.args.get('path')
    stat = request.args.get('stat')
    
    if stat == '1': #Total number of files in that folder
        nb_file = nbrecur(path, 0)
        return 'NUMBER OF FILES: ' + str(nb_file)

    if stat == '2': #Average number of alphanumeric characters per text file (and standard deviation) in that folder
        list_len = listrecur(path, [])
        mean = np.mean(list_len)
        standard_dev = np.std(list_len)
        return 'NUMBER OF ALPHANUMERIC CHARACTERS PER TEXT FILE: \n' + 'MEAN: '+ str(round(mean,2)) + '\n' + 'STANDARD DEVIATION: ' + str(round(standard_dev,2))

    if stat == '3': #Average word length (and standard deviation) in that folder
        list_len = listwordrecur(path, [])
        mean = np.mean(list_len)
        standard_dev = np.std(list_len)
        return 'AVERAGE WORD LENGTH: \n' + 'MEAN: '+ str(round(mean,2)) + '\n' + 'STANDARD DEVIATION: ' + str(round(standard_dev,2))

    if stat == '4': #Total number of bytes stored in that folder
        size = bytesrecur(path, 0)
        return 'TOTAL NUMBER OF BYTES: ' + str(size)

if __name__ == '__main__':
    app.run()