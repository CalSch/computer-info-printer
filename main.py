import subprocess
import pystache
import re

def run(cmd:str):
    args=["bash","-c",cmd]
    print(f"\nrunning '{' '.join(args)}'")
    out=subprocess.check_output(args).decode().removesuffix("\n")
    print(out)
    return out
def parse_text_table(text:str,delim:str=" +"):
    rows=[]
    for line in text.split("\n"):
        row=[]
        line=line.replace("Mounted on","Mounted_on")
        for l in re.split(delim,line):
            row.append(l)
        rows.append(row)
    return rows
def data_to_table(data,useHeader:bool=True):
    text="<table>\n"
    isHeader=useHeader
    for row in data:
        text+="\t<tr>\n"
        for col in row:
            if isHeader:
                text+=f"\t\t<th>{col}</th>\n"
            else:
                text+=f"\t\t<td>{col}</td>\n"
        text+="\t</tr>\n"
        isHeader=False
    text+="</table>\n"
    return text

cpu_text=run("lscpu")
cpu_lines=[]
for line in cpu_text.split("\n"):
    if (line=="" or
        line.startswith("Flags") or
        line.startswith("Vulnerability") or
        line.startswith("NUMA") or
        re.search(".* cache",line)
    ):
        continue
    cpu_lines.append(line)
cpu_text="\n".join(cpu_lines)
cpu_text=data_to_table(parse_text_table(cpu_text,"  +"),useHeader=False)

info={
    "disks"  :data_to_table(parse_text_table(run("df --si --print-type --exclude tmpfs"))),
    "ram"    :data_to_table(parse_text_table(run("free --human --si"))),
    "cpu"    :cpu_text,
    "usb"    :run("lsusb").replace(": ",":\n  "),
    "uname"  :run("uname -a"),
    "users"  :run("awk -F: '{ print $1}' /etc/passwd").replace("\n"," "),
    "ip"     :run("ip ad"),
}

with open('page.html','w') as f:
    text=open('template.html','r').read()
    for thing in info.keys():
        text=text.replace("{{"+thing+"}}",info[thing])
    f.write(text)