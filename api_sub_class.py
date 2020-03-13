import os
import sys
import numpy as np
import json
import config
import base64
 
import cv2
import pickle
from flask import jsonify
 
from restful_api_image_superclass import RESTfulAPIImageSuperclass
 
class RESTfulAPIImageSubclass(RESTfulAPIImageSuperclass):
    
    def __init__(self, image_width_resize=None, image_height_resize=None):
        super().__init__()
        if image_width_resize is not None:
            self.image_width = image_width_resize
        if image_height_resize is not None:
            self.image_height = image_height_resize
       
    def image_resize_flatten_opencv(self, image, nparray_dimension="1d"):
        """
        resize and flatten the image from 1d to 2d array with fixed width and height        
        :param image_path_name: image path and file name
        :param nparray_dimension: nparray 1d dimension type
        :return image flatten array      
        """
        image_nparray = None
        try:           
            image_dimension = (self.image_width, self.image_height)
            image = cv2.resize(image, image_dimension, interpolation=cv2.INTER_AREA)
            image_nparray = np.fromstring(image.tobytes(), dtype=np.uint8)
            if (nparray_dimension == "1d"):
                image_nparray = image_nparray.reshape((1, self.image_height * self.image_width))
        except:
            self.print_exception_message()
        return image_nparray
        
    def image_classification_opencv_encoding_json(self, request): 
        try:
#             encoding iso_8859_1
            encoding = config.ENCODING_ISO_8859_1
#             get request data
            request_data = request.data
#             decode json data
            image_dencode_json = json.loads(request_data)
#             get content string image data only
            image_string = image_dencode_json["content"]            
#             convert string of image data to uint8
            np_array_encode = np.fromstring(image_string.encode(encoding), np.uint8)    
#             image numpy array decode
            image = cv2.imdecode(np_array_encode, cv2.IMREAD_GRAYSCALE)
#             image data pre-processing:
#             1. resize and flatten
            image_1d_nparray = self.image_resize_flatten_opencv(image)
#             2. cast and normalization
            X_test = self.image_data_cast_normalization(image_1d_nparray)                   
#             open and close image classification pickle model
            project_directory_path = os.path.dirname(os.path.realpath(__file__))                   
            mlp_classifier_model_pkl = open(os.path.join(project_directory_path, "fiducial_image_flat_tilt_classification.pkl"), "rb")                                    
            mlp_classifier_model_file = pickle.load(mlp_classifier_model_pkl)  
            mlp_classifier_model_pkl.close()
#             get y predict
            y_predict_file = mlp_classifier_model_file.predict(X_test)
            if y_predict_file == 1:
                result = {"image type":"{}".format(1)}
            else:
                result = {"image type":"{}".format(0)}
#             get json result and set response with 200 status code        
            response = jsonify(result)
            response.status_code = config.HTTP_200_OK
        except:
    #         get exception message, json result and set response with 400 status code
            exception_message = self.get_exception_message()                                
            result = {"An error occurred":exception_message}          
            response = jsonify(result)
            response.status_code = config.HTTP_400_BAD_REQUEST
        return response
    
    def image_classification_opencv_encoding(self, request): 
        try:
#             get request data
            request_data = request.data                    
#             convert string of image data to uint8
            np_array_encode = np.fromstring(request_data, np.uint8)    
#             image numpy array decode
            image = cv2.imdecode(np_array_encode, cv2.IMREAD_GRAYSCALE)
#             image data pre-processing:
#             1. resize and flatten
            image_1d_nparray = self.image_resize_flatten_opencv(image)
#             2. cast and normalization
            X_test = self.image_data_cast_normalization(image_1d_nparray)                   
#             open and close image classification pickle model
            project_directory_path = os.path.dirname(os.path.realpath(__file__))                   
            mlp_classifier_model_pkl = open(os.path.join(project_directory_path, "fiducial_image_flat_tilt_classification.pkl"), "rb")                                    
            mlp_classifier_model_file = pickle.load(mlp_classifier_model_pkl)  
            mlp_classifier_model_pkl.close()
