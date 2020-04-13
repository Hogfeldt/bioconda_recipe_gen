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
 
WORKDIR /home
ENTRYPOINT ["birg"]
CMD [ "/bin/bash" ]
