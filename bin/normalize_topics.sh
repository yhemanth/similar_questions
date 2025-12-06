#!/bin/sh

cd src/
python normalize_topics.py ../input/physics_input_topics.txt ../input/physics_normalized_topics.txt
python normalize_topics.py ../input/chemistry_input_topics.txt ../input/chemistry_normalized_topics.txt
python normalize_topics.py ../input/maths_input_topics.txt ../input/maths_normalized_topics.txt