FROM golang:1.19-alpine as source

WORKDIR /workspace
COPY go.mod go.mod
COPY go.sum go.sum
RUN go mod download

COPY main.go main.go


FROM source AS builder

RUN apk --no-cache add ca-certificates
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 GO111MODULE=on go build -a -o download main.go


FROM scratch AS runtime

WORKDIR /

COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /workspace/download .

ENTRYPOINT [ "/download" ]
