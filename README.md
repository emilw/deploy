# Deploy
A deploy structure that helps keeping smart devices up to date from a GitHub repository.
In short:
- Clone this repository
- Let the this library keep track of the repository in terms of what and when to execute something on the device. 

## Get going

```
git clone https://github.com/emilw/deploy.git
chmod +x install.sh 
./install.sh
./go.py -r https://github.com/emilw/deployTest
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