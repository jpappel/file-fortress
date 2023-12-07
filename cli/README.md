# File Fortress CLI

A command-line interface for interacting with the File Fortress API.

Created with Go using the Cobra CLI framework.

The program sends requests and uploads to http://filefortress.xyz by default, unless a `--url` flag is provided with a different instance.

## Example Syntax
```bash
file-fortress [command] [arguments] --flags
```

## Running

Make sure you are in directory that contains this README file.

Use `go run` on main.go, in tandem with the command and arguments you want to use.

### With compilation
```bash
go build -o file-fortress main.go
```

This will create a file-fortress executable in the current directory. Run this file as if it were a command-line program
```
./file-fortress [command] [arguments] --flags
```

### Without compilation
```bash
go run main.go [command] [arguments] --flags
```


## Upload a file
```bash
file-fortress upload [file] --url [url] --shortlink [shortlink]
```

Uploads a file to the File Fortress instance at the given URL. If no URL is provided, the default instance at http://filefortress.xyz is used.

The shortlink will default to the filename if one is not provided.

## Download a File

TODO

## Delete a File

TODO


## Resources Used
- [Cobra CLI](https://cobra.dev)
- [Go](https://go.dev)
