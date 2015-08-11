from general import files
import os
import shutil


class Action(object): # Herencia en python
    
    def __init__(self, name, folder):
        self.name = name
        self.folder = folder
        self.path = self.folder + os.sep + self.name
        
    def get_name(self):
        return self.name
    
    def set_name(self, name):
        self.name = name
    
    def get_folder(self):
        return self.folder
    
    def get_path(self):
        return self.path
    
    def perform_action(self, sender):
        raise Exception("NotImplementedException")
    
    def to_string(self):
        raise Exception("NotImplementedException")




class MakeResponse(Action):

    def __init__(self, name, size, folder):
        Action.__init__(self, name, folder)
        self.size = size

    def get_size(self):
        return self.size

    def perform_action(self, sender):
        '''
        create file locally and in the remove host
        :param sender:
        :param path:
        :return:
        '''
        try:
            files.create_named_file(self.size, self.path)
            sender.send(self.path)
        except Exception as e:
            print e
        return self.size

    def to_string(self):
        return "MakeResponse "+str(self.name)+" "+str(self.size) + "\n"




class PutContentResponse(Action):
    def __init__(self, name, modifications, folder):
        Action.__init__(self, name, folder)
        self.modifications = modifications

    def get_modifications(self):
        return self.modifications

    def perform_action(self, sender):
        modificated_bytes = 0
        for modification in self.modifications:
            byte_start = modification[0]
            byte_end = modification[1]

            if byte_start == 0 or byte_start == -1:
                diff = byte_end
            else:
                diff = byte_end - byte_start
            try:
                files.modify_file(self.path, byte_start, diff)
            except Exception as e:
                print e.message

            modificated_bytes += diff
        try:
            sender.send(self.path)
        except Exception as e:
            print e
        return modificated_bytes

    def to_string(self):
        description = "UPDATE "+str(self.name)+" "
        for modification in self.modifications:
            description += str(modification[0]) + " " + str(modification[1]) + " "

        description += "\n"
        return description



class Unlink(Action):

    def __init__(self, name, folder):
        Action.__init__(self, name, folder)

    def perform_action(self, sender):
        '''
        Perform a remove action deleting the file from the FS
        and from the FTP.
        Return: 0 as no bytes are added or modified
        '''
        try:
            sender.delete(self.name)
            os.remove(self.folder+os.sep+self.name)
        except Exception as e:
            print e.message
        return 0

    def to_string(self):
        return "Unlink "+str(self.name)+"\n"


class MoveResponse(Action):

    def __init__(self, name, dst, folder):
        Action.__init__(self, name, folder)
        self.dst = dst

    def perform_action(self, sender):
        '''
        Perform a remove action deleting the file from the FS
        and from the FTP.
        Return: 0 as no bytes are added or modified
        '''
        try:
            sender.mv(self.name, self.dst)
        except Exception as e:
            print e.message
        try:
            shutil.move(self.folder+self.name, self.dst)
        except Exception as e:
            print e.message
        return 0

    def to_string(self):
        return "MoveResponse "+str(self.name)+"\n"


class GetContentResponse(Action):
    def __init__(self, name, dst, folder):
        Action.__init__(self, name, folder)
        self.dst = dst

    def perform_action(self, sender):
        try:
            sender.get('RETR %s' % self.name, open(self.dst+self.name, 'wb').write)
        except Exception as e:
            print e.message
        print 'Perform Action'

    def to_string(self):
        return "GetContentResponse "+str(self.name)+"\n"





def get_action(args, folder):
    
    action_str = args[0]
    name = args[1]
    print action_str

    if action_str == "MakeResponse":
        size = int(args[2])
        action = MakeResponse(name, size, folder)
    elif action_str == "GetContentResponse":
        dst = args[2]
        action = GetContentResponse(name, dst, folder)
    elif action_str == "PutContentResponse":
        updates = []
        modifications = args[2]
        i = 0
        while i < len(modifications):
            start = int(modifications[i])
            end = int(modifications[i+1])
            updates.append((start, end))
            i += 2
        action = PutContentResponse(name, updates, folder)
    elif action_str == "Unlink":
        action = Unlink(name, folder)
    elif action_str == "MoveResponse":
        tgt = args[2]
        action = MoveResponse(name, tgt, folder)
    else:
        print 'Action Not Found!'
    return action
        
### ------------------------- ###
### ------------------------- ###
if __name__ == '__main__':
    print 'This is the main Program'