# Video Slicing for image labeling

run the following commands with python 3.9 or above
* `python -m venv slice-env`
* `.\slice-env\Scripts\activate`
* `pip install -r requirements.txt`
* `.\slicing.py` - Creates a folder per video and saves frames in `.png` format at the [desired stride](https://github.com/ianre/video-slicing/blob/ae62821bd103996333adb272bb77f9b2d253441e/slicing.py#L6)