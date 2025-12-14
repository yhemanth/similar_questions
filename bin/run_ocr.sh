#!/bin/sh

if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <module-name> <file-count> [model-name]"
    exit 1
fi

MODULE_NAME="${1}"
FILE_COUNT="${2}"
IMG_SRC_DIR="${HOME}/Desktop/images"
QUESTIONS_FILE="all-questions.md"

MODEL_NAME="gpt-5.2"
if [ "$#" -eq 3 ]; then
    MODEL_NAME="${3}"
fi

mkdir -p output/${MODULE_NAME}
cd src/
for (( i=1; i<=${FILE_COUNT}; i++ )); 
do 
    python image_to_questions.py ${IMG_SRC_DIR}/${MODULE_NAME}-$i.jpg ../output/${MODULE_NAME}/${MODULE_NAME}-$i.md ${MODEL_NAME};
    sleep 5; 
done