import requests
import pandas as pd
import sys

INPUTFILE = sys.argv[1]

def get_hit(query):
    GTDB_URL = "https://api.gtdb.ecogenomic.org/search/gtdb?search={}&page=1&itemsPerPage=1&searchField=all&gtdbSpeciesRepOnly=false&ncbiTypeMaterialOnly=false".format(query)
    x = requests.get(GTDB_URL)
    if x.status_code == 200:
        hits = x.json()
        try:
            output_id = hits['rows'][0]['gid']
            if output_id.startswith('GCF'):
                output_id = 'RS_'+output_id
            elif output_id.startswith('GCA'):
                output_id = 'GB_'+output_id
            sys.stdout.write(query+'\t'+output_id+'\n')
            return output_id
        except:
            sys.stdout.write(query+'\t'+'None '+ query+'\n')
            return None
    else:
        sys.stdout.write(query+'\t'+'Failed '+ query+'\n')
        return None

def main():
    with open(INPUTFILE) as f:
        gca_ids = f.read().splitlines()
    for gca_id in gca_ids:
        get_hit(gca_id)
    
    # df = pd.read_csv(INPUTFILE,delimiter='\t')

    # df['GCF'] = df['GCA'].apply(get_hit)
    # df['GCA'].to_csv('GCAids.tsv',sep='\t',index=False)
    # df.to_csv('taxa_example2.tsv',sep='\t',index=False,headers=True)
    return

if __name__ == '__main__':
    main()