# Workflow for selecting representative questions

## Current workflow
This is the current workflow, which can be hugely improved.

* Scan the questions using Adobe scanner on mobile.
   * It is best to scan one module at a time.
* Transfer to laptop.
* Upload the file to https://snip.mathpix.com/home
* Export the file as a markdown.
* Post-process the file to make each question come up in a single line.
* Convert them into a list of strings, enclosing in double quotes.
* Start the docker container with the similar_questions notebook.
* Copy the questions into the cell with the sample questions.
* Change the number of clusters to be according to the number of samples needed.
* Run the cells in the notebook to generate the clusters and representative questions.
* Mark the questions in the notebook.

## Improvements possible

* Do we really need mathpix? What we want is to convert a PDF with text including mathematical symbols to a markdown format. Is there a library that can do this for us?
   * Research with GPT shows that the PDF I scan does not embed text well, it is actually some kind of image embedding. Hence, the workflow requires PDF -> OCR -> Markdown.
   * I verified this by copy-pasting content in the PDF and it is garbled where the math symbols start showing up.
* If the above is present, then we don't need to do post-processing like converting to a single line etc. That can be folded into code.
* Even if the mathpix usage cannot be avoided, we can:
   * Look to automate mathpix through their API.
   * Do post processing through code.
* The inputs to the ipynb can be read through a file that can be replaced. That way we don't need to copy the questions into a python array format everytime.
* The whole workflow can be easily automated from the point of generating the questions in a single line to getting the representative questions from the clusters.
* It is not entirely clear if the similarity is working as well as it should. We can check if there is a more superior embedding model that we can try.
