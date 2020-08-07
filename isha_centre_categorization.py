import csv
import requests

origin_map={"94117":"San Francisco","95050":"San Jose","94582":"San Ramon","95814":"Sacramento"}
origin_zip="94117|95050|94582|95814"

f_open=open("input_zip.csv","r")
csv_reader=csv.reader(f_open)

try:

    for row in csv_reader:
        dest_zip=row[0]
        url="https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={0}&destinations={1}&key=AIzaSyD53iK5pkHysczcQUJdzptxoKARux_pec8".format(origin_zip,dest_zip)
        response=requests.get(url)
        #print("full output of response {0}".format(response.json()))
        try:
            for i in range(0,len(response.json()['rows'])):
                print("dist={0}".format(response.json()['rows'][i]['elements'][0]['distance']['text']))
                if(i==0):
                    least_dist=float(response.json()['rows'][0]['elements'][0]['distance']['text'].split(" ")[0])
                    least_key=0
                    #print("least key when i=0 block: {0} and least distance : {1}".format(least_key,least_dist))
                    continue
                if (float(response.json()['rows'][i]['elements'][0]['distance']['text'].split(" ")[0]) < least_dist):
                    least_dist=float(response.json()['rows'][i]['elements'][0]['distance']['text'].split(" ")[0])
                    least_key=i
                    #print("least key when i!=0 block: {0} and least distance : {1}".format(least_key,least_dist))
            print("\n final least distance = {0} and least key = {1}".format(least_dist,least_key))
            f_out=open("Categorized_file.csv","a")
            f_out.write(dest_zip+","+origin_map[origin_zip.split("|")[least_key]]+"\n")
        except Exception as e:
            print("Exception occured while processing destination zip {0}. Error message is {1}".format(dest_zip,str(e)))
            continue
except Exception as e1:
    print("exception occured while processing destination zip {0}. Error message is {1}".format(dest_zip,str(e1)))
