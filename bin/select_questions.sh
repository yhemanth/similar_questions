#!/bin/sh

if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <module-name> <question-count>"
    exit 1
fi

MODULE_NAME="${1}"
QUESTION_COUNT="${2}"

cat output/${MODULE_NAME}/${MODULE_NAME}-*.md > output/${MODULE_NAME}/all-questions.md
cd src/
python similar_questions.py ${MODULE_NAME} ${QUESTION_COUNT}