import time
import boto
from boto.emr import StreamingStep, EmrConnection, BootstrapAction
from boto.s3.key import Key
from datetime import datetime

# TODO: The base name for 2 buckets that will be created in your S3 account
BUCKET_BASE_NAME = 'witoff-hadoop'

# TODO: Add your S3 Credentials here.  EMR, EC2 & S3 permission is needed.
AWS_ACCESS_KEY_ID = 'xxx'
AWS_SECRET_ACCESS_KEY = 'xxx'

#TODO: Replace this keyname with one that you've already created in EC2
EC2_KEYNAME = 'aws-east'

def upload_to_bucket(bucket, filename, folder=""):
  """ Upload a local <filename> into the provided <bucket> object with an
  optional folder
  """
  k = Key(bucket)
  k.key = folder + "/" + filename
  k.set_contents_from_filename(filename)

def upload_files(bucket_name, local_file_names):
  """
  Given an array of <local_file_names>, upload each of them to the provided
  <bucket_name> string in your account.
  """

  conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

  try:
    bucket = conn.get_bucket(bucket_name)
  except Exception, e:
    print 'bucket not found.  Creating bucket.'
    bucket = conn.create_bucket(bucket_name)

  print "Uploading files to bucket: %s" % bucket_name

  # Upload Files
  for u in local_file_names:
      print "Uploading file to bucket: %s" % u
      upload_to_bucket(bucket, u)
      print "...uploaded"
  return bucket

if __name__ == '__main__':

  # Get Bucket Names
  bucket_emr = '%s-emr' % BUCKET_BASE_NAME
  bucket_input = '%s-cc' % BUCKET_BASE_NAME


  #Define the local files that we want to upload
  file_mapper = "mapper.py"
  file_reducer = "reducer.py"
  file_bootstrapper = "bootstrap.sh"
  file_input = "manifest.wet.txt"

  # Upload these files
  bucket = upload_files(bucket_input, [file_input])
  bucket = upload_files(bucket_emr, [file_mapper, file_reducer, file_bootstrapper])



  # Name our cluster
  jobname = "Common Crawl Cruncher"
  # Location for EMR's log & output files
  output_folder = "output/"


  print "Initializing EMR Connection..."
  conn = EmrConnection(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

  print "Setting Up Hadoop Streaming Step..."
  result_folder = output_folder + str(datetime.now()).split('.')[0].replace(' ','_')
  step = StreamingStep(name='URL Cruncher',
                   mapper='s3n://%s/%s' % (bucket_emr, file_mapper),
                   reducer='s3n://%s/%s' % (bucket_emr, file_reducer),
                   #input='s3n://%s/%s'% (input_bucket, input_path),
                   input='s3n://%s/%s'% (bucket_input, file_input),
                   output='s3n://%s/%s' % (bucket_emr, result_folder),
                   action_on_failure='CANCEL_AND_WAIT',
                   step_args = ["-jobconf", "mapred.map.tasks=24", "mapred.reduce.tasks=2"]
                   )

  # Other possible step args include:
  #   mapred.max.split.size=1
  #   mapred.min.split.size
  #   mapred.map.tasks = 20
  #   mapred.task.timeout=800000
  #   mapred.tasktracker.map.tasks.maximum
  #   mapred.tasktracker.reduce.tasks.maximum

  # Define an action that will bootstrap these machines and install our needed
  #  dependencies
  bootstrap_action = BootstrapAction("Install Dependiences",
      's3://%s/%s' % (bucket_emr, file_bootstrapper),
      None)


  # if an existing cluster is running, let's use that
  running_clusters = conn.list_clusters(cluster_states="WAITING").clusters
  if len(running_clusters) > 0:
    job_id = running_clusters[0].id
    print "A waiting cluster is already setup.  Running Job on : %s" % job_id
    conn.add_jobflow_steps(job_id, [step])
  else:
    print 'No waiting EMR clusters found.  Starting new cluster with name: %s' % jobname
    answer = raw_input('Do you want to start a new cluster? [N/y]: ')
    if 'y' not in answer.lower():
      print 'exiting'
      exit()

    print 'creating a new EMR cluster'

    job_id = conn.run_jobflow(name=jobname,
              steps=[step],
              log_uri="s3://"+bucket_emr+"/logs/",
              bootstrap_actions=[bootstrap_action],
              enable_debugging = True,
              keep_alive=True,
              master_instance_type='m1.small', # I like m3.xlarge this b/c networking == high and cost is $.35/instance/hour,
              slave_instance_type='m1.small',
              num_instances=4,
              ec2_keyname=EC2_KEYNAME)
              #instance_groups =  # OPTIONAL: Add Spot Support)

  # OPTIONAL: Add Spot Support
  #ig = InstanceGroup(6, 'TASK', 'c1.medium', 'SPOT', 'spot-0.07', '0.07')
  #c.add_instance_groups(jf.jobflowid, ig)

  time.sleep(20)
  status = conn.describe_jobflow(job_id).state
  while status not in ['WAITING', 'COMPLETED']:
    status = conn.describe_jobflow(job_id).state
    print "Status: %s for Job Id: %s" % (status, job_id)
    time.sleep(10)

  print "Job finished"

  print "Retrieve Results in bucket: ", bucket_emr
  print " and folder: ", result_folder
