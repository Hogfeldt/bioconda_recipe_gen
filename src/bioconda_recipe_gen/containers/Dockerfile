FROM alpine:3.7

RUN echo http://dl.alpinelinux.org/alpine/edge/testing >> /etc/apk/repositories
#RUN echo http://dl.alpinelinux.org/alpine/edge/main >> /etc/apk/repositories

RUN apk add --update \ 
    bash \
    g++ \
    gcc \
    cmake \
    make  
    
WORKDIR /package
