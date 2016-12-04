import urllib2
import log
import os
import datetime
import json
import sys

class DeployConfig:
    def __init__(self, sourceURL, created, updated, versiontag, branch, name):
        self.SourceURL = sourceURL
        self.Created = created.isoformat()
        self.Updated = updated.isoformat()
        self.VersionTag = versiontag
        self.Branch = branch
        self.Name = name

def getDeployConfPath():
    home = os.path.expanduser("~")
    deployConfPath = home+"/.deploy"
    return deployConfPath

def jdefault(o):
    return o.__dict__

def writeJson(object, path):
    with open(path, 'w') as fp:
        json.dump(object, fp, default=jdefault, indent=4)

def readJson(path):
    with open(path, 'r') as fp:
        return json.load(fp)
def datetimefromiso(isoString):
    return datetime.datetime.strptime( isoString, "%Y-%m-%dT%H:%M:%S.%f" )

def getExistingDeployConfigs(deployConfPath):
    jsonDataArray = readJson(deployConfPath)
    deployConfigs = []
    for jsonData in jsonDataArray:
        created = datetimefromiso(jsonData["Created"])
        updated = datetimefromiso(jsonData["Updated"])
        d = DeployConfig(jsonData["SourceURL"], created, updated, jsonData["VersionTag"], jsonData["Branch"], jsonData["Name"])
        deployConfigs.append(d)
    return deployConfigs

def setupConfig(gitURL, name, branch, versionTag):
    log.info("Starting to configure: " + gitURL)
    deployConfPath = getDeployConfPath()
    deployConfigs = []
    if(not os.path.exists(deployConfPath)):
        log.info(".deploy will be created")
        d = DeployConfig(gitURL, datetime.datetime.now(),datetime.datetime.now(),versionTag, branch, name)

        deployConfigs.append(d)
        writeJson(deployConfigs, deployConfPath)
    else:
        log.info("Deployment already exists, updating....")
        deployConfigs = getExistingDeployConfigs(deployConfPath)
        for d in deployConfigs:
            log.info("Deployment '%s''(%s)" % (d.Name, d.SourceURL))
            if(gitURL == d.SourceURL):
                log.info("Found hit")
        log.info("Deployment updated")
    

def deployConfigForRepository(gitURL):
    content = ""
    try:
        deployJsonURL = gitURL+"/raw/master/deploy.json"
        log.info("Checking URL %s" % (deployJsonURL))
        request = urllib2.urlopen(deployJsonURL)
        status = request.getcode()
        content = request.read()
    except urllib2.HTTPError:
        log.info("Failed to find deploy.json in path, please verify path %s in browser" % (deployJsonURL))
        return False
    
    jsonData = json.loads(content)

    try:
        appName = jsonData["name"]
        log.info("Application identified as %s" % (appName))

        setupConfig(gitURL, appName, jsonData["branch"], jsonData["versiontag"])
        log.info("Setup created for %s" % appName)
    except KeyError as e:
        log.info("Failed to load property %s from deploy.json" % (e.message))
        log.info(content)
        return False
    
    return True

def listExistingDeploymentConfigs():
    deployConfPath = getDeployConfPath()
    deployConfigs = getExistingDeployConfigs(deployConfPath)
    for d in deployConfigs:
        log.info("Deployment %s(%s)" % (d.Name, d.SourceURL))