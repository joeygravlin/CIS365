#!/usr/bin/env bash

# http://www.cis.gvsu.edu/~moorejar/WS18_CIS365/
COURSE=WS18_CIS365
PROF_USER=moorejar
COURSE_DIR='cis365/w18'
OUTPUT_DIR="${HOME}/gvsu/${COURSE_DIR}/${PROF_USER}/"
URL="http://www.cis.gvsu.edu/~${PROF_USER}/${COURSE}/"

#echo "${OUTPUT_DIR}"
#mkdir -p ./"${OUTPUT_DIR}"

wget --mirror --limit-rate=100k --wait=1 -e robots=off --no-parent --page-requisites --convert-links \
     -N \
     --no-if-modified-since \
     --no-host-directories --cut-dirs=1 \
     --directory-prefix="${OUTPUT_DIR}" \
     "${URL}"


