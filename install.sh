#!/bin/bash

echo "Setting up pre reqs"
git --version 2>&1 >/dev/null
GIT_IS_INSTALLED=$?

python3 --version 2>&1 >/dev/null
PYTHON_IS_INSTALLED=$?


if [ $GIT_IS_INSTALLED -ne 0 ]; then
    echo "Git is not installed, please install it to continue"
elif [ $PYTHON_IS_INSTALLED -ne 0 ]; then
    echo "Python3 is not installed, please install it to continue"
else
    #pip3 install urllib2
    pip3 install gitpython
    chmod +x go.py
    echo "All is set, run ./go.py -r https://github.com/youruser/yourrepository example: "
    #echo "All pre reqs are installed"
    #echo "Checking if the install script is in the root of deploy or if it should be pulled"
    #if [ ! -f go1.py ]; then
    #    git clone https://github.com/emilw/deploy.git
    #    echo "Pull is needed"
    #else
    #    echo "This library is already connected to GIT"
    #fi
fi
