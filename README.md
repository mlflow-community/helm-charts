# MLflow Community Helm Charts

Community-maintained Helm charts for [MLflow](https://mlflow.org/).

Forked from [community-charts/helm-charts](https://github.com/community-charts/helm-charts) to apply the fix for the official MLflow image and ensure continued maintenance. This chart uses the **official `ghcr.io/mlflow/mlflow` image** published by the MLflow project.

## Add the Helm repository

```bash
helm repo add mlflow-community https://mlflow-community.github.io/helm-charts
helm repo update
```

## Install MLflow

```bash
helm install mlflow mlflow-community/mlflow
```

## Upgrade MLflow

```bash
helm upgrade mlflow mlflow-community/mlflow
```

## Charts

| Chart | Description |
|-------|-------------|
| [mlflow](charts/mlflow) | MLflow — open source platform for the machine learning lifecycle |

---

## Image

This chart uses the **official MLflow image** from `ghcr.io/mlflow/mlflow`, maintained by the MLflow project and published automatically on every release.

The default image flavor is `full`, which includes extra ML framework dependencies (scikit-learn, PyTorch, etc.):

```
ghcr.io/mlflow/mlflow:<version>-full
```

To use the minimal image instead:

```yaml
# values.yaml
image:
  flavor: ""
```

To pin an exact tag (overrides `flavor`):

```yaml
image:
  tag: "v3.10.1-full"
```

---

## Extra pip packages

For cloud storage backends, auth plugins, or other extras, use `extraPipPackages`. This creates an init container that installs the packages at startup — no custom image required.

```yaml
# values.yaml
extraPipPackages:
  - boto3              # AWS S3 artifact storage
  - azure-identity     # Azure Blob artifact storage
```

The packages are installed to `/mlflow/pip-packages` and `PYTHONPATH` is set automatically.

### Common examples

**AWS S3 artifact storage:**

```yaml
extraPipPackages:
  - boto3

artifactRoot:
  s3:
    enabled: true
    bucket: my-bucket
    path: mlflow
```

**Azure Blob Storage:**

```yaml
extraPipPackages:
  - azure-identity
  - azure-storage-blob

artifactRoot:
  azureBlob:
    enabled: true
    storageAccount: myaccount
    container: mlflow
    path: artifacts
```

**Google Cloud Storage:**

```yaml
extraPipPackages:
  - google-cloud-storage

artifactRoot:
  gcs:
    enabled: true
    bucket: my-bucket
    path: mlflow
```

**MLflow basic auth:**

```yaml
extraPipPackages:
  - mlflow[auth]

auth:
  enabled: true
```

**OIDC auth:**

```yaml
extraPipPackages:
  - mlflow-oidc-auth
```

**Prometheus metrics:**

```yaml
extraPipPackages:
  - prometheus-flask-exporter
```

---

## Logging

MLflow 3.x uses uvicorn as the default server. The chart injects `--uvicorn-opts=--log-level=<level>` automatically when `log.enabled: true`. To disable log-level injection:

```yaml
log:
  enabled: false
```

---

## Attribution

This chart is based on the work from [community-charts/helm-charts](https://github.com/community-charts/helm-charts), licensed under MIT.
