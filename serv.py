from flask import Flask, request, abort
import os
import json
import re
import numpy as np
import glob

app = Flask(__name__)


def invalid(path):
    return  path.startswith('/') or '..' in path

# Create a text file with some contents stored in a given path
@app.route('/file', methods=['POST'])
def createfile():
    path = request.form['path']
    name = request.form['name']
    if invalid(path)  or invalid(name):
        abort(403)

    if os.path.isfile(path):
        with open(path, 'r') as f:
            file_content = f.read()
        with open(name, 'w') as write_file:
            json.dump(file_content, write_file)
        return name
    else:
        abort(404)


# Retrieve the contents of a text file under the given path
@app.route('/file', methods=['GET'])
def getfile():
    path = request.args.get('path')
    if invalid(path):
        abort(403)

    if os.path.isfile(path):
        with open(path, 'r') as f:
            file_content = f.read()
        return file_content
    else:
        abort(404)


# Replace the contents of a text file
@app.route('/file', methods=['PUT'])
def replacefile():
    path = request.form['path_file']
    content = request.form['path_content']
    if invalid(path) or invalid(content):
        abort(403)

    if os.path.isfile(path) & os.path.isfile(content):
        with open(content, 'r') as f_cont:
            file_content = f_cont.read()

        with open(path, 'r+') as f:
            f.truncate(0)
            f.write(file_content)
        return path
    else:
        abort(404)


# Delete the resource that is stored under a given path
@app.route('/file', methods=["DELETE"])
def deletefile():
    path = request.form['path']
    if invalid(path):
        abort(403)

    if os.path.isfile(path):
        os.remove(path)
        return path
    else:
        abort(404)


@app.route('/statistics', methods=['GET'])
def statistics():
    path = request.args.get('path')
    stat = request.args.get('stat')
    if invalid(path):
        abort(403)

    if os.path.isdir(path):
        list_total = glob.glob(path + '/**/*', recursive=True)
        list_file = [name for name in list_total if os.path.isfile(name)]

        if stat == 'total_number_files':  # Total number of files in that folder
            nb_file = len(list_file)
            return 'NUMBER OF FILES: ' + str(nb_file)

        if stat == 'average_number_char':  # Average number of alphanumeric characters per text file (and standard deviation) in that folder
            list_len = []
            for file in list_file:
                with open(file, 'r') as f:
                    file_content = f.read()
                    file_alpha_num = re.sub(r'[^a-zA-Z]', "", file_content)
                    list_len.append(len(file_alpha_num))
            mean = np.mean(list_len)
            standard_dev = np.std(list_len)
            return 'NUMBER OF ALPHANUMERIC CHARACTERS PER TEXT FILE: \n' + 'MEAN: ' + str(
                round(mean, 2)) + '\n' + 'STANDARD DEVIATION: ' + str(round(standard_dev, 2))

        if stat == 'average_word_length':  # Average word length (and standard deviation) in that folder
            list_len = []
            for file in list_file:
                with open(file, 'r') as f:
                    file_content = f.read()
                    file_alpha_num = re.sub(r'([^\s\w]|_)+', '', file_content)
                    for x in file_alpha_num.split():
                        list_len.append(len(x))
            mean = np.mean(list_len)
            standard_dev = np.std(list_len)
            return 'AVERAGE WORD LENGTH: \n' + 'MEAN: ' + str(round(mean, 2)) + '\n' + 'STANDARD DEVIATION: ' + str(
                round(standard_dev, 2))

        if stat == 'total_number_bytes':  # Total number of bytes stored in that folder
            size = 0
            for file in list_file:
                size += os.path.getsize(file)
            return 'TOTAL NUMBER OF BYTES: ' + str(size)

    else:
        abort(404)


if __name__ == '__main__':
    app.run()
