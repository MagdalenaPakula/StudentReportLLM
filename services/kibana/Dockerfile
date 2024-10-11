FROM docker.elastic.co/kibana/kibana:7.10.0

COPY --chown=kibana setup_kibana.sh setup_kibana.sh

ENTRYPOINT ["./setup_kibana.sh"]