#             get y predict
            y_predict_file = mlp_classifier_model_file.predict(X_test)
            if y_predict_file == 1:
                result = {"image type":"{}".format(1)}
            else:
                result = {"image type":"{}".format(0)}
#             get json result and set response with 200 status code        
            response = jsonify(result)
            response.status_code = config.HTTP_200_OK
        except:
#             get exception message, json result and set response with 400 status code
            exception_message = self.get_exception_message()                                
            result = {"An error occurred":exception_message}     
            response = jsonify(result)
            response.status_code = config.HTTP_400_BAD_REQUEST
        return response
    
    def image_classification_base64_encoding_json(self, request):
        try:
#             get request data
            request_data = request.data                            
#             decode json data
            image_dencode_json = json.loads(request_data)          
#             get content string image data only
            image_string = image_dencode_json["content"]         
#             image string base64 decode
            image_string = base64.b64decode(image_string)      
#             convert string of image data to uint8
            np_array_encode = np.fromstring(image_string, np.uint8)    
#             image numpy array decode
            image = cv2.imdecode(np_array_encode, cv2.IMREAD_GRAYSCALE)
#             image data pre-processing:
#             1. image resize and flatten          
            image_1d_nparray = self.image_resize_flatten_opencv(image)    
#             2. image data cast and normalization
            X_test = self.image_data_cast_normalization(image_1d_nparray)                   
#             open and close image classification pickle model
            project_directory_path = os.path.dirname(os.path.realpath(__file__))                   
            mlp_classifier_model_pkl = open(os.path.join(project_directory_path, "fiducial_image_flat_tilt_classification.pkl"), "rb")                                    
            mlp_classifier_model_file = pickle.load(mlp_classifier_model_pkl)  
            mlp_classifier_model_pkl.close()                            
#             get y predict
            y_predict_file = mlp_classifier_model_file.predict(X_test)
            if y_predict_file == 1:
                result = {"image type":"{}".format(1)}
            else:
                result = {"image type":"{}".format(0)}
#             get json result and set response with 200 status code        
            response = jsonify(result)
            response.status_code = config.HTTP_200_OK 
        except:
#             get exception message, json result and set response with 400 status code
            exception_message = self.get_exception_message()                                
            result = {"An error occurred":exception_message}    
            response = jsonify(result)
            response.status_code = config.HTTP_400_BAD_REQUEST    
        return response
    
    def image_classification_base64_encoding(self, request):
        try:
#             get request data
            request_data = request.data
#             image string base64 decode
            image_base64_decode = base64.decodebytes(request_data)
#             convert string of image data to uint8
            np_array_encode = np.fromstring(image_base64_decode, np.uint8)    
#             image numpy array decode
            image = cv2.imdecode(np_array_encode, cv2.IMREAD_GRAYSCALE)
#             image data pre-processing:
#             1. image resize and flatten          
            image_1d_nparray = self.image_resize_flatten_opencv(image)    
#             2. image data cast and normalization
            X_test = self.image_data_cast_normalization(image_1d_nparray)                   
#             open and close image classification pickle model
            project_directory_path = os.path.dirname(os.path.realpath(__file__))                   
            mlp_classifier_model_pkl = open(os.path.join(project_directory_path, "fiducial_image_flat_tilt_classification.pkl"), "rb")                                    
            mlp_classifier_model_file = pickle.load(mlp_classifier_model_pkl)  
            mlp_classifier_model_pkl.close()
#             get y predict
            y_predict_file = mlp_classifier_model_file.predict(X_test)
            if y_predict_file == 1:
                result = {"image type":"{}".format(1)}
            else:
                result = {"image type":"{}".format(0)}
#             get json result and set response with 200 status code        
            response = jsonify(result)
            response.status_code = config.HTTP_200_OK 
        except:
#             get exception message, json result and set response with 400 status code
            exception_message = self.get_exception_message()                                
            result = {"An error occurred":exception_message}    
            response = jsonify(result)
            response.status_code = config.HTTP_400_BAD_REQUEST    
        return response