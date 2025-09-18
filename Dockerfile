FROM python:3.10

RUN apt-get update && apt-get install -y git

RUN pip install --default-timeout=100 sentence-transformers scikit-learn pandas matplotlib seaborn jupyter

WORKDIR /app
COPY . /app

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]