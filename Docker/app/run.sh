#!/bin/bash

set -xe
python shuffledWatermark.py | tee shuffle.txt
python extractWatermark.py | tee extract.txt