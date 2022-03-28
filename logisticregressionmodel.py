import numpy
import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

class logisticregressionmodel:
    
    def __init__(self, dataset) -> None:
        self.dataset1 = pd.read_csv(dataset)
    
    def features(self):
        return self.dataset1.columns
    
    def encodetext(self, list):
        self.dataset = pd.get_dummies(self.dataset1, columns = list)
        print(self.dataset)

    def updatex(self, list1):
        logisticregressionmodel.X = self.dataset[list1]
        # print(logisticregressionmodel.X.head())
    
    def updatey(self, list1):
        a = self.dataset[list1]
        b = numpy.round_(a, decimals=0, out=None)
        self.dataset[list1] = b.astype(int)
        logisticregressionmodel.y = self.dataset[list1]

    
    def trainmodel(self):
        logisticregressionmodel.X_train, logisticregressionmodel.X_test, logisticregressionmodel.y_train, logisticregressionmodel.y_test = train_test_split(logisticregressionmodel.X , logisticregressionmodel.y, test_size = 0.2, random_state = 1)
        logisticregressionmodel.classifier = LogisticRegression(random_state = 1) #, solver='lbfgs', max_iter=100
        logisticregressionmodel.classifier.fit(logisticregressionmodel.X_train, logisticregressionmodel.y_train)  
    
    def testmodel(self, list1):
        return logisticregressionmodel.classifier.predict([list1])

    def createpickle(self, name):
        pickle.dump(logisticregressionmodel.classifier, open('models/'+name+'.pkl','wb'))

    def accuracy(self):
        y_pred = logisticregressionmodel.classifier.predict(logisticregressionmodel.X_test)
        return accuracy_score(logisticregressionmodel.y_test, y_pred)

# model = logisticregressionmodel('AttendanceMarksSA.csv')
# features = model.features()
# print(features)
# model.updatex(['Attendance', 'MSE'])
# model.updatey(['ESE'])
# model.trainmodel()
# output = model.testmodel([75, 10])
# print(output)

# X = dataset.drop(columns = ['ESE'])
# y = dataset['ESE']



# pickle.dump(classifier, open('model.pkl','wb'))
# model = pickle.load(open('model.pkl','rb'))
# print(model.predict([[75, 10]]))

