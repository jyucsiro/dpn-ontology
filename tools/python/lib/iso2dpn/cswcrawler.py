from owslib.csw import CatalogueServiceWeb
import json, xmltodict
import sys
from pprint import pprint

#queries csw endpoint and returns json representation
#if MAX_RECORDS == -1, means process everything
def query_csw(outputfile, endpoint, MAX_RECORDS, chunk_size):
   csw = CatalogueServiceWeb(endpoint)
   #csw.getrecords2( maxrecords=chunk_size, outputschema='http://www.isotc211.org/2005/gmd',typenames='gmd:MD_Metadata' )
   csw.getrecords2(esn='full', maxrecords=chunk_size)
   #csw.getrecords2(esn='full', maxrecords=chunk_size, outputschema='http://www.isotc211.org/2005/gmd',typenames='gmd:MD_Metadata')
   #print csw.response
   #print csw.results 
   result_arr = []

   nextrecord = csw.results['nextrecord']
   returned = csw.results['returned']
   matches = csw.results['matches']
   while returned > 0:
      for rec in csw.records:
         #print(csw.records[rec].title)
         #print(csw.records[rec].identifier)
         #print(csw.records[rec].subjects)
         #print(csw.records[rec].format)
         #print(csw.records[rec].abstract)
         #if csw.records[rec].distribution and csw.records[rec].distribution.online:
         #   for d in csw.records[rec].distribution.online:
         #      print d.url
         #queries csw endpoint and returns json representation
         outputfile.write('\n') 
         record = jsonify_csw_record(csw.records[rec].__dict__)

         #curr = {'title': csw.records[rec].title, 'format': csw.records[rec].format, 'identifier': csw.records[rec].identifier, 'subjects': csw.records[rec].subjects, 'abstract': csw.records[rec].abstract}
         #result_arr.append(curr)


      print("Records count"  + str(len(result_arr)))
      print( "nextrecord: "  + str(nextrecord))
      print("nextrecord: "  + str(nextrecord))
      if MAX_RECORDS != -1 and len(result_arr) > MAX_RECORDS:
         break
      else:
         #csw.getrecords2( startposition=nextrecord, maxrecords=chunk_size, outputschema='http://www.isotc211.org/2005/gmd',typenames='gmd:MD_Metadata' )
         csw.getrecords2( esn='full', startposition=nextrecord, maxrecords=chunk_size)
         nextrecord = csw.results['nextrecord']
         returned = csw.results['returned']
         matches = csw.results['matches']
         print("nextrecord: "  + str(nextrecord))
         if csw.results['nextrecord'] == 0 \
            or csw.results['returned'] == 0 \
            or csw.results['nextrecord'] > csw.results['matches']:  # end the loop, exhausted all records
            break
   #return result_arr 
   return 

def jsonify_csw_record(record):
   curr = record
   xmlobj = curr.pop('xml', None)
   o = xmltodict.parse(xmlobj)
   curr = o

   #print json.dumps(o, indent=4, sort_keys=True)
   json.dump(curr, outputfile, sort_keys=True)


def serialize_md_distribution(obj):
   if isinstance(obj, Friend):
       serial = obj.name + "-" + str(obj.phone_num)
       return serial
   else:
       raise TypeError ("Type not serializable")


if __name__ == "__main__":

   filename = sys.argv[1]
   with open(filename) as data_file:    
     csw_catalogs = json.load(data_file)


   for c in csw_catalogs:
      outputfile = 'csw/' + c['id'] + ".json"
      print('processing ' + c['name'])

      #print json.dumps(result, indent=4, sort_keys=True)
      with open(outputfile, 'w') as outfile:
         result = query_csw(outfile, c['url'], -1, 10)
         #json.dump(result, outfile, indent=4, sort_keys=True)
   
   #result = query_csw('https://geonetwork.nci.org.au/geonetwork/srv/eng/csw', 1000, 20)
   #pprint(result)
   #with open('out/nci.json', 'w') as outfile:
   #   json.dump(result, outfile, indent=4, sort_keys=True)

   #result = query_csw('http://neii.bom.gov.au/services/catalogue/csw', 10, 20)
   #pprint(result)
   #print json.dumps(result, indent=4, sort_keys=True)
   #with open('out/neii.json', 'w') as outfile:
   #   json.dump(result, outfile, indent=4, sort_keys=True)
