from zipfile import ZipFile

def main():
    
    # Use to unzip files in workspace testing
    with ZipFile('data/log-data.zip', 'r') as zipObj:
        zipObj.extractall('data/log_data/')
        
    with ZipFile('data/song-data.zip', 'r') as zipObj:
        zipObj.extractall('data/')           

if __name__ == "__main__":
    main()