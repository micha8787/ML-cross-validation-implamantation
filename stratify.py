import csv
import os
import pandas as pd
from pathlib import Path
import sys


def split_full_or_empty(df):# handle a case of ratio == 0.0 or 1.0
    #full will be a pandas dataframe with all the data
    full = df
    # empty will be a pandas dataframe with the headers only and no data at all:
    headers = list(df.columns.values)
    headers_map = {}
    for header in headers:
        headers_map[header] = None
    empty = pd.DataFrame([headers_map])
    return full,empty #returns 2 files- one is full and one is empty



def get_indexes(columns,fields):
    fields_indexes = [] * len(fields)
    for i in range(0, len(columns)):
        if columns[i] in fields:
            fields_indexes.append(i)
    return fields_indexes

def build_counter(df, fields_indexes,file_length): #returns a dictionary which holds the number of cells in every category for each field
    counter_dictonary = {}
    overall_counter = {}
    for column in fields_indexes:
        for row in range (0,file_length):
            cell = df[row][column]
            if cell in counter_dictonary:
                counter_dictonary[cell] = counter_dictonary[cell]+1
            else:
                counter_dictonary[cell] = 1
        # multiply the numbers  by ratio
        for category in counter_dictonary:
            counter_dictonary[category] = round(counter_dictonary[category] * ratio)
        overall_counter[column]=counter_dictonary.copy()
        counter_dictonary.clear()
    return overall_counter
def make_train_test_df(df,fields_indexes,overall_counter,file_length):
    train = []
    test = []
    for row in range(0, file_length): #loop over the data file
        istest = True
        for field in fields_indexes:
            character = df[row][field]
            if overall_counter[field][character] <= 0:  # in that case, this row should be copied to the train file
                istest = False
        if istest:# in case that all the fields values at our counter are greater then 0 we wull copy the row to the test file
            test.append(df[row])
            for field in fields_indexes:
                character = df[row][field]
                overall_counter[field][character] = overall_counter[field][character] - 1
        else:
            train.append(df[row])
    return train,test

def manual_efficient_stratify(df, path, ratio, fields ):
    columns = df.columns #holds the header of the data frame
    fields_indexes = get_indexes(columns,fields)#get the indexs of the fields we should stratify
    df = df.to_numpy()#turn the pandas data frame into numpy array (more efficient to loop)
    file_length = len(df) #hold the length of the data.csv file
    overall_counter=build_counter(df, fields_indexes,file_length) #build counter dictionary which represents the apearence number of the diffrent kinds of cells
    train,test = make_train_test_df(df,fields_indexes,overall_counter,file_length)#splits the data o train and test
    train = pd.DataFrame(train,columns=columns)
    test = pd.DataFrame(test,columns=columns)
    return train,test


def stratify_file(path, ratio, fields ):# returns Two files(train,test) containing the data split according to the input ratio
    try: #trying to read the csv and printing error message if it can't
        df = pd.read_csv(path)
    except:
        print("can't find the file ", path)
    if ratio == 0:
        train,test = split_full_or_empty(df)
    elif ratio==1:
        test,train = split_full_or_empty(df)
    elif ((ratio<0) |(ratio>1)):# in case that the ratio is not valid we will print error message
        print("the ratio is not valid.")
        return
    else:
        train,test = manual_efficient_stratify(df, path, ratio, fields)
        #train, test = train_test_split(df, test_size=ratio, stratify=df[fields])
    #getting the absolute directory path where the train and test will be saved
    directory_path = os.path.abspath(os.path.dirname(path))
    train.to_csv(directory_path + '/train.csv')
    test.to_csv(directory_path +'/test.csv')
    print("The stratify is done successfully ")


def parse_arguments():#parse the arguments from the command line. supports path with white space
    path = sys.argv[2]
    ratio = float(sys.argv[4])
    # parse the string of the fields:
    fields_to_stratify = sys.argv[6].split(',')
    return path,ratio,fields_to_stratify

if __name__ == "__main__":

    path,ratio,fields = parse_arguments()
    #send the command line arguments to the stratify function:
    stratify_file(path,ratio,fields)



