#!/bin/bash

if [ -z $1 ]
then
  echo "Needs a program name as argument"
fi

python3 lexic.py $1
python3 parser.py