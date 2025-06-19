# Containerfile
FROM docker.io/library/gcc:12 as builder

WORKDIR /app
COPY . .
RUN mkdir build && \
    cd build && \
    cmake .. && \
    make

FROM docker.io/library/ubuntu:22.04
WORKDIR /app
COPY --from=builder /app/build/webapp .
RUN apt-get update && apt-get install -y libpistache-dev

EXPOSE 8080
CMD ["./webapp", "8080"]
