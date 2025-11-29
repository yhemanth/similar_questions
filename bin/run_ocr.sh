#!/bin/sh

if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <module-name> <file-count>"
    exit 1
fi

MODULE_NAME="${1}"
FILE_COUNT="${2}"
IMG_SRC_DIR="${HOME}/Desktop/images"
QUESTIONS_FILE="all-questions.md"

mkdir -p output/${MODULE_NAME}
for (( i=1; i<=${FILE_COUNT}; i++ )); 
do 
    python image_to_questions.py ${IMG_SRC_DIR}/${MODULE_NAME}/${MODULE_NAME}-$i.jpg output/${MODULE_NAME}/${MODULE_NAME}-$i.md; 
    sleep 5; 
done

cat output/${MODULE_NAME}/${MODULE_NAME}*.md > output/${MODULE_NAME}/${QUESTIONS_FILE}