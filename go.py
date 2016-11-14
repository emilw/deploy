import os
import git
import json

class Config(object):
    def __init__(self, jsonData):
        self.__dict__ = jsonData


def log(text):
    print(text)

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
        git.Repo.clone_from(gitURL, localFolder)
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

def setupConfig(conf):
    log("Starting to configure: " + conf.name)
    #log("Number of python pre reqs: " + len(conf.prerequisitesPython))
log("Starting deployment")

deployPath = createDeploymentIfNotExists("https://github.com/emilw/deployTest.git")
conf = getConfiguration(deployPath)

setupConfig(conf)
