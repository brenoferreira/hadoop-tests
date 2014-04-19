2 - EMR Size Counts
===============

Iterate Through all EMR filenames and reduce the total (compressed) object size.  
This script will upload your local files to S3 and launch an EMR cluster to process your data.

### Instructions:
1. Update all 'TODO' items in code.  Includes adding your AWS & SSH keys
2. Initiate and run job via  ```runJob.py``` script
3. Update ```reducer.py``` to sum up all values and return sum into reduced file
4. Record the combined size in bytes of all common crawl files.


### Notes:
* We're using the python 'boto' library to access AWS APIs
* You may need to `pip install boto` on your development machine

### Resources:
* Common Crawl files are available in this bucket:
  * 'aws-publicdatasets'
* Some sample WARC & WET files for testing in this folder:
  * common-crawl/crawl-data/CC-MAIN-2013-48/segments/1386164789076/warc/
* And here are some files:
  * common-crawl/crawl-data/CC-MAIN-2013-48/segments/1386164789076/wet/CC-MAIN-20131204134629-00001-ip-10-33-133-15.ec2.internal.warc.wet.gz
  * common-crawl/crawl-data/CC-MAIN-2013-48/segments/1386164789076/warc/CC-MAIN-20131204134629-00001-ip-10-33-133-15.ec2.internal.warc.gz
* And here is a fully qualified URL:
  * http://aws-publicdatasets.s3.amazonaws.com/common-crawl/crawl-data/CC-MAIN-2013-48/segments/1386164789076/warc/CC-MAIN-20131204134629-00001-ip-10-33-133-15.ec2.internal.warc.gz
