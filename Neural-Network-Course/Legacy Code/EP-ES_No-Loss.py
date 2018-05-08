import numpy
import math
import csv
import random


#A -> control
#B -> case

class PNNTrain:
    def __init__(self):
        #Run the command to import the data
        self.allData = self.importData()
        #Initialize the Five Folds
        self.Fold1 = self.allData[0]
        self.Fold2 = self.allData[1]
        self.Fold3 = self.allData[2]
        self.Fold4 = self.allData[3]
        self.Fold5 = self.allData[4]
        
        #Create an Array of all the data
        self.allDataArray = numpy.array(self.allData)

        #Create an empty list for the sample data and training data
        self.sampleArray = []
        self.trainArray = []

        #Create Values for the priors and losses
        self.lA = 1
        self.lB = 1
        self.hA = (1-(44/float(102)))
        self.hB = 44/float(102)

        #Create an empty list of working sigmas for each 
        self.sigmaList = list()

        #Create a List of 100 PNNs
        self.hundredPNNs = self.create100PNNs()
        #Create a List of Scores
        self.scoreList = list()
        self.bestScore = 0
        self.avgScore = 0

    def setLoss(self, lA, lB):
        self.lA =lA
        self.lB =lB
    
    def importData(self):
        #Open the files
        self.imFold1 = open("C:/Users/tm/Documents/Spring 2012/302_EP-ES/EP_fold1.csv", "r")
        self.imFold1Reader = csv.reader(self.imFold1)
        self.imFold2 = open("C:/Users/tm/Documents/Spring 2012/302_EP-ES/EP_fold2.csv", "r")
        self.imFold2Reader = csv.reader(self.imFold2)
        self.imFold3 =open("C:/Users/tm/Documents/Spring 2012/302_EP-ES/EP_fold3.csv", "r")
        self.imFold3Reader = csv.reader(self.imFold3)
        self.imFold4 =open("C:/Users/tm/Documents/Spring 2012/302_EP-ES/EP_fold4.csv", "r")
        self.imFold4Reader = csv.reader(self.imFold4)
        self.imFold5 =open("C:/Users/tm/Documents/Spring 2012/302_EP-ES/EP_fold5.csv", "r")
        self.imFold5Reader = csv.reader(self.imFold5)

        
        #Read The files
        self.imFold1Read = list()
        self.imFold2Read = list()
        self.imFold3Read = list()
        self.imFold4Read = list()
        self.imFold5Read = list()
        

        for row in self.imFold1Reader:
            self.imFold1Read.append(row)
        for row in self.imFold2Reader:
            self.imFold2Read.append(row)
        for row in self.imFold3Reader:
            self.imFold3Read.append(row)
        for row in self.imFold4Reader:
            self.imFold4Read.append(row)
        for row in self.imFold5Reader:
            self.imFold5Read.append(row)

        return (self.imFold1Read, self.imFold2Read, self.imFold3Read, self.imFold4Read, self.imFold5Read)

    def orgFold(self, t, s1, s2, s3, s4):
        dataSample = self.allData[s1]+ self.allData[s2] + self.allData[s3]+ self.allData[s4]
        self.sampleArray = numpy.array(dataSample)
        self.trainArray = numpy.array(self.allData[t])

    #Create a List of 100 PNN's
    def create100PNNs(self):
        initialScore = 0
        numSigmas = 6
        botRange = 0.00001
        topRange = 0.4

        masterPnn = list()
        for i in range (50):
            singlePnn = list()
            singlePnn.append(initialScore)
            for i in range(numSigmas):
                rand = random.uniform(botRange, topRange)
                singlePnn.append(rand)
            masterPnn.append(singlePnn)
        masterPnnArray = numpy.array(masterPnn)
        return masterPnnArray

    def run100PNNs(self, numCycles):
        cycles = numCycles
        for j in range(cycles):
            self.scoreList = list()
            for i in range(len(self.hundredPNNs)):
                s1 = self.hundredPNNs[i,1]
                s2 = self.hundredPNNs[i,2]
                s3 = self.hundredPNNs[i,3]
                s4 = self.hundredPNNs[i,4]
                s5 = self.hundredPNNs[i,5]
                s6 = self.hundredPNNs[i,6]
                self.sigmaList = (s1, s2, s3, s4, s5, s6)
                newScore = self.runPNN()
                self.hundredPNNs[i,0] = newScore
                self.scoreList.append(newScore)
            #print(self.scoreList)
            self.trimTheFat()


    def trimTheFat(self):
        medianScore = numpy.median(self.scoreList)
        self.bestScore = min(self.scoreList)
        self.avgScore = medianScore
        trimmedPNNs = list()
        i = 0
        while len(trimmedPNNs) < 25 and i <50:
            if self.hundredPNNs[i,0] < medianScore:
                singlePNN = self.hundredPNNs[i]
                trimmedPNNs.append(singlePNN)
            i+=1
        i = 0
        while len(trimmedPNNs) < 25 and i <50:
            if self.hundredPNNs[i,0] == medianScore:
                singlePNN = self.hundredPNNs[i]
                trimmedPNNs.append(singlePNN)
            i+=1
        
        trimmedArray = numpy.array(trimmedPNNs)
        self.mutateTheBest(trimmedArray)

    def mutateTheBest(self, trimmedArray):
        numSigmas = 6
        rebuildList = list(trimmedArray)
        for j in range(25):
            singlePNN = list()
            singlePNN.append(0)
            fixed = (1/math.sqrt(2 * numSigmas))*random.normalvariate(0,1)
            for i in range (1,7):
                cauchy = numpy.random.standard_cauchy() 
                v = random.uniform(0.009, 0.020)
                x = trimmedArray[j,i]
                rndm = (1/math.sqrt(2*(math.sqrt(numSigmas))))*random.normalvariate(0,1)
                v_prime= v*math.exp(fixed+rndm)
                x_prime= x + (cauchy * v_prime)
                singlePNN.append(abs(x_prime))
            rebuildList.append(singlePNN)
        self.hundredPNNs = numpy.array(rebuildList)
                          
            
    def runPNN(self):
        total = 0
        incorrect = 0
        falsePositive = 0
        falseNegative = 0
        score = 0
        fPWeight = 1
        fNWeight = 3
        casePos = 6
        
                        
        #Create a for loop to cycle through all of the training pairs
        for t in range(len(self.trainArray)):
            #When moving onto to next training pair and reset the counters and summations
            #Create variables that can record each value to be added and the number by which it will be divided
            controlSumSingle = 0
            caseSumSingle = 0 
            numControls = 0
            numCases = 0
            #print("B")
            #Go through each sigma for each training pair
            for y in range(casePos):
                sigma = self.sigmaList[y]
                #Cycle through all of the samples for every sigma at each training pair
                #print("C")
                for i in range(len(self.sampleArray)):
                    
                    #Calculate the value of the Summation function For the Given training pair
                    difference = (float(self.sampleArray[i,y]) - float(self.trainArray[t,y]))
                    denominator = 2*(math.pow(sigma,2))
                    numerator = -(math.pow(difference,2))
                    avgDistance = math.exp(numerator/denominator)

                    
                    if (int(self.sampleArray[i,casePos])) == 0:
                        #If it is a control, add it to the control summation function
                        controlSumSingle += avgDistance
                        numControls+=1
        
            
                    else:
                        #If it is a case, add it to the case summation function
                        caseSumSingle += avgDistance
                        numCases+=1

                    #print("D")
            #Once all of the sigmas for all of the samples have been cycled through
            #Divide by the number of samples
            f_A = controlSumSingle/numControls
            f_B = caseSumSingle/numCases
            
            #Multiply By the Losses and Priors
            controlOutput = (f_A)*(self.lA)*(self.hA)
            caseOutput = (f_B)*(self.lB)*(self.hB)


            #Make Decision. Control or Case?
            if controlOutput > caseOutput:
                result = 0
            else:
                result = 1
        
            #Check if false positive
            if result == 1 and result != int(self.trainArray[t,casePos]):
                falsePositive +=1
                incorrect+=1
                
            #Check if false negative
            if result == 0 and result != int(self.trainArray[t,casePos]):
                falseNegative +=1
                incorrect+=1

            total+=1
        #print("incorrect",incorrect)
        #print("total",total)

        score += (((fPWeight*falsePositive)+(fNWeight*falseNegative))*(float(incorrect)/total))
        
        return score
        

        
    #Create functions to get access to data
    def getAllData(self):
        return self.allData
    
    def getDataSample(self):
        return self.dataSample

    def getSampleArray(self):
        return self.sampleArray

    def getTrainArray(self):
        return self.trainArray

    def get100PNNs(self):
        return self.hundredPNNs

    def getBestScore(self):
        return self.bestScore

    def getAvgScore(self):
        return self.avgScore



