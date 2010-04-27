#!/bin/sh

if [ -e $1 ]
then
    cd $1
    for i in `ls`
    do 
	if [ -d $i ]
	then
	    cd $i
	    echo "creating $i.all"
	    for j in  `find . -name "$2"`
	    do
		echo "\t adding $j"
		cat $j >> ../$i.all
	    done
	    cd ..
	fi
    done 
    cd ..
else
    echo "dossier $1 introuvable"
    exit 1
fi

