# esphome-lambda-build
Experimental AWS Lambda function to build an ESPHome firmware quickly cheaply in the cloud.
The idea is to trigger a lambda function with a path to an ESPHome config file, and build the firmware on AWS Lambda and drop the resulting bin file(s) in S3.

## WARNING: This does not work!
I ran into a blocking [issue related to the virtual environment creaded by PlatformIO core during the build](https://community.platformio.org/t/using-global-python-packages-for-platformio-command-line-build/37799). It almost works though! The build actually succeeds but can't get past an apparent path issue with _esptool.py_. Publishing this here in case anyone comes across this with a solution.

### Lambda function config
These are lambda parameters used
* Runtime: Python 3.12
* Handler: `build.handler`
* Architecture: x86_64
* Memory: 4GB
* Ephemeral Storage: 4GB

### Layers
Use the `build_layer.sh` to install Python dependencies on a similar x86_64 runtime. I used an EC2 instance to do this. Upload the created layer.zip as a custom layer.

Also required:
* [git-lambda2](https://github.com/lambci/git-lambda-layer): `arn:aws:lambda:us-east-1:553035198032:layer:git-lambda2:8`

### Environment variables
Not sure about all of these.
* `PLATFORMIO_CORE_DIR`: `/tmp/.platformio`
* `PLATFORMIO_DISABLE_COLOR`: `true`
* `PLATFORMIO_DISABLE_PROGRESSBAR`: `true`
* `PYTHONEXEPATH`: `python3`
* `PYTHONPATH`: `/opt/python`


### Test
Test with the following event JSON:
```
{
  "config_url": "https://raw.githubusercontent.com/konnected-io/esphome-lambda-build/main/simple-test.yaml"
}
```
