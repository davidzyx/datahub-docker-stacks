ARG BASE_TAG=latest
FROM davidzz/datahub-base-notebook:$BASE_TAG

USER jovyan

RUN pip install dpkt \
                nose \
                datascience && \
    python -c 'import matplotlib.pyplot' && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

RUN conda clean -tipsy

# import integration tests
# ENV TESTDIR=/usr/share/datahub/tests
# ARG DATASCIENCE_TESTDIR=${TESTDIR}/datascience-notebook
# COPY tests ${DATASCIENCE_TESTDIR}
# RUN chmod -R +rwx ${DATASCIENCE_TESTDIR}
# RUN chown 1000:1000 ${DATASCIENCE_TESTDIR}

ENV SHELL=/bin/bash
