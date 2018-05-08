import csv
import numpy
import math

class PNN:
    def __init__(self):
        #Import the Data
        self.data1 = open("C:/Users/tm/Documents/Spring 2012/302_pnn_homework/fold1.csv","r")
        self.dataReader1 = csv.reader(self.data1)
        self.data2 = open("C:/Users/tm/Documents/Spring 2012/302_pnn_homework/fold2.csv","r")
        self.dataReader2 = csv.reader(self.data2)
        self.data3 = open("C:/Users/tm/Documents/Spring 2012/302_pnn_homework/fold3.csv","r")
        self.dataReader3 = csv.reader(self.data3)
        self.data4 = open("C:/Users/tm/Documents/Spring 2012/302_pnn_homework/fold4.csv","r")
        self.dataReader4 = csv.reader(self.data4)
        self.data5 = open("C:/Users/tm/Documents/Spring 2012/302_pnn_homework/fold5.csv","r")
        self.dataReader5 = csv.reader(self.data5)


        #Import Data with unknown values
        self.dataTst = open("C:/Users/tm/Documents/Spring 2012/302_pnn_homework/testdata2.csv","r")
        self.dataReaderTst = csv.reader(self.dataTst)

        #Create Empty Lists to accept extracted Data
        self.dataRead1 = list()
        self.dataRead2 = list()
        self.dataRead3 = list()
        self.dataRead4 = list()
        self.dataRead5 = list()

        self.dataReadTst = list()
        
        for row in self.dataReader1:
            self.dataRead1.append(row)
                
        for row in self.dataReader2:
            self.dataRead2.append(row)
                
        for row in self.dataReader3:
            self.dataRead3.append(row)
                
        for row in self.dataReader4:
            self.dataRead4.append(row)
                
        for row in self.dataReader5:
            self.dataRead5.append(row)


        for row in self.dataReaderTst:
            self.dataReadTst.append(row)
        
        #Create a List to hold all five folds
        #self.allDataRead = list()
        self.allDataRead = (self.dataRead1, self.dataRead2, self.dataRead3, self.dataRead4, self.dataRead5)

        #Create an Array of All five data sets when running the PNN
        self.masterSamples = self.dataRead1 + self.dataRead2 + self.dataRead3 + self.dataRead4 + self.dataRead5
        self.masterSampleArray = numpy.array(self.masterSamples)

        #Turn the test data into an array
        self.testArray = numpy.array(self.dataReadTst)
        
        #Initialize the priors and losses
        self.l_A = 1
        self.h_A = 0.9
        self.l_B = 10
        self.h_A = 0.1


    #Use a function to create sample and training arrays
    def orgFld(self,t1, s1, s2, s3, s4): 
        self.dataSample = self.allDataRead[s1] + self.allDataRead[s2]+ self.allDataRead[s3]+self.allDataRead[s4]
        self.sampleArray = numpy.array(self.dataSample)
        self.trainArray = numpy.array(self.allDataRead[t1])



    #Return values of interest
    def getDataRead(self):
        return self.allDataRead

    def getSampleArray(self):
        return self.sampleArray

    def getDataSample(self):
        return self.dataSample

    

    #Create a function to train each trait
    def train(self,trait, start, stop, sigmaInterval):

        #Create a file to record accuracies for each training value
        accuracyRecord = open("Accuracy.csv", "w")

        #Cycle through a number of Sigmas
        for y in range(start,stop):
            sigma = y/float(sigmaInterval)
      
            #Create values to track the accuracy of the given sigma
            correct = 0
            incorrect = 0 
            total = 0

            #Create a for loop to cycle through all of the training pairs
            
            for t in range(len(self.trainArray)):
                #Create variables that can record each value to be added and the number by which it will be divided
                controlSumSingle = 0
                caseSumSingle = 0 
                numControls = 0
                numCases = 0

                #Cycle through all of the samples
                #print(len(self.sampleArray))
                for i in range(len(self.sampleArray)):
                    
                    #Calculate the value of the Summation function
                    difference = (float(self.sampleArray[i,trait]) - float(self.trainArray[t,trait]))
                    denominator = 2*(math.pow(sigma,2))
                    numerator = -(math.pow(difference,2))
                    avgDistance = math.exp(numerator/denominator)

                    
                    if (int(self.sampleArray[i,3])) == 0:
                        #If it is a control, add it to the control summation function
                        controlSumSingle += avgDistance
                        numControls+=1
        
            
                    else:
                        #If it is a case, add it to the case summation function
                        caseSumSingle += avgDistance
                        numCases+=1
        

                #Divide by the number of samples
                #print("numCont",numControls)
                #print("numCase",numCases)
                f_A = controlSumSingle/numControls
                f_B = caseSumSingle/numCases
        
                #Multiply By the Losses and Priors
                controlOutput = (f_A)*(self.l_A)*(self.h_A)
                caseOutput = (f_B)*(self.l_A)*(self.h_A)

                #print("Cont", controlOutput)
                #print("Case", caseOutput)


                #Check the Accuracy
                if controlOutput > caseOutput:
                    result = 0
                else:
                    result = 1

                if result == int(self.trainArray[t,3]):
                    correct +=1

                else:
                    incorrect +=1


                total+=1


            accuracy = (correct/float(total))
            accuracyRecord.write(str(accuracy)+"\n")

        accuracyRecord.close


    #Run the PNN
    def runFoldsPNN(self, sigmaOne, sigmaTwo, sigmaThree):
        sigmas = (sigmaOne, sigmaTwo, sigmaThree)
        resultRecord = open("resultRecord.csv", "w")
        #Create A file to cycle through all of the accuracies of each training value
        accuracyRecord = open("Accuracy.csv", "w")

        correct = 0
        incorrect = 0 
        total = 0
                        
        #Create a for loop to cycle through all of the training pairs
        for t in range(len(self.trainArray)):
            #When moving onto to next training pair and reset the counters and summations
            #Create variables that can record each value to be added and the number by which it will be divided
            controlSumSingle = 0
            caseSumSingle = 0 
            numControls = 0
            numCases = 0

            #Go through each sigma for each training pair
            for y in range(3):
                sigma = sigmas[y]
                #Cycle through all of the samples for every sigma at each training pair
                #print(len(self.sampleArray))
                for i in range(len(self.sampleArray)):
                    
                    #Calculate the value of the Summation function For the Given training pair
                    difference = (float(self.sampleArray[i,y]) - float(self.trainArray[t,y]))
                    denominator = 2*(math.pow(sigma,2))
                    numerator = -(math.pow(difference,2))
                    avgDistance = math.exp(numerator/denominator)

                    
                    if (int(self.sampleArray[i,3])) == 0:
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
            controlOutput = (f_A)*(self.l_A)*(self.h_A)
            caseOutput = (f_B)*(self.l_A)*(self.h_A)

            #print("Cont", controlOutput)
            #print("Case", caseOutput)
            

            #Chck the Accuracy
            if controlOutput > caseOutput:
                result = 0
            else:
                result = 1

            if result == int(self.trainArray[t,3]):
                correct +=1

            else:
                incorrect +=1


            total+=1



            resultRecord.write(str(result)+"\n")

        print(correct)
        print(total)
        print(correct/float(total))
        accuracyRecord.close
        resultRecord.close
        
    def masterRunPNN(self, sigmaOne, sigmaTwo, sigmaThree):
        sigmas = (sigmaOne, sigmaTwo, sigmaThree)
        resultRecord = open("resultRecord.csv", "w")

        correct = 0
        incorrect = 0 
        total = 0
                        
        #Create a for loop to cycle through all of the training pairs
        for t in range(len(self.testArray)):
            #When moving onto to next training pair and reset the counters and summations
            #Create variables that can record each value to be added and the number by which it will be divided
            controlSumSingle = 0
            caseSumSingle = 0 
            numControls = 0
            numCases = 0

            #Go through each sigma for each training pair
            for y in range(3):
                sigma = sigmas[y]
                #Cycle through all of the samples for every sigma at each training pair
                #print(len(self.masterSampleArray))
                for i in range(len(self.masterSampleArray)):
                    
                    #Calculate the value of the Summation function For the Given training pair
                    difference = (float(self.masterSampleArray[i,y]) - float(self.testArray[t,y]))
                    denominator = 2*(math.pow(sigma,2))
                    numerator = -(math.pow(difference,2))
                    avgDistance = math.exp(numerator/denominator)

                    
                    if (int(self.masterSampleArray[i,3])) == 0:
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
            controlOutput = (f_A)*(self.l_A)*(self.h_A)
            caseOutput = (f_B)*(self.l_A)*(self.h_A)

            #print("Cont", controlOutput)
            #print("Case", caseOutput)
            

            #Compare the outputs
            if controlOutput > caseOutput:
                result = 0
            else:
                result = 1


            total+=1

            resultRecord.write(str(result)+"\n")

        
        print(total)

        resultRecord.close
        








