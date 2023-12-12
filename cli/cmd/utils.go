package cmd

import "strings"

func ContainsHTTP(url string) bool {
    return strings.HasPrefix(url, "http://") || strings.HasPrefix(url, "https://")
}
