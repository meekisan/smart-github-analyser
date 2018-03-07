FROM neo4j:3.3
USER root
RUN apk add --update \
    python3 \
    py-pip \
  && pip install neo4j-doc-manager --pre
RUN echo "browser.remote_content_hostname_whitelist=*" >> /var/lib/neo4j/conf/neo4j.conf
