import os, errno

def check_dir(yyyy, mm):
  try:
      os.makedirs(f'NewsData/{yyyy}/{mm}')
  except OSError as e:
      if e.errno != errno.EEXIST:
          raise e