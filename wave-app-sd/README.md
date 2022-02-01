## To be modified to our Wildfire application

## Wave App Development

### Requirements

1. Install Python 3.6+, and pip3

2. Install H2O Wave SDK - follow instructions for your platform at https://wave.h2o.ai/docs/installation

3. Install H2O AI Cloud CLI (v0.9.1-rc1) to debug, bundle and execute your H2O Wave app: 
   https://h2oai-cloud-release.s3.amazonaws.com/releases/ai/h2o/h2o-cloud/v0.9.1-rc1/index.html

4. Install `tar` (or an alternative, to create a compressed archive file for submission)

### 1. Run the H2O Wave Server

Go to your H2O Wave SDK directory and run the Wave server:

```bash
cd $HOME/wave && ./waved
```
> INFO: On Windows, run `waved.exe` to start the server.
> WARNING: You could get an error (e.g. httpcore.ConnectError: [Errno 10061] Connect call failed ('127.0.0.1', 10101)) if you don't run the server



### 2. Clone the Pablito's Wildfire Challenge GitHub repo

```bash
git clone https://github.com/Dauriel/h2o_wildfires.git
```

### 3. Run your Wave app

Install requirements

```bash
cd wave-app-sd
pip install -r requirements.txt
```

### 4. Run your Wave app

This step is using installed h2o-wave package to run the application.

```bash
wave run sage-identification-pipeline/app.py
```

Point your web browser to http://localhost:10101/ to access the app and enjoy.

... to be continued with an app
... to be continued with app pub on cloud
