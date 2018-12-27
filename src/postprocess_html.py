import glob
import os

'''
This file to post-process the output of pydoc 
generating documents for source code
'''

files = glob.glob('doc/*.html', recursive=True)

start_token = '<big><strong>Data</strong></big>'
stop_token = '</body></html>'

for file in files:
    deleteFlag = False
    index = file.find('.html')
    output_file = file[:index]+ '_doc' + file[index:]
    print(output_file)
    # get a iterator over the lines in the file:
    with open(file, 'rt') as lines, open (output_file, 'w') as dest:
        # while the line is not empty drop it
        for line in lines:
            if start_token in line:
                deleteFlag = True
            if stop_token in line:
                deleteFlag = False
            if (deleteFlag == False):
                dest.write(line)

    ## Try to delete the file ##
    try:
        os.remove(file)
    except OSError as e:  ## if failed, report it back to the user ##
        print ("Error: %s - %s." % (e.filename, e.strerror))
