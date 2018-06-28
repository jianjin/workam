package main

import (
    "log"
    "crypto/tls"
)

func main() {
    log.SetFlags(log.Lshortfile)

    conf := &tls.Config{
         InsecureSkipVerify: true,
    }

    conn, err := tls.Dial("tcp", "127.0.0.1:4431", conf)
    if err != nil {
        log.Println(err)
        return
    }
    defer conn.Close()

    n, err := conn.Write([]byte("hello\n"))
    if err != nil {
        log.Println(n, err)
        return
    }

	buf := make([]byte, 10000000)
	for {
    n, err = conn.Read(buf)
    if err != nil {
        log.Println(n, err)
        return
	} else {
		log.Println(n)
	}
}
}