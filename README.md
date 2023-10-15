## Coral

# Docker image build

```bash
docker build . -t coral -f dockerfile/Dockerfile
```

```bash
docker run --rm -v ".\data:/data" coral -u "/data/For_Curtain_Raw_PPM1H- PROTAC_TP.txt" -a "/data/annotation.txt" -o "/data/output.txt" -c "/data/comparison.txt" -x "T: Index,T: Gene"
```