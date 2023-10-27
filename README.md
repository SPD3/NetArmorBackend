# NetArmorBackend

## Intent
The intent behind this repository is to provide a set of REST endpoints that the
NetArmor application can use to access its database. It is **strongly** 
recommended running this application through the [NetArmorCompose repository](https://github.com/SPD3/NetArmorCompose) 
as that handles all the environment setup to link the frontend to the 
backend to the database.

## To run unit tests:
In order to run unit tests you must have the docker engine running. Additionally,
you have to enable default Docker socket. To do so, open the Docker Desktop app 
and click on the settings wheel in the top right corner, click the advanced tab 
and then click the check mark next to the "Enable default Docker socket". You 
may have to enter your password and restart Docker, but unit tests should run 
afterwards.