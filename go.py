import deployconfig
import deployment
import argparse
import log

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
    deployPath = deployment.createDeploymentIfNotExists(registerGitHubURL)
    conf = deployment.getConfiguration(deployPath)
    log.info("Done deploying application specific code and configuration")
if(args.schedule):
    log.info("Running scheduling to keep deployments up to date")
    deployconfig.listExistingDeploymentConfigs()
    log.info("Running actions")

log.info("All done!")
