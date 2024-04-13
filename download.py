import os
import firebase_admin
from firebase_admin import credentials, firestore, storage
from urllib.parse import urlparse, unquote

def initialize_firebase():
    # Use environment variables to load credentials and bucket info securely
    cred_path = os.environ.get('FIREBASE_CREDENTIALS', 'path_to_default_credentials.json')
    bucket_name = os.environ.get('FIREBASE_BUCKET_NAME', 'example.appspot.com')
    
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {'storageBucket': bucket_name})

def clean_filename(url):
    parsed = urlparse(url)
    filename = os.path.basename(parsed.path)
    filename = unquote(filename)
    return filename.replace('?', '_').replace('&', '_').replace('%', '_')

def download_photos():
    initialize_firebase()
    bucket = storage.bucket()
    db = firestore.client()
    
    download_folder = 'downloaded_photos'
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    accidents_ref = db.collection('collection_name')
    docs = accidents_ref.stream()

    for doc in docs:
        doc_dict = doc.to_dict()
        field = doc_dict.get('field', 'DefaultFolder')
        safe_folder_name = field.replace('/', '_').replace(' ', '_')
        doc_folder_path = os.path.join(download_folder, safe_folder_name)
        if not os.path.exists(doc_folder_path):
            os.makedirs(doc_folder_path)

        photos = doc_dict.get('photos', {})
        for photo_name, photo_details in photos.items():
            if isinstance(photo_details, dict) and 'url' in photo_details:
                photo_url = photo_details['url']
                file_name = clean_filename(photo_url)
                local_file_path = os.path.join(doc_folder_path, file_name)
                file_blob = bucket.blob(photo_name)
                try:
                    file_blob.download_to_filename(local_file_path)
                    print(f'Downloaded {photo_url} to {local_file_path}')
                except Exception as e:
                    print(f"Failed to download {photo_url}: {str(e)}")

if __name__ == '__main__':
    download_photos()
