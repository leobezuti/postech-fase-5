FROM golang:1.25 AS builder
ENV CGO_ENABLED=0 \
    GOOS=linux \
    GOARCH=amd64 \
    GOTOOLCHAIN=auto

WORKDIR /app
COPY . .
RUN go mod tidy && go build -o myapp .

FROM alpine:3.21 AS final
WORKDIR /root/
COPY --from=builder /app/myapp .
EXPOSE 8001
CMD ["./myapp"]
