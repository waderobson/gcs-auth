## Introduction
This project allows you to host your munki repo, securely from a Google cloud storage bucket.

## Getting Started
What you need:  
* Google Cloud Platform account
* A google storage bucket
* Service account with read only access.
* Developement build of munki version 2.6.1.2721 or higher to use middleware. You can find that [here](https://munkibuilds.org/)


### Create bucket and Read Only account
1. Create a new project or navigate to an exsiting one.
2. create your readonly service account under [IAM & Admin](https://console.cloud.google.com/iam-admin)
3. Creat a new service account called whatever you want. Make to check the **"Furnish a private new key"** checkbox. Choose JSON as the keytype. That's the file we need for munki so keep that, you can't download that JSON file again but you can create a new one later. 
5. Go to the IAM section and find the service account, should be under editors. And remove all roles.
6. Next we create new bucket, once its created click on the bucket view then chose the elipsis buttons on the very right next to the bucket. You should have the option to **Edit bucket bermissions** and **Edit object default permissions**
7. You need to add the service account as a user with reader access. Add it to both **Edit bucket bermissions** and **Edit object default permissions**

### Uploading your files
You can upload you munki repo to the bucket using gsutil. Get it [here](https://cloud.google.com/storage/docs/gsutil_install#mac)
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
