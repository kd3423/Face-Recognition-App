# Face Recognition

Here we will be training a neural network to identify the different features of the face(e.g. jaw line, eyebrow, eyes, lips) of the specific person and then using these for the matching with other input images. We will be using a trained model present in "dlib library". The output from the above stated model will be the face encodings.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system. Assuming you have python 2.7 up and running.

### Prerequisites


All things you need to install are present in the requirement.txt
```
pip install -r requirements.txt
```

### Data Description
Dataset is extracted using image search api(Googel custom Search) on the search query 'narendra modi' and 'arvind kejriwal' and 'narendra modi with arvind kejriwal' and collected the images against each in the seperate mongo collection. A total of 71(nm)+74(ak)+65(nm and ak). All the corresponding scripts for data collection can be found in the 'dataCollection' folder along with the .json files containing the mongoDB collections. Please bear in mind that you will first have to create your own google custom search for which you will need the google cloud account.


### Train

Just simply add the images with labels that you want the model to recognize in the 'images' folder.
Make sure to remove the saved files 'weights.out' and 'classes.txt', as they are for the images that I trained on. If these files are not found the model will itself train again when you run the app.

```
rm -rf weights.out classes.txt
```


### Testing the Web application

Simply run the app.py file

```
python app.py
```

On the web app, simply upload the image to test the model. The output to the image will be simply a json format text, showing if the face(s) is present in the image or not.

### Accuracy

After just using 2 images out of the batch of 210 images in training. So the images used for testing is 208.
The model gave the test accuracy of 98%. 

## Authors

* **Karan Dabas**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

