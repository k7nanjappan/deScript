
![Banner](https://github.com/k7nanjappan/deScript/assets/20095039/d70bae9f-c1fa-4db9-975a-4a495d1cdd3f)



**deScript** is a python script that generates a brief description of a **YouTube** video.

Whether you are unable to decide if you want to invest your time in a long video or the video does not have a description, deScript will generate a comprehensive summary of any YouTube video and all you need to do is provide the url.

deScript makes use of the **YouTube API v3** to obtain details of the video and the description is generated using Google's **PaLM API**.

## Usage

deScript can be executed by simply passing the YouTube url as a command line argument to **model.py**.

```
$ python3 model.py youtube_url
```

## Installation

### Obtain API keys
**YouTube V3**
* Login to [Google Developers Console](https://console.cloud.google.com/cloud-resource-manager).
* Create a new project.
* Using the **Navigation menu** on the top left of the website, hover over **Cloud overview** and click **Dashboard**.
* In the Dashboard, click **→ Go to APIs overview** and select **＋ENABLE APIS AND SERVICES** on top of the page.
* Search for the **YouTube Data Api v3** and enable it.
* At the navigation bar on the left, click on **Credentials** and select **＋CREATE CREDENTIALS** on top of the page.
* Select **OAuth client ID** and if necessary, complete the OAuth consent form.
* Download the OAuth client JSON and rename it to **"google_cloud_api_key.json"**
>API documentation can be found [here](https://developers.google.com/youtube/v3)


**PaLM**
* Login to Google's [MakerSuite](https://makersuite.google.com/) and create an API key.
* Copy the API and store it in text file named **"palm_api_key.txt"**
> If you're unable to use MakerSuite, you can request access by joining the [waitlist](https://makersuite.google.com/waitlist)

### Setup environment
* Create a new folder named **"keys"** and place _google_cloud_api_key.json_ and _palm_api_key.txt_ in it.
* Install all the required packages from the **requirements.txt** by running: 
``` $ pip install -r requirements.txt```
