# # import flask microframework library
# from flask import Flask,request,jsonify
# import json,sys
 
# # initialize the flask application
# app = Flask(__name__)

#  # endpoint api_1() with get method
# @app.route("/", methods=["GET"])
# def api_1():
#     return "Halo Welt!!"
    
# @app.route("/api/v1.0/csharp_python_restfulapi_json", methods=["POST"])
# def csharp_python_restfulapi_json():
#     """
#     simple c# test to call python restful api web service
#     """
#     try:                
# #         get request json object
#         request_json = request.get_json()      
# #         convert to response json object 
#         response = jsonify(request_json)
#         response.status_code = 200  
#     except:
#         exception_message = sys.exc_info()[1]
#         response = json.dumps({"content":exception_message})
#         response.status_code = 400
#     return response

# if __name__ == "__main__":
# #     run flask application in debug mode
#     app.run(debug=True)

import sys
import json
import config
 
from flask import Flask, jsonify, request
from restful_api_image_subclass import RESTfulAPIImageSubclass
 
app = Flask(__name__)
 
@app.route("/api/v1.0/image_classification_base64_encoding", methods=["POST"])
def image_classification_base64_encoding():
    response = restful_api_image_subclass.image_classification_base64_encoding(request)      
    return response
 
@app.route("/api/v1.0/image_classification_base64_encoding_json", methods=["POST"])
def image_classification_base64_encoding_json():
    response = restful_api_image_subclass.image_classification_base64_encoding_json(request)      
    return response
 
@app.route("/api/v1.0/image_classification_opencv_encoding", methods=["POST"])
def image_classification_opencv_encoding():    
    response = restful_api_image_subclass.image_classification_opencv_encoding(request)      
    return response
        
@app.route("/api/v1.0/image_classification_opencv_encoding_json", methods=["POST"])
def image_classification_opencv_encoding_json():    
    response = restful_api_image_subclass.image_classification_opencv_encoding_json(request)      
    return response
 
@app.route("/api/v1.0/image_classification_file_encoding_json", methods=["POST"])
def image_classification_file_encoding_json():    
    response = restful_api_image_subclass.image_classification_opencv_encoding_json(request)      
    return response
 
if __name__ == "__main__":
    global restful_api_image_subclass
    restful_api_image_subclass = RESTfulAPIImageSubclass(config.IMAGE_WIDTH_RESIZE, config.IMAGE_HEIGHT_RESIZE)
    app.run(debug=True)