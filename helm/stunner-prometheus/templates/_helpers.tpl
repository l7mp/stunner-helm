{{/*
Common labels
*/}}
{{- define "stunner-prometheus-helm-v1.labels" -}}
{{ include "stunner-prometheus-helm-v1.selectorLabels" . }}
app.kubernetes.io/version: {{ .Values.selectorLabels.version }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "stunner-prometheus-helm-v1.selectorLabels" -}}
app.kubernetes.io/component: {{ .Values.selectorLabels.component }}
app.kubernetes.io/name: {{ .Values.selectorLabels.name }}
{{- end }}
