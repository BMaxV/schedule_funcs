
#task class is the template for a particular task
#task is the intance.

#so "cleaning" vs. "cleaning on thursday for 30 minutes"

class task_class:
    def __init__(self,name,
            planned_duration=1,
            prefered_day_frequency=0,
            prefered_time=None,
            prefered_day_type=None,
            priority=float("inf")):
        self.name=name
        self.planned_duration=planned_duration
        self.prefered_day_frequency=prefered_day_frequency
        self.prefered_time=prefered_time
        self.prefered_day_type=prefered_day_type
        self.priority=priority
        
        #day_types
        #there are "work day" and "free" days

class task:
    def __init__(self,name,
            planned_duration=1,
            prefered_day_frequency=None,
            prefered_time=None,
            prefered_day_type=None,
            priority=float("inf")):
                
        self.name=name
        self.planned_duration=planned_duration
        self.prefered_day_frequency=prefered_day_frequency
        self.prefered_time=None
        self.prefered_day_type=prefered_day_type
        self.priority=priority
        
    def __repr__(self):
        s="<"+self.name+str(self.planned_duration)+str(self.prefered_day_frequency)+">"
        return s

def remove_conflict(day):
    print("start listing")
    for x in day:
        print(x)
    
    cant_schedule=[]
    
    #create a local copy
    day=list(day)
    restart=True
    while restart:
        #when the thing HAS BEEN RESCHEDULED
        #restart to check things are actually conflict free now.
        #when I find nothing, quit the loop.
        restart=False
        day.sort(key=lambda x : x[1])
        c=0
        m=len(day)
        while c < m-1:
            event0=day[c]
            event1=day[c+1]
            
            #this is I HAVE FOUND SOMETHING.
            #so at the end of this, I need to set restart to True.
            #do I have to break?
            
            #how do I make sure stuff I couldn't schedule doesn't
            #end up in this thing again?
            
            if event0[2]>event1[1]:
                #if end time bigger start time.
                print("conflict")
                print(event0)
                print(event1)
                print(event0[3].name,event1[3].name)
                #move the task with lower priority
                if event0[3].priority <= event1[3].priority:
                    move_event=event1
                else: 
                    move_event=event0
                
                for x in day:
                    print(x)
                print("removing",move_event[3])
                
                    
                #remove the old one from the day.
                day.remove(move_event)
                for x in day:
                    print(x)
                #only the task matters now.
                task = move_event[3]
                print("moving", task.name)
                
                #move it close to my prefered time, 
                #minimize squared distance
                #to the end of a different task.
                if task.prefered_time!=None:
                    copy_y=list(day)
                    copy_y.sort(key = lambda x : (x[2]-task.prefered_time)**2)
                else:
                    copy_y=list(day)
                    
                done=False
                c=0
                m=len(copy_y)
                #then loop through my minimized results
                while c < m:
                    event_i=day.index(copy_y[c])
                    if event_i+1>=m:
                        #if it's already the last one get out.
                        break
                    event_j=day[event_i+1]
                    slot=event_j[1]-copy_y[c][2]
                    print(task.__dict__)
                    print(event_j[3].name,"start",event_j[1])
                    print(copy_y[c][3].name,"end",copy_y[c][2])
                    print(task.name,task.planned_duration)
                    #is there a time slot available?
                    if slot >= task.planned_duration:
                        print("putting",task.name,"at the end of",copy_y[c][3].name)
                        day.insert(event_i+1,(copy_y[c][0],copy_y[c][2],copy_y[c][2]+task.planned_duration,task))
                        
                        print(day[event_i][3].name,"'",day[event_i+1][3].name,"'",day[event_i+2][3].name)
                        print("timing",event_j[0],event_j[2],event_j[2]+task.planned_duration)
                        
                        #
                        done=True  
                        #yes, great, let's quit this assignment loop  
                        #restart here?         
                        print("done")   
                        for x in day:
                            print(x)
                        print("---")
                        
                    c+=1
                
                if not done:
                    #I didn't find a time slot.
                    #I don't want to schedule stuff that's
                    #interfering with sleep. like... no.
                    #exceptions can be made manually.
                    #just put it here for now.
                    cant_schedule.append(task)
                restart=True
                break
            c+=1
    
    return day, cant_schedule

