import csv
import os, os.path

offers_list = [ [266, "uni1" ,"empresa1", 3, 10000, "pais1", "provincia1", "ciudad1" , "decripcion1" , True, ["carrera1", "carrera2", "carrera2"]] ]


def offers_csv(offers):

    if os.path.isfile('offers.csv'):
        print ("File offers.csv updated")
    else:
        print ("File  DO NOT exist, let's create offers.csv")
        os.system("touch offers.csv")

    with open('offers.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "University", "Enterprise", "Months", "Salary", "Country", "Province", "City", "Description", "Immediate"])
        for o in offers:
            writer.writerow([o[0], o[1], o[2], o[3], o[4], o[5], o[6], o[7], o[8], o[9]])


def degrees_csv(offers):

    if os.path.isfile('degrees.csv'):
        print ("File degrees.csv updating")
    else:
        print ("File  DO NOT exist, lets create degrees.csv")
        os.system("touch degrees.csv")

    with open('degrees.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "idOferta", "Nombre"])
        i = 0
        for o in offers:
            for d in o[10]:
                i = i+1
                writer.writerow([i, o[0], d])