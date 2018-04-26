# Real Time Database Synchronization Publisher
[![pipeline status](https://gitlab.com/sorbotics/rtdb-sync-pub/badges/master/pipeline.svg)](https://gitlab.com/sorbotics/rtdb-sync-pub/commits/master)

Publish Real Time Database events in order to synchronize two instances of the 
Real Time Database.

## Building Debian package

The `Pipfile` include a dev-dependency used for this purpose. Use the command:

    pipenv run python setup.py --command-packages=stdeb.command bdist_deb
