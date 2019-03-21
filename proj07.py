'''Introductory information goes here.'''

import pylab   # needed for plotting

STATUS = ['Approved','Denied','Settled'] 

def open_file():    
   '''Opens the file and only allows it to work if the file is found, otherwise reprompts'''
   open_file = input("Please enter a file name: ")
   while True:
        try:       
            return open(open_file,'r')
        except FileNotFoundError:
            #print("File not found.")
            open_file = input("File not found. Please enter a valid file name: ")
           

def read_file(fp):
    '''Docstring goes here.'''
    fp.readline()
    list_TSA = []  

    for line in fp:
        line = line.split(",")
        date_received = line[1] 
        airport_name = line[4]
        claim_amount = line[9].strip("$").replace(";","")
        status = line[10]
        close = line[11].strip("$").replace(";","")
        if date_received == "" or airport_name == "" or claim_amount == "" or status == "" or close == "":
            continue
        
        year = int(date_received.split("-")[2])
        if year > 9 or year < 2:
            continue 
    
        list_TSA.append(tuple([date_received,airport_name,float(claim_amount),status,float(close)]))
               
    return list_TSA
def process(data):
    '''Docstring goes here.'''
    approved = 0
    approved1 = 0
    settled = 0
    settled1 = 0
    denied = 0 
    closed_amount = 0
    closed_approved = 0
    closed_settled = 0
    max_claim = 0
    max_claim_airport = 0
    list1 = [0]*8
    list2 = [0]*8
    list3 = [0]*8
    
    for line in data:
        if line[3].lower().strip() == "approved":
            approved += 1
            
            if line[2] > max_claim:
                max_claim = line[2]
                max_claim_airport = line[1]
            year = int(line[0].split("-")[2])
            if line[4] != 0:
                closed_approved += line[4]
                approved1 += 1
                closed_amount += line[4]
                list2[year-2] += 1
                list1[year-2] += 1
                
        elif line[3].lower().strip() == "settled":
            settled += 1
            
            if line[2] > max_claim:
                max_claim = line[2]
                max_claim_airport = line[1]
            year = int(line[0].split("-")[2])
            if line[4] != 0:
                closed_settled += line[4]
                settled1 += 1
                closed_amount += line[4]
                list2[year-2] += 1
                list1[year-2] += 1
                
        elif line[3].lower().strip() == "denied":
            denied += 1
            year = int(line[0].split("-")[2])
            if line[2] > max_claim:
                max_claim = line[2]
                max_claim_airport = line[1]
            list3[year-2] += 1
            list1[year-2] += 1     
                 
    total = approved + settled + denied
    average = ((closed_approved + closed_settled)/(approved1+settled1))
      
    return list1,list2,list3,total,average,max_claim,max_claim_airport
    
   
def display_data(tup):
    '''Docstring goes here.'''
    
    print("TSA Claims Data: 2002 - 2009")
    print()
    print("N = {:<,d}   ".format(tup[3]))
    print()
    print("{:<8s}{:>8s}{:>8s}{:>8s}{:>8s}{:>8s}{:>8s}{:>8s}{:>8s}".format(" ",'2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009'))
    print("{:<8s}{:>8,d}{:>8,d}{:>8,d}{:>8,d}{:>8,d}{:>8,d}{:>8,d}{:>8,d}".format("Total",tup[0][0],tup[0][1],tup[0][2],tup[0][3],tup[0][4],tup[0][5],tup[0][6],tup[0][7]))
    print("{:<8s}{:>8,d}{:>8,d}{:>8,d}{:>8,d}{:>8,d}{:>8,d}{:>8,d}{:>8,d}".format("Settled",tup[1][0],tup[1][1],tup[1][2],tup[1][3],tup[1][4],tup[1][5],tup[1][6],tup[1][7]))
    print("{:<8s}{:>8,d}{:>8,d}{:>8,d}{:>8,d}{:>8,d}{:>8,d}{:>8,d}{:>8,d}".format("Denied",tup[2][0],tup[2][1],tup[2][2],tup[2][3],tup[2][4],tup[2][5],tup[2][6],tup[2][7]))
    print()
def plot_data(accepted_data, settled_data, denied_data):
    '''Plot the three lists as bar graphs.'''

    X = pylab.arange(8)   # create 8 items to hold the data for graphing
    # assign each list's values to the 8 items to be graphed, include a color and a label
    pylab.bar(X, accepted_data, color = 'b', width = 0.25, label="total")
    pylab.bar(X + 0.25, settled_data, color = 'g', width = 0.25, label="settled")
    pylab.bar(X + 0.50, denied_data, color = 'r', width = 0.25,label="denied")

    # label the y axis
    pylab.ylabel('Number of cases')
    # label each bar of the x axis
    pylab.xticks(X + 0.25 / 2, ("2002","2003","2004","2005","2006","2007","2008","2009"))
    # create a legend
    pylab.legend(loc='best')
    # draw the plot
    pylab.show()
    # optionally save the plot to a file; file extension determines file type
    # pylab.savefig("plot.png")
    
def main():
    '''Docstring goes here.'''
    fp = open_file()
    data = read_file(fp)
    processed = process(data)
    accepted_data = processed[0]
    settled_data = processed[1]
    denied_data = processed[2]
    display_data(processed)
    print("Average settlement: ${:.2f}    ".format(processed[4]))
    print("The maximum claim was ${:,.2f}".format(processed[5]),"at",processed[6],"Airport")
    
    plot_input = input("Plot data (yes/no): ")
    if plot_input.lower() == "yes":
        plot = plot_data(accepted_data, settled_data, denied_data)
        print(plot)



if __name__ == "__main__":
    main()