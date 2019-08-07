FROM jupyter/scipy-notebook

LABEL maintainer="Robert Koch <robert@kochie.io>"

# Install Tensorflow
RUN pip install --upgrade tensorflow==2.0.0-beta1
RUN conda clean --all -f -y
RUN fix-permissions $CONDA_DIR
RUN fix-permissions /home/$NB_USER
RUN python -c 'import tensorflow as tf; print(tf.__version__)'

USER $NB_UID