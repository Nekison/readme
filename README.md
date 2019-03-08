# Real Time Database Synchronization Publisher
[![pipeline status](https://gitlab.com/sorbotics/rtdb-sync-pub/badges/master/pipeline.svg)](https://gitlab.dev.sorbapp.com/sorbotics/rtdb/rtdb-sync-pub/commits/master)
[![coverage report](https://gitlab.com/sorbotics/rtdb-sync-pub/badges/master/coverage.svg)](https://gitlab.dev.sorbapp.com/sorbotics/rtdb/rtdb-sync-pub/commits/master)

Publish Real Time Database events in order to synchronize two instances of the 
Real Time Database.

Following policies apply to the development of this project:

 - [General Policies](https://gitlab.dev.sorbapp.com/sorbotics/website/blob/master/policies/general-policies.md)
 - [Policies for Server Side development using the Python programming language](https://gitlab.dev.sorbapp.com/sorbotics/website/blob/master/policies/runtime-specific/python.md)

## Setup

This application use [pipenv](https://docs.pipenv.org) as dependency management 
tool. You can simply install it using the following command:

    pip install pipenv

Execute the following command to create a virtual environment for the 
application and install all its dependencies:

    pipenv install
