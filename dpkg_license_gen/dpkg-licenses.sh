#!/bin/bash
# Copyright (c) 2020 Intel Corporation
#
# SPDX-License-Identifier: Apache-2.0
#
# Author: Karthik Kumaar 
set -e

CSV=0

case "$1" in
  --help|-h)
    cat >&2 <<.e
Lists all installed packages (dpkg -l similar format) and prints their licenses

Usage: $0
.e
    exit 1
    ;;
  -c)
    CSV=1
    ;;
esac

SCRIPTLIB=$(dirname $(readlink -f "$0"))/lib/
test -d "$SCRIPTLIB"

if [[ $CSV -eq 1 ]]
then 
  printf "\"St\",\"Name\",\"Version\",\"Arch\",\"Description\",\"Licenses\"\n"
else 
  format='%-2s %-2s %s %s \n'
  #printf "$format" "St" "Name" "Version" "Arch" "Description" "Licenses"
  printf "$format" "--" "----" "-------" "----" "-----------" "--------"
  printf "$format" "Name","Licenses","Version","Arch" >> out.csv
fi 

echo "collecting dpkg packages ..........."
COLUMNS=2000 dpkg -l | grep '^.[iufhwt]' | while read pState package pVer pArch pDesc; do
  license=
  for method in "$SCRIPTLIB"/reader*; do
    [ -f "$method" ] || continue
    license=$("$method" "$package")
    [ $? -eq 0 ] || exit 1
    [ -n "$license" ] || continue
    
    # remove line breaks and spaces
    #license=$(echo "$license" | tr '\n' ' ' | sed -r -e 's/ +/ /g' -e 's/^ +//' -e 's/ +$//')
    license=$(echo $license | cut -d' ' -f1)
    #echo "after:"$license
    [ -z "$license" ] || break
  done
  [ -n "$license" ] || license='unknown'

  if [[ $CSV -eq 1 ]]
  then
    #printf "\"$pState\",\"$package\",\"$pVer\",\"$pArch\",\"$pDesc\",\"$license\"\n"
    #printf "$format" "Name" "Version" "Licenses" >> test.csv
    printf "${package},${license},${pVer},${pArch}" >> test.csv
  else 
        
    printf "$format" "${package:0:30}","${license}","${pVer:0:6}","${pArch:0:6}","\n" >> out.csv
    #printf "$format" "$pState" "${package:0:30}" "${pVer:0:30}" "${pArch:0:6}" "${pDesc:0:60}" "$license" >> test1.csv
  fi 
done

# python modules
if [ -f "/usr/local/bin/pip3" ]  
then
    echo "collecting pip3 packages ..........."
    pip3 list --format=freeze > CSV_outputs/pip3_freeze_all_packages.txt
    printf "Name,Origin,License,Distributed,Notes/Comments\n" >> CSV_outputs/pip3_freeze_all_packages.csv
    pip3 list --format=freeze | cut -d= -f1 | \
    while read PYNAME; do
        ORIGIN=$(pip3 show $PYNAME | awk '/^Home-page/{printf $2}')
        LICENSE="$(pip3 show $PYNAME | sed -n '/License/p' | cut -d: -f2 | sed 's/\<Licences\>//g' | sed 's/\<License\>//g' | tr -d '[:space:]' | sed 's/[,]/\//')" 
        printf "${PYNAME},${ORIGIN},${LICENSE},Yes,\n" >> CSV_outputs/pip3_freeze_all_packages.csv
    done
fi