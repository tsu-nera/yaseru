#!/bin/bash
source ~/miniconda3/etc/profile.d/conda.sh
conda activate yaseru

HOMEDIR=${HOME}/repo/yaseru

cd ${HOMEDIR}

inv daily-today
inv merge
