package cmd

import (
	"bytes"
	"fmt"
	"io"
	"log"
	"mime/multipart"
	"net/http"
	"os"
	"path/filepath"

	"github.com/spf13/cobra"
)

// uploadCmd represents the upload command
var uploadCmd = &cobra.Command{
	Use:   "upload [FILE] --url [URL]",
	Short: "Uploads a file to File Fortress",
	Long: `Upload a file to File Fortress, , or a given instance if a url is specified.:

Cobra is a CLI library for Go that empowers applications.
This application is a tool to generate the needed files
to quickly create a Cobra application.`,
	Run: func(cmd *cobra.Command, args []string) {
		if len(args) < 1 {
			log.Fatalf("Error: no file specified")
		}
		url, err := cmd.Flags().GetString("url")
		if err != nil {
			log.Fatalf("Error getting 'url' flag: %v", err)
		}

		file, err := cmd.Flags().GetString("file")

		// Open the file
		f, err := os.Open(file)
		if err != nil {
			log.Fatal(err)
		}
		defer f.Close()

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
		req, err := http.NewRequest("POST", url+"/api/v1/file/"+file, &b)
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
		defer resp.Body.Close()

		// Read the response
		bodyText, err := io.ReadAll(resp.Body)
		if err != nil {
			log.Fatal(err)
		}
		fmt.Printf("%s\n", bodyText)
	},
}

func init() {
	rootCmd.AddCommand(uploadCmd)

	// Here you will define your flags and configuration settings.

	// Cobra supports Persistent Flags which will work for this command
	// and all subcommands, e.g.:
	// uploadCmd.PersistentFlags().String("foo", "", "A help for foo")
	uploadCmd.PersistentFlags().String("url", "https://filefortress.xyz", "The url of the File Fortress instance to upload to")

	// Cobra supports local flags which will only run when this command
	// is called directly, e.g.:
	// uploadCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
}
