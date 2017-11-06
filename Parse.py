
# coding: utf-8


# In[16]:

import re
def parse(a):
    dic = None
    
    ## rerouted
    if 'rerouted' in a:

        a_split = a.split('rerouted')
        first = a_split[0]
        second = a_split[1]

        ##find lines reroute other
        line_a = re.findall('[a-zA-Z0-9]*_LINE', second)

        ##find lines that will be rerouted
        line_b = re.findall('[a-zA-Z0-9]*_LINE', first)

        #direction
        bound = re.findall('_LINE (.*?) trains', first)

        ##between
        stations = re.findall('after (.*?) to (.*)', a)
        start = stations[0][0]
        end = stations[0][1]


        dic = {'type': 'rerout',
               'rerouted by': line_a,
               'rerouting': line_b,
               'from': start,
               'to': end }
    

    elif ('platform' in a and 'closed' in a) or ('platforms' in a and 'closed' in a):

        linebound, rest = re.split('platforms|platform', a)

        #line
        line = re.findall('[a-zA-Z0-9]*_LINE', linebound)

        #direction
        bound = re.findall('[a-zA-Z0-9]*-bound', linebound)

        #reason
        reason = re.findall('for (.*)', rest)

        #stations
        stations_s = re.findall('platform at (.*?) closed|platforms at (.*?) closed ', a)[-1][-1].strip(' are').strip(' is')
        stations = re.split(', | and ',stations_s)

        dic = {'type': 'platform close',
              'direction': bound[0],
              'reason': reason[0],
              'stations':stations,
              'lines': line}  
    
    
    ## close
    elif 'closed' in a:

        ## find lines 
        lines = re.findall('[a-zA-Z0-9]*_LINE', a)

        ## stations
        last_station = lines[-1]
        s = last_station + ' (.*?) is|'+ last_station + ' (.*?) are'
        stations_s = re.findall(s, a)[-1][-1]
        stations = re.split(', | and ',stations_s)


        ## reason 
        reason = re.findall('closed for (.*)', a)[0]

        dic = {'type': 'close',
               'lines': lines,
               'stations': stations,
               'reason': reason}
    
    ## local stops
    elif 'local stops' in a:

        ## find lines 
        lines = re.findall('[a-zA-Z0-9]*_LINE', a)

        ## direction
        bound = re.findall('in (.*?) directions', a)[0]

        ## stations
        stations_s = re.findall('local stops (.*?) at (.*)', a)[0][1]
        stations = re.split(', | and ',stations_s)

        dic = {'type': 'local stops',
               'lines': lines,
               'direction': bound ,
               'stations': stations}
    
    
    
    ## platform change
    elif ('platforms' or 'platform' in a) and ('board' in a):

        ##find lines 
        lines = re.findall('[a-zA-Z0-9]*_LINE', a)

        ##from to
        stations = re.findall('from (.*?) to (.*) board', a)
        start = stations[0][0]
        end = stations[0][1]

        ##new platform
        platform = re.findall('at the (.*?) platform', a)[0]

        
        dic = {'type': 'change platform',
               'lines': lines,
               'board at': platform,
               'from': start,
               'to': end }
        
        
    ## replace
    elif 'replace' in a:

        a_split = a.split('replace')
        first = a_split[0]
        second = a_split[1]

        ##find lines replacing other
        line_a = re.findall('[a-zA-Z0-9]*_LINE', first)

        ##find lines that will be replaced
        line_b = re.findall('[a-zA-Z0-9]*_LINE', second)

        ##find time 
        time = re.findall('replace (.*?)  [a-zA-Z0-9]*_LINE', a)[-1]

        ##between
        stations = re.findall('between (.*?) and (.*)', a)
        start = stations[0][0]
        end = stations[0][1]


        dic = {'type': 'replace',
               'replaced by': line_a,
               'replacing': line_b,
               'time': time,
               'from': start,
               'to': end }
        
    
    ## skip
    elif 'skip' in a:
        ##find lines
        line = re.findall('[a-zA-Z0-9]*_LINE', a)
        
        ##find bound
        last_line = line[-1]
        text = str(last_line) + r' (.*?) trains'
        bounds = re.findall(text, a)
        if bounds == []:
            bound = []
        else:
            bound = bounds[0]
        
        ##Stations
        stations_s = re.findall('skip (.*)', a)
        stations = re.split(', | and ',stations_s[0])
        
        dic = {'type': 'skip',
               'lines': line,
               'direction': bound,
               'stations': stations}
     

        
    ## run express
    elif 'run express' in a:
        ##find lines
        line = re.findall('[a-zA-Z0-9]*_LINE', a)

        ##find bound
        last_line = line[-1]
        text = str(last_line) + r' (.*?) trains'
        bound = re.findall(text, a)[0]

        ##station from 
        start = re.findall(r'from (.*?) to', a)

        ##station to
        end = re.findall('to (.*)', a)
        

        dic = {'type': 'run express',
               'lines': line,
               'direction': bound,
               'from': start,
               'to': end}
    
    ## run local
    elif 'run local' in a:
        
        if 'via' in a:
            
            ##split the sentence 
            first, second = a.split('via')
            
            ##find lines 
            line = re.findall('[a-zA-Z0-9]*_LINE', first)
            
            ##via
            via = re.findall('[a-zA-Z0-9]*_LINE', first)
            
            ##find bound
            last_line = line[-1]
            text = str(last_line) + r' (.*?) trains'
            bound = re.findall(text, first)[0]

            ##station from 
            start = re.findall(r'from (.*?) to', second)

            ##station to
            end = re.findall('to (.*)', second)
            
            dic = {'type': 'run local',
                   'lines': line,
                   'via' : via,
                   'direction': bound,
                   'from': start,
                   'to': end}
                      
        else:
            ##find lines
            line = re.findall('[a-zA-Z0-9]*_LINE', a)

            ##find bound
            last_line = line[-1]
            text = str(last_line) + r' (.*?) trains'
            bound = re.findall(text, a)[0]

            ##station from 
            start = re.findall(r'from (.*?) to', a)

            ##station to
            end = re.findall('to (.*)', a)
            
            ##via?
            via = 'itself'
            
            dic = {'type': 'run local',
                   'lines': line,
                   'via' : via,
                   'direction': bound,
                   'from': start,
                   'to': end}

        
    ## operation frequency    
    elif 'operates every' in a:
        
        ##find lines
        line = re.findall('[a-zA-Z0-9]*_LINE Service', a)
        line = [x.strip(' Service') for x in line]

        ##frequency
        freq = re.findall('every (.*) between',a)

        ##start from
        start = re.findall(r'between (.*?) and', a)

        ##end to
        end = re.findall('%s and (.*)'%start[0], a)

        dic = {'type' : 'operate frequency',
              'lines' : line,
              'frequency' : freq[0],
              'from' : start[0],
              'to' : end[0]}
        
        
    ## Service end early
    elif 'ends early' in a or 'end early' in a:

        ##find lines
        line = re.findall('[a-zA-Z0-9]*_LINE Service', a)
        line = [x.strip(' Service') for x in line]

        ##No direction

        ##start from
        start = re.findall(r'between (.*?) and', a)

        ##alternative lines
        s_2 = a.replace(line[0],'')
        alt_lines = re.findall('[a-zA-Z0-9]*_LINE', s_2)
        
        ##end to
        end = re.findall('and (.*) %s'%alt_lines[0], a)

        dic = {'lines': line,
               'from': start[0],
               'to' : end,
               'alt lines' : alt_lines,
               'type' : 'end early'}    
    
    
    ## NO TRAIN
    elif 'No trains' in a:

        ##find lines
        line = re.findall('[a-zA-Z0-9]*_LINE', a)

        if 'running' in a:
            start = 'all stations'
            end = 'all stations'
            
        else:
            ##station from
            start = re.findall(r'between (.*?) and', a)[0]

            ##station to
            end = re.findall('and (.*)', a)[0]

        dic = {'lines' : line,
               'from': start,
               'to': end,
              'type': 'No train'}
     
    ## ENTRANCE CLOSURE
    elif 'Entrance Closure' in a:

        ##find lines
        line = re.findall('[a-zA-Z0-9]*_LINE', a)

        ##stop
        stop = re.findall('_LINE (.*?) Station', a)

        dic = {'lines' : line,
                'station' : stop,
                'type' : 'Entrance Closure'}
 
   
    ## restore
    elif 'restored' in a:
        
        ##find lines
        lines = re.findall('[a-zA-Z0-9]*_LINE', a)
        
        ##stations
        stations_s = re.findall('at (.*)', a)[0]
        stations = re.split(', | and ',stations_s)
        
        dic = {'lines' : lines,
               'station' : stations,
               'type' : 'restore'}

    if dic == None:
        print("no category found")
        return None
    else:
        return dic

