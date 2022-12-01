#!/bin/sh

FILE="input.txt"
INPUT=$(curl \
    --cookie "session=<cookie>" \
    https://adventofcode.com/2022/day/1/input)

echo $INPUT >> $FILE
