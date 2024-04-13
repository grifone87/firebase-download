# Firebase Storage Image Downloader

This Python script automates the process of downloading images from Firebase Storage based on data stored in Firestore. It's especially useful for projects that require automated management of digital assets linked to specific records in Firestore.

## Features

- **Firebase Initialization:** Configure and initialize the Firebase environment using your access credentials.
- **Automatic Download:** Download all images related to specific documents within a Firestore collection.
- **File Organization:** Saves images in local subfolders based on custom fields (e.g., 'field') from Firestore documents, facilitating organization.
- **Error Handling:** Robust error management ensures the download process does not fail unexpectedly.

## Technologies Used

- Python 3.x
- Firebase Admin SDK for interacting with Firebase and Firestore
- Google Cloud Storage Library for accessing and downloading files

## Initial Setup

1. **Firebase Credentials:** Ensure you have a 'credit.json' file containing your Firebase credentials.
2. **Install Dependencies:** Execute the following commands in your terminal:

pip install firebase-admin
pip install google-cloud-storage


4. **Storage Bucket Configuration:** Modify the script to include your specific Firebase Storage bucket.

## Usage

To run the script, execute:

python download.py

This will start the process of downloading images based on the defined structure in your Firestore and save them locally following the specified organizational structure.

## Contribute

You are invited to contribute to this project by improving the script's efficiency or adding features. To contribute, submit a pull request with your changes.
