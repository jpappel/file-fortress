package cmd

import (
	"bytes"
	"fmt"
	"github.com/spf13/cobra"
	"io"
	"log"
	"mime/multipart"
	"net/http"
	"os"
	"path/filepath"
	"strconv"
	"strings"
)

// uploadCmd represents the upload command
var uploadCmd = &cobra.Command{
	Use:   "upload [file] --url [url] --shortlink [shortlink]",
	Short: "Uploads a file to File Fortress",
	Run: func(cmd *cobra.Command, args []string) {

		// make sure the user inputs a file
		if len(args) < 1 {
			log.Fatalf("Error: no file specified")
		}

		// Make sure the file exists as well
		if _, err := os.Stat(args[0]); os.IsNotExist(err) {
			log.Fatalf("Error: file %s does not exist", args[0])
		}

		// If the path starts with a tilde, replace it with the home directory
		if strings.HasPrefix(args[0], "~/") {
			home, err := os.UserHomeDir()
			if err != nil {
				log.Fatal(err)
			}
			args[0] = filepath.Join(home, args[0][2:])
		}

		url, err := cmd.Flags().GetString("url")
		if err != nil {
			log.Fatalf("Error getting 'url' flag: %v", err)
		}

		shortlink, err := cmd.Flags().GetString("shortlink")
		if err != nil {
			log.Fatalf("Error getting 'shortlink' flag: %v", err)
		}
		if shortlink == "" {
			// shortlink will be the filename if not specified
			shortlink = filepath.Base(args[0])
		}
		url += "/api/v1/file/" + shortlink

		if !containsHTTP(url) {
			url = "http://" + url
		}

		file, err := filepath.Abs(args[0])
		if err != nil {
			log.Fatal(err)
		}

		// Open the file
		f, err := os.Open(file)
		if err != nil {
			log.Fatal(err)
		}
		defer func(f *os.File) {
			err := f.Close()
			if err != nil {
				log.Fatal(err)
			}
		}(f)

		// Create a buffer to store the multipart form data
		var b bytes.Buffer
		w := multipart.NewWriter(&b)

		// Create a form file
		fw, err := w.CreateFormFile("file", filepath.Base(file))
		if err != nil {
			log.Fatal(err)
		}

		// Copy the file into the form file
		_, err = io.Copy(fw, f)
		if err != nil {
			log.Fatal(err)
		}

		// Close the multipart writer to get the terminating boundary
		err = w.Close()
		if err != nil {
			log.Fatal(err)
		}

		// Create a new request with the form data
		req, err := http.NewRequest("POST", url, &b)
		if err != nil {
			log.Fatal(err)
		}

		// Set the content type, this is important, the part after the semicolon must be the boundary from the writer
		req.Header.Set("Content-Type", w.FormDataContentType())

		// Send the request
		client := &http.Client{}
		resp, err := client.Do(req)
		if err != nil {
			log.Fatal(err)
		}
		defer func(Body io.ReadCloser) {
			err := Body.Close()
			if err != nil {
				log.Fatal(err)
			}
		}(resp.Body)

		if resp.StatusCode == 200 {
			fmt.Println("File " + args[0] + " uploaded successfully!")
			fmt.Println("Link: " + url)
		} else {
			errorMessage := "Error " + strconv.Itoa(resp.StatusCode) + ": file download failed"
			fmt.Println(errorMessage)
		}
	},
}

func init() {
	rootCmd.AddCommand(uploadCmd)

	uploadCmd.PersistentFlags().String("shortlink", "", `The shortlink to assign on the instance`)
}
