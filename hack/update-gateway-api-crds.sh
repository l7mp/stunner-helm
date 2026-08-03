#!/bin/sh
# Regenerate the Gateway API CRD subcharts of the stunner chart from the pinned upstream
# release. The subcharts vendor the per-CRD files from config/crd/<channel>/ of the release
# tag; the safe-upgrades ValidatingAdmissionPolicy that ships next to them is deliberately
# not taken (see the chart history: a cluster-wide fail-closed guard does not belong in a
# helm crds/ directory, which is install-only). Run from the repository root, then review
# the diff and bump the subchart and dependency versions if the release changed:
#
#     GATEWAY_API_VERSION=v1.6.1 ./hack/update-gateway-api-crds.sh
#     helm dependency update helm/stunner
set -eu

GATEWAY_API_VERSION="${GATEWAY_API_VERSION:?set GATEWAY_API_VERSION, e.g. v1.6.1}"
RAW="https://raw.githubusercontent.com/kubernetes-sigs/gateway-api/${GATEWAY_API_VERSION}/config/crd"
API="https://api.github.com/repos/kubernetes-sigs/gateway-api/contents/config/crd"

for channel in standard experimental; do
    out="helm/stunner/charts/gateway-api-${channel}-crds/crds/gateway-api-crds.yaml"
    : > "$out"
    # one file per CRD; skip the ValidatingAdmissionPolicy and the kustomization
    files=$(curl -sf "${API}/${channel}?ref=${GATEWAY_API_VERSION}" \
        | sed -n 's/.*"name": *"\(gateway\.networking[^"]*\)".*/\1/p' | grep -v vap)
    [ -n "$files" ] || { echo "no CRD files found for ${channel}" >&2; exit 1; }
    for f in $files; do
        printf -- '---\n' >> "$out"
        curl -sf "${RAW}/${channel}/${f}" >> "$out"
    done
    echo "${out}: $(grep -c '^kind: CustomResourceDefinition' "$out") CRDs at ${GATEWAY_API_VERSION}"
done
