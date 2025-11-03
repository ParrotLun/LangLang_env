FROM quay.io/jupyter/minimal-notebook:2025-09-30

COPY requirements.txt /tmp/requirements.txt


USER root

RUN pip install --no-cache-dir -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt && \
    rm -rf /tmp/* \
    echo "jovyan ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

USER $NB_USER

WORKDIR /mlsteam/lab

CMD ["sh", "-c", "start-notebook.py --port=${JUPYTER_PORT:-8888} --NotebookApp.token='' --NotebookApp.password=''"]

