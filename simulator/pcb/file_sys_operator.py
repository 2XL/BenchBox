


class Node():
    def __init__(self, name):
        self.name = name


class File(Node):
    def __init__(self, name):
        print 'file'
        self.name = name


class Folder(Node):
    def __init__(self, name, path):
        print 'folder'
        self.name = name
        self.path = path
        self.childs = list()

class FileSysOperator():



    def __init__(self):
        print 'Constructor'
        self.localFS = list() # linkedlist of localfs folders


    def generateFS(self):
        print 'gen initial FS'

    def createFile(self, args = {}):
        print 'create a file...'


    def moveFile(self, args = {}):
        print 'move a file...'