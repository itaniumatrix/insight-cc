import json
import datetime
import sys

def main(argv):
    """Main Function, read input/output filenames from commandline.
    """
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    clean_and_count(in_file, out_file)

def clean_and_count(filein, fileout):
    with open(filein) as tweetfile:
        f_out=open(fileout, 'w+')
        num_Unicode = 0
        for line in tweetfile:
            data = json.loads(line)
            try:
                text = data['text']
                timestamp = data['created_at']
                # Clean string of escape characters
                cleaned_string = clean_text_escape(text)
        
                #Remove Unicode characters if needed, increment counter
                if(has_unicode(cleaned_string)):
                    cleaned_string = clean_text_unicode(cleaned_string)
                    num_Unicode += 1
                
                #print('{} (timestamp: {})'.format(cleaned_string, timestamp))
                print('{} (timestamp: {})'.format(cleaned_string, timestamp), file=f_out)
                    
                    
            except:
                #Catch exception - Using this as a pass for errors, and
                #problems in input (missing 'text', and 'created_at' fields)
    
                pass
        print('\n{} tweets contained unicode.'.format(num_Unicode), file=f_out)
        f_out.close()

def clean_text_escape(string):
    """Remove Unicode - Python 3.x does this very cleanly with encoding / decoding. For escape characters,
    Only \n and \t and \/need to be manually changed. The other spec \" \' escape chars are automatically decoded 
    by Python during print. \' Seems to be disallowed in JSON, but if it makes it into the string, is managed by Python.
    """
    return string.replace('\n', ' ').replace('\t', ' ').replace('\/', '/')
    
    """For readability - above coded for slight speed bump
    string = string.replace('\n', ' ')
    string = string.replace('\t', ' ')
    string = string.replace('\/', '/')
    """

def clean_text_unicode(string):
    #Strip Unicode characters above ASCII 127
    string = string.encode('ascii', 'ignore').decode()
    return string
    
def has_unicode(string):
    """Returns boolean: if string has any Unicode characters (>127)
    Characters with decimal <32 are not, included since these are replaced rather than deleted
    """
    for char in string:
        if (ord(char) > 127):
            return True
    #If entire loop executes, all chars are ASCII
    return False
        

# Run this main program if the file is being called (not imported)
if __name__ == "__main__":
   main(sys.argv[1:])