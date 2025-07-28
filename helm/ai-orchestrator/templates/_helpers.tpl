{{- define "ai-orchestrator.name" -}}
ai-orchestrator
{{- end -}}

{{- define "ai-orchestrator.fullname" -}}
{{ include "ai-orchestrator.name" . }}
{{- end -}}
