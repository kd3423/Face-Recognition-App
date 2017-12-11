# Face Recognition

Here we will be training a neural network to identify the different features of the face(e.g. jaw line, eyebrow, eyes, lips) of the specific person and then using these for the matching with other input images. We will be using a trained model present in "dlib library". The output from the above stated model will be the face encodings.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

All things you need to install are present in the requirement.txt
```
pip install -r requirements.txt
```

### Train

Just simply add the images with labels that you want the model to recognize in the 'images' folder.
Make sure to remove the saved files 'weights.out' and 'classes.txt', as they are for the images that I trained on.

```
rm -rf weights.out classes.txt
```


Testing the Web application

Simply run the app.py file

```
python app.py
```

On the web app, simply upload the image to test the model. The output to the image will be simply a json format text, showing if the face(s) is present in the image or not.


## Authors

* **Karan Dabas**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

