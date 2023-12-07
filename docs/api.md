# File Fortress API Documentation

## Download a file

```
GET /api/v1/file/<short_link>
```

### Curl Command

```
curl -X GET https://filefortress.xyz/api/v1/file/<short_link>
```

## Upload a file

```
POST /api/v1/file/<short_link>
```

### Curl Command
```
curl -X POST https://filefortress.xyz/api/v1/file/<short_link> -F "file=@<PATH>;type=<MIME_TYPE>"
```

## Delete a file

```
DELETE /api/v1/file/<short_link>
```

### Curl Command

```
curl -X DELETE https://filefortress.xyz/api/v1/file/<short_link>
```
