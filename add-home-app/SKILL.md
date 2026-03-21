---
name: add-home-app
description: "A skill for adding new applications to the `home-apps` Kubernetes cluster. Use this skill whenever the user wants to 'add an app', 'install a service', or 'setup a new tool' in the cluster, even if they don't explicitly mention the multi-source ArgoCD pattern, Tailscale, or CNPG."
---
# add-home-app


A skill for adding new applications to the `home-apps` Kubernetes cluster.

## Triggering
Use this skill whenever the user wants to "add an app", "install a service", or "setup a new tool" in the cluster. It triggers on requests like "Add Nextcloud to my cluster" or "Install a new instance of Gotify".

## Core Workflow
1. **App Directory**: Create a new directory `apps/<app-name>/`.
2. **Helm Values**: Create `apps/<app-name>/values.yaml` with appropriate overrides.
3. **Database (Optional)**: If the app requires Postgres, create `apps/<app-name>/postgres-cluster.yaml` using the CloudNative-PG (CNPG) `Cluster` resource.
4. **Ingress (Optional)**: If the app needs external access, create `apps/<app-name>/ingress.yaml` using the `tailscale` ingress class.
5. **Kustomization**: Create `apps/<app-name>/kustomization.yaml` to include local manifests (DB, Ingress, etc.).
6. **ArgoCD Application**: Create `argocd-apps/apps/<app-name>.yaml` using the multi-source pattern:
    - Source 1: Upstream Helm chart.
    - Source 2: Local repo for `valueFiles` (using `ref: values`).
    - Source 3: Local repo for Kustomize manifests (path `apps/<app-name>`).

## Reference Patterns

### Ingress (Tailscale)
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: <app-name>
  namespace: <app-name>
  annotations:
    tailscale.com/hostname: <app-name>
spec:
  ingressClassName: tailscale
  rules:
    - http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: <service-name>
                port:
                  number: <port>
```

### Database (CNPG)
```yaml
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: <app-name>-db
  namespace: <app-name>
spec:
  instances: 1
  imageName: ghcr.io/cloudnative-pg/postgresql:17.5
  storage:
    size: 2Gi
    storageClass: local-path
  bootstrap:
    initdb:
      database: <app-name>
      owner: <app-name>
```

### ArgoCD Application (Multi-source)
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: <app-name>
  namespace: argocd
spec:
  project: default
  sources:
    - repoURL: <upstream-repo>
      chart: <chart-name>
      targetRevision: <version>
      helm:
        valueFiles:
          - $values/apps/<app-name>/values.yaml
    - repoURL: https://github.com/grantmcd/home-apps.git
      targetRevision: main
      ref: values
    - repoURL: https://github.com/grantmcd/home-apps.git
      targetRevision: main
      path: apps/<app-name>
  destination:
    server: https://kubernetes.default.svc
    namespace: <app-name>
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```
