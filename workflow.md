# Workflow for selecting representative questions

This is the current workflow, which can be hugely improved.

* Scan the questions using Adobe scanner on mobile.
   * It is best to scan one module at a time.
* Transfer to laptop.
* Upload the file to https://snip.mathpix.com/home
* Export the file as a markdown.
* Pre-process the file to make each question come up in a single line.
* Convert them into a list of strings, enclosing in double quotes.
* Start the docker container with the similar_questions notebook.
* Copy the questions into the cell with the sample questions.
* Change the number of clusters to be according to the number of samples needed.
* Run the cells in the notebook to generate the clusters and representative questions.
* Mark the questions in the notebook.