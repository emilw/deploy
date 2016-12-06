import os
import git
import json
import datetime
import log

class Config(object):
    def __init__(self, jsonData):
        self.__dict__ = jsonData

def createDeploymentIfNotExists(gitURL):
    localFolder = gitURL.split("/")[-1].split(".")[0]
    localFolder = "deployments/" + localFolder
    log.info(localFolder)
    if os.path.exists(localFolder):
        log.info("Deployment exists, updating...")
        g = git.cmd.Git(localFolder)
        g.pull()
        log.info("...Done")
    else:
        log.info("The deployment do not exists, downloading....")
        git.Repo.clone_from(gitURL+".git", localFolder)
        log.info("....Done")
        #os.makedirs(localFolder)
    
    return localFolder

def getConfiguration(deployPath):
    log.info("Starting to read configuration from deployment: " + deployPath)
    configFileContent = open(deployPath+"/deploy.json")
    data = json.load(configFileContent)
    log.info("deploy.json is loaded")
    conf = Config(data)
    return conf