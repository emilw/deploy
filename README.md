# Deploy
A deploy structure that helps keeping smart devices up to date from a GitHub repository.
In short:
- Clone this repository
- Let the this library keep track of the repository in terms of what and when to execute something on the device. 

## Get going

```bash
#Get the runtime
git clone https://github.com/emilw/deploy.git
#Setup the install/prereq script and run it
chmod +x install.sh 
./install.sh
#Register a repository to deploy from
./go.py -r https://github.com/emilw/deployTest
#Run/Start all registered repositories
./go.py -s
```

## Requirement on the repository
The repository that is referenced need to have the following json file in the master.
```json
{
    "name": "Test program",
    "prerequisitesPython":[
        "git"
    ],
    "prerequisitesSystem":[
        ""
    ],
    "executionSettings": [
        {
            "script":"myScript.py",
            "schedules":["0****"]
        }
    ],
    "versiontag":"",
    "branch":"master"
}
```