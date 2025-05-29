# SolicitudService - Plataforma de Servicios Estudiantiles

Este proyecto implementa un microservicio `SolicitudService` que forma parte de una arquitectura basada en microservicios orquestados en Kubernetes e integrados con **Istio**. El servicio permite la recepción, validación y reenvío de solicitudes académicas a un sistema externo mediante un adaptador SOAP, aplicando mecanismos de resiliencia, monitoreo y control de tráfico.

---

## 🧱 Arquitectura General

```
[Usuario] → [API Gateway con JWT + Rate Limiting] → [SolicitudService]
                                                  → [Sistema Académico]
                                                  → [Sistema de Seguridad]
                                                  → [Servicio Externo SOAP]
```

Todos los componentes están desplegados en Kubernetes y gestionados con Istio como malla de servicios, lo que permite aplicar políticas de tráfico, observabilidad y resiliencia.

---

## 🚀 Despliegue

### 1. Pre-requisitos

- Kubernetes (Minikube recomendado)
- Istio instalado (`istioctl install --set profile=demo`)
- Docker configurado con el contexto de Minikube
- Herramientas opcionales: `Prometheus`, `Grafana`, `Jaeger`, `Kiali`

### 2. Construcción de la imagen

```bash
cd solicitud_service/
eval $(minikube docker-env -p progreso2)
docker build -t solicitudservice:1.0 .
```

### 3. Despliegue de recursos

```bash
cd k8s/
kubectl apply -f .
kubectl port-forward -n istio-system svc/istio-ingressgateway 8080:80
```

> Asegúrate de tener activo el tunnel: `minikube tunnel`

---

## 🔁 Resiliencia

Se aplicaron las siguientes configuraciones en Istio:

### Retry Automático

- **Intentos:** 2
- **Timeout por intento:** 2s
- **Rutas afectadas:** `/soap`

### Circuit Breaker

- **Errores 5xx permitidos:** 3
- **Intervalo de detección:** 60s
- **Tiempo de expulsión:** 30s

Archivos YAML:

- `virtualservice-soap.yaml`
- `destinationrule-soap.yaml`

---

## 🔐 Seguridad y Políticas

El API Gateway aplica:

| Política                   | Implementación                   |
| -------------------------- | -------------------------------- |
| Autenticación JWT          | Istio AuthorizationPolicy        |
| Rate Limiting              | Istio Envoy Filter + ConfigMap   |
| Acceso solo a /solicitudes | VirtualService con match por URI |

---

## 📈 Monitoreo y Observabilidad

Herramientas empleadas:

| Herramienta | Función                          |
| ----------- | -------------------------------- |
| Prometheus  | Recolección de métricas          |
| Grafana     | Visualización en dashboards      |
| Jaeger      | Trazabilidad distribuida         |
| Kiali       | Visualización de tráfico y salud |

### Métricas capturadas

- `istio_requests_total`
- `istio_request_duration_milliseconds`
- `istio_request_size`
- `istio_response_size`

### Trazabilidad

Las trazas permiten rastrear la solicitud desde su entrada hasta el envío al sistema externo, identificando tiempos de respuesta, errores y latencia por servicio.

---

## 🧪 Pruebas

Puedes probar el endpoint principal:

```bash
curl -X POST http://<EXTERNAL-IP>/solicitudes -H "Authorization: Bearer <TOKEN>" -d '{"tipo":"certificado"}'
```

---

## 📂 Estructura del Proyecto

```
solicitud_service/
├── app/
│   └── main.py
├── Dockerfile
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── gateway.yaml
│   ├── virtualservice.yaml
│   ├── virtualservice-soap.yaml
│   └── destinationrule-soap.yaml
```

---

## ✍️ Autor

Julissa Ruales - Ingeniería de Software, Universidad de Las Américas (UDLA)
