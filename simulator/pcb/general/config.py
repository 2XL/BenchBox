'''
Created on 15 Jul 2014

@author: cotes
'''
import ConfigParser

class Config:
    
    BENCHMARK_SECTION = "Benchmark"
    CLIENT_SECTION = "Client"
    
    def __init__(self):
        self._read_configuration()

    def _read_configuration(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read("../config.ini")
        self.benchmark_options = {}
        self._read_config_section(self.BENCHMARK_SECTION)
        self._read_config_section(self.CLIENT_SECTION)
        
    def _read_config_section(self, section):
        
        options = self.config.options(section)
        for option in options:
            try:
                self.benchmark_options[option] = self.config.get(section, option)
            except:
                print("exception on %s!" % option)
                self.benchmark_options[option] = None
                
    def get_file_size(self):
        file_size = self.benchmark_options["filesize"]
        if file_size is not None:
            return file_size
        else:
            # TODO exception
            pass
                
    def get_inter_operation_time(self):
        interop_time = self.benchmark_options["interoptime"]
        if interop_time is not None:
            return interop_time
        else:
            # TODO exception
            pass
        
    def get_client_folder(self):
        folder = self.benchmark_options["folder"]
        if folder is not None:
            return folder
        else:
            # TODO exception
            pass