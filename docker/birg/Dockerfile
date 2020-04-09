FROM perhogfeldt/conda-base:latest

# Install dependecies
RUN conda create --yes -n birg python=3.6 bioconda-utils &&\
    conda clean --all

# Conda activate
ENV PATH="/opt/conda/envs/birg/bin:${PATH}"

# Install BiRG
RUN git clone https://github.com/birgorg/birg.git &&\
    pip install birg/ &&\
    rm -rf birg

# TEST
RUN bioconda-utils --help
RUN birg --help

# Setup TINI
ENV TINI_VERSION v0.16.1
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini

WORKDIR /home
ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD [ "/bin/bash" ]

