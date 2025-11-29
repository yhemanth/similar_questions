#!/bin/sh

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <module-name>"
    exit 1
fi

MODULE_NAME="${1}"
IMG_SRC_DIR="${HOME}/Desktop/images"
IMG_SRC_FILE="Photos-1-001.zip"
unzip -d ${IMG_SRC_DIR} ${IMG_SRC_DIR}/${IMG_SRC_FILE}
i=1; 
for file in `ls -l ${IMG_SRC_DIR}/*.jpg | awk '{print $NF}'`; 
do 
    mv $file ${IMG_SRC_DIR}/${MODULE_NAME}-$i.jpg; 
    ((i++)); 
done