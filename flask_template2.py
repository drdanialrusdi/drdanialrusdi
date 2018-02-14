# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 17:52:35 2018

@author: 00130161
"""

import os
import re
import pandas as pd
import google_api_utils


from flask import Flask, request, render_template
def classification_rule(filename, APP_ROOT, text, no_file):
    if re.search('sijil kematian', text.lower()):
        target = os.path.join(APP_ROOT, 'savefiles/death_cert')
        with open(target+'/'+filename+'.txt', "w") as text_file:
            text_file.write(text)
        
        info=text.split('\n')
        df=pd.read_excel(target+'/death_info.xlsx')
        data={
           'FILENAME':[filename], 
           'REGISTRATION_AREA':[info[16]],
           'REGISTRATION_CENTRE':[info[17]],
           'NAME':[info[21]],
           'IC_NO':[info[4]],
           'AGE':[info[22]],
           'GENDER':[info[24]],
           'DATE_DEATH':[info[34]],
           'TIME_DEATH':[info[35]],
           'RACE':[info[36]],
           'LAST_ADDRESS':[re.sub('SEBAB.*','',re.sub('.*Last Address','',' '.join(info)))],
           'PLC_OF_DEATH':[re.sub('Alamat Terakhir.*','',re.sub('.*Place of Death','',' '.join(info)))],
           'CAUSE_OF_DEATH':[re.sub('THE CAUSE OF DEATH.*','',re.sub('.*Sebab Kematian','',' '.join(info)))]
           }
        df1 = pd.DataFrame(data)
        df=df.append(df1,ignore_index=True)
        df.to_excel(target+'/death_info.xlsx',index=False)
        
        
        current=int(no_file['D'])
        no_file['D']=current+1
        template=template_to_use[0]
        return template, no_file, target, data
        
    elif re.search('sijil kelahiran', text.lower()):
        target = os.path.join(APP_ROOT, 'savefiles/birth_cert')
        with open(target+'/'+filename+'.txt', "w") as text_file:
            text_file.write(text)
            
        info=text.split('\n')
        df=pd.read_excel(target+'/birth_info.xlsx')
        data={'FILENAME':[filename], 
               'REGISTRATION_AREA':[info[11]],#re.findall('(.*)',' '.join(info))
               'REGISTRATION_CENTRE':[info[12]],
               'FULL_NAME':[info[16]],
               'DATE_TIME_BIRTH':[info[17]+info[21]],
               'RACE':[info[23]],
               'PLACE_OF_BIRTH':[info[22]],
               'CITIZENSHIP':[info[25]],
               'GENDER':re.findall(r'Jantina (.*?) ',' '.join(info)),
               'RELIGION':re.findall(r'Agama (.*?) ',' '.join(info)),
               'FATHER_NAME':re.findall(r'FATHER Nama (.*?) No',' '.join(info)),
               'FATHER_IC':re.findall(r'FATHER.*(\d{6}-\d{2}-\d{4}).*MOTHER ',' '.join(info)),
               'FATHER_AGE':re.findall(r'FATHER.*?Umur (\d{2}) ',' '.join(info)),
               'FATHER_CITIZENSHIP':re.findall(r'FATHER.*?Citizenship (.*?) ',' '.join(info)),
               'FATHER_RACE':re.findall(r'FATHER.* (.*?) Taraf',' '.join(info)),
               'FATHER_RELIGION':re.findall(r'FATHER.*? Agama (.*?) ',' '.join(info)),
               'MOTHER_NAME':re.findall(r'MOTHER Nama (.*?) No',' '.join(info)),
               'MOTHER_IC':re.findall(r'MOTHER.*(\d{6}-\d{2}-\d{4}) ',' '.join(info)),
               'MOTHER_AGE':re.findall(r'MOTHER.*?Umur (\d{2}) ',' '.join(info)),
               'MOTHER_CITIZENSHIP':re.findall(r'MOTHER.*?Citizenship (.*?) ',' '.join(info)),
               'MOTHER_RACE':re.findall(r'MOTHER.* Keturunan(.*?) ',' '.join(info)),
               'MOTHER_RELIGION':re.findall(r'MOTHER.? Agama (.*?) ',' '.join(info))
              }
        df1 = pd.DataFrame(data)
        df=df.append(df1,ignore_index=True)
        df.to_excel(target+'/birth_info.xlsx',index=False)
        
        current=int(no_file['B'])
        no_file['B']=current+1
        template=template_to_use[1]
        return template, no_file, target, data
        
    elif re.search('repot polis', text.lower()):
        target = os.path.join(APP_ROOT, 'savefiles/police_report')
        with open(target+'/'+filename+'.txt', "w") as text_file:
            text_file.write(text)
        
        info=text.split('\n')
        df=pd.read_excel(target+'/police_info.xlsx')
        data={'FILENAME':[filename], 
               'BALAI':[info[4]],
               'DAERAH':[info[5]],
               'KONTINJEN':[info[6]],
               'NO_REPORT':re.findall(r' (\w+ \w+\/\d\/\d\(.8\)) ',' '.join(info)),
               'TARIKH':re.findall(r' (\d{2}\/\d{2}\/\d{5}) ',' '.join(info)),
               'WAKTU':re.findall(r' (\d{4} \wM) ',' '.join(info)),
               'NAMA_PENERIMA_REPORT':re.findall(r'Penerima Repot Nama: (.*?) No Personel',' '.join(info)),
               'NO_PERSONAL':re.findall(r' No Personel: (.*?) Pangkat',' '.join(info)),
               'PANGKAT':re.findall(r' Pangkat (.*?) Butir',' '.join(info)),
               'NAMA_PENGADU':re.findall(r' Pengadu Nama: (.*?) No',' '.join(info)),
               'IC_NO':re.findall(r' No K\/P \(Baru\): (.*?) No',' '.join(info)),
               'NO_POLICE_SOLDIER':re.findall(r' No Polis\/Tentera: (.*?) No',' '.join(info)),
               'NO_PASSPORT':re.findall(r' No Paspot: (.*?) No',' '.join(info)),
               'GENDER':re.findall(r' Jantina: (.*?) ',' '.join(info)),
               'DOB':re.findall(r' Tarikh Lahir: (\d{2}\/\d{2}\/\d{4}) ',' '.join(info)),
               'AGE':re.findall(r' Umur: (.*?) Keturunan',' '.join(info)),
               'RACE':re.findall(r' Keturunan:(.*?) Pekerjaan',' '.join(info)),
               'CITIZENSHIP':re.findall(r' Warganegara: (.*?) Umur',' '.join(info)),
               'OCCUPATION':re.findall(r' Pekerjaan(.*?) Alamat',' '.join(info)),
               'ADDRESS':re.findall(r' Alamat Tempat Tinggal :(.*?) Alamat',' '.join(info)),
               'REPORT':re.findall(r'Pengadu Menyatakan:(.*?) Tandatangan',' '.join(info))
               }
        df1 = pd.DataFrame(data)
        df=df.append(df1,ignore_index=True)
        df.to_excel(target+'/police_info.xlsx',index=False)
        
        current=int(no_file['P'])
        no_file['P']=current+1
        template=template_to_use[2]
        return template, no_file, target, data
        
    elif re.search('kad pengenalan', text.lower()):
        target = os.path.join(APP_ROOT, 'savefiles/ic')
        with open(target+'/'+filename+'.txt', "w") as text_file:
            text_file.write(text)
        
        info=text.split('\n')
        df=pd.read_excel(target+'/ic_info.xlsx')
        data={'FILENAME':[filename], 
              'NAME':re.findall(r'\d{6}-\d{2}-\d{4} (\w.*) \d',' '.join(info)),
              'IC_NUM':re.findall(r' (\d{6}-\d{2}-\d{4}) ',' '.join(info)),
              'ADDRESS':re.findall(r' (\d+ \w.*) WARGANEGARA',' '.join(info)),
              'CITIZENSHIP':re.findall(r'(WARGANEGARA)',' '.join(info)),
              'RELIGION':re.findall(r'(ISLAM)',' '.join(info)),
              'GENDER':re.findall(r'(LELAKI|PEREMPUAN)',' '.join(info))
               }
        df1 = pd.DataFrame(data)
        df=df.append(df1,ignore_index=True)
        df.to_excel(target+'/ic_info.xlsx',index=False)
            
        current=int(no_file['I'])
        no_file['I']=current+1
        template=template_to_use[3]
        return template, no_file, target, data

    else:
        target = os.path.join(APP_ROOT, 'savefiles/unknown')
        with open(target+'/'+filename+'.txt', "w") as text_file:
            text_file.write(text)
        data=text
        current=int(no_file['U'])
        no_file['U']=current+1
        template=template_to_use[5]
        return template, no_file, target, data
'''       
    elif re.search('surat perakuan nikah', text.lower()):
        target = os.path.join(APP_ROOT, 'savefiles/marriage_cert')
        with open(target+'/'+filename+'.txt', "w") as text_file:
            text_file.write(text)
        
        info=text.split('\n')
        df=pd.read_excel(target+'/marriage_info.xlsx')
        data={'FILENAME':[filename], 
           'HUSBAND_NAME':[info[]],
           'HUSBAND_IC':[info[]],
           'HUSBAND_AGE':[info[]],
           'HUSBAND_CITIZENSHIP':[info[]],
           'HUSBAND_RACE':[info[]],
           'HUSBAND_ADDRESS':[info[]],
           'WIFE_NAME':[info[]],
           'WIFE_IC':[info[]],
           'WIFE_AGE':[info[]],
           'WIFE_CITIZENSHIP':[info[]],
           'WIFE_RACE':[info[]],
           'WIFE_ADDRESS':[info[]],
           'WALI_NAME':[info[]],
           'WALI_IC':[info[]],
           'WALI_AGE':[info[]],
           'WALI_RELATIONSHIP':[info[]],
           'WALI_ADDRESS':[info[]]
           }
        df1 = pd.DataFrame(data)
        df=df.append(df1,ignore_index=True)
        df.to_excel(target+'/marriage_info.xlsx',index=False)
            
        current=int(no_file['M'])
        no_file['M']=current+1
        template=template_to_use[4]
        return template, no_file, target, data  
'''     
    






app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))#current directory
template_to_use=['death_certh.html','birth_cert.html','police_report.html',
                     'ic.html', 'marriage_cert.html','unknown.html']



@app.route("/")
def index():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload():
    no_file={'D':0,'B':0,'P':0,'I':0,'M':0,'U':0}
  
    for upload in request.files.getlist("file"):
        filename = upload.filename
        
        # This is to verify files are supported
        ext = os.path.splitext(filename)[1]
        if (ext == ".jpg") or (ext == ".png") or (ext == ".jpeg"):
            print("File supported moving on...")
        else:
            render_template("Error.html", message="Files uploaded are not supported...")
        
        #Need to check whether to use upload or upload.filename
        response, textjson = google_api_utils.main(upload)
        textinfo=textjson.split('\n')
        template, no_file, target, data = classification_rule(filename, APP_ROOT, textjson, no_file)
        
        
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        upload.save(destination)
    
    if len(request.files.getlist("file"))>1:
        return render_template('all_cert.html',no_file)
    # return send_from_directory("images", filename, as_attachment=True)
    else:
        return render_template(template, data=data)








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
