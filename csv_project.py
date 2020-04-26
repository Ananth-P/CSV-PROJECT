#importing modules
import os
import glob
from pymongo import MongoClient
import codecs
import csv
import shutil


# database setup
client=MongoClient()
db=client["Csv_file_db"]
collection_name=db["csv_collection"]





def insert_data_from_csv_file(Sourcefile,coll_instance,keywords):
    """ 
    This function response to insert data into database based on keywords
    
    Parameters
    SourceFile :- SourceFile which is used to extract data 
    coll_instance :- mongodb database collection instance object
    Keywords :- which can be set of words used to identify in specfic set of rows

    return :-
    """
   
    fp = codecs.open(Sourcefile, 'r', 'utf-8')
    lines = fp.readlines()
   
    cl0 = lines[0].replace('\r', '').replace('\n','')
    sr0 = cl0.split(',')
   
    count=0
    for row in lines[1:]:
        # print(row)
        data ={}
        cl = row.replace('\r', '').replace('\n','')
        sr = cl.split(',')
        row_in_list=sr
        #check keywords with no case sensitive
        lowered_row = [s.lower() for s in sr]
        if keywords.lower() in lowered_row:
            for ind,key in enumerate(sr0):
                data[key]=row_in_list[ind]
            count+=1
            coll_instance.insert_one(data)  

    return count




def read_csv_from_directory(phys_folder,keywords):

    """ 
        this function used to read csv file and callback the function for inserting data into databas
    """
    
    files = glob.glob(phys_folder+"/*.csv")

    total_rows=0
    for file_ind in files:
        file_to_db=insert_data_from_csv_file(file_ind,collection_name,keywords)
        total_rows+=file_to_db
    return total_rows  

def main(folder,keywords):
    dirname = os.path.dirname(__file__)
    phys_folder = dirname+"/"+folder
    print("Your Physical path folder ",phys_folder)
    print("Keywords to update ",keywords)
    # keywords=input()
    print(dirname)
    src=dirname+"/csv_data"
    src_files = os.listdir(src)
    
    #create directory if not exists
    if not os.path.exists(phys_folder):
        os.makedirs(phys_folder)
    for file_name in src_files:
        # print("yes")
        full_file_name = os.path.join(src, file_name)
        if os.path.isfile(full_file_name):
            
            statinfo = os.stat(full_file_name)
            # copying the files only between 1kb and 200Mb 
            if statinfo.st_size>=1024 and statinfo.st_size <=209715200:  # values in bytes
                print("copying ... %s"%file_name)
                shutil.copy(full_file_name, phys_folder)
                print("copied %s"%file_name)
    rows_added=read_csv_from_directory(phys_folder,keywords)
    if rows_added:
        print("Rows updated in database",rows_added)
    else:
        print("keywords not found in database")
    
    return rows_added

if __name__ == '__main__':
    print("Enter the physical folder")
    phys_folder=input()
    print("Enter the Keywords to update")
    keywords=input()
    main(phys_folder,keywords)
    
