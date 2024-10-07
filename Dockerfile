FROM continuumio/miniconda3

COPY env.yml .

RUN conda env create -f env.yml

ENV PATH /opt/miniconda3/envs/ip-rest-api-py/bin:$PATH

COPY . /app
WORKDIR /app

EXPOSE 5000

CMD ["conda", "run", "-n", "ip-rest-api-py", "python", "app/main.py"]
