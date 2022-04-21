f1 = open("OS_Auto_Schedule.xml", "w").writelines([l for l in open("_tealeaves\\tealeaves.log").readlines() if  "E - core_analytics - missing process " in l])

with open("Conf\\OS_Shell\\rba_osshell_sched_dy.xml", "r") as f:
    contents = f.readlines()

Lines = open("OS_Auto_Schedule.xml", "r").readlines()

Line_Init_formats= []
Line_Run_formats= []
Line_others_formats = []

for line in Lines:
    str_add = line.replace("E - core_analytics - missing process ", "                    <SW-SERVICE-REF>").replace('\n','') + "</SW-SERVICE-REF>\n"

    if str_add not in contents:
        if "_Init" or "_SyncIni" or "_SyncAngular" in line:
            Line_Init_formats.append(str_add)
        elif "_Run" or "_SyncS0" or "_SyncS1" or "_Sync" in line:
            Line_Run_formats.append(str_add)
        else:
            Line_others_formats.append(str_add)

add_contents=[""]

proc_others = "".join(Line_others_formats)
add_contents.insert(0, proc_others)

proc_runs = "".join(Line_Run_formats)
add_contents.insert(0, proc_runs)

proc_inits = "".join(Line_Init_formats)
add_contents.insert(0, proc_inits)

with open("OS_Auto_Schedule.xml", "w") as f:
    add_contents_str = "".join(add_contents)
    f.write(add_contents_str)





section=[]

c = 0
st_line = 0
for line in contents:
    c+=1
    
    if "<SHORT-LABEL>None related adapters</SHORT-LABEL>" in line:
        section.append(c)
        st_line += 1

    if (st_line==1):
        if "_Init</SW-SERVICE-REF>" or "_SyncIni</SW-SERVICE-REF>" or "_SyncAngular</SW-SERVICE-REF>" in line:
            section.append(c)
            #print("proc init add line: ",c)
            st_line += 1
            

    if (st_line==3):
        if "_Run</SW-SERVICE-REF>" or "_SyncS0</SW-SERVICE-REF>" or "_SyncS1</SW-SERVICE-REF>" or "_Sync</SW-SERVICE-REF>" in line:
            section.append(c)
            #print("proc run add line: ",c)
            st_line = 0
        
        
if Line_Init_formats == []:
    print ('No line _Init added')
else:
    proc_inits = "".join(Line_Init_formats)
    print(proc_inits)
    contents.insert(section[1], proc_inits)
    print("Added from line: ",section[1])
print ("\n***********************************************************\n")

if Line_Run_formats == []:
    print ('No line _Run added')
else:
    proc_runs = "".join(Line_Run_formats)
    print(proc_runs)
    contents.insert(section[3]+1, proc_runs)
    print("Added from line: ",section[3]+1)
print("\n***********************************************************\n")

if Line_others_formats == []:
    print ('No line _Other added')
else:
    proc_others = "".join(Line_others_formats)
    print(proc_others)
    #contents.insert(section[3]+1, proc_runs)
    print("WARNING: Other procs please take care by hand")
print("\n***********************************************************\n")

with open("Conf\\OS_Shell\\rba_osshell_sched_dy.xml", "w") as f:
    contents_str = "".join(contents)
    f.write(contents_str)