class PNNValidate:
    def __init__(self):
        #Run the command to import the data
        self.allData = self.importData()
        #Initialize the Five Folds
        self.Fold1 = self.allData[0]
        self.Fold2 = self.allData[1]
        self.Fold3 = self.allData[2]
        self.Fold4 = self.allData[3]
        self.Fold5 = self.allData[4]
        
        #Create an Array of all the data
        self.allDataArray = numpy.array(self.allData)

        #Create an empty list for the sample data and training data
        self.sampleArray = []
        self.trainArray = []

        #Create Values for the priors and losses
        self.lA = 1
        self.lB = 1
        self.hA = (1-(44/float(102)))
        self.hB = 44/float(102)

        #Create an empty list of working sigmas for each 
        self.sigmaList = list()


    def setLoss(self, lA, lB):
        self.lA =lA
        self.lB =lB
    
    def importData(self):
        #Open the files
        self.imFold1 = open("C:/Users/tm/Documents/Spring 2012/302_EP-ES/EP_fold1.csv", "r")
        self.imFold1Reader = csv.reader(self.imFold1)
        self.imFold2 = open("C:/Users/tm/Documents/Spring 2012/302_EP-ES/EP_fold2.csv", "r")
        self.imFold2Reader = csv.reader(self.imFold2)
        self.imFold3 =open("C:/Users/tm/Documents/Spring 2012/302_EP-ES/EP_fold3.csv", "r")
        self.imFold3Reader = csv.reader(self.imFold3)
        self.imFold4 =open("C:/Users/tm/Documents/Spring 2012/302_EP-ES/EP_fold4.csv", "r")
        self.imFold4Reader = csv.reader(self.imFold4)
        self.imFold5 =open("C:/Users/tm/Documents/Spring 2012/302_EP-ES/EP_fold5.csv", "r")
        self.imFold5Reader = csv.reader(self.imFold5)

        
        #Read The files
        self.imFold1Read = list()
        self.imFold2Read = list()
        self.imFold3Read = list()
        self.imFold4Read = list()
        self.imFold5Read = list()
        

        for row in self.imFold1Reader:
            self.imFold1Read.append(row)
        for row in self.imFold2Reader:
            self.imFold2Read.append(row)
        for row in self.imFold3Reader:
            self.imFold3Read.append(row)
        for row in self.imFold4Reader:
            self.imFold4Read.append(row)
        for row in self.imFold5Reader:
            self.imFold5Read.append(row)

        return (self.imFold1Read, self.imFold2Read, self.imFold3Read, self.imFold4Read, self.imFold5Read)

    def orgFold(self, t, s1, s2, s3, s4):
        dataSample = self.allData[s1]+ self.allData[s2] + self.allData[s3]+ self.allData[s4]
        self.sampleArray = numpy.array(dataSample)
        self.trainArray = numpy.array(self.allData[t])

    def setSigmaList(self, s1, s2, s3, s4, s5, s6):
        self.sigmaList = (s1, s2, s3, s4, s5, s6)

    def runPNN(self):
        caseRecord = open("caseRec.csv", "w")
        #Create A file to cycle through all of the accuracies of each training value
        controlRecord = open("controlRec.csv", "w")
        correctRec = open("correctRec.csv", "w")

        correct = 0
        incorrect = 0 
        total = 0
        casePos = 6
                        
        #Create a for loop to cycle through all of the training pairs
        for t in range(len(self.trainArray)):
            #When moving onto to next training pair and reset the counters and summations
            #Create variables that can record each value to be added and the number by which it will be divided
            controlSumSingle = 0
            caseSumSingle = 0 
            numControls = 0
            numCases = 0

            #Go through each sigma for each training pair
            for y in range(casePos):
                sigma = self.sigmaList[y]
                #Cycle through all of the samples for every sigma at each training pair
                #print(len(self.sampleArray))
                for i in range(len(self.sampleArray)):
                    
                    #Calculate the value of the Summation function For the Given training pair
                    difference = (float(self.sampleArray[i,y]) - float(self.trainArray[t,y]))
                    denominator = 2*(math.pow(sigma,2))
                    numerator = -(math.pow(difference,2))
                    avgDistance = math.exp(numerator/denominator)

                    
                    if (int(self.sampleArray[i,casePos])) == 0:
                        #If it is a control, add it to the control summation function
                        controlSumSingle += avgDistance
                        numControls+=1
        
            
                    else:
                        #If it is a case, add it to the case summation function
                        caseSumSingle += avgDistance
                        numCases+=1


            #Once all of the sigmas for all of the samples have been cycled through
            #Divide by the number of samples
            #print("numCont",numControls)
            #print("numCase",numCases)
            f_A = controlSumSingle/numControls
            f_B = caseSumSingle/numCases
        
            #Multiply By the Losses and Priors
            controlOutput = (f_A)*(self.lA)*(self.hA)
            caseOutput = (f_B)*(self.lB)*(self.hB)

            #print("Cont", controlOutput)
            #print("Case", caseOutput)
            

            #Chck the Accuracy
            if controlOutput > caseOutput:
                result = 0
            else:
                result = 1

            if result == int(self.trainArray[t,casePos]):
                correct +=1

            total+=1

            caseRecord.write(str(caseOutput)+"\n")
            controlRecord.write(str(controlOutput) + "\n")
            correctRec.write(str(self.trainArray[t,casePos]) + "\n")


        #DEBUG: print(correct)
        #DEBUG: print(total)
        print(correct/float(total))
        controlRecord.close
        caseRecord.close
        correctRec.close

    #Create functions to get access to data
    def getAllData(self):
        return self.allData
    
    def getDataSample(self):
        return self.dataSample

    def getSampleArray(self):
        return self.sampleArray

    def getTrainArray(self):
        return self.trainArray





        






        
