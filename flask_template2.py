# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 17:52:35 2018

@author: 00130161
"""

import os
import re
import pandas as pd
import google_api_utils
import json

from flask import Flask, request, render_template, send_from_directory

def classification_rule(text):
    if re.search('sijil kematian', text.lower()):
        template=update_death(text)
        
        
        
        
        
        
        template=template_to_use[0]
    elif re.search('sijil kelahiran', text.lower()):
        template=template_to_use[1]
    elif re.search('repot polis', text.lower()):
        template=template_to_use[2]
    elif re.search('kad pengenalan', text.lower()):
        template=template_to_use[3]
    elif re.search('surat perakuan nikah', text.lower()):
        template=template_to_use[4]
    else:
        dassda






app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))#current directory
no_file={'D':0,'B':0,'P':0,'I':0,'M':0,'U':0}
template_to_use=['death_certh.html','birth_cert.html','police_report.html','ic.html',
                 'marriage_cert.html','unknown.html']



@app.route("/")
def index():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload():

    
        

    
    
    for upload in request.files.getlist("file"):
        filename = upload.filename
        
        # This is to verify files are supported
        ext = os.path.splitext(filename)[1]
        if (ext == ".jpg") or (ext == ".png"):
            print("File supported moving on...")
        else:
            render_template("Error.html", message="Files uploaded are not supported...")
        
        #Need to check whether to use upload or upload.filename
        response,textjson = google_api_utils.main(upload)
        classification_rule(textjson)
        
        
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print(type(upload))
        upload.save(destination)
    
    if len(request.files.getlist("file"))>1:
        return render_template('all_cert.html',no_file)
    # return send_from_directory("images", filename, as_attachment=True)
    else:
        return render_template(template, textjson=textjson)








#    folder_name='document'
#    target = os.path.join(APP_ROOT, 'savefiles/{}'.format(folder_name))
#    print(target)
#    if not os.path.isdir(target):
#        os.mkdir(target)






'''
@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)


@app.route('/gallery')
def get_gallery():
    image_names = os.listdir('./images')
    print(image_names)
    return render_template("gallery.html", image_names=image_names)
'''

if __name__ == "__main__":
    app.run()
