# python-rest

REST webservice in Python that allows to operate over text files.

* Create a text file with some contents stored in a given path.
* Retrieve the contents of a text file under the given path.
* Replace the contents of a text file.
* Delete the resource that is stored under a given path.

Some statistics are provided:

* Total number of files in that folder.
* Average number of alphanumeric characters per text file (and standard deviation) in that folder.
* Average word length (and standard deviation) in that folder. 
* Total number of bytes stored in that folder.

## Environement

Pyhton 3.6

Flask (framework)

## How to use

Postman can be used for interacting with HTTP APIs. Run by default on http://127.0.0.1:5000/ 

### /file
#### POST: 
* path, name: create a text file with some contents stored in a given path
#### GET: 
* path: retrieve the contents of a text file under the given path
#### PUT: 
* path_file, path_content: replace the contents of a text file
#### DELETE:
* path: delete the resource that is stored under a given path

### / statistics
#### GET:
* stat = 1: total number of files in that folder
* stat = 2: average number of alphanumeric characters per text file (and standard deviation) in that folder
* stat = 3: average word length (and standard deviation) in that folder
* stat = 4: total number of bytes stored in that folder


## Example

GET request:

```
127.0.0.1:5000/statistics?path=.&stat=3
```
This request results in:
```
AVERAGE WORD LENGTH: 
MEAN: 6.5
STANDARD DEVIATION: 5.16
```

## Built With

* [Flask](http://flask.pocoo.org/) - The web framework used
