#!/bin/sh

for i in $( ls *-top*); do
    nl $i > $i.numbered
done
