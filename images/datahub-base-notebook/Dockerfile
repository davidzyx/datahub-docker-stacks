ARG PYTHON_VERSION=python-3.8.8
FROM jupyter/datascience-notebook:$PYTHON_VERSION

USER root
RUN apt-get update -y && \
    apt-get -qq install -y --no-install-recommends \
    git \
    curl \
    rsync \
    unzip \
    less \
    nano \
    vim \
    openssh-client \
    cmake \
    tmux \
    screen \
    gnupg \
    htop \
    wget \
    p7zip \
    p7zip-full && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
	chmod g-s /usr/bin/screen && \
	chmod 1777 /var/run/screen

COPY /scripts /usr/share/datahub/scripts/
COPY /scripts/jupyter_notebook_config.py /tmp/jupyter_notebook_config_extra.py
RUN cat /tmp/jupyter_notebook_config_extra.py >> /etc/jupyter/jupyter_notebook_config.py && \
    chmod -R uga+x /usr/share/datahub/scripts/ && \
    chmod -R uga+x /etc/jupyter/jupyter_notebook_config.py

USER jovyan

ARG PY_VER_SHORT=3.8

# nbconvert downgrade needed for nbgrader to work
RUN /usr/share/datahub/scripts/install-python-all.sh && \
	pip install pandas --upgrade && \
	pip install nltk && \
    pip install nbconvert==5.6.1 && \
    pip install jupyterhub==0.9.2 && \
	cat /usr/share/datahub/scripts/canvas_exporter.py > /opt/conda/lib/python$PY_VER_SHORT/site-packages/nbgrader/plugins/export.py && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER && \
    chown -R jovyan:users /opt/conda/etc/jupyter/nbconfig && \
    chmod -R +r /opt/conda/etc/jupyter/nbconfig

WORKDIR /home/jovyan
