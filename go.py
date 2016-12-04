import os
import git
import json
import datetime
import deployconfig
import log
import argparse

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


parser = argparse.ArgumentParser()
parser.add_argument("-r", "--register", help="Register a new deployment GitHub URL")
parser.add_argument("-s", "--schedule", help="Schedule mode", action="store_true")
args =  parser.parse_args()

if(args.register):
    registerGitHubURL = args.register.strip()
    log.info("Register the repo to the central configuration")
    if(not deployconfig.deployConfigForRepository(registerGitHubURL)):
        log.info("Failed to update or register based on the url")
        exit()
    
    log.info("Starting to deploy application specific code and configuration")
    deployPath = createDeploymentIfNotExists(registerGitHubURL)
    conf = getConfiguration(deployPath)
    log.info("Done deploying application specific code and configuration")
if(args.schedule):
    log.info("Running scheduling to keep deployments up to date")
    deployconfig.listExistingDeploymentConfigs()
    log.info("Running actions")

log.info("All done!")
