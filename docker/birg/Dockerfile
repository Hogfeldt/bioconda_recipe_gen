FROM perhogfeldt/conda-base:latest

RUN conda create --yes -n birg python=3.6 bioconda-utils

# Conda activate
ENV PATH="/opt/conda/envs/birg/bin:${PATH}"

# Install Bioconda_Recipe_Gen
RUN git clone https://github.com/birgorg/birg.git 
RUN pip install birg/

# TEST
RUN bioconda-utils --help
RUN birg --help

ENV TINI_VERSION v0.16.1
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini

ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD [ "/bin/bash" ]

