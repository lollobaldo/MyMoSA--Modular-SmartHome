# MyMoSA -- My Modular SmartHome Automator

Built for my Raspberry Pi, MyMoSA is a modular server/client meant to manage
inputs, outputs and logging.

Current modules supported / in production
-[X] DHT 11
-[X] Lights - really just a relay, could do pretty much anything
-[X] Remote commands to shell
-[X] System stats

## Getting Started

These instructions will get you a copy of the project up and running on your
local RasPi. 

### Installing

After cloning the repository, install the required python modules

```
pip install requirements.txt
```

Then setup the credentials for your MQTT server in [credentials.template.ini]
(../server/credentials.template.ini). Remember to rename it to
`credentials.ini`.

After that, the server is ready to run. Have a look at the other settings in
[config.ini](../server/config.ini). They're mostly about channel naming and
IO settings in the RasPi.

You should add this script to your `.bashrc` file, make sure to add an `&` so
that it runs in the background

```
python3 /path/to/file/server.py &
```

## Authors

* **Lorenzo Baldini** - *Initial work* - [lollobaldo]
(https://github.com/lollobaldo)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE)
file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc