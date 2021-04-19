import urllib.request
import json
import ast
import argparse

"""

## Since the cdxj API does not work correctly we cannot use these parameters

parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('-p','--path', help='Localization of the file with URLs to patch (without https. and www.)(e.g., publico.pt)', default= "urls_to_patch.txt")
parser.add_argument('-d','--destination', help='Localization of the output file', default= "output.txt")
parser.add_argument('-f','--from', help='Timestamp From', type=int, default=201700)
parser.add_argument('-t','--to', help='Timestamp To', type=int, default=201900)
args = vars(parser.parse_args())
"""

########################################################################

###1. Get all the digests from the URLs within a specific timestamp.

list_digest_publico = []
#1. run the command --> find /data/indexes_cdx -type f -exec ./sgrep "pt,publico," {} \; > all_pulico_pt.txt
with open("all_pulico_pt.txt") as file:
    for line in file:   
        try:
            list_line = line.split(' ')
            #Restrict URLs by the timestamp
            if int(list_line[1][:6]) > 201700 and int(list_line[1][:6]) < 201900:
                string = ' '.join(list_line[2:]).replace("\n", "").replace("\t", "")
                dic_string = ast.literal_eval(string)
                list_digest_publico.append(dic_string["digest"])
        except:
            # Problems with the cdxj (i.e., #issue1093)
            continue
            #import pdb;pdb.set_trace()


list_digest_sapo = []
#1. run the command --> find /data/indexes_cdx -type f -exec ./sgrep "pt,sapo)/noticias" {} \; > all_sapo_noticia_pt.txt
with open("all_sapo_noticia_pt.txt") as file:
    for line in file:   
        try:
            list_line = line.split(' ')
            #Restrict URLs by the timestamp
            if int(list_line[1][:6]) > 201700 and int(list_line[1][:6]) < 201900:
                string = ' '.join(list_line[2:]).replace("\n", "").replace("\t", "")
                dic_string = ast.literal_eval(string)
                list_digest_sapo.append(dic_string["digest"])
        except:
            #Problems with the cdxj (i.e., #issue1093)
            continue
            #import pdb;pdb.set_trace()

########################################################################

###2. Check if the digestion of the AI are the same as those retrive from Arquivo.pt.

list_digest_url_publico_ia = []
list_digest_url_sapo_ia = []
with open("links_to_patching.txt", "w") as output:
    #http://web.archive.org/cdx/search/cdx?url=sapo.pt/noticias/*&output=json&filter=statuscode:200&from=2017&to=2018
    data_json = json.load(open("publico_IA_2017_2018.txt"))
    first = True
    for elem in data_json:
        if not first:
            if elem[5] not in list_digest_publico:
                #Put the parameters URL in this verification is just a double check
                digest_url_ia = elem[5] + elem[2]
                if digest_url_ia not in list_digest_url_publico_ia:
                    output.write("https://preprod.arquivo.pt/noFrame/patching/record/" + elem[1] + "/" + elem[2] + "\n")
                    list_digest_url_publico_ia.append(digest_url_ia)
        first = False

    #########################
    #http://web.archive.org/cdx/search/cdx?url=sapo.pt/noticias/*&output=json&filter=statuscode:200&from=2017&to=2018
    data_json = json.load(open("sapo_noticia_IA_2017_2018.txt"))
    first = True
    for elem in data_json:
        if not first:
            if elem[5] not in list_digest_sapo:
                #Put the parameters URL in this verification is just a double check
                digest_url_ia = elem[5] + elem[2]
                if digest_url_ia not in list_digest_url_sapo_ia:
                    output.write("https://preprod.arquivo.pt/noFrame/patching/record/" + elem[1] + "/" + elem[2] + "\n")
                    list_digest_url_sapo_ia.append(digest_url_ia)
        first = False