def schedule_this(day,my_task,day_counter):
    if my_task.prefered_time !=None:
        day.append((day_counter,
                    my_task.prefered_time,
                    my_task.prefered_time+my_task.planned_duration,
                    task(**my_task.__dict__)))
                    
    else:
        day.append((day_counter,
                    8,
                    8+my_task.planned_duration,
                    task(**my_task.__dict__)))

def schedule_tasks(tasks):
    
    week=[]
    last_occurance={}
    day_counter=0
    
    print("tasks 0",tasks[0])
    #no. I shouldn't sort by prefered time first, I should sort by
    #priority first.
    prefered_times=[]
    non_specified=[]
    for x in tasks:
        if x.prefered_time!=None:
            prefered_times.append(x)
        else:
            non_specified.append(x)
    tasks.sort(key =lambda x : x.priority)
    prefered_times.sort(key=lambda x : x.prefered_time)
    couldnt_schedule=[]
    m_days=7
    
    while day_counter < m_days:
        print("day",day_counter)
        hour_counter=8
        day=[]
        
        for my_task in tasks:
            if my_task.prefered_day_type!=None:
                #should I schedule this at all?
                #if a preference is specified
                if is_special_day(day_counter)!=my_task.prefered_day_type:
                    #and it doesn't match
                    continue
            
            first_time=(my_task.name not in last_occurance)
            
            if first_time:
                print("first time",my_task.name)
                #but this doesn't check for conflicts.
                #I will start with priority 0, so it's pretty save to
                #say I absolutely want this to happen here.
                
                #and it's not certain that the prefered times are in order, so.
                schedule_this(day,my_task,day_counter)
                day, cant_schedule = remove_conflict(day)
                if my_task not in cant_schedule:
                    last_occurance[my_task.name]=day_counter
                couldnt_schedule+=cant_schedule
            
            print("doing frequency stuff now")
            print("---")
            frequency = ( day_counter > ( last_occurance[my_task.name] + my_task.prefered_day_frequency) )
            if frequency:
                print("frequency")
                schedule_this(day,my_task,day_counter)
                day, cant_schedule = remove_conflict(day)
                if my_task not in cant_schedule:
                    last_occurance[my_task.name]=day_counter
                couldnt_schedule+=cant_schedule
            for x in day:
                print(x)
            print("day, done")
            
        #So now I have just shoved things into my schedule.
        #is this the same?
        #hmmm.
        if False:
        #scheduling 'any time' things.
            for my_task in non_specified:
                done=False
                c=0
                m=len(day)-1
                while c < m:
                    this_e=day[c]
                    next_e=day[c+1]
                    print(this_e[3].name,next_e[3].name)
                    this_e[2]
                    next_e[1]
                    #if this event fits between the last and the next event,
                    #schedule it.
                    if this_e[2]+ my_task.planned_duration < next_e[1]:
                        print("squeezing in",my_task.name,this_e[2])
                        day.insert(day.index(next_e),
                        (day_counter,
                                this_e[2],
                                this_e[2]+my_task.planned_duration,
                                task(**my_task.__dict__)))
                        done=True
                            
                        break
                    c+=1
                if not done:
                    day.append((day_counter,day[-1][2],day[-1][2]+my_task.planned_duration,
                    task(**my_task.__dict__)))
            
        week+=day
        day, cant_schedule=remove_conflict(day)
        day_counter+=1
        
    return week

def is_special_day(d):
    """this has to return day type"""
    if d in [5,6]:
        return "free"
    return "work"

    
def convert_to_external(week):
    new_week=[]
    blocked=task_class("unavailable")
    event_block_start=0
    current_event=1
    block_counter=1
    
    while event_block_start+block_counter < len(week):
        print("event block start")
        print(event_block_start)
        #input()
        event1=week[event_block_start]
        block_counter=1
        while event_block_start+block_counter < len(week):
            
            #print(current_event)
            event2=week[event_block_start+block_counter]
            print(event1,event2)
            if event1[2]==event2[1]:
                print(event1[2],event2[1])
                #input()
                block_counter+=1
                current_event+=1
                event1=event2
                continue
            else:
                print("bc",block_counter)
                print(week[event_block_start])
                print(week[event_block_start+block_counter-1])
                new_week.append((week[event_block_start][0],
                                week[event_block_start][1],
                                week[event_block_start+block_counter-1][2],
                                task(**blocked.__dict__)))
                print("new_week",new_week)
                #input()
                event_block_start=event_block_start+block_counter+1
                break
                
    return new_week

if __name__=="__main__":
    test()
    
    
