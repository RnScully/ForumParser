#Readme: this will take a text file with the Events.cfg events score in it and turn that into a nicer thing. 
#it eats a file called events.txt and outputs a file called events_output. Simple. 
#Also its terrible and needs a bit more work. 
#like, this is just not a finished thing. for example, further work includes it just GOING TO THE FORUM and collecting the information


def get_name_and_score(string):
    equal = string.index('=')
    text = string[equal+2:]
    space = text.index(' ')
    score = int(text[space:].strip('\n'))
    name = text[:space].strip(',') #if anyone has put a comma at the end of their name, this will mess them up. 
    return name, score


if __name__=="__main__":
    
    path = 'events.txt'
    with open(path, 'r') as file:
                lines = file.readlines()

    #cargoculting the hard way from geeks for geeks. Thanks geeks!
    # initializing split index list  
    block_indexes = []
    for idx, line in enumerate(lines):
        if line == '[EventData]\n':
            block_indexes.append(idx)
    block_indexes.pop(0) #get rid of the list made that will be "the guys up to the first entry"...because there are no guys before the first entry. No more empty list at front! 
    # using list comprehension + zip() to perform custom list split 
    events = [lines[i : j] for i, j in zip([0] + block_indexes, block_indexes + [None])] 

    sorted_scores =[]
    for groups in events:
        scores =[]
        sorted_scores.append(groups[1][5:].strip('\n'))
        for players in groups[2:]:
            scores.append(get_name_and_score(players))
        descending = sorted(scores, key=lambda player: player[1], reverse = True)
        sorted_scores.append('Total: {:,}'.format(sum([players[1] for players in scores])))
        formatted = []
        for i in descending:
            x = [i[0], "{:,}".format(i[1])]

            formatted.append(' '.join(x))  
        sorted_scores+=formatted
        sorted_scores.append('')

    output_document = open("events_output.txt", "w")
    for line in sorted_scores:
        output_document.write(line+'\n')
    output_document.close()

    
