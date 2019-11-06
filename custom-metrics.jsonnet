local kp =
  (import 'kube-prometheus/kube-prometheus.libsonnet') +
  (import 'kube-prometheus/kube-prometheus-kubespray.libsonnet') +
  (import 'kube-prometheus/kube-prometheus-node-ports.libsonnet') +
  // Uncomment the following imports to enable its patches
  // (import 'kube-prometheus/kube-prometheus-anti-affinity.libsonnet') +
  // (import 'kube-prometheus/kube-prometheus-managed-cluster.libsonnet') +
  // (import 'kube-prometheus/kube-prometheus-static-etcd.libsonnet') +
  // (import 'kube-prometheus/kube-prometheus-thanos-sidecar.libsonnet') +
  {
    _config+:: {
      namespace: 'monitoring',
      // append extra configuration in prometheus adapter config (config.yaml)
      prometheusAdapter+:: {
        config+:: (importstr 'prometheus-adapter-extra-conf.yaml'),
      },
    },
    prometheusRules+:: {
      groups+: [
        {
          name: 'custom-metrics-group',
          rules: [
            {
              record: 'flask_latency_per_30',
              expr: 'rate(flask_http_request_duration_seconds_sum[30s])/rate(flask_http_request_duration_seconds_count[30s])',
            },
            {
              record: 'flask_latency_per_60',
              expr: 'rate(flask_http_request_duration_seconds_sum[60s])/rate(flask_http_request_duration_seconds_count[60s])',
            },
            {
              record: 'flask_latency_per_120',
              expr: 'rate(flask_http_request_duration_seconds_sum[120s])/rate(flask_http_request_duration_seconds_count[120s])',
            },
          ],
        },
      ],
   },
  };

{ ['00namespace-' + name]: kp.kubePrometheus[name] for name in std.objectFields(kp.kubePrometheus) } +
{ ['0prometheus-operator-' + name]: kp.prometheusOperator[name] for name in std.objectFields(kp.prometheusOperator) } +
{ ['node-exporter-' + name]: kp.nodeExporter[name] for name in std.objectFields(kp.nodeExporter) } +
{ ['kube-state-metrics-' + name]: kp.kubeStateMetrics[name] for name in std.objectFields(kp.kubeStateMetrics) } +
{ ['alertmanager-' + name]: kp.alertmanager[name] for name in std.objectFields(kp.alertmanager) } +
{ ['prometheus-' + name]: kp.prometheus[name] for name in std.objectFields(kp.prometheus) } +
{ ['prometheus-adapter-' + name]: kp.prometheusAdapter[name] for name in std.objectFields(kp.prometheusAdapter) } +
{ ['grafana-' + name]: kp.grafana[name] for name in std.objectFields(kp.grafana) }
