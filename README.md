# text-extraction-4fun

You should install the script's dependencies using PIP.

Remember to replace **BUCKET_NAME** and **REGION** accordingly.

Call the script passing the path to a document on your environment:
```shell
$ python recognizer.py /path/to/document/example-doc.jpg 
```

The document will be uploaded into s3 bucket and it's text content will be extracted. Raw response from textract will be stored as output.json and a summary will be displayed in your terminal.
