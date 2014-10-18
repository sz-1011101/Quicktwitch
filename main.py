# This simple script retrieves streams from a searched term via twitch api, and opens this stream with livestreamer
# TODO:
#     use curses for proper menues
#     use livestreamer api instead of os.system(...)
#     code cleanup
import json
import urllib2
import os

#  input: List of streams
#  output: List of lists with relevant stream info(status, game, viewers)
def gather_stream_info(streams):
    stream_list = []
    for item in streams:
        stream_list.append([item["channel"]["display_name"], item["channel"]["game"], item["viewers"]])
    return stream_list

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
    for item in stream_list:
        print("(" + str(counter) + ") " + item[0] + " | "+ item[1] + " | " + unicode(item[2]) + " Viewers")
        counter += 1

#  Script entry point
def main():
   
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
        while (not valid_selection_done):   
            number_selected_stream = int(raw_input("-----------Enter number to open stream-------------:\n"))
            if number_selected_stream < 0 or number_selected_stream >= len(stream_list):
                print "Invalid number entered! Please try again!"
            else:
                valid_selection_done = True;
        
        # get stream quality
        valid_selection_done = False
        quality_options = { 0:"worst",
                           1:"mobile",
                         2:"low",
                         3:"medium",
                         4:"high",
                         5:"source",
                         6:"best"}
    
    
        while (not valid_selection_done):  
            
            print "O: worst"
            print "1: low"
            print "2: medium"
            print "3: high"
            print "4: source"
            print "5: best"
            
            number_selected_quality = int(raw_input("-----------Enter quality---------:\n"))
            

            
            if number_selected_quality < 0 or number_selected_quality > 4:
                print "Invalid number entered! Please try again!"
            else:
                valid_selection_done = True;
             
        
        # call livestreamer via os
        os.system("livestreamer twitch.tv/" + stream_list[number_selected_stream][0] + " " + quality_options[number_selected_quality])
    else:
        print "No stream found"
        
# Run entry point
main()
 
    
    
