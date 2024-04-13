import os
import firebase_admin
from firebase_admin import credentials, firestore, storage


def initialize_firebase():
    # NOTE: Replace with the path to your Firebase service account key JSON file
    cred = credentials.Certificate('path/to/your/serviceAccountKey.json')
    firebase_admin.initialize_app(
        cred, {'storageBucket': 'your-firebase-storage-bucket'})



def get_blob_path_from_url(url):
    # Remove the domain part from the URL
    path_start = url.find('/o/') + 3  # Adjust according to your URL structure
    path_end = url.find('?')
    # Extract the file path within the storage bucket
    file_path = url[path_start:path_end]
    # Replace any '%2F' with '/' to get the correct blob path
    return file_path.replace('%2F', '/')


def download_photos():
    # Reference to the storage service
    bucket = storage.bucket()
    # Firestore client
    db = firestore.client()
    # Local folder for downloads
    download_folder = 'downloaded_photos'
    # Ensure the folder exists
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Reference to the Firestore collection
    accidents_ref = db.collection('accidents')
    # Stream the documents in the collection
    docs = accidents_ref.stream()

    for doc in docs:
        doc_dict = doc.to_dict()
        admin_notes = doc_dict.get('adminNotes', 'default')
        safe_admin_notes = admin_notes.replace('/', '_').replace(' ', '_')
        folder_path = os.path.join(download_folder, safe_admin_notes)
        # Ensure the individual document's folder exists
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Check if photos are present and is a dictionary
        if 'photos' in doc_dict and isinstance(doc_dict['photos'], dict):
            for photo_name, photo_url in doc_dict['photos'].items():
                try:
                    # Extract the blob path from the URL
                    blob_path = get_blob_path_from_url(photo_url)
                    local_file_path = os.path.join(
                        folder_path, photo_name + '.jpg')
                    blob = bucket.blob(blob_path)
                    blob.download_to_filename(local_file_path)
                    print(f'Downloaded {photo_url} to {local_file_path}')
                except Exception as e:
                    print(f"Failed to download {photo_url}: {e}")


if __name__ == '__main__':
    download_photos()
