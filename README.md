## Introduction
This project allows you to host your munki repo, securely from a Google cloud storage bucket.

## Getting Started
What you need:  
* Google Cloud Platform account
* A google storage bucket
* Service account with read only access.
* Munki version 2.7.0 or higher to use middleware. You can find that [here](https://github.com/munki/munki/releases)


### Create bucket and Read Only account
1. Create a new project or navigate to an exsiting one.
2. Create your read-only service account under [IAM & Admin](https://console.cloud.google.com/iam-admin)
3. Create a new service account called whatever you want. Make sure to check the **"Furnish a private new key"** checkbox. Choose JSON as the keytype. That's the file we need for munki so keep that, you can't download that JSON file again but you can create a new one later. 
5. Go to the IAM section and find the service account, should be under editors and remove all roles (if there are any).
6. Create new bucket, under [Storage](https://console.cloud.google.com/storage). 
7. Once created, we need to assign read permissions to the service account we created. To do so, select the bucket from the list then click the three dots button on the right end of the line where the bucket is. In the sidebar, search for your service account and add the **Storage Object Viewer permissions to it**.

### Uploading your files
You can upload you munki repo to the bucket using gsutil get it [here](https://cloud.google.com/storage/docs/gsutil_install#mac).  
The following command will upload all the files from `/path/to/munki_repo` into your bucket. For more details run `gsutil help rsync`
```bash
gsutil -m rsync -r -d -x '.DS_Store|.git' /path/to/munki_repo gs://<bucket goes here>/
```

### Installing on client

###### Step 1:  
Copy `middleware_gcs.py` into `/usr/local/munki/`  

###### Step 2:
Copy the service account json keystore file to `/usr/local/munki/`. Rename it to `gcs.json`

###### Step 3:
Change your repo to point to your Google Storage bucket.  
```bash
sudo defaults write /Library/Preferences/ManagedInstalls SoftwareRepoURL  "https://storage.googleapis.com/<bucket goes here>"
```
