#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

#-------------------------------------------------------------------------------
# Produce random files
#-------------------------------------------------------------------------------
#from PIL import Image
import numpy
import uuid
import array
import os

import random, tempfile
#from bzrlib.plugins.bash_completion.bashcomp import BashCodeGen

word_list = []

#-------------------------------------------------------------------------------
# reads the word list to use for the 'readable' text tests
#-------------------------------------------------------------------------------
def prepare_word_list():
    # Word list from FreeBSD Dict
    f = open("wordlist", "r")
    for line in f:
        word_list.append(line.strip())

#-------------------------------------------------------------------------------
# create a valid but random image (jpeg or png)
#-------------------------------------------------------------------------------
def get_image(size, extension):
    fsize = 0
    fname = os.path.join(tempfile.gettempdir(), \
        '%s.%s' % (str(uuid.uuid4()), extension))

    # This will give a max JPEG of few mega
    x_max = 3500
    x_min = 0

    while x_max >= x_min:
        # Mid of the interval
        x = 1.0 * (x_max + x_min) / 2

        # save the image
        a = numpy.random.rand(x,x,3) * 255
        image_out = Image.fromarray(a.astype('uint8')).convert('RGBA')
        image_out.save(fname)
        fsize = os.path.getsize(fname)

        # lets go on binary search for the size
        diff = (1.0 * (fsize - size)/ size)
        if abs(diff) > 0.01 and diff > 0:
            x_max = x
        elif abs(diff) > 0.01 and diff < 0:
            x_min = x
        elif x_max - x_min <= 2.0:
            break
        else:
            break
            # got it!
    return fname

#-------------------------------------------------------------------------------
# Produces a random text from the word_list given the size in bytes.
# Returns exactly this amount of bytes.
#-------------------------------------------------------------------------------
def get_text(size):
    t = ""
    while len(t) < size:
        t += random.choice(word_list)
        # We want to read the text :)
        if random.random() > 0.1:
            t +=  " "
        else:
            t += "\r\n"
    t = t[0:size]
    return t

#-------------------------------------------------------------------------------
# Prepare the file for the test given size and the file type
#-------------------------------------------------------------------------------
def get_file(size, file_type):
    if file_type == 1:
        # put random data in the file -- call it a gzip
        rand_bytes = bytearray(random.getrandbits(8) for _ in range(size-2))
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".gz")
        fname = tfile.name
        tfile.write(array.array('B', "1f8b".decode("hex")))
        tfile.write(rand_bytes)
        tfile.close()
        return fname

    elif file_type == 2:
        # put a readable text in the file
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
        fname = tfile.name
        tfile.write(get_text(size))
        tfile.close()
        return fname

    elif file_type == 3:
        # put a valid jpeg image with random pixels
        return get_image(size, "jpeg")

    elif file_type == 4:
        # create a file with magic number of jpeg, jpeg extension,
        # but only normal text afterward
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".jpeg")
        fname = tfile.name
        tfile.write(array.array('B', "ffd8ffe0".decode("hex")))
        tfile.write(get_text(size-4))
        tfile.close()
        return fname
    elif file_type == 5:
        # Create plain text file from SDGen characterization
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".tar")
        fname = tfile.name
        tfile.close()
        bashCommand = "java -jar ./general/data_generator/DatasetGenerator.jar -c ./general/data_generator/characterization.ser -d "+str(fname)+" -s 14428160"
        os.system(bashCommand)
        return fname
    
def create_named_file(size, file_path):
    # put random data in the file -- call it a gzip
    rand_bytes = bytearray(random.getrandbits(8) for _ in range(size-2))
    with open(file_path, 'w+b') as f:
        f.write(array.array('B', "1f8b".decode("hex")))
        f.write(rand_bytes)
        f.close()
        
def modify_file(file_path, starting_point, num_bytes):
    
    rand_bytes = bytearray(random.getrandbits(8) for _ in range(num_bytes))
    
    if starting_point == 0: # Prepend
        with tempfile.TemporaryFile() as f:
            f.write(rand_bytes)
            f.write(open(file_path).read())
            f.seek(0)
            dest_file = open(file_path, 'wb+')
            dest_file.write(f.read())
            dest_file.close()
    elif starting_point == -1: # Append
        with open(file_path, 'ab+') as dest_file:
            dest_file.write(rand_bytes)  
    else: # Modification in the middle
        with open(file_path, 'r+b') as dest_file:
            dest_file.seek(starting_point)
            dest_file.write(rand_bytes)
            dest_file.close()
            
def add_content_file(file_path, starting_point, num_bytes):
    
    rand_bytes = bytearray(random.getrandbits(8) for _ in range(num_bytes))
    
    with open(file_path, 'r+b') as dest_file:
        dest_file.seek(starting_point)
        final_content = dest_file.read()
        dest_file.seek(starting_point)
        dest_file.write(rand_bytes)
        dest_file.write(final_content)
        dest_file.close()
    
#-------------------------------------------------------------------------------
# start-up the dictionary
#-------------------------------------------------------------------------------
#prepare_word_list()
