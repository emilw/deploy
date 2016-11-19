import os
import git
import json
import datetime
import urllib2

class Config(object):
    def __init__(self, jsonData):
        self.__dict__ = jsonData

class DeployConfig:
    def __init__(self, sourceURL, created, updated, versiontag):
        self.SourceURL = sourceURL
        self.Created = created.isoformat()
        self.Updated = updated.isoformat()
        self.VersionTag = versiontag
def jdefault(o):
    return o.__dict__

def log(text):
    print(text)

def writeJson(object, path):
    with open(path, 'w') as fp:
        json.dump(object, fp, default=jdefault, indent=4)

def createDeploymentIfNotExists(gitURL):
    localFolder = gitURL.split("/")[-1].split(".")[0]
    localFolder = "deployments/" + localFolder
    log(localFolder)
    if os.path.exists(localFolder):
        log("Deployment exists, updating...")
        g = git.cmd.Git(localFolder)
        g.pull()
        log("...Done")
    else:
        log("The deployment do not exists, downloading....")
        git.Repo.clone_from(gitURL+".git", localFolder)
        log("....Done")
        #os.makedirs(localFolder)
    
    return localFolder

def getConfiguration(deployPath):
    log("Starting to read configuration from deployment: " + deployPath)
    configFileContent = open(deployPath+"/deploy.json")
    data = json.load(configFileContent)
    log("deploy.json is loaded")
    conf = Config(data)
    return conf

def setupConfig(conf, gitURL):
    log("Starting to configure: " + conf.name)
    home = os.path.expanduser("~")
    deployConfPath = home+"/.deploy"
    deployConfigs = []
    if(not os.path.exists(deployConfPath)):
        log(".deploy will be created")
        d = DeployConfig(gitURL, datetime.datetime.now(),datetime.datetime.now(),"")

        deployConfigs.append(d)
        writeJson(deployConfigs, deployConfPath)
    else:
        deployConfigs = json.load(deployConfPath)
    

gitURL = "https://github.com/emilw/deployTest"


try:
    deployJsonURL = gitURL+"/blob/master/deploy.json"
    status = urllib2.urlopen(deployJsonURL).getcode()
except urllib2.HTTPError:
    log("Failed to find deploy.json in path, please verify path %s in browser" % (deployJsonURL))
    exit()

deployPath = createDeploymentIfNotExists(gitURL)
conf = getConfiguration(deployPath)

setupConfig(conf, gitURL)

log("All done!")
