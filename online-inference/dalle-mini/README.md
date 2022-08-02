# Docker
1. Build+Push downloader:
```bash
docker build -t tweldoncw/model-downloader:1 -f Dockerfile.downloader .
docker push tweldoncw/model-downloader:1
```
2. Deploy PVC
```bash
kubectl create -f 00-model-pvc.yaml
```
3. Deploy Download Job
```bash
kubectl create -f 01-model-download-job.yaml
```
4. Deploy/get isvc
5. Make request:
```bash
curl 10.146.217.19:8080/v1/models/dalle-mini:predict -d '{"prompt": "A grassy field with a single tree on a hill"}' | jq -r .image | base64 -d prediction.png && open prediction.png
```
# TODO
* Finish inferenceService Spec
    * Compute resources
* Test Mega
* Cleanup comments/logging
* Docs