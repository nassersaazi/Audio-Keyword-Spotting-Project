import sys
import time
import traceback
import json
# import numpy as np
import pandas as pd
import config
import logging

from flask import jsonify

from encapsulate_data_class import ErrorMessageClass
from encapsulate_data_class import ContentDataClass

class RESTfulAPIImageSuperclass(object):   
    def __init__(self):
        pass 
        
    def is_json_data(self, data):
        """
        check if data is a json format
        :param data: any data
        :return: json data format and boolean true/false
        """
        json_data = None
        try:
            json_data = json.loads(data)
            return json_data, True
        except:
            self.print_exception_message()
            return json_data, False
       
    def image_data_cast_normalization(self, image_1d_nparray, cast_data_type="float32"):
        """
        cast and normalize image 1-d flatten numpy array
        :param image_1d_nparray: image 1-d flatten numpy array
        :param cast_data_type: cast data type
        :return image cast and normalize array
        """
        try:
            image_data_frame = pd.DataFrame(image_1d_nparray)      
            X_min = config.X_MIN; X_max = config.X_MAX
            image_data_frame = (image_data_frame.astype(cast_data_type) - X_min) / (X_max - X_min)           
        except:
            self.print_exception_message()
        return  image_data_frame
        
    def print_exception_message(self, message_orientation="horizontal"):
        """
        print full exception message
        :param message_orientation: horizontal or vertical
        :return None
        """
        try:
            exc_type, exc_value, exc_tb = sys.exc_info()           
            file_name, line_number, procedure_name, line_code = traceback.extract_tb(exc_tb)[-1]      
            time_stamp = " [Time Stamp]: " + str(time.strftime("%Y-%m-%d %I:%M:%S %p"))
            file_name = " [File Name]: " + str(file_name)
            procedure_name = " [Procedure Name]: " + str(procedure_name)
            error_message = " [Error Message]: " + str(exc_value)       
            error_type = " [Error Type]: " + str(exc_type)                   
            line_number = " [Line Number]: " + str(line_number)               
            line_code = " [Line Code]: " + str(line_code)
            if (message_orientation == "horizontal"):
                print("An error occurred:{};{};{};{};{};{};{}".format(time_stamp, file_name, procedure_name, error_message, error_type, line_number, line_code))
            elif (message_orientation == "vertical"):
                print("An error occurred:\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(time_stamp, file_name, procedure_name, error_message, error_type, line_number, line_code))                    
        except:
            pass
        
    def get_exception_message(self):      
        """
        get full exception message as string
        :return exception message
        """     
        try:     
            exc_type, exc_value, exc_tb = sys.exc_info()               
            file_name, line_number, procedure_name, line_code = traceback.extract_tb(exc_tb)[-1]           
            exception_message = ''.join('[Time Stamp]: ' + str(time.strftime('%Y-%m-%d %I:%M:%S %p')) + ' '
                                            + '[File Name]: ' + str(file_name) + ' '
                                            + '[Procedure Name]: ' + str(procedure_name) + ' '
                                            + '[Error Message]: ' + str(exc_value) + ' '  
                                            + '[Error Type]: ' + str(exc_type) + ' '                                                                                                                                
                                            + '[Line Number]: ' + str(line_number) + ' '
                                            + '[Line Code]: ' + str(line_code))       
            return exception_message   
        except:
            pass
        
    def write_log_file(self, log_file_name, event_level, message):
        """
         write to a log file
        :param log_file_name: log file path and name
        :param event_level: even level name (CRITICAL, DEBUG, ERROR, INFO and WARNING)
        :param message: message to be written 
        :return None
        """       
        try:
            if event_level == "CRITICAL".lower():
                logging.basicConfig(format=message, filename=log_file_name, level=logging.CRITICAL)      
                logging.critical(message)        
            elif event_level == "DEBUG".lower():
                logging.basicConfig(format=message, filename=log_file_name, level=logging.DEBUG)      
                logging.debug(message)
            elif event_level == "ERROR".lower():
                logging.basicConfig(format=message, filename=log_file_name, level=logging.ERROR)      
                logging.error(message)
            elif event_level == "INFO".lower():
                logging.basicConfig(format=message, filename=log_file_name, level=logging.INFO)      
                logging.info(message)
            elif event_level == "WARNING".lower():
                logging.basicConfig(format=message, filename=log_file_name, level=logging.WARNING)      
                logging.warning(message)               
        except:
            self.print_exception_message()      
    
    def create_json_error_message(self, message):
        """
        create a json error message
        :param message: string error message
        :return json error message
        """
        try:
            encapsulate_data_class = ErrorMessageClass(message)
            result = json.dumps(encapsulate_data_class.__dict__)            
        except:
            exception_message = sys.exc_info()[1]
            encapsulate_data_class = ErrorMessageClass(exception_message)
            result = json.dumps(encapsulate_data_class.__dict__) 
        return jsonify(result)
    
    def create_json_content_data(self, data):
        """
        create any json content data
        :param data: any data type
        :return json content data
        """
        try:
            encapsulate_data_class = ContentDataClass(data)            
            result = json.dumps(encapsulate_data_class.__dict__)            
        except:
            exception_message = sys.exc_info()[1]
            encapsulate_data_class = ErrorMessageClass(exception_message)
            result = json.dumps(encapsulate_data_class.__dict__) 
        return jsonify(result)