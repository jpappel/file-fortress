package cmd

import (
	"fmt"
	"github.com/spf13/cobra"
	"io"
	"log"
	"net/http"
)

// deleteCmd represents the delete command
var removeCmd = &cobra.Command{
	Use:   "remove [shortlink] --url [url]",
	Short: "Remove a file from File Fortress instance",
	Run: func(cmd *cobra.Command, args []string) {

		// make sure the user inputs a link
		if len(args) < 1 {
			log.Fatalf("Error: no link specified")
		}

		url, err := cmd.Flags().GetString("url")
		if err != nil {
			log.Fatalf("Error getting 'url' flag: %v", err)
		}

		url += "/api/v1/file/" + args[0]

		if !containsHTTP(url) {
			url = "http://" + url
		}

		client := &http.Client{}
		req, err := http.NewRequest("DELETE", url, nil)

		if err != nil {
			fmt.Println(err)
			return
		}
		res, err := client.Do(req)
		if err != nil {
			fmt.Println(err)
			return
		}

		body, err := io.ReadAll(res.Body)
		if err != nil {
			fmt.Println(err)
			return
		}
		fmt.Println(string(body))
	},
}

func init() {
	rootCmd.AddCommand(removeCmd)
}
