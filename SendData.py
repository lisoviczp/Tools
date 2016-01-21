import threading
import sys
import os
import requests

# This is a script that receives a list of files as an argument, does some simple reformatting
# and then sends the files to an endoint. 


def main(listOfFiles):
    global n_fail
    global n_sent
    global n_error
    lock = threading.Lock()
    i = 0
    threads = []

    # For each file in the arguments passed to the function, start a thread and run sendFile() 
    for eachFile in listOfFiles:
        i+=1
        t = threading.Thread(target= formatFile, args=[eachFile, i, lock])
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    # Log the summary of each run
    print "\n--- Summary ---"
    print "Sent: {}".format(n_sent)
    print "Failed: {}".format(n_fail)
    print "Error: {}".format(n_error)
    print "---------------\n"

def sendFile(inputFile, iteration, lock):
    global n_fail
    global n_sent
    global n_error
    newFileName = str(iteration) + "new_file_name.url"
    jsonWrite = open(newFileName, "w+")
    jsonWrite.write('{"type": "01", "list_of_things": [' )

    # lines is a list of every line in the file, ll is the last line
    readFile=open(inputFile, "r")
    lines = readFile.readlines()[:-1]
    try:
        lastLine = lines[-1][:-1]

        # Due to system restraints, we were forced to manually re-format some files that were to be delivered
        for aLine in lines:
            if aLine.count('FOO') == 1:
                if aLine[:-1] != lastLine:
                    aLine = aLine.replace('FOO==="thing_id":', '{"thing_id":')
                    aLine = aLine.replace('---', ']},')
                    jsonWrite.write(aLine)
                else:
                    aLine = aLine.replace('FOO==="thing_id":', '{"thing_id":')
                    aLine = aLine.replace('---', ']}]}')
                    jsonWrite.write(aLine)
            else:
                pass #print('Bad line: {}'.format(aLine))

        jsonWrite.close()
        readFile.close()

        # This is where one would specify the endpoint
        url = "www.sampleurl.com"

        # Using Python's Requests module to post the file to the endpoint
        payload = open(newFileName, 'r').read()
        r = requests.post(url,data=payload, headers={'content-type': 'application/json'})

        # Logging the output to retain records of each upload. Output from this script is written to log files elsewhere
        print("------ Sending File ------  \n"
            "\n > " + str(r.request.method) +
            "\n > Content-Length: " + str(r.request.headers.get('Content-Length')) +
            "\n File Sent - Response Code is: " + str(r.status_code) +
            "\n Response Text is: " + str(r.text)
            )

        # To save space, and if we see a successful post (202), we will delete the file already sent
        if r.status_code == 202:
            with lock:
                n_sent += 1
            print('Deleting file: {}'.format(inputFile))
            os.remove(inputFile)

        # If the receiving server cannot receive the file on first try, we will save the file under another name and
        # another process can pick it up. Due to space restraints, sometimes we have to utright delete the file 
        elif r.status_code == 400 or r.status_code == 403:
            with lock:
                n_fail += 1
            fail_file = '{}.fail'.format(inputFile)
            os.rename(inputFile, fail_file)
            # os.remove(fail_file)
        print('Deleting file: {}'.format(newFileName))
        os.remove(newFileName)
    except IndexError:
        with lock:
            n_error += 1
        print 'ERROR: Caught a bad file'
        error_file = '{}.fail'.format(inputFile)
        os.rename(inputFile, error_file)
        # os.remove(error_file)


if __name__ == '__main__':
    n_fail = 0
    n_sent = 0
    n_error = 0
    main(sys.argv[1:])