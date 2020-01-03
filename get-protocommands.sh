#!/bin/bash

function filterprotodoc(){
    egrep '#### Command|### Device ' protocol.md | sed 's/#### Command /,/' | sed  's/### Device /;/'  | tr '\n' ' ' | tr ';' '\n' 
    echo 
}

function listcmdsraw(){
    filterprotodoc | while read line ;do 
        dev=""
        IFS=, 
        for elem in  $( echo "$line" ) ;do 
            if [ "$dev" == "" ] ;then 
                dev=$elem 
            else 
                echo "$( echo $dev| awk '{ print $1 }' ),$elem"
            fi
        done
    done
}

echo "DEVICE, COMMAND - DESCRIPTION" 

function listcmds(){
    listcmdsraw | sed 's/ - /;/' | sed 's/ $//' | tr ' /' '__' | awk -F\; '{ print $1 "," toupper($2)}' 
}

function dictify(){
#    cat | awk -F, '{ print "\""$3"\""" : { \n\t \"device\": \""$1"\" , \n\t \"command\": \""$2"\" \n},"  }'
    cat | awk -F, '{ cmdname="\""$3"\""; device="\""$1"\""; command="\""$2"\"" ; printf " %-35s : { \"device\": %4s , \"command\": %4s }, \n", cmdname,device,command  }'
}

#listcmds | awk -F, '{ print "\""$3"\""" : {  \"device\": \""$1"\" ,  \"command\": \""$2"\" },"  }'

#listcmds | awk -F, '{ print "\""$3"\""" : { \n\t \"device\": \""$1"\" , \n\t \"command\": \""$2"\" \n},"  }'
listcmds | grep _RESPONSE | dictify
echo "----------------------------"
listcmds | grep _EVENT | dictify
echo "----------------------------"
listcmds | egrep -v "_EVENT|_RESPONSE" | dictify