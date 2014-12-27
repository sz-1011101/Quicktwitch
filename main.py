# This simple script retrieves streams from a searched term via twitch api, and opens this stream with livestreamer

import json
import urllib2
import os
import livestreamer

#  input: List of streams
#  output: List of lists with relevant stream info(status, game, viewers)
def gather_stream_info(streams):
    stream_list = []
    for item in streams:
        stream_list.append([item["channel"]["display_name"], item["channel"]["game"], item["viewers"]])
    return stream_list

#  input url as string
#  output url as string with escaped chars
#  replace unescaped chars
def escape_url(url):
    url = url.replace("=","\\=")
    url = url.replace("&","\\&")
    url = url.replace("?","\\?")
    return url

#  input: String with unescaped chars
#  output: String with escaped chars
def escape_string(unescaped_string):
    return unescaped_string.replace(" ", "%20")

#  input: List with stream attributes gathered previously
#  
#  Prints this list in readable format
def print_stream_list(stream_list):
    print "Results: "
    counter = 0
    string_to_display = ""
    for item in stream_list:
        string_to_display = string_to_display + "(" + str(counter) + ") " + item[0] + " | "+ item[1] + " | " + str(item[2]) + " Viewers\n"
        counter += 1
    print string_to_display
    
#  input: a streamer's name
#  output: returns list with tuples of quality and HLSStream-Objects
def get_avaible_streams(name):
    avaible = livestreamer.streams("http://twitch.tv/"+name)
    return avaible.items()

#  Script entry point
def main():
    try:
        # get the string and replace unescaped chars
        search_term = raw_input("Enter search term:\n")
        search_term = escape_string(search_term)
        
        # get the stream list and print it
        response = urllib2.urlopen("https://api.twitch.tv/kraken/search/streams?q=" + search_term + "&limit=100")
        response_read = response.read()
        response_json = json.loads(response_read)
        all_streams = response_json["streams"]
        stream_list = gather_stream_info(all_streams)
        print_stream_list(stream_list)
        
        if (len(stream_list) > 0):
            valid_selection_done = False
            number_selected_stream = -1
            number_selected_quality = -1
            
            # get user input number
            while not valid_selection_done:   
                number_selected_stream = int(raw_input("-----------Enter number to open stream-------------:\n"))
                if number_selected_stream < 0 or number_selected_stream >= len(stream_list):
                    print "Invalid number entered! Please try again!"
                else:
                    valid_selection_done = True;
            print "Retrieving qualitys..."
            counter = 0
            quality_stream_tuples = get_avaible_streams(stream_list[number_selected_stream][0])
            
            for (quality, url) in quality_stream_tuples:
                print("("+str(counter)+")"+str(quality))
                counter += 1
                
            # user selects quality
            valid_selection_done = False
            quality_setting = None
            
            while not valid_selection_done:
                quality_setting = int(raw_input("Enter quality:\n"))
                if quality_setting<0 or quality_setting >= len(quality_stream_tuples):
                    print "Invalid entry! Please try again!"
                else:
                    valid_selection_done = True
                        
            # user done selecting, extract url
            url_pipe = escape_url(quality_stream_tuples[quality_setting][1].url)
            print url_pipe
            os.system("vlc "+url_pipe)
            
            
        else:
            print "No stream found"
    except (KeyboardInterrupt): # Ctrl - C aborts the script
        print "Script interupted by user..."
        
# Script entry point
if __name__=="__main__":
    main()
 
    
    
