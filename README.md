# Open-TTS-App
A fully open source Web Application for generating Speech from Text.

## What is this project about?
Open-TTS-App is a Text-To-Speech synthesizer webservice written in Python with the FastAPI Framework.

## What dependencies do I need?
You will need...
- Python
- Piper
- One or more Piper Models installed on your system

## How do I use it?
### Cloning and environment-setup
First, you will need to clone this repository:
```bash
git clone https://github.com/Moritisimor/Open-TTS-App
```

Then, cd into the newly cloned repository's source folder:
```bash
cd Open-TTS-App/src
```

You will then need to set up a virtual environment:
```bash
python -m venv .venv
```

Then, update your environment variables:
#### Linux/macOS/BSD
```bash
source .venv/bin/activate
```
(If you use fish or csh, use activate.fish or activate.csh respectively)

#### Windows PowerShell
```bash
. .venv\Scripts\Activate.ps1
```

And finally install all pip dependencies:
```bash
pip install -r requirements.txt
```

### Running the application
```bash
python main.py <Directory>
```

Directory is important because it's the location where all your piper models are stored.

Piper models consist of a .onnx and a .json file. For example, a model named en_male consists of ```en_male.onnx``` and ```en_male.onnx.json```.

I have found [this site](https://docs.gladecore.com/files/piper-voice-models) to be very helpful for finding models.

And that's it. if everything is configured correctly, the API should work as it should.

## REST-Endpoints
### ```POST /api/speak```
This endpoint is the heartpiece of the application and is what synthesizes speech from text. 

It expects a JSON of this schema:
```json
{
    "text": "this should be a string",
    "model": "this should also be a string"
}
```

### ```GET /api/models```
This endpoint is meant for getting a list of available models which the API serves. 

It returns a JSON Array of all available models. It could, for example, look like this:
```json
["en_male", "en_female", "es_male", "es_female"]
```
