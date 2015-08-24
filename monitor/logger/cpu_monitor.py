
__author__ = 'Anna'

import psutil # python system and process utilities




print "This line will be printed."

def main(argv=None):
    print "Main Function..."
    print psutil.cpu_times()



if __name__ == '__main__':
    print "Probar de obtener cpu & ram de mi portatil"
    main()