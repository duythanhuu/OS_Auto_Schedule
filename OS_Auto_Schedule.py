f1 = open("OS_Auto_Schedule.xml", "w").writelines([l for l in open("_tealeaves\\tealeaves.log").readlines() if  "E - core_analytics - missing process " in l])


Lines = open("OS_Auto_Schedule.xml", "r").readlines()

Line_Init_formats= []
Line_Run_formats= []
Line_others_formats = []

for line in Lines:
    if "_Init" in line:
        Line_Init_formats.append(line.replace("E - core_analytics - missing process ", "<SW-SERVICE-REF>").strip() + "</SW-SERVICE-REF>\n")
    elif "_Run" in line:
        Line_Run_formats.append(line.replace("E - core_analytics - missing process ", "<SW-SERVICE-REF>").strip() + "</SW-SERVICE-REF>\n")
    else:
        Line_others_formats.append(line.replace("E - core_analytics - missing process ", "<SW-SERVICE-REF>").strip() + "</SW-SERVICE-REF>\n")

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


# C:\Users\THD2HC\Desktop\source\HD431\MG1CS051_H_RQONE029141670\Conf\OS_Shell\rba_osshell_sched_dy.xml

with open("Conf\\OS_Shell\\rba_osshell_sched_dy.xml", "r") as f:
    contents = f.readlines()
line_Init_section = 0
line_10ms_section = 0
for line in contents:
    if "<SHORT-NAME>OS_Ini_Task</SHORT-NAME>" in line:
        line_Init_section = contents.index(line)
        #print(line_Init_section)
    if "<SHORT-NAME>OS_10ms_Task</SHORT-NAME>" in line:
        line_10ms_section = contents.index(line)
        #print(line_10ms_section)

section=[]

c = 0
st_line = 0
for line in contents:
    c+=1
    
    if "<SHORT-LABEL>None related adapters</SHORT-LABEL>" in line:
        section.append(c)
        st_line += 1

    if (st_line==1):
        if "_Init</SW-SERVICE-REF>" in line:
            section.append(c)
            #print("proc init add line: ",c)
            st_line += 1
            

    if (st_line==3):
        if "_Run</SW-SERVICE-REF>" in line:
            section.append(c)
            #print("proc run add line: ",c)
            st_line = 0
        
        
#print(section)
        
proc_inits = "".join(Line_Init_formats)
print(proc_inits)
contents.insert(section[1], proc_inits)
print("Added from line: ",section[1], "\n***********************************************************\n")

proc_runs = "".join(Line_Run_formats)
print(proc_runs)
contents.insert(section[3]+1, proc_runs)
print("Added from line: ",section[3]+1, "\n***********************************************************\n")

proc_others = "".join(Line_others_formats)
print(proc_others)
contents.insert(section[3]+1, proc_runs)
print("WARNING: Other procs please take care by hand")

with open("Conf\\OS_Shell\\rba_osshell_sched_dy.xml", "w") as f:
    contents_str = "".join(contents)
    f.write(contents_str)


