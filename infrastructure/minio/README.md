# MinIO Local Setup

## Installation

### Windows
```bash
# Download MinIO
wget https://dl.min.io/server/minio/release/windows-amd64/minio.exe

# Start server
minio.exe server ./minio_data --console-address ":9001"
```

### Linux/Mac
```bash
# Download MinIO
wget https://dl.min.io/server/minio/release/linux-amd64/minio
chmod +x minio

# Start server
./minio server ./minio_data --console-address ":9001"
```

## Access

- **API:** http://localhost:9000
- **Console:** http://localhost:9001
- **Default credentials:** minioadmin / minioadmin

## Bucket Structure

```
audio-chunks/       # Intermediate TTS chunks
final-outputs/      # Completed audio files
book-metadata/      # Job metadata, book structures
```

## Create Buckets

```bash
# Using MinIO client (mc)
mc alias set local http://localhost:9000 minioadmin minioadmin
mc mb local/audio-chunks
mc mb local/final-outputs
mc mb local/book-metadata
```
