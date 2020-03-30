FROM perhogfeldt/conda-base:latest

RUN conda install bioconda-utils

RUN git clone https://github.com/Hogfeldt/bioconda_recipe_gen.git 

RUN pip install bioconda_recipe_gen/

ENV TINI_VERSION v0.16.1
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini

ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD [ "/bin/bash" ]
