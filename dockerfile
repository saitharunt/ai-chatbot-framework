FROM python:2

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m nltk.downloader "averaged_perceptron_tagger"; python
RUN python -m nltk.downloader "punkt"; python
RUN python -m nltk.downloader "stopwords"; python
RUN python -m nltk.downloader "wordnet"; python
RUN python -m spacy download en; python
RUN pip install --user numpy

RUN pip install --user Cython

RUN pip install --user fasttext  flask flask_cors

EXPOSE 8080

COPY . .

COPY ./app/training_data !data.* /usr/src/app/training_data

RUN chmod 777 /usr/src/app/training_data/data.txt

CMD ["make","run_docker"]