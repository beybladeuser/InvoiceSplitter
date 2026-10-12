FROM quay.io/keycloak/keycloak:26.4.0

ENV KC_DB=postgres \
    KC_HEALTH_ENABLED=true

RUN /opt/keycloak/bin/kc.sh build

ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]
CMD ["start", "--optimized"]