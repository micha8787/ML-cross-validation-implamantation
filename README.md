# ML-cross-validation-implamantation
ML cross validation implamantation (split a data into train and test set)

When training a supervised model, we use a technique called cross validation wherein we split our data into two files, a train set and a test set.
However, we want to keep the same ratio of certain data characteristics. In other words, if we want to keep the ratio of the “device” field. And looking at the input data the device field is made up of 25% “d1” 25% “d2” and 50% “d3” then we want that same ratio (or as close as possible) in the two files. This technique is called “stratify”

I implemented an alghorythem for stratify by couple of fields.
the algorithm:
1. loop over the data for each field in fields and hold the numbers of appearances for each category.
we will hold this data in a dictionary.
the keys will be the indexs of the columns and the values will be anothe dictionarys which holds the categorys of each columns and how many apearences of each category.

dictionary example: 
{1: {d1:5, d2:5},2:{l1:5, l2:2, l3:3}}

2. multiply the numbers inside the internal dictionary and round the result.
3. this is the numbers of each category that should be in the test file in order to preserve the categorys ratio.we will loop over the rows of the data and copy rows with those categorys to the test file. 


