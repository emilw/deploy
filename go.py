import os

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
        os.makedirs(localFolder)
    
    return localFolder

def getConfiguration(deployPath):
    log("Starting to read configuration from deployment: " + deployPath)
    conf = Config(deployPath, 15, "doit.py")
    return conf

def setupConfig(conf):
    log(conf.script)
log("Starting deployment")

deployPath = createDeploymentIfNotExists("https://github.com/emilw/testrepo.git")
conf = getConfiguration(deployPath)

setupConfig(conf)
