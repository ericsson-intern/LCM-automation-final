
from Pom.util import PomEditor
from Gerrit.util import *
from Logging import config


import click
import twiggy
from urlparse import urlparse
import csv
import os
import shutil
import json
import random


config.clear()
config.setup()

Log = twiggy.log

def empty(arg):
    pass

msg = {
        'a': "CAUTION : Should non-ref local-artifact get updated version?",
        'b': "Checking POM for modification in artifacts..",
        'c+': "\t[Yes]: requires file rewriting",
        'c-': "\t[No]: does not require file rewriting",
        'd': "[already updated]"

}   


cmd = {
        'info': Log.info,
        'confirm':click.confirm,
        'pause':raw_input,
        'warn' : Log.warning,
        'file': Log.name('file').notice,
        'repo': Log.name('repo').notice,
        'commit':Log.notice,
        'heads': empty,
}

# ////////////////////////////// UTILS /////////////////////////////


COMMIT_FILE = os.path.abspath('.COMMIT_MSG')
print(COMMIT_FILE)

# //////////////////////////////////////////// COMMITS //////////////////////////////////////////////

def prepare_commit(f_path):
    COMMIT = []
    clog_file = config.LOG_FILES['commit']
    # clog_file = config.LOG_FILES['runtime']

    with open(clog_file,'r') as f:
        l = f.readlines()
        for i in l:
            line = ''
            msg = i.split('|')
            dtype = msg[0].split(':')[-1]
            if dtype == 'repo':
                pass
            elif dtype == 'file':
                line = msg[1]
            else:
                line = '    '+msg[1]
            COMMIT.append('  '+line)

    with open(f_path, 'w') as f:
        f.write(''.join(COMMIT)) 
    print('prepared commit....')
# //////////////////////////////////////////// COMMITS //////////////////////////////////////////////


def tsv_util(file):
    rows=[]
    with open(file) as f:
        r = csv.DictReader(f, dialect='excel-tab')
        for row in r:
            rows.append(row)
    return rows


def csv_util(file):
    rows=[]
    with open(file) as f:
        r = csv.reader(f)
        fields = r.next()
        headers = ['groupId','version']
        
        for row in r:
            artifact = {}
            for i in headers:
                artifact[i] = row[fields.index(i)]
            rows.append(artifact)
    pass
    return rows
    
    # print("total count of artifacts: %s \ncsv_file: %s" % (str(len(rows)), str(file)) )
    

def url_build(protocol,port,base,path):
    return str(protocol +'://' + base + ':'+ str(port) +'/' + path)
    

class ppcli:
    def __init__(self):
        self.chars = ['=','~','/','*']
        self.trails = {}
        for c in self.chars:
            self.trails[c] = ''.join([c for i in xrange(128)])
    
    def tag(self, msg, c, offset = 36):
        off = str('%.'+str(offset)+'s')
        v = str(off + ' %s ' + off)
        return v % (self.trails[c],msg,self.trails[c])

pp = ppcli()

print(cmd['heads'](pp.tag('pulkit','=',32)))
            



# //////////////////////// DRIVER CODE /////////////////////////////



def update_artifacts(CACHE=None, ARTIFACTS_CSV=None, REPO_URL=None, BRANCH = None, COMMIT = None):
    

    config.clear()
    #import artifacts
    try:
        ARTIFACTS = csv_util(ARTIFACTS_CSV)
    except:
        raise Exception("Please provide a valid csv file")

    try:
        os.makedirs(CACHE)
    except:
        pass


    if not COMMIT:
        COMMIT = ''
    else:
        COMMIT = ': ' + COMMIT

    ## default Params
    if not CACHE:
        CACHE= os.path.abspath(os.path.join(os.path.dirname(__name__),'./.gerrit'))
   
    #==============#
    if not ARTIFACTS_CSV:
        ARTIFACTS_CSV = os.path.abspath(os.path.join(os.path.dirname(__name__),'artifacts.csv'))
    #==============#
    
    # cmd['heads'](pp.tag('GIT','='))
    adaptor = GitAdaptor(REPO_URL, CACHE)
    cmd['repo'](REPO_URL)
    REPO = adaptor.CACHE 

    for root, dirs, files in os.walk(REPO, topdown=True):
        git_ignore(dirs)
        for f in files:
            if f.endswith('pom.xml'):
                f_loc = os.path.join(root,f)
                
                rel_loc = os.path.relpath(f_loc,REPO)
                print(rel_loc)
                abs_loc = os.path.abspath(f_loc)
                POM = PomEditor(abs_loc)

                print('------------')
                for artifact in ARTIFACTS:
                    name = artifact['groupId']
                    new_v = artifact['version'] 
                    POM.update_artifact(name, new_v)
                    pass

                if POM.STATUS:
                    cmd['file']('$%s' % str(rel_loc)) 

                POM.save()
    


    config.commit_file.close()
    prepare_commit(COMMIT_FILE)
    adaptor.fcommit("Automated StepUp" + str(COMMIT),f_path = COMMIT_FILE)
    config.clear()
    config.commit_file._open()
    pass

    return adaptor
    

