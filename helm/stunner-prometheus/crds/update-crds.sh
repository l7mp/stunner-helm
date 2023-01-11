#!/usr/bin/env bash
# Helper script to manage CRD updates
if [ -z $1 ];
then
    echo "Usage: $0 <version to get>"
    exit 1
fi

set -e

VERSION=$1

FILES=(
    "crd-alertmanager-config.yaml"
    "crd-alertmanager.yaml"
    "crd-podmonitor.yaml"
    "crd-probes.yaml"
    "crd-prometheusrules.yaml"
    "crd-prometheus.yaml"
    "crd-servicemonitor.yaml"
    "crd-thanosrulers.yaml"
)

URL_PREFIX="https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v${VERSION}/example/prometheus-operator-crd/"
URL_POSTFIXS=(
    "monitoring.coreos.com_alertmanagerconfigs.yaml"
    "monitoring.coreos.com_alertmanagers.yaml"
    "monitoring.coreos.com_podmonitors.yaml"
    "monitoring.coreos.com_probes.yaml"
    "monitoring.coreos.com_prometheusrules.yaml"
    "monitoring.coreos.com_prometheuses.yaml"
    "monitoring.coreos.com_servicemonitors.yaml"
    "monitoring.coreos.com_thanosrulers.yaml"
)


for n in ${!FILES[@]};
do
    URL="${URL_PREFIX}${URL_POSTFIXS[$n]}"
    CONTENT=`curl -s $URL`
    echo "# ${URL}" > ${FILES[$n]}
    echo "$CONTENT" >> ${FILES[$n]}
done
