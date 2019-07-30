
import csv
import numpy as np
# import collections
from apyori import apriori
# import matplotlib.pyplot as plt  
import pandas as pd
from os import path
import pickle

movie_data = pd.read_csv('data1.csv', header = None)
num_records = len(movie_data)
# print movie_data.values[0]
records = []  
for i in range(0, num_records):  
    records.append([str(movie_data.values[i,j]) for j in range(0, 20)])


if path.exists("movie_suggestion.txt"):
	with open('movie_suggestion.txt','r') as file1:
		movie_suggestion = pickle.load(file1)
else:
	association_rules = apriori(records, min_support=0.0053, min_confidence=0.15, min_lift=3, min_length=3)
	association_results = list(association_rules)
	
	results = []
	for item in association_results:
	    
	    # first index of the inner list
	    # Contains base item and add item
	    pair = item[0] 
	    items = [x for x in pair]
	    
	    value0 = str(list(item[2][0][0]))
	    value1 = str(list(item[2][0][1]))

	    #second index of the inner list
	    value2 = str(item[1])[:7]

	    #third index of the list located at 0th
	    #of the third index of the inner list

	    value3 = str(item[2][0][2])[:7]
	    value4 = str(item[2][0][3])[:7]
	    
	    rows = (value0, value1,value2,value3,value4)
	    results.append(rows)
	    
	labels = ['Title1','Title2','Support','Confidence','Lift']
	movie_suggestion = pd.DataFrame.from_records(results, columns = labels)

	with open('movie_suggestion.txt','w') as file1:
		pickle.dump(movie_suggestion,file1)
print(movie_suggestion)

print "Enter number of movies"
loop = input()
print "Enter Movies name"
movies_list = [raw_input() for x in range(0,loop)]

result_dataframe = movie_suggestion.loc[ movie_suggestion['Title1'] == str(sorted(movies_list)) ]
if not result_dataframe.empty:
	v = result_dataframe.groupby(['Title2'], as_index=False)['Confidence'].max()
	print "Next Movie will be"
	print v['Title2'][0][1:-1]
else:
	print "We are not sure about next movie"