FROM perhogfeldt/conda-base:latest

RUN conda install conda-build conda-verify conda-forge-pinning

# Add conda_build config_file path to point at 'conda_build_config.yaml' from conda-forge-pinning package
RUN echo '\nconda_build:\n  config_file:  /opt/conda/conda_build_config.yaml' >> /root/.condarc

ENV TINI_VERSION v0.16.1
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini

ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD [ "/bin/bash" ]
