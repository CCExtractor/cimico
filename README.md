# Cimico
Hello there!
Cimico is a debugger that is written in python which debugs python code!

This project was created under CCExtractorDevelopment in Google Code-In 2019

![Demo](https://github.com/CCExtractor/cimico/blob/master/cimico/DebuggerVideo.gif)

# Installation
Cimico can be downloaded using pip.

```
pip install cimico
```

# How to use?
After installation, cimico is accessible using the command line.
```
$ cimico
```
Using cimico, you can generate a JSON file, which in turn can be used to generate a video by cimico itself. Enter the path to the JSON file or the Python file when prompted. You may also need to enter the path to the YAML style sheet containing the configuration to the file. 

Generating the JSON file.

```
$ cimico
----------------------------------------------
                 TAKING INPUT                 
----------------------------------------------
Do you want to use the test suite? (y/n): n
Enter the name of the file you want to debug: /pth/to/pythonfile
Enter the name of the function you want to debug: functionname
Enter the arguments for the function (space seperated): arguements
----------------------------------------------
              RUNNING FUNCTION                
----------------------------------------------
Where do you want your JSON file to be stored? /pth/to/where/the/json/file/should/be/stored
Written to json file!

```

Generating the video and/or the GIF.

```
$ cimico
----------------------------------------------
                 TAKING INPUT                 
----------------------------------------------
Do you want to use the test suite? (y/n): n
Enter the name of the file you want to debug: /pth/to/jsonfile
Do you want to generate a video? (y/n): y
Generating video...
Enter the path to the yaml file: /pth/to/yaml/file
Where do you want your video to be stored? /pth/to/where/the/video/should/be/stored 
Do you want to generate a GIF file as well? (y/n) y
Generating GIF...
```
Note: The GIF and the Video will be saved in the same folder.



# Contribution
Found a bug/typo in the code or want to suggest new functionality? Open up an Issue for the same or send a Pull Request.  

# License
The code is licensed under the MIT license.
