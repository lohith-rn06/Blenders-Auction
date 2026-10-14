#!/bin/bash
for i in linux git jenkins kubernetes docker terraform
do 
	mkdir $i
	touch $i/Notes.md

done
