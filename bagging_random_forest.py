#-------------------------------------------------------------------------
# AUTHOR: Ahmad Alkadi
# FILENAME: bagging_random_forest
# SPECIFICATION: base classifier, ensemble accuracy, and Forest accuracy prediction
# FOR: CS 5990- Assignment #4
# TIME SPENT: 3 hr
#-----------------------------------------------------------*/

#importing some Python libraries
from sklearn import tree
from sklearn.utils import resample
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pandas as pd

dbTraining = []
dbTest = []
X_training = []
y_training = []
classVotes = [] #this array will be used to count the votes of each classifier
base_accuracy = 0
ensemble_accuracy = 0
random_forest_accuracy = 0

#reading the training data from a csv file and populate dbTraining
#--> add your Python code here
dataSets = ['optdigits.tra', 'optdigits.tes']
dfOne = pd.read_csv(dataSets[0])
dbTraining = np.array(dfOne.values)

#reading the test data from a csv file and populate dbTest
#--> add your Python code here
dfTwo = pd.read_csv(dataSets[1])
dbTest = np.array(dfTwo.values)

#inititalizing the class votes for each test sample. Example: classVotes.append([0,0,0,0,0,0,0,0,0,0])
#--> add your Python code here
for i in dbTest:
    classVotes.append([0,0,0,0,0,0,0,0,0,0])

print("Started my base and ensemble classifier ...")

for k in range(20): #we will create 20 bootstrap samples here (k = 20). One classifier will be created for each bootstrap sample

  bootstrapSample = resample(dbTraining, n_samples=len(dbTraining), replace=True)

  #populate the values of X_training and y_training by using the bootstrapSample
  #--> add your Python code here
  X_training = bootstrapSample[:, :-1]  # All columns except the last one are features
  y_training = bootstrapSample[:, -1]  # Last column is the label

  #fitting the decision tree to the data
  clf = tree.DecisionTreeClassifier(criterion = 'entropy', max_depth=None) #we will use a single decision tree without pruning it
  clf = clf.fit(X_training, y_training)

  for i, testSample in enumerate(dbTest):

      #make the classifier prediction for each test sample and update the corresponding index value in classVotes. For instance,
      # if your first base classifier predicted 2 for the first test sample, then classVotes[0,0,0,0,0,0,0,0,0,0] will change to classVotes[0,0,1,0,0,0,0,0,0,0].
      # Later, if your second base classifier predicted 3 for the first test sample, then classVotes[0,0,1,0,0,0,0,0,0,0] will change to classVotes[0,0,1,1,0,0,0,0,0,0]
      # Later, if your third base classifier predicted 3 for the first test sample, then classVotes[0,0,1,1,0,0,0,0,0,0] will change to classVotes[0,0,1,2,0,0,0,0,0,0]
      # this array will consolidate the votes of all classifier for all test samples
      #--> add your Python code here
      class_predict = clf.predict([testSample[:-1]])
      classVotes[i][int(class_predict[0])] = int(classVotes[i][int(class_predict[0])]) + 1

      if k == 0: #for only the first base classifier, compare the prediction with the true label of the test sample here to start calculating its accuracy
          # --> add your Python code here
          if class_predict == testSample[-1]:
              base_accuracy += 1

  if k == 0: #for only the first base classifier, print its accuracy here
     #--> add your Python code here
     accuracy = base_accuracy / len(dbTest)
     print("Finished my base classifier (fast but relatively low accuracy) ...")
     print("My base classifier accuracy: " + str(accuracy))
     print("")

  #now, compare the final ensemble prediction (majority vote in classVotes) for each test sample with the ground truth label to calculate the accuracy of the ensemble classifier (all base classifiers together)
  #--> add your Python code here
  for i, testSample in enumerate(dbTest):
      if classVotes[i].index(max(classVotes[i])) == int(testSample[-1]):
          ensemble_accuracy += 1

#printing the ensemble accuracy here
accuracy = ensemble_accuracy / (len(dbTest)*20)
print("Finished my ensemble classifier (slow but higher accuracy) ...")
print("My ensemble accuracy: " + str(accuracy))
print("")

print("Started Random Forest algorithm ...")
#Create a Random Forest Classifier
clf=RandomForestClassifier(n_estimators=20) #this is the number of decision trees that will be generated by Random Forest. The sample of the ensemble method used before

#Fit Random Forest to the training data
clf.fit(X_training,y_training)

#make the Random Forest prediction for each test sample. Example: class_predicted_rf = clf.predict([[3, 1, 2, 1, ...]]
#--> add your Python code here
for i, testSample in enumerate(dbTest):
    class_predicted_rf = clf.predict([testSample[0:-1]])

#compare the Random Forest prediction for each test sample with the ground truth label to calculate its accuracy
#--> add your Python code here
    if class_predicted_rf == testSample[-1]:
                random_forest_accuracy += 1

#printing Random Forest accuracy here
accuracy = random_forest_accuracy /  len(dbTest)
print("Random Forest accuracy: " + str(accuracy))

print("Finished Random Forest algorithm (much faster and higher accuracy!) ...")
