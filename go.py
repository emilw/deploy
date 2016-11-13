import os
import git
import json

class Config:
    def __init__(self, path, schedule, script):
        self.path = path
        self.schedule = schedule
        self.script = script

def log(text):
    print(text)

def createDeploymentIfNotExists(gitURL):
    localFolder = gitURL.split("/")[-1].split(".")[0]
    localFolder = "deployments/" + localFolder
    log(localFolder)
    if os.path.exists(localFolder):
        log("Deployment exists, updating...")
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
    log(data["preRequisitePython"][0])
    conf = Config(deployPath, 15, "doit.py")
    return conf

def setupConfig(conf):
    log(conf.script)
log("Starting deployment")

deployPath = createDeploymentIfNotExists("https://github.com/emilw/deployTest.git")
conf = getConfiguration(deployPath)

setupConfig(conf)
