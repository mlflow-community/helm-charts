# MLflow Community Helm Charts

Community-maintained Helm charts for [MLflow](https://mlflow.org/).

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

## Attribution

This chart is based on the work from [community-charts/helm-charts](https://github.com/community-charts/helm-charts), licensed under MIT.
