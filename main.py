import os
import time
import firebase_admin
from firebase_admin import credentials, firestore, storage

# Inizializza Firebase con le credenziali fornite
cred = credentials.Certificate('credit.json')
firebase_admin.initialize_app(
    cred, {'storageBucket': 'id.appspot.com'})

# Definisce una funzione per pulire il nome del file


def get_blob_path_from_url(url):
    path_start = url.find('/o/') + 3
    path_end = url.find('?')
    file_path = url[path_start:path_end]
    return file_path.replace('%2F', '/')

# Definisce una funzione per scaricare le foto


def download_photos(bucket, download_folder):
    db = firestore.client()
    accidents_ref = db.collection('accidents')
    docs = accidents_ref.stream()

    for doc in docs:
        doc_dict = doc.to_dict()
        admin_notes = doc_dict.get('adminNotes', 'default')
        folder_path = os.path.join(download_folder, admin_notes)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        photos = doc_dict.get('photos', {})
        # Filtra le chiavi che non contengono "thumbnail"
        photo_keys = [key for key in photos.keys() if "thumbnail" not in key]
        photo_count = len(photo_keys)  # Conta solo le foto senza thumbnails

        print(f"Checking '{admin_notes}' with {photo_count} photos.")
        if photo_count < 11:
            print(f"'{admin_notes}' has less than 11 photos, skipping download.")
            continue

        for photo_name in photo_keys:
            photo_url = photos[photo_name]
            # Usa un metodo per ottenere il path corretto del blob da photo_url...
            blob_path = get_blob_path_from_url(
                photo_url)  # Definisci questa funzione
            local_file_path = os.path.join(folder_path, photo_name + '.jpg')
            blob = bucket.blob(blob_path)

            if not os.path.isfile(local_file_path):
                blob.download_to_filename(local_file_path)
                print(f"Downloaded {photo_name} to {local_file_path}")
            else:
                print(f"File {photo_name} already exists. Skipping download.")

        # Aspetta per 10 secondi prima di controllare la prossima pratica
        time.sleep(10)


def main_loop():
    download_folder = 'downloaded_photos'
    bucket = storage.bucket()

    while True:
        download_photos(bucket, download_folder)
        print("Waiting for 10 seconds before next check...")
        time.sleep(10)


if __name__ == '__main__':
    main_loop